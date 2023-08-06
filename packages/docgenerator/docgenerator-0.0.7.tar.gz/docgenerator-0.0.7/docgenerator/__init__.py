from helpers.logger import Colors
from lib import services_oper
from lib import volumes_oper
from lib import desc_oper
from lib import file_oper
from lib import apps_oper
import helpers.setup


def main():
    if not setup.GENERATE_VOLUME_FILE and not setup.GENERATE_PORT_FILE:
        print(Colors.RED + "No files to generate")
        exit(1)
    if setup.GENERATE_VOLUME_FILE:
        all_volumes = []
        volume_file_content = ""
        volume_file_content += setup.VOLUME_LIST_INTRO
        file_oper.delete_file(setup.VOLUME_LIST_FILE)

    if setup.GENERATE_PORT_FILE:
        all_ports = []
        port_file_content = ""
        port_file_content += setup.PORT_LIST_INTRO
        file_oper.delete_file(setup.PORT_LIST_FILE)

    if setup.GENERATE_DESCRIPTION_FILE:
        all_descriptions = []
        description_file_content = ""
        description_file_content += setup.DESCRIPTION_LIST_INTRO
        file_oper.delete_file(setup.DESCRIPTION_LIST_FILE)

    ordered_trains = apps_oper.get_ordered_trains(apps_oper.get_trains())
    for train in ordered_trains:
        apps = apps_oper.get_apps(train)
        if setup.GENERATE_PORT_FILE:
            # Add the list that is returned to the raw_services_list,
            # can't append or we will end up with a list of lists
            raw_services_list = services_oper.get_raw_services_list(apps)
            all_ports += services_oper.get_processed_services_list(
                raw_services_list, train.stem)
        if setup.GENERATE_VOLUME_FILE:
            raw_volumes_list = volumes_oper.get_raw_volumes_list(apps)
            all_volumes += volumes_oper.get_processed_volumes_list(
                raw_volumes_list, train.stem)
        if setup.DESCRIPTION_LIST_FILE:
            all_descriptions += desc_oper.get_descriptions_list(
                apps, train.stem)

    services_oper.append_conflicts_to(all_ports)
    for train in ordered_trains:
        if setup.GENERATE_PORT_FILE:
            port_file_content += services_oper.create_port_list_content(
                all_ports, train.stem)
        if setup.GENERATE_VOLUME_FILE:
            volume_file_content += volumes_oper.create_volume_list_content(
                all_volumes, train.stem)
        if setup.GENERATE_DESCRIPTION_FILE:
            description_file_content += desc_oper.create_description_list_content(
                all_descriptions, train.stem)
    if setup.GENERATE_PORT_FILE:
        port_file_content += setup.PORT_LIST_OUTRO
        port_file_content += services_oper.get_next_available_port(all_ports)
        file_oper.add_text_to_file(setup.PORT_LIST_FILE, port_file_content)
    if setup.GENERATE_VOLUME_FILE:
        volume_file_content += setup.VOLUME_LIST_OUTRO
        file_oper.add_text_to_file(setup.VOLUME_LIST_FILE, volume_file_content)
    if setup.GENERATE_DESCRIPTION_FILE:
        description_file_content += setup.DESCRIPTION_LIST_OUTRO
        file_oper.add_text_to_file(
            setup.DESCRIPTION_LIST_FILE, description_file_content)


if __name__ == "__main__":
    main()
