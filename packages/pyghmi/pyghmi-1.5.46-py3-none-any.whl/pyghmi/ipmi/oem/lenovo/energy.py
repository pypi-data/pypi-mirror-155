# Copyright 2017 Lenovo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

import pyghmi.constants as const
import pyghmi.exceptions as pygexc
import pyghmi.ipmi.sdr as sdr


class EnergyManager(object):

    def __init__(self, ipmicmd):
        # there are two IANA possible for the command set, start with
        # the Lenovo, then fallback to IBM
        # We start with a 'find firmware instance' to test the water and
        # get the handle (which has always been the same, but just in case
        self.iana = bytearray(b'\x66\x4a\x00')
        try:
            rsp = ipmicmd.xraw_command(netfn=0x2e, command=0x82,
                                       data=self.iana + b'\x00\x00\x01')
        except pygexc.IpmiException as ie:
            if ie.ipmicode == 193:  # try again with IBM IANA
                self.iana = bytearray(b'\x4d\x4f\x00')
                rsp = ipmicmd.xraw_command(netfn=0x2e, command=0x82,
                                           data=self.iana + b'\x00\x00\x01')
            else:
                raise
        if rsp['data'][4:6] not in (b'\x02\x01', b'\x02\x06', b'\x02\x09'):
            raise pygexc.UnsupportedFunctionality(
                "Energy Control {0}.{1} not recognized".format(rsp['data'][4],
                                                               rsp['data'][5]))
        self.modhandle = bytearray(rsp['data'][6:7])
        if self.get_ac_energy(ipmicmd):
            self.supportedmeters = ('AC Energy', 'DC Energy')
        else:
            self.supportedmeters = ('DC Energy',)

    def get_energy_precision(self, ipmicmd):
        rsp = ipmicmd.xraw_command(
            netfn=0x2e, command=0x81,
            data=self.iana + self.modhandle + b'\x01\x80')
        print(repr(rsp['data'][:]))

    def get_ac_energy(self, ipmicmd):
        try:
            rsp = ipmicmd.xraw_command(
                netfn=0x2e, command=0x81,
                data=self.iana + self.modhandle + b'\x01\x82\x01\x08')
            # data is in millijoules, convert to the more recognizable kWh
            return float(
                struct.unpack('!Q', rsp['data'][3:])[0]) / 1000000 / 3600
        except pygexc.IpmiException as ie:
            if ie.ipmicode == 0xcb:
                return 0.0
            raise

    def get_dc_energy(self, ipmicmd):
        rsp = ipmicmd.xraw_command(
            netfn=0x2e, command=0x81,
            data=self.iana + self.modhandle + b'\x01\x82\x00\x08')
        # data is in millijoules, convert to the more recognizable kWh
        return float(struct.unpack('!Q', rsp['data'][3:])[0]) / 1000000 / 3600


class Energy(object):

    def __init__(self, ipmicmd):
        self.ipmicmd = ipmicmd

    def get_energy_sensor(self):
        # read the cpu usage

        try:
            rsp = self.ipmicmd.xraw_command(netfn=0x04,
                                            command=0x2d,
                                            bridge_request={"addr": 0x2c,
                                                            "channel": 0x06},
                                            data=[0xbe])
        except pygexc.IpmiException:
            return
        rdata = bytearray(rsp["data"])
        cpu_usage = rdata[0] * 100 / 0xff
        # mimic the power sensor
        temp = {'name': "CPU_Usage",
                'health': const.Health.Ok,
                'states': [],
                'state_ids': [],
                'type': "Processor",
                'units': "%",
                'value': cpu_usage,
                'imprecision': None}
        yield (sdr.SensorReading(temp, temp['units']))


if __name__ == '__main__':
    import os
    import pyghmi.ipmi.command as cmd
    import sys
    c = cmd.Command(sys.argv[1], os.environ['BMCUSER'], os.environ['BMCPASS'])
    EnergyManager(c).get_dc_energy(c)
