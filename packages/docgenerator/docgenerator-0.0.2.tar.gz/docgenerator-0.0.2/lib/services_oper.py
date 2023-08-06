from helpers.logger import logger
from lib import file_oper
from pathlib import Path
import setup
import copy


def get_service(app):
    """
    Returns the SERVICE section of an app
    """
    data = file_oper.get_values(Path.joinpath(app, "values.yaml"))

    return data['service'] if 'service' in data else None


def get_raw_services_list(apps):
    """
    Returns a LIST of dicts
    Each Dict has the APP name and the SERVICE Section
    """
    service_list = []
    for app in apps:
        service = get_service(app)
        if not service is None:
            service_list.append({"app_name": app.stem, "service": service})
        else:
            service_list.append(
                {"app_name": app.stem, "service": False})

    return service_list


def create_row(app_name, status, train, svc_name="-", port_name="-", port=0, protocol="-", note="-"):
    """
    Creates a row for the processed services list
    """
    if status == "port_dis":
        status = setup.Status.PORT_DIS
    if status == "port_und":
        status = setup.Status.PORT_UND
    if status == "svc_dis":
        status = setup.Status.SVC_DIS
    if status == "svc_und":
        status = setup.Status.SVC_UND
    return {
        "app_name": app_name,
        "svc_name": svc_name,
        "port_name": port_name,
        "port": port,
        "protocol": protocol,
        "status": status,
        "train": train,
        "note": note
    }


def get_processed_services_list(raw_services_list, curr_train):
    """
    Returns a processes list of services
    """
    services_list = []
    for service_section in raw_services_list:
        # If there is no service, create a row accordingly
        if not service_section['service']:
            logger(
                f'App: <{service_section["app_name"]}> has no Service Defined', "GREEN")
            services_list.append(create_row(
                app_name=service_section['app_name'],
                status="svc_und",
                train=curr_train
            ))
        else:
            # if there is service, process it
            for service in service_section['service'].items():
                services_list += process_service(
                    service, service_section['app_name'], curr_train)

    return services_list


def process_service(service, app_name, curr_train):
    """
    Processes the service and create rows
    """
    rows = []
    # If there is no "enabled" key, it's probably main. Assume service is enabled.
    # If there is "enabled" key and it's true, service is enabled
    # If there is "enabled" key and it's false, service is disabled
    if (not 'enabled' in service[1]) or ('enabled' in service[1] and service[1]['enabled']):
        # If there are no ports (This is probably unusual), but still create a row
        if not 'ports' in service[1]:
            logger(
                f'Service: <{service[0]}> of App: <{app_name}> has no ports defined', "RED")
            rows.append(create_row(
                app_name=app_name,
                status="port_und",
                svc_name=service[0],
                train=curr_train
            ))
        else:
            for port in service[1]['ports'].items():
                processed_port = process_port(port, app_name, service[0])
                rows.append(create_row(
                    app_name=app_name,
                    svc_name=service[0],
                    status=processed_port['status'],
                    train=curr_train
                ) if 'port' not in processed_port else create_row(
                    app_name=app_name,
                    status=processed_port['status'],
                    svc_name=service[0],
                    port_name=processed_port['port_name'],
                    port=processed_port['port'],
                    protocol=processed_port['protocol'],
                    train=curr_train
                ))
    else:
        logger(
            f'App: <{app_name}> has it\'s Services Disabled', "BLUE")
        rows.append(create_row(
            app_name=app_name,
            status="svc_dis",
            svc_name=service[0],
            train=curr_train
        ))
    return rows


def process_port(port, app_name, svc_name):
    """
    Returns a processed port
    """
    # If there is no "enabled" key, it's probably main. Assume port is enabled.
    # If there is "enabled" key and it's true, port is enabled
    # If there is "enabled" key and it's false, port is disabled
    if (not 'enabled' in port[1]) or ('enabled' in port[1] and port[1]['enabled']):
        return {
            "port_name": port[0],
            "port": port[1]['port'],
            "protocol": port[1]['protocol'] if 'protocol' in port[1] else "TCP",
            "status": setup.Status.ACTIVE
        }
    else:
        logger(
            f'Port <{port[0]}> of Service: <{svc_name}> in App: <{app_name}> is Disabled', "YELLOW")
        return {"port_name": port[0], "svc_name": svc_name, "status": "port_dis"}


