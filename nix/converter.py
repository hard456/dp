from nix import utils

metadata = ''


# adds context to the json-ld structure
def add_context():
    context = '''{
  "@context": [
  {
    "@vocab": "http://example.com/eeg/"
  }]'''
    add_content(context)


# converts metadata for the selected experiment
def convert_metadata(experiment_id, file_name):
    nix_file = utils.open_nix_file(experiment_id, file_name)
    global metadata
    metadata = ""
    add_context()
    parse_metadata(nix_file)
    close_metadata_structure()
    return metadata


# parses NIX file metadata
def parse_metadata(nix_file):
    if nix_file.blocks is not None:
        parse_blocks(nix_file.blocks)
    if nix_file.sections is not None:
        for i in range(len(nix_file.sections)):
            content = recursive_section_search(nix_file.sections[i], 1, nix_file)
            add_content(content)


# parses blocks
def parse_blocks(blocks):
    if len(blocks) > 0:
        content = '  "blocks": ['
        # loop blocks
        for i in range(len(blocks)):
            block = blocks[i]
            content += '\n    {\n    "name": "' + block.name + '"'
            if block.metadata is not None:
                name = utils.edit_name(block.metadata.name)
                content += ',\n    "metadataLinkTo": "' + name + '"'
            # parses groups
            if len(block.groups) > 0:
                content += ',\n    "groups": ['
                content += parse_groups(block.groups)
                content += '\n    ]'
            # parses data_arrays
            if len(block.data_arrays) > 0:
                content += ',\n    "dataArrays": ['
                content += parse_data_arrays(block.data_arrays)
                content += '\n    ]'
            # parses multi tags
            if len(block.multi_tags) > 0:
                content += ',\n    "multiTags": ['
                content += parse_multi_tags(block.groups)
                content += '\n    ]'

            content += '\n    }'
            if i < len(blocks) - 1:
                content += ','
        content += '\n  ]'
        add_content(content)


# parses groups
def parse_groups(groups):
    content = ""
    for i in range(len(groups)):
        group = groups[i]
        content += '\n      {\n      "name": "' + group.name + '"'
        if group.metadata is not None:
            name = utils.edit_name(group.metadata.name)
            content += ',\n      "metadataLinkTo": "' + name + '"'
        # data arrays links
        if len(group.data_arrays) > 0:
            content += ',\n      "dataArrayLinks": ['
            for j in range(len(group.data_arrays)):
                content += '\n        {\n        "nameLinkTo": "' + group.data_arrays[j].name + '"\n        }'
                if i < len(group.data_arrays) - 1:
                    content += ','
            content += '\n      ]'
        # multi tags links
        if len(group.multi_tags) > 0:
            content += ',\n      "multiTagLinks": ['
            for j in range(len(group.multi_tags)):
                content += '\n        {\n        "nameLinkTo": "' + group.multi_tags[j].name + '"\n        }'
                if i < len(group.multi_tags) - 1:
                    content += ','
            content += '\n      ]'
        content += '\n      }'
        if i < len(groups) - 1:
            content += ','
    return content


# parses multi tags
def parse_multi_tags(multi_tags):
    content = ""
    multi_tags = multi_tags[0].multi_tags
    for i in range(len(multi_tags)):
        content += '\n      {'
        tag = multi_tags[i]
        content += '\n      "name": "' + tag.name + '"'
        # positions data array link
        if tag.positions is not None:
            content += ',\n      "positionsLinkTo": "' + tag.positions.name + '"'
        # extents data array link
        if tag.extents is not None:
            content += ',\n      "extentsLinkTo": "' + tag.extents.name + '"'
        content += '\n      }'
        if i < len(multi_tags) - 1:
            content += ','
    return content


# parses data arrays
def parse_data_arrays(data_arrays):
    content = ""
    for i in range(len(data_arrays)):
        array = data_arrays[i]
        content += '\n      {\n      "name": "' + array.name + '",'
        content += '\n      "type": "' + array.type + '",'
        if array.metadata is not None:
            name = utils.edit_name(array.metadata.name)
            content += '\n      "metadataLinkTo": "' + name + '",'
        # loop dimensions
        if len(array.dimensions) > 0:
            content += '\n      "dimensions": ['
            content += parse_dimensions(array)
            content += '\n      ]}'
        if i < len(data_arrays) - 1:
            content += ','
    return content


# parses dimensions
def parse_dimensions(array):
    content = ""
    for i in range(len(array.data_extent)):
        content += '\n        {\n        "size": "' + str(array.data_extent[i]) + '"'
        if hasattr(array.dimensions[i], 'label'):
            content += ',\n        "label": "' + array.dimensions[i].label + '"'
        if hasattr(array.dimensions[i], 'unit'):
            content += ',\n        "unit": "' + array.dimensions[i].unit + '"'
        content += '\n        }'
        if i < len(array.data_extent) - 1:
            content += ','
    return content


# finds the metadata section recursively
def recursive_section_search(section, iteration, nix_file):
    content = ""
    gap = " " * iteration * 2
    if hasattr(section, 'name'):
        name = utils.edit_name(section.name)
        content += gap + '"' + name + '": {'
        # parses props
        if hasattr(section, 'props') and section.props:
            iteration += 1
            content += parse_props(section.props, iteration, nix_file)
            iteration -= 1
        # nesting in another subsection
        if hasattr(section, 'sections') and section.sections:
            if hasattr(section, 'props') and section.props:
                content += ','
            content += recursive_section_search(section.sections, iteration, nix_file)
        content += '\n' + gap + '}'
    else:
        if len(section) > 0:
            for i in range(len(section)):
                content += '\n'
                iteration += 1
                content += recursive_section_search(section[i], iteration, nix_file)
                iteration -= 1
                if i < len(section) - 1:
                    content += ','
    return content


# finds the section by identification number
def find_section_by_id(section, id, found_section):
    if found_section is None:
        if hasattr(section, 'name'):
            if section.id == id:
                found_section = section
                return found_section
            if hasattr(section, 'sections') and section.sections:
                found_section = find_section_by_id(section.sections, id, found_section)
        else:
            if len(section) > 0:
                for i in range(len(section)):
                    found_section = find_section_by_id(section[i], id, found_section)
    return found_section


# parses props
def parse_props(props, iteration, nix_file):
    content = ""
    gap = " " * iteration * 2
    for i in range(len(props)):
        name = utils.edit_name(props[i].name)
        value = ""
        for j in range(len(props[i].values)):
            # checks property value length
            if len(str(props[i].values[j])) == 36:
                section = find_section_by_id(nix_file.sections, props[i].values[j], None)
                if section is not None and hasattr(section, 'name'):
                    tmp_value = utils.edit_name(section.name)
                else:
                    tmp_value = str(props[i].values[j])
            else:
                tmp_value = str(props[i].values[j])

            if j < len(props[i].values) - 1:
                value += tmp_value + ', '
            else:
                value += tmp_value
        value = value.replace('\"', '')
        value = value.replace('\n', ' ')
        content += '\n' + gap + '"' + name + '": ' + '"' + value + '"'
        if i < len(props) - 1:
            content += ','
    return content


# adds content to the metadata structure
def add_content(content):
    global metadata
    if len(metadata) == 0:
        metadata += content
    else:
        metadata += ",\n" + content


# closes the metadata structure
def close_metadata_structure():
    global metadata
    metadata += '\n}'
