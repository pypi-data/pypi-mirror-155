import setup
from pathlib import Path


def get_trains():
    """
    Returns TRAINS that are not excluded
    """
    if Path(setup.TRAINS_PATH).exists():
        trains = [train for train in Path(
            setup.TRAINS_PATH).iterdir() if train.stem not in setup.EXCLUDE_TRAINS]

    return trains


def get_apps(train):
    """
    Returns APPS that are nto excluded
    """
    apps = [app for app in Path(train).iterdir()
            if app.stem not in setup.EXCLUDE_APPS]

    return apps


def get_ordered_trains(trains):
    """
    Returns trains in order based on the config variable
    """
    # Convert list variable to list of Paths
    train_order = [
        Path(setup.TRAINS_PATH, train)
        for train in setup.TRAIN_ORDER_FOR_FILES
    ]
    # Add trains from config variable that also exists in the actual trains
    ordered_trains = [
        train for train in train_order
        if train in trains
    ]
    # Add the rest of the trains that are not in the config variable but exists
    ordered_trains += [train for train in trains if train not in train_order]
    return ordered_trains
