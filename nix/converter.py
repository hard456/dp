from nix import utils
test = ""


def create_context():
    context = '''{
  "@context": [ "https://schema.org/docs/jsonldcontext.json", {
  "detailedDescription": "http://example.com/eeg-vocabulary#detailedDescription",
  "experimentator": "http://example.com/eeg-vocabulary#experimentator",
  "subject": "http://example.com/eeg-vocabulary#subject",
  "laterality": "http://example.com/eeg-vocabulary#laterality"
  }],'''
    return context


def convert_metadata(id, file_name):
    nix_file = utils.open_nix_file(id, file_name)
    content = create_context()
    get_metadata(nix_file)
    content = content + add_metadata() + '\n}'
    return content


def get_metadata(nix_file):
    for i in range(len(nix_file.blocks)):
        loop_block(nix_file.blocks[i])
    for i in range(len(nix_file.sections)):
        if nix_file.sections[i].type == "nix.metadata.eeg":
            loop_metadata_eeg(nix_file.sections[i])
        elif nix_file.sections[i].type == "nix.metadata.session":
            loop_metadata_session(nix_file.sections[i])
    print("konec")


def loop_block(block):
    for i in range(len(block.data_arrays)):
        array = block.data_arrays[i]
        print("array")


def loop_metadata_eeg(section):
    for i in range(len(section.sections)):
        print(section.sections[i].name)
    print("eeg")


def loop_metadata_session(section):
    for i in range(len(section.sections)):
        if section.sections[i].name == "Experimenters":
            section = section.sections[i]
            print("yolo")
        print(section.sections[i].name)
    print("session")


def add_metadata():
    data = '''
  "description": "xxx",
  "detailedDescription": "yyyyyy",
  "subject": {
    "@type": "Person",
    "name": "Karlito Subjito",
    "laterality": "right-hand"
  },
  "experimentator": [
    {
    "@type": "Person",
    "name": "Peter Venkman"
    },
    {
    "@type": "Person",
    "name": "Karel Venkman"
    }
  ]'''
    return data