def create_port_list_content(port_list, train):
    """
    Creates and returns content to the port list file
    """
    content = ""
    table = []
    svc_und_table = []
    svc_dis_table = []
    port_und_table = []
    port_dis_table = []
    active_table = []
    # Deepcopy is a must here, otherwise, later when we delete keys, it will modify the original list as well
    filtered_list = copy.deepcopy(port_list)
    filtered_list = filter(lambda item: item['train'] == train, filtered_list)
    # Sort by name
    sorted_list = sorted(filtered_list, key=lambda item: item['app_name'])
    # Then sort by port number
    sorted_list = sorted(sorted_list, key=lambda item: item['port'])
    # Delete train key, as we don't need it anymore. So it won't end up in the markdown table
    for x in sorted_list:
        del x['train']
    for port in sorted_list:
        # When there was no port, we have set port to 0
        # That was to be easier to sort the list
        # Before we print it, we make it "-"
        if not port['port']:
            port['port'] = "-"
        if port['status'] == setup.Status.SVC_UND:
            svc_und_table.append(port)
        if port['status'] == setup.Status.SVC_DIS:
            svc_dis_table.append(port)
        if port['status'] == setup.Status.PORT_UND:
            port_und_table.append(port)
        if port['status'] == setup.Status.PORT_DIS:
            port_dis_table.append(port)
        if port['status'] == setup.Status.ACTIVE:
            active_table.append(port)
    # Order in which they will appear in the file
    table = svc_und_table + svc_dis_table + \
        port_und_table+port_dis_table + active_table
    content += f'## {train.capitalize()}'
    content += '\n\n'
    content += "| App | Service | Port Name | Port | Protocol | Status | Note |"
    content += '\n'
    content += "|:----|:-------:|:---------:|:----:|:--------:|:------:|:-----|"
    content += '\n'
    # Check that table has data
    if table:
        content += file_oper.create_table(table)
        content += '\n\n'
    return content


def append_conflicts_to(all_ports):
    """
    Modifies the list of ports and adds the conflict status
    """
    conflicts = []
    for port in all_ports:
        # For each port... if the port is a number (It's not "-")
        if port['port'] != 0:
            # Generate a list of port numbers(0 position holds the port numbers)
            temp_list = [conflict[0] for conflict in conflicts]
            # If the port number is in the... list
            if port['port'] in temp_list:
                # Get the index of the port number in the conflicts list
                index = temp_list.index(port['port'])
                # If the protocol of the port is the same as on the port in the mentioned index (1 position holds protocol)
                if port['protocol'] == conflicts[index][1]:
                    # Then append the app name to the to the list in position 2
                    conflicts[index][2].append(port['app_name'])
            else:
                # If the port number is in NOT the... list
                # Create it
                # Save, port number, protocol and app name
                conflicts.append(
                    [port['port'], port['protocol'], [port['app_name']]])
    # Get the real conflicts, by keeping only the ports that have more than one app in list in position 2
    conflicts = [c for c in conflicts if len(c[2]) > 1]
    # Modify all_ports to add the conflict info
    for port in all_ports:
        for conflict in conflicts:
            if port['port'] == conflict[0] and port['protocol'] == conflict[1]:
                port['note'] = setup.PORT_CONFLICT_NOTE
                for app in conflict[2]:
                    if app != port['app_name']:
                        port['note'] += app
                        port['note'] += " "


# Example output:
# [
#   [
#     53,
#     "UDP",
#     ["k8s-gateway", "pihole", "mosdns", "adguard-home", "technitium"]
#   ],
#   [10113, "TCP", ["clarkson", "quassel-core"]],
#   [25, "TCP", ["protonmail-bridge", "anonaddy"]],
#   [3478, "UDP", ["unifi", "ispy-agent-dvr"]],
#   [1935, "TCP", ["owncast", "frigate"]],
#   [8008, "TCP", ["synapse", "acestream"]]
# ]


def get_next_available_port(ports_list):
    next_port = 0
    for port in ports_list:
        # We might want to update this range in the future
        if port['port'] > next_port and port['port'] > 10000 and port['port'] < 10700:
            next_port = port['port']
    next_port += 1
    return f"""
> Next available port should be {next_port}
"""
