from helpers.logger import logger
from lib import file_oper
from pathlib import Path
import helpers.setup
import copy


def get_volume(app):
    """
    Returns the PERSISTENCE section of an app
    """
    data = file_oper.get_values(Path.joinpath(app, "values.yaml"))

    return data['persistence'] if 'persistence' in data else None


def get_raw_volumes_list(apps):
    """
    Returns a LIST of dicts
    Each Dict has the APP name and the PERSISTENCE Section
    """
    volume_list = []
    for app in apps:
        volume = get_volume(app)
        if not volume is None:
            volume_list.append({"app_name": app.stem, "persistence": volume})
        else:
            volume_list.append(
                {"app_name": app.stem, "persistence": False})

    return volume_list


def get_processed_volumes_list(raw_volumes_list, curr_train):
    """
    Returns a processes list of volumes
    """
    volume_list = []
    for volume_section in raw_volumes_list:
        # If there is no service, create a row accordingly
        if not volume_section['persistence']:
            logger(
                f'App: <{volume_section["app_name"]}> has no Persistence Defined', "GREEN")
            volume_list.append(create_row(
                app_name=volume_section['app_name'],
                status="vol_und",
                train=curr_train
            ))
        else:
            # if there is service, process it
            for volume in volume_section['persistence'].items():
                volume_list.append(process_volume(
                    volume, volume_section['app_name'], curr_train))

    return volume_list


def process_volume(volume, app_name, curr_train):
    """
    Processes the persistence and create rows
    """
    if 'enabled' in volume[1] and volume[1]['enabled']:
        if not 'mountPath' in volume[1]:
            if volume[0] == "varrun":
                return create_row(
                    app_name=app_name,
                    status="enabled",
                    vol_name=volume[0],
                    vol_type="emptyDir",
                    mountPath="/var/run",
                    train=curr_train
                )
            else:
                logger(
                    f'Persistence: <{volume[0]}> of App: <{app_name}> has no mountPath defined, probably varrun', "RED")
                return create_row(
                    app_name=app_name,
                    status="mnt_und",
                    vol_name=volume[0],
                    train=curr_train
                )
        else:
            temp = {}
            temp['type'] = volume[1]['type'] if 'type' in volume[1] else "PVC"
            temp['mountPath'] = volume[1]['mountPath'] if 'mountPath' in volume[1] else "-"
            temp['hostPath'] = volume[1]['hostPath'] if 'hostPath' in volume[1] else "-"
            temp['mode'] = "Read Only" if 'readOnly' in volume[1] and volume[1]['readOnly'] else "Read/Write"
            return create_row(
                app_name=app_name,
                status="enabled" if volume[1]['enabled'] else "disabled",
                train=curr_train,
                vol_name=volume[0],
                vol_type=temp['type'],
                mountPath=temp['mountPath'],
                hostPath=temp['hostPath'],
                mode=temp["mode"]
            )
    else:
        logger(f'App: <{app_name}> has it\'s Persistence Disabled', "BLUE")
        return create_row(
            app_name=app_name,
            status="vol_dis",
            vol_name=volume[0],
            train=curr_train,
            vol_type="emptyDir" if volume[0] == "varrun" else "PVC"
        )


def create_volume_list_content(volume_list, train):
    """
    Creates and returns content to the volume list file
    """
    content = ""
    table = []

    filtered_list = copy.deepcopy(volume_list)
    filtered_list = filter(lambda item: item['train'] == train, filtered_list)

    sorted_list = sorted(filtered_list, key=lambda item: item['app_name'])
    for x in sorted_list:
        del x['train']

    if setup.SORT_VOLUMES_BY_STATUS:
        vol_und_table = []
        vol_dis_table = []
        mnt_und_table = []
        disabled_table = []
        enabled_table = []
        for vol in sorted_list:
            if vol['status'] == setup.Status.VOL_UND:
                vol_und_table.append(vol)
            if vol['status'] == setup.Status.VOL_DIS:
                vol_dis_table.append(vol)
            if vol['status'] == setup.Status.MNT_UND:
                mnt_und_table.append(vol)
            if vol['status'] == setup.Status.DISABLED:
                disabled_table.append(vol)
            if vol['status'] == setup.Status.ENABLED:
                enabled_table.append(vol)
        # Order in which they will appear in the file
        table = vol_und_table + vol_dis_table + \
            mnt_und_table + disabled_table + enabled_table
    else:
        table = sorted_list

    content += f'## {train.capitalize()}'
    content += '\n\n'
    content += "| App | Volume Name | Type | Host Path | Mount Path | Mode | Status |"
    content += '\n'
    content += "|:----|:-----------:|:----:|:----------|:-----------|:----:|:------:|"
    content += '\n'
    # Check that table has data
    if table:
        content += file_oper.create_table(table)
        content += '\n\n'

    return content


def create_row(app_name, status, train, vol_name="-", vol_type="PVC", mountPath="-",  hostPath="-", mode="Read/Write"):
    """
    Creates a row for the processed volumes list
    """
    if status == "enabled":
        status = setup.Status.ENABLED
    if status == "disabled":
        status = setup.Status.DISABLED
    if status == "vol_und":
        status = setup.Status.VOL_UND
        vol_type = "-"
        mode = "-"
    if status == "vol_dis":
        status = setup.Status.VOL_DIS
    if status == "mnt_und":
        status = setup.Status.MNT_UND
    return {
        "app_name": app_name,
        "vol_name": vol_name,
        "type": vol_type,
        "hostPath": hostPath,
        "mountPath": mountPath,
        "mode": mode,
        "status": status,
        "train": train
    }
