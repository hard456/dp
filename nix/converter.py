from nix import utils

metadata = ''


def add_context():
    context = '''{
  "@context": [
  {
    "@vocab": "http://example.com/eeg/"
  }]'''
    add_content(context)
    return context


def convert_metadata(id, file_name):
    nix_file = utils.open_nix_file(id, file_name)
    global metadata
    metadata = ""
    add_context()
    find_metadata(nix_file)
    close_metadata_structure()
    return metadata


def find_metadata(nix_file):
    parse_blocks(nix_file.blocks)
    for i in range(len(nix_file.sections)):
        if nix_file.sections[i].type == "nix.metadata.eeg":
            loop_metadata_eeg(nix_file.sections[i])
        elif nix_file.sections[i].type == "nix.metadata.session":
            loop_metadata_session(nix_file.sections[i])


def parse_blocks(blocks):
    if len(blocks) > 0:
        content = '  "blocks": ['
        # loop blocks
        for i in range(len(blocks)):
            block = blocks[i]
            content += '\n    {\n    "name": "' + block.name + '",'
            # parse groups
            if len(block.groups) > 0:
                content += '\n    "groups": ['
                content += parse_groups(block.groups)
                content += '\n    ]'
            # parse data_arrays
            if len(block.data_arrays) > 0:
                content += ',\n    "data_arrays": ['
                content += parse_data_arrays(block.data_arrays)
                content += '\n    ]'
            # parse multi tags
            if len(block.multi_tags) > 0:
                content += ',\n    "multi_tags": ['
                content += parse_multi_tags(block.groups)
                content += '\n    ]'

            content += '\n    }'
            if i < len(blocks) - 1:
                content += ','
        content += '\n  ]'
        add_content(content)


def parse_groups(groups):
    content = ""
    for i in range(len(groups)):
        group = groups[i]
        content += '\n      {\n      "name": "' + group.name + '"'
        # data arrays links
        if len(group.data_arrays) > 0:
            content += ',\n      "dataArrayLinks": ['
            for j in range(len(group.data_arrays)):
                content += '\n        {\n        "nameLink": "' + group.data_arrays[j].name + '"\n        }'
                if i < len(group.data_arrays) - 1:
                    content += ','
            content += '\n      ]'
        # multi tags links
        if len(group.multi_tags) > 0:
            content += ',\n      "multiTagLinks": ['
            for j in range(len(group.multi_tags)):
                content += '\n        {\n        "nameLink": "' + group.multi_tags[j].name + '"\n        }'
                if i < len(group.multi_tags) - 1:
                    content += ','
            content += '\n      ]'
        content += '\n      }'
        if i < len(groups) - 1:
            content += ','
    return content


def parse_multi_tags(multi_tags):
    content = ""
    multi_tags = multi_tags[0].multi_tags
    for i in range(len(multi_tags)):
        content += '\n      {'
        tag = multi_tags[i]
        # positions data array link
        if tag.positions is not None:
            content += '\n      "positionsDataArrayLink": "' + tag.positions.name + '"'
        # extents data array link
        if tag.extents is not None:
            content += ',\n      "extentsDataArrayLink": "' + tag.extents.name + '"'
        content += '\n      }'
        if i < len(multi_tags) - 1:
            content += ','
    return content


def parse_data_arrays(data_arrays):
    content = ""
    for i in range(len(data_arrays)):
        array = data_arrays[i]
        content += '\n      {\n      "name": "' + array.name + '",'
        content += '\n      "type": "' + array.type + '",'
        # loop dimensions
        if len(array.dimensions) > 0:
            content += '\n      "dimensions": ['
            content += parse_dimensions(array)
            content += '\n      ]}'
        if i < len(data_arrays) - 1:
            content += ','
    return content


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


def loop_metadata_eeg(section):
    print("eeg:")
    # for i in range(len(section.sections)):
    #     if section.sections[i].name == "HardwareSettings":
    #         get_experimenters(section.sections[i])
    #     elif section.sections[i].name == "Recording":
    #         get_experimenters(section.sections[i])


