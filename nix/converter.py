from nix import utils

metadata = ''


def add_context():
    context = '''{
  "@context": [
  {
    "detailedDescription": "http://example.com/eeg-vocabulary#detailedDescription",
    "experimenters": "http://example.com/eeg-vocabulary#experimenters",
    "subject": "http://example.com/eeg-vocabulary#subject",
    "laterality": "http://example.com/eeg-vocabulary#laterality"
  }]'''
    print(context)
    add_content(context)
    return context


def convert_metadata(id, file_name):
    nix_file = utils.open_nix_file(id, file_name)
    add_context()
    find_metadata(nix_file)
    close_metadata_structure()
    return metadata


def find_metadata(nix_file):
    loop_blocks(nix_file.blocks)
    for i in range(len(nix_file.sections)):
        if nix_file.sections[i].type == "nix.metadata.eeg":
            loop_metadata_eeg(nix_file.sections[i])
        elif nix_file.sections[i].type == "nix.metadata.session":
            loop_metadata_session(nix_file.sections[i])


def loop_blocks(blocks):
    content = '  "blocks": ['
    # loop blocks
    for i in range(len(blocks)):
        block = blocks[i]
        content += '\n    {\n    "name": "' + block.name + '",'
        content += '\n    "data_arrays": ['
        # loop data_arrays
        for j in range(len(block.data_arrays)):
            array = block.data_arrays[j]
            content += '\n      {\n      "name": "' + array.name + '",'
            content += '\n      "dimensions": ['
            # loop dimensions
            for k in range(len(array.data_extent)):
                content += '\n        {\n        "size": "' + str(array.data_extent[k]) + '"'
                # dimension = block.data_arrays[j].dimensions[0]
                # dimension2 = block.data_arrays[j].dimensions[1]
                content += '\n        }'
                if k < len(array.data_extent)-1:
                    content += ','
            content += '\n      ]}'
            if j < len(block.data_arrays) - 1:
                content += ','
        content += '\n    ]}'
        if i < len(blocks) - 1:
            content += ','
    content += '\n  ]'
    print(content)
    add_content(content)


def loop_metadata_eeg(section):
    print("eeg:")
    # for i in range(len(section.sections)):
    #     if section.sections[i].name == "HardwareSettings":
    #         get_experimenters(section.sections[i])
    #     elif section.sections[i].name == "Recording":
    #         get_experimenters(section.sections[i])


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
            add_experimenters(section.sections[i])
        print(section.sections[i].name)


def add_experiment(section):
    for i in range(len(section.props)):
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
    print("electrodes")


def add_software(section):
    print("software")


def add_experimenters(section):
    content = '  "experimenters": ['
    for i in range(len(section.sections)):
        content += '\n    {'
        # content += '\n    "@type": "Person",'
        for j in range(len(section.sections[i].props)):
            if section.sections[i].props[j].name == 'Role':
                content += '\n    "Role": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'FirstName':
                content += '\n    "FirstName": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'LastName':
                content += '\n    "LastName": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'Gender':
                content += '\n    "Gender": ' + '"' + section.sections[i].props[j].values[0] + '"'

            if j < len(section.sections[i].props)-1:
                content += ','
        content += '\n    }'
        if i < len(section.sections) - 1:
            content += ','
    content += '\n  ]'
    add_content(content)


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
