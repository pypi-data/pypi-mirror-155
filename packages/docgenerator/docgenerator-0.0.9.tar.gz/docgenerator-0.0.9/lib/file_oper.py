from markdownTable import markdownTable
from ruamel.yaml import YAML
from pathlib import Path
from helpers import settings

yaml = YAML()
port_file = Path(settings.PORT_LIST_FILE)
volume_file = Path(settings.VOLUME_LIST_FILE)


def get_values(yaml_path):
    """
    Returns the yaml data of the path
    """

    return yaml.load(yaml_path)


def delete_file(file):
    """
    Delets port file, so it gets recreated clean
    """
    if Path(file).exists():
        Path(file).unlink()


def add_text_to_file(file, intro):
    """
    Prints text to the file
    """
    with Path(file).open(mode='a', encoding='utf_8') as file:
        file.write(intro)


def create_table(port_list):
    """
    Returns a markdown list
    """
    # Generates a nice table with spacing
    table = markdownTable(port_list).setParams(
        padding_weight='right', row_sep='markdown', quote=False).getMarkdown()
    # Removes the first 2 lines (headers) as it uses the key from the dict which is not nice

    return table.split("\n", 2)[2]
