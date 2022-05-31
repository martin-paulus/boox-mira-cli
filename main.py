# Copyright (C) 2022 Martin Paulus <m.paulus@linuxoperator.nl>
'''
main class for the Boox Mira 13.3" device
'''
import hid
from .utils import CMD, compose_command, detect_device, parse_parameters


class BooxMira:
    '''
    class for the Boox Mira 13.3" device
    '''
    def __init__(self):
        devices = detect_device()
        self._full_version = 'N/A'
        if len(devices) >= 2:
            print('multiple mira monitors detected\n')  # WARNING
        try:
            self._hid = hid.Device(
                devices[0]['vendor_id'],
                devices[0]['product_id']
            )
            # self._hid.nonblocking = 1
        except IndexError:
            print('no mira monitor detected\n')   # ERROR
            raise

    def _read(self, message=None):
        if not message:
            return None
        self._hid.write(message)
        return self._hid.read(64)

    def _write(self, message=None):
        if not message:
            return
        self._hid.write(message)

    def all_settings(self):
        '''
        show current values of all settings
        '''
        cmd = compose_command(direction='receive', topic=CMD['all'])
        raw_result = self._read(cmd)
        settings_versions = parse_parameters(raw_result)
        self._full_version = settings_versions.pop('versionFull')
        return settings_versions

    def cold_light(self, value):
        '''
        configure the blue light intensity
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['coldLight'], value=value
        )
        self._write(cmd)

    def color_filter(self, white, black):
        '''
        configure the white balance
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['colorFilter'],
            value=[white, black]
        )
        self._write(cmd)

    def contrast(self, value):
        '''
        configure the contrast
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['contrast'], value=value
        )
        self._write(cmd)

    def full_refresh(self):
        '''
        trigger a full display refresh
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['fullRefresh']
        )
        self._write(cmd)

    def refresh_mode(self, value):
        '''
        configure the display refresh mode
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['swMode'], value=value
        )
        self._write(cmd)

    def speed(self, value):
        '''
        configure the display refresh speed
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['a2Feq'], value=value
        )
        self._write(cmd)

    def warm_light(self, value):
        '''
        configure the yellow light intensity
        '''
        cmd = compose_command(
            direction='submit', topic=CMD['warmLight'], value=value
        )
        self._write(cmd)
