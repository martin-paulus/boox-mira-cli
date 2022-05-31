# Copyright (C) 2022 Martin Paulus <m.paulus@linuxoperator.nl>
'''
utils for the Boox Mira 13.3" device
'''
from typing import Final, List, Optional, TypedDict
import hid


class CommandID(TypedDict):
    '''
    command ids
    '''
    fullRefresh:    int
    swMode:         int
    refreshTime:    int
    a2Feq:          int
    contrast:       int
    light:          int
    coldLight:      int
    warmLight:      int
    vcom:           int
    ditherMode:     int
    colorFilter:    int
    autoDither:     int
    version:        int
    fpgaVersion:    int
    all:            int
    reset:          int
    req_upgrade:    int
    write_firmware: int
    upgrade_done:   int
    erasing:        int


CMD: Final[CommandID] = {
    'fullRefresh':    1,      # OK
    'swMode':         2,      # OK: 1-3
    'refreshTime':    3,
    'a2Feq':          4,      # OK: 11-4; Home/index.vue: 1-7, step 1
    'contrast':       5,      # OK: 0-15:
                              # Home/index.vue': min-max, black_filter
    'light':          6,
    'coldLight':      6,      # OK: 0-255; Home/index.vue: 0-255
    'warmLight':      7,      # OK: 0-255; Home/index.vue: 0-255
    'vcom':           8,
    'ditherMode':     9,
    'colorFilter':    0x11,   # 0-255. 0-255?;
                              # Home.index.vue': 0-127, white_filter
    'autoDither':     0x12,
    'version':        0x0a,
    'fpgaVersion':    0x0b,
    'all':            0x0f,   # OK
    'reset':          0x1f,
    'req_upgrade':    0x21,
    'write_firmware': 0x22,
    'upgrade_done':   0x23,
    'erasing':        0x25
}


class DeviceID(TypedDict):
    '''
    usb device id
    '''
    vendor_id:  int
    product_id: int


DEVICE_ID: Final[DeviceID] = {
    'vendor_id':  0x0416,
    'product_id': 0x5020
}


def compose_command(
    direction: str='receive', topic: int=CMD['all'], value: Optional[int]=None
) -> bytes:
    '''
    compose HID payload to submit as command
    distinguish reading from writing as the device does
    '''
    mesg = bytearray(65)
    head: int = 128 if direction == 'receive' else 0
    mesg[1] = head | topic
    if value:
        # this.setSettings(CMD.colorFilter,
        #     [this.whiteFilter, this.blackFilter])
        # this.sendCmd(command().setColorFilter(), [255 - val[0], val[1]])
        if topic == CMD['colorFilter']:
            mesg[2] = value
            mesg[3] = 0
        else:
            mesg[2] = value
    return bytes(mesg)


def detect_device(device_id: DeviceID=DEVICE_ID) -> List[str]:
    '''
    scan hid devices for matches of DEVICE_ID
    '''
    devices: List[str] = hid.enumerate(
        vid=device_id['vendor_id'],
        pid=device_id['product_id']
    )
    return devices


class Versions(TypedDict, total=False):
    '''
    versions parsed from hid response
    '''
    mcuHV:  str
    mcuSV:  str
    rtdHV:  str
    rtdSV:  str
    fpgaHV: str
    fpgaSV: str
    full:   str


class SettingsVersions(TypedDict, total=False):
    '''
    settings and versions parsed from hid response
    '''
    sw_mode:      int
    auto_time:    int
    req:          int
    contrast:     int
    coldLight:    int
    warmLight:    int
    vcom:         int
    version:      List[int]
    versionAll:   Versions
    versionFull:  str


def parse_parameters(settings_block: bytes) -> SettingsVersions:
    '''
    parse settngs into human-readable form
    '''
    versions = view_version(settings_block[32:64])
    version_full = versions.pop('full')
    return {
        'sw_mode':      int(settings_block[1:2].hex(), 16),   # OK
                                                              # (refresh mode)
        'auto_time':    int(settings_block[2:4].hex(), 16),
        'req':          int(settings_block[4:5].hex(), 16),   # OK (speed)
        'contrast':     int(settings_block[5:6].hex(), 16),   # OK
        'coldLight':    int(settings_block[6:7].hex(), 16),   # OK
        'warmLight':    int(settings_block[7:8].hex(), 16),   # OK
        'vcom':         int(settings_block[8:9].hex(), 16),   # b/w filter?
        'version':      [
            int(settings_block[9:10].hex(), 16),
            int(settings_block[10:11].hex(), 16)
        ],
        'versionAll':   versions,
        'versionFull':  version_full
    }


def view_version(version_block: bytes) -> Versions:
    '''
    format version information
    '''
    # versionAll = 'Ver:b@03:6@08:a@05-1af2fdf\x00\x00\x00\x00\x00\x00'
    # versionAll.replace(/^[\s\uFEFF\xA0\0]+|[\s\uFEFF\xA0\0]+$/g, "")
    #   => /g: all occurences
    #   => ^: starts with
    #       => \s: single space (incl, space, tab, form feed, line feed, etc.)
    #       => \uFEFF: zero width no-break space
    #       => \xA0: no-break space
    #       => \0: null character
    #   => $: ends with
    #       => (same collection of spaces)
    #   => 'Ver:b@03:6@08:a@05-1af2fdf'
    # versionAll.replace(/Ver/, '')
    #   => ':b@03:6@08:a@05-1af2fdf'
    #
    version_chunk = ''.join(version_block.decode().split())
    version_chunk = version_chunk.replace('Ver', '', 1)
    return {
        'mcuHV':  version_chunk[1:2],
        'mcuSV':  version_chunk[3:5],
        'rtdHV':  version_chunk[6:7],
        'rtdSV':  version_chunk[8:10],
        'fpgaHV': version_chunk[11:12],
        'fpgaSV': version_chunk[13:15],
        'full':   version_block.decode()
    }
