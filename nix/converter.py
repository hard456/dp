from nix import utils
test = ""


def create_context():
    context = '''{
  "@context": [
  {
    "detailedDescription": "http://example.com/eeg-vocabulary#detailedDescription",
    "experimenters": "http://example.com/eeg-vocabulary#experimenters",
    "subject": "http://example.com/eeg-vocabulary#subject",
    "laterality": "http://example.com/eeg-vocabulary#laterality"
  }],'''
    print(context)
    return context


def convert_metadata(id, file_name):
    nix_file = utils.open_nix_file(id, file_name)
    content = create_context()
    get_metadata(nix_file)
    content = content + '\n}'
    return content


def get_metadata(nix_file):
    for i in range(len(nix_file.blocks)):
        loop_block(nix_file.blocks[i])
    for i in range(len(nix_file.sections)):
        if nix_file.sections[i].type == "nix.metadata.eeg":
            loop_metadata_eeg(nix_file.sections[i])
        elif nix_file.sections[i].type == "nix.metadata.session":
            loop_metadata_session(nix_file.sections[i])


def loop_block(block):
    content = '  "blocks": ['
    content_body = '\n    {\n    "name": "' + block.name + '"'
    for i in range(len(block.data_arrays)):
        array = block.data_arrays[i]
        print("array")
    content_body += '\n    }'
    content += content_body
    content += '\n  ]'
    print(content)
    print("test")


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
            get_experiment(section.sections[i])
        elif section.sections[i].name == "Recording":
            get_recording(section.sections[i])
        elif section.sections[i].name == "Environment":
            get_environment(section.sections[i])
        elif section.sections[i].name == "Project":
            get_project(section.sections[i])
        elif section.sections[i].name == "Subject":
            get_subject(section.sections[i])
        elif section.sections[i].name == "Weather":
            get_weather(section.sections[i])
        elif section.sections[i].name == "HardwareProperties":
            get_hardware_properties(section.sections[i])
        elif section.sections[i].name == "Electrodes":
            get_electrodes(section.sections[i])
        elif section.sections[i].name == "Software":
            get_software(section.sections[i])
        elif section.sections[i].name == "Experimenters":
            get_experimenters(section.sections[i])
        print(section.sections[i].name)


def get_experiment(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Private Experiment":
            print(section.props[i].values[0])
        elif section.props[i].name == "ProjectName":
            print(section.props[i].values[0])


def get_recording(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Start":
            print(section.props[i].values[0])
        elif section.props[i].name == "End":
            print(section.props[i].values[0])
        elif section.props[i].name == "Experimenter":
            print(section.props[i].values[0])


def get_environment(section):
    for i in range(len(section.props)):
        if section.props[i].name == "RoomTemperature":
            print(section.props[i].values[0])


def get_project(section):
    for i in range(len(section.props)):
        if section.props[i].name == "PrincipleInvestigator":
            print(section.props[i].values[0])
        elif section.props[i].name == "Title":
            print(section.props[i].values[0])
        elif section.props[i].name == "Topic":
            print(section.props[i].values[0])


def get_subject(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Gender":
            print(section.props[i].values[0])
        elif section.props[i].name == "Age":
            print(section.props[i].values[0])
        # elif section.props[i].name == "HealthStatus":
        #     print(section.props[i].values[0])


def get_weather(section):
    for i in range(len(section.props)):
        if section.props[i].name == "Weather":
            print(section.props[i].values[0])
        elif section.props[i].name == "Description":
            print(section.props[i].values[0])


def get_hardware_properties(section):
    print("hard_properties")


def get_electrodes(section):
    print("electrodes")


def get_software(section):
    print("software")


def get_experimenters(section):
    content = '  "experimenters": ['
    for i in range(len(section.sections)):
        content_body = '\n    {\n    "@type": "Person",'
        for j in range(len(section.sections[i].props)):
            if section.sections[i].props[j].name == 'Role':
                content_body += '\n    "Role": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'FirstName':
                content_body += '\n    "FirstName": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'LastName':
                content_body += '\n    "LastName": ' + '"' + section.sections[i].props[j].values[0] + '"'
            elif section.sections[i].props[j].name == 'Gender':
                content_body += '\n    "Gender": ' + '"' + section.sections[i].props[j].values[0] + '"'

            if j < len(section.sections[i].props)-1:
                content_body += ','
        content_body += '\n    }'
        content += content_body
    content += '\n  ]'
    print(content)
