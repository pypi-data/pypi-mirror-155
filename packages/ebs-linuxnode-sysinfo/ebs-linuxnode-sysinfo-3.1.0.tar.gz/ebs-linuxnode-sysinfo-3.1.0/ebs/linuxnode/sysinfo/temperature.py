

import re
import psutil

from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks

from functools import partial
from .base import SysInfoBase


class TemperatureInfo(SysInfoBase):

    _cpu_sensor_candidates = [
        'cpu',
        'k10temp',
        'coretemp:Package id 0',
    ]

    _gpu_sensor_candidates = [
        'gpu',
        'amdgpu',
    ]

    def __init__(self, *args):
        super(TemperatureInfo, self).__init__(*args)

    def install(self):
        super(TemperatureInfo, self).install()
        result = psutil.sensors_temperatures()
        for device in result.keys():
            zones = result[device]
            if len(zones) == 1:
                self._items[device] = partial(self._read_temp, device, 0)
            else:
                self._items[device] = SysInfoBase(self.actual)
                for idx, zone in enumerate(zones):
                    self._items[device].items[zone.label] = partial(self._read_temp, device, idx)
        if self.actual.config.platform == 'rpi':
            self._items['gpu'] = self._read_raspi_gpu_temp
        if 'cpu' not in self._items.keys():
            self._items['cpu'] = self._find_default_temperature(self._cpu_sensor_candidates)
        if 'gpu' not in self._items.keys():
            self._items['gpu'] = self._find_default_temperature(self._gpu_sensor_candidates)

    def _find_default_temperature(self, candidates):
        for candidate in candidates:
            parts = candidate.split(':')
            candidate_device = parts[0]
            candidate_zone = None
            if len(parts) > 1:
                candidate_zone = parts[1]
            if candidate_device not in self._items.keys():
                continue
            if candidate_zone and candidate_zone not in getattr(self, candidate_device)._items.keys():
                continue
            return partial(self._proxy_temperature, candidate_device, candidate_zone)

    def _proxy_temperature(self, device, zone=None):
        if not zone:
            return getattr(self, device)
        else:
            return getattr(getattr(self, device), zone)

    @inlineCallbacks
    def _read_temp(self, device, zone):
        result = yield threads.deferToThread(psutil.sensors_temperatures)
        return result[device][zone].current

    def _read_raspi_gpu_temp(self):
        def _handle_result(result):
            return float(re.findall(r"[\d.]+", result.decode())[0])
        d = self._shell_execute(['vcgencmd', 'measure_temp'], _handle_result)
        return d
