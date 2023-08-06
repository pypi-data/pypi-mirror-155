from lib import file_oper
from pathlib import Path
import helpers.setup
import copy


def get_description(app):
    """
    Returns the Description of an app
    """
    data = file_oper.get_values(Path.joinpath(app, "Chart.yaml"))
    if 'description' in data:
        clean_string = clean_strings(data['description'])
        splitted_string = break_long_string(clean_string)
        return splitted_string
    return None


def break_long_string(string):
    """
    Breaks long strings, if the character at break point is not space,
    it will break on the nearest space
    """

    # If length is smaller thant the split, return it as is
    if len(string) <= setup.SPLIT_DESCRIPTION_EVERY:
        return string

    splitted_times = 1
    stopped_at_index = 0
    splitted_str = ""
    # Loop over the string
    for idx, char in enumerate(string):
        # Index divided with splitted_times, will let us know
        # in what "chuck" of the string we are. So we can split only after each chuck.
        # eg. If a string is 100 chars, we split every 50.
        # index 1 / splitted_times = 1 is not > than 50. So we won't split here.
        # index 50 / splitted_times = 1 is < than 50. So we can split here (if conditions met, else check next char for conditions)
        # index 51 / splitted_times = 1 is < than 50. So we can split here (lets say conditions met, we increase splitted_times by 1)
        # index 52 / splitted_times = 2 is not > than 50. So we won't split here.
        # index 100 / splitted_times = 2 is < than 50. So we can split here (if conditions met, else check next char for conditions)
        # And so on..
        if idx / splitted_times > setup.SPLIT_DESCRIPTION_EVERY:
            # If the current character is " " add the line break
            if char == " ":
                # First time: Concat string from index 0 until current idx + line break
                # Second time: Concat string from the index we stopped on last concat + 1 + line break
                splitted_str += string[stopped_at_index+1:idx] + \
                    "<br>" if stopped_at_index else string[:idx]+"<br>"
                # Store the index we stopped
                stopped_at_index = idx
                # Store how many times we splitted
                splitted_times += 1
    # If we stopped to break line (meaning string is larger than the split length) and there is still a part of string left.
    # Append the rest of the string
    if stopped_at_index and string[stopped_at_index+1:]:
        splitted_str += string[stopped_at_index+1:]
    # If string was larger than the split length, but we didn't apply line breaks (maybe there was not any spaces after the split length)
    # Return the string as is
    if not stopped_at_index:
        return string
    return splitted_str


def get_home_url(app):
    """
    Returns the Home of an app
    """
    data = file_oper.get_values(Path.joinpath(app, "Chart.yaml"))

    return data['home'] if 'home' in data else setup.FALLBACK_URL


def get_source_image(app):
    """
    Returns the image of an app
    """
    if setup.PRINT_IMAGE_SOURCE:
        dockerfile_path = Path(setup.IMAGE_PATH, app, "Dockerfile")
        if dockerfile_path.exists():
            with open(dockerfile_path, "r", encoding="utf_8") as file:
                content = file.readline()
                content = content.split(" ")[1].split(":")[0]
                return content
    return "Not Found"


def get_icon(app):
    """
    Returns the Icon of an app
    """
    data = file_oper.get_values(Path.joinpath(app, "Chart.yaml"))

    return data['icon'] if 'icon' in data else setup.FALLBACK_URL


def clean_strings(string):
    """
    Some descriptions have line breaks, so we clean them here
    """
    return string \
        .replace('\n', " ") \
        .replace('\r', " ") \
        .replace('\\', " ")


def get_descriptions_list(apps, train):
    """
    Returns a LIST of dicts
    Each Dict has the APP name and the DESCRIPTION
    """
    description_list = []
    for app in apps:
        description = get_description(app)
        container = get_source_image(app.stem)
        home_url = get_home_url(app)
        icon = get_icon(app)
        if not description is None:
            description_list.append(create_row(
                app_name=app.stem, container=container, description=description, home_url=home_url, icon=icon, train=train))
        else:
            description_list.append(create_row(
                app_name=app.stem, container=container, description=False, home_url=home_url, icon=icon, train=train))
    return description_list


def create_row(app_name, container, description, home_url, icon, train):
    """
    Creates a row for the processed description list
    """
    if not description:
        description = setup.Status.NO_DESC
    return {
        "app_name": f'<img src="{icon}" width="{setup.IMAGE_WIDTH}" height="{setup.IMAGE_HEIGHT}"> [{app_name}]({home_url})',
        "container": f'{container}',
        "description": description,
        "train": train
    } if setup.PRINT_IMAGE_SOURCE else {
        "app_name": f'<img src="{icon}" width="{setup.IMAGE_WIDTH}" height="{setup.IMAGE_HEIGHT}"> [{app_name}]({home_url})',
        "description": description,
        "train": train
    }


def create_description_list_content(description_list, train):
    """
    Creates and returns content to the description list file
    """
    content = ""
    filtered_list = copy.deepcopy(description_list)
    filtered_list = filter(lambda item: item['train'] == train, filtered_list)

    sorted_list = sorted(filtered_list, key=lambda item: item['app_name'])
    for x in sorted_list:
        del x['train']

    content += f'## {train.capitalize()}'
    content += '\n\n'
    content += "| App | Container Source | Description |" if setup.PRINT_IMAGE_SOURCE else "| App | Description |"
    content += '\n'
    content += "|:----|:-----------------|:------------|" if setup.PRINT_IMAGE_SOURCE else "|:----|:------------|"
    content += '\n'
    # Check that table has data
    if sorted_list:
        content += file_oper.create_table(sorted_list)
        content += '\n\n'

    return content
