import os
from setuptools import setup, find_packages
from os.path import abspath, dirname, join

# Path where trains are stored
TRAINS_PATH = os.getenv('TRAINS_PATH', './charts')

# Path where "mirror" is stored (mirror contains folders named after the apps, which they contain the Dockerfile)
IMAGE_PATH = os.getenv('IMAGE_PATH_PATH', './mirror')


# Name and path of the port list file
PORT_LIST_FILE = os.getenv('PORT_LIST_FILE', './default_port_list.md')


# Name and path of the volume list file
VOLUME_LIST_FILE = os.getenv('VOLUME_LIST_FILE', './volume_list.md')


# Name and path of the description list file
DESCRIPTION_LIST_FILE = os.getenv(
    'DESCRIPTION_LIST_FILE', './description_list.md')

# Exclude specific trains
exc_trains = [item for item in os.getenv('EXCLUDE_TRAINS').split(
    ',')] if os.getenv('EXCLUDE_TRAINS') else None
EXCLUDE_TRAINS = [
    # "dev",
] if not exc_trains else exc_trains


exc_apps = [item for item in os.getenv('EXCLUDE_APPS').split(
    ',')] if os.getenv('EXCLUDE_APPS') else None
# Exclude specific apps
EXCLUDE_APPS = [
    # "traefik",
] if not exc_apps else exc_apps


# This ordered will be used,
# any trains not listed here and not excluded
# will be added automatically to the end
# Any trains not existing in file system will be ignored
# Also, don't forget to add comma on each line -.- It happily accepts it without and messes the order
train_ord = [item for item in os.getenv('TRAIN_ORDER_FOR_FILES').split(
    ',')] if os.getenv('TRAIN_ORDER_FOR_FILES') else None
TRAIN_ORDER_FOR_FILES = [
    "stable",
    "dependency",
    "incubator"
] if not train_ord else train_ord


# Print Verbose Output
VERBOSE = os.getenv('VERBOSE', 'True').lower() in ('true', '1')

# Split even n character
SPLIT_DESCRIPTION_EVERY = int(os.getenv('SPLIT_DESCRIPTION_EVERY', "70"))
PRINT_IMAGE_SOURCE = os.getenv(
    'PRINT_IMAGE_SOURCE', 'True').lower() in ('true', '1')

# Set to false to NOT generate a file
GENERATE_PORT_FILE = os.getenv(
    'GENERATE_PORT_FILE', 'True').lower() in ('true', '1')
GENERATE_VOLUME_FILE = os.getenv(
    'GENERATE_VOLUME_FILE', 'True').lower() in ('true', '1')
GENERATE_DESCRIPTION_FILE = os.getenv(
    'GENERATE_DESCRIPTION_FILE', 'True').lower() in ('true', '1')


# Volumes make sense to order by app name,
# So each app has it's volumes one after the other.
# If we sort by status, (eg disabled etc), volumes will be all over the place
SORT_VOLUMES_BY_STATUS = os.getenv(
    'SORT_VOLUMES_BY_STATUS', 'False').lower() in ('true', '1')


# URL to return if the URL we are trying to get does not exist
FALLBACK_URL = os.getenv('FALLBACK_URL', 'https://truecharts.org/')


# Size for images in Description list
IMAGE_HEIGHT = 25
IMAGE_WIDTH = 25


class Status:
    PORT_DIS = "Port is Disabled"
    PORT_UND = "Port not Defined"
    SVC_DIS = "Service is Disabled"
    SVC_UND = "Service not Defined"
    ACTIVE = "Active"
    VOL_UND = "Persistence not Defined"
    VOL_DIS = "Persistence is Disabled"
    MNT_UND = "Mount Path not Defined"
    ENABLED = "Enabled"
    DISABLED = "Disabled"
    NO_DESC = "No Description"


PORT_CONFLICT_NOTE = "Potential conflict with: "


PORT_LIST_INTRO = """# Default Ports

This document lists the default ports used by Apps.
These defaults can of course be changed, but as we guarantee "sane, working defaults",
they should provide no or minimal conflicts without being changed.

"""