def loop_metadata_session_all(section):
    sections = section.sections
    for i in range(len(sections)):
        if hasattr(sections, 'sections'):
            content = '  "' + utils.first_character_lower_case(section[i].name) + '": ['


def loop_metadata_session(section):
    print("session:")
    for i in range(len(section.sections)):
        if section.sections[i].name == "Experiment":
            add_experiment(section.sections[i])
        elif section.sections[i].name == "Recording":
            add_recording(section.sections[i])
        elif section.sections[i].name == "Environment":
            add_environment(section.sections[i])
        elif section.sections[i].name == "Project":
            add_project(section.sections[i])
        elif section.sections[i].name == "Subject":
            add_subject(section.sections[i])
        elif section.sections[i].name == "Weather":
            add_weather(section.sections[i])
        elif section.sections[i].name == "HardwareProperties":
            add_hardware_properties(section.sections[i])
        elif section.sections[i].name == "Electrodes":
            add_electrodes(section.sections[i])
        elif section.sections[i].name == "Software":
            add_software(section.sections[i])
        elif section.sections[i].name == "Experimenters":
            parse_experimenters(section.sections[i])
        print(section.sections[i].name)


def add_experiment(section):
    for i in range(len(section.props)):
        props = section.props[i]
        if section.props[i].name == "Private Experiment":
            print(section.props[i].values[0])
        elif section.props[i].name == "ProjectName":
            print(section.props[i].values[0])


def add_recording(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Start":
            print(section.props[i].values[0])
        elif section.props[i].name == "End":
            print(section.props[i].values[0])
        elif section.props[i].name == "Experimenter":
            print(section.props[i].values[0])


def add_environment(section):
    for i in range(len(section.props)):
        if section.props[i].name == "RoomTemperature":
            print(section.props[i].values[0])


def add_project(section):
    for i in range(len(section.props)):
        if section.props[i].name == "PrincipleInvestigator":
            print(section.props[i].values[0])
        elif section.props[i].name == "Title":
            print(section.props[i].values[0])
        elif section.props[i].name == "Topic":
            print(section.props[i].values[0])


def add_subject(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Gender":
            print(section.props[i].values[0])
        elif section.props[i].name == "Age":
            print(section.props[i].values[0])
        # elif section.props[i].name == "HealthStatus":
        #     print(section.props[i].values[0])


def add_weather(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Weather":
            print(section.props[i].values[0])
        elif section.props[i].name == "Description":
            print(section.props[i].values[0])


def add_hardware_properties(section):
    print("hard_properties")


def add_electrodes(section):
    content = '  "electrodes": ['
    for i in range(len(section.sections)):
        content += '\n    {'
        for j in range(len(section.sections[i].props)):
            name = utils.first_character_lower_case(section.sections[i].props[j].name)
            value = section.sections[i].props[j].values[0]
            content += '\n    "' + name + '": ' + '"' + value.replace('"', '') + '"'
            if j < len(section.sections[i].props)-1:
                content += ','
        content += '\n    }'
        if i < len(section.sections) - 1:
            content += ','
    content += '\n  ]'
    add_content(content)


def add_software(section):
    print("software")


def parse_experimenters(section):
    content = '  "experimenters": ['
    for i in range(len(section.sections)):
        content += '\n    {'
        content += parse_props(section.sections[i].props)
        content += '\n    }'
        if i < len(section.sections) - 1:
            content += ','
    content += '\n  ]'
    add_content(content)


def parse_props(props):
    content = ""
    for i in range(len(props)):
        name = utils.first_character_lower_case(props[i].name)
        value = props[i].values[0]
        value = value.replace('"', '')
        content += '\n    "' + name + '": ' + '"' + value + '"'
        if i < len(props) - 1:
            content += ','
    return content


def add_content(content):
    global metadata
    print(content)
    if len(metadata) == 0:
        metadata += content
    else:
        metadata += ",\n" + content


def close_metadata_structure():
    global metadata
    metadata += '\n}'