PORT_LIST_OUTRO = """## Official Apps

> Please keep mind that this list is not updated automatically like the rest of this doc

| App            |   Service   | Port  |                     Note                     |
| :------------- | :---------: | :---: | :------------------------------------------: |
| chia           |    main     | 8444  |                                              |
| chia           | farmerport  | 8447  |                                              |
| collabora      |    main     | 9980  |                                              |
| emby           |    main     | 9096  |                                              |
| home-assistant |    main     | 20810 |                                              |
| ipfs           |  swarmport  | 9401  |                                              |
| ipfs           |   apiport   | 9501  |                                              |
| ipfs           | gatewayport | 9880  |                                              |
| machinaris     |    main     | 9003  |                                              |
| machinaris     |   apiport   | 8927  |                                              |
| minio          |    main     | 9000  | Potential conflict with traefik (TrueCharts) |
| minio          | consoleport | 9002  |                                              |
| netdata        |    main     | 20489 |                                              |
| nextcloud      |    main     | 9001  |                                              |
| photoprism     |    main     | 20800 |                                              |
| pihole         |    main     | 20720 |                                              |
| pihole         |   dns-tcp   | 20721 |                                              |
| pihole         |   dns-upd   | 20721 |                                              |
| pihole         |    dhcp     | 20722 |                                              |
| plex           |    main     | 32400 |  Potential conflict with plex (TrueCharts)   |
| qbittorent     |    main     | 20909 |                                              |
| qbittorent     |  tcp_port   | 20988 |                                              |
| qbittorent     |  udp_port   | 20989 |                                              |
| syncthing      |    main     | 20910 |                                              |
| syncthing      |  tcp_port   | 20978 |                                              |
| syncthing      |  udp_port   | 20979 |                                              |

## TrueNAS Scale Services

> Please mind that this list is not updated automatically like the rest of this doc

| Service | Port | Protocol | Note |
| :------ | :--: | :------: | :--: |
| ssh     |  22  |   TCP    |      |
| webui   |  80  |   HTTP   |      |
| webui   | 443  |  HTTPS   |      |

## Ports that are blocked in major web browsers

> Please mind that this list is not updated automatically like the rest of this doc

| Port  |            Used by (example)             |
| :---: | :--------------------------------------: |
|   1   |                  tcpmux                  |
|   7   |                   echo                   |
|   9   |                 discard                  |
|  11   |                  systat                  |
|  13   |                 daytime                  |
|  15   |                 netstat                  |
|  17   |                   qotd                   |
|  19   |                 chargen                  |
|  20   |                 ftp data                 |
|  21   |                ftp access                |
|  22   |                   ssh                    |
|  23   |                  telnet                  |
|  25   |                   smtp                   |
|  37   |                   time                   |
|  42   |                   name                   |
|  43   |                 nicname                  |
|  53   |                  domain                  |
|  69   |                   tftp                   |
|  77   |                 priv-rjs                 |
|  79   |                  finger                  |
|  87   |                 ttylink                  |
|  95   |                  supdup                  |
|  101  |                hostriame                 |
|  102  |                 iso-tsap                 |
|  103  |                 gppitnp                  |
|  104  |                 acr-nema                 |
|  109  |                   pop2                   |
|  110  |                   pop3                   |
|  111  |                  sunrpc                  |
|  113  |                   auth                   |
|  115  |                   sftp                   |
|  117  |                uucp-path                 |
|  119  |                   nntp                   |
|  123  |                   NTP                    |
|  135  |              loc-srv /epmap              |
|  137  |                 netbios                  |
|  139  |                 netbios                  |
|  143  |                  imap2                   |
|  161  |                   snmp                   |
|  179  |                   BGP                    |
|  389  |                   ldap                   |
|  427  | SLP (Also used by Apple Filing Protocol) |
|  465  |                 smtp+ssl                 |
|  512  |               print / exec               |
|  513  |                  login                   |
|  514  |                  shell                   |
|  515  |                 printer                  |
|  526  |                  tempo                   |
|  530  |                 courier                  |
|  531  |                   chat                   |
|  532  |                 netnews                  |
|  540  |                   uucp                   |
|  548  |       AFP (Apple Filing Protocol)        |
|  554  |                   rtsp                   |
|  556  |                 remotefs                 |
|  563  |                 nntp+ssl                 |
|  587  |              smtp (rfc6409)              |
|  601  |          syslog-conn (rfc3195)           |
|  636  |                 ldap+ssl                 |
|  989  |                ftps-data                 |
|  990  |                   ftps                   |
|  993  |                 ldap+ssl                 |
|  995  |                 pop3+ssl                 |
| 1719  |               h323gatestat               |
| 1720  |               h323hostcall               |
| 1723  |                   pptp                   |
| 2049  |                   nfs                    |
| 3659  |       apple-sasl / PasswordServer        |
| 4045  |                  lockd                   |
| 5060  |                   sip                    |
| 5061  |                   sips                   |
| 6000  |                   X11                    |
| 6566  |                sane-port                 |
| 6665  |      Alternate IRC [Apple addition]      |
| 6666  |      Alternate IRC [Apple addition]      |
| 6667  |      Standard IRC [Apple addition]       |
| 6668  |      Alternate IRC [Apple addition]      |
| 6669  |      Alternate IRC [Apple addition]      |
| 6697  |                IRC + TLS                 |
| 10080 |                  Amanda                  |

> Note: TCP and UDP ports that are the same in some Apps, are not by mistake

> If you notice something wrong in the above info, please notify us so we can update the generator script
"""


VOLUME_LIST_INTRO = """# Mounted Volumes

This document lists the mounted volumes for each App.
The intro needs improvement ;)

"""

VOLUME_LIST_OUTRO = """> If you notice something wrong in the above info, please notify us so we can update the generator script
"""


DESCRIPTION_LIST_INTRO = """# Apps List

> List of all our apps with a short description

"""

DESCRIPTION_LIST_OUTRO = """> If you notice something wrong in the above info, you are more than welcome to submit a PR, updating Chart.yaml for the app in question
"""