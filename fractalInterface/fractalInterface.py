'''
User Apple's Audio-Midi Setup to connect to MD-BT01.
This way apple handles all the BT communication
Will this work for RPI?

probably not; but we can use this to build the sysex IO on laptop
without having to wire into device.

For sysex communication, we may want to thread the read/write,
such that a request-response is correctly captured; but how?

submit_req_resp(msg):
-> send message
-> wait response (with timeout); this will pool get_message until a
    valid response is received
'''


import time
import rtmidi
import mido



"""
preset_state {
    blocks: {
        block_name: {
            
        }
    }
}
"""


class FractalInterface:

    def __init__(self, model='FM3', midi_in=None, midi_out=None, channel=1):
        # validate model is in constants
        self.header = [0xF0, 0x00, 0x01, 0x74]
        self.model = model
        self.model_code = self.__fractal_models__(model)
        self.midi_in = midi_in
        self.midi_out = midi_out
        # create parsing callback:
        self.midi_in.set_callback(self.parse_midi_in)
        self.expected_response_buffer = []
        self.last_received = []
        self.channel = channel
        # Preset_state
        self.preset_state = {}


    @staticmethod
    def __lsb_msb_to_int__(arr=(0, 0)):
        return arr[-1] << 7 ^ arr[0]

    @staticmethod
    def __int_to_lsb_msb__(val=0):
        return [val & 0x7f, (val >> 7) & 0x7f]

    @staticmethod
    def __create_checksum__(msg=()):
        ret = msg.copy()
        cs = ret[0]
        for j in ret[1:]:
            cs ^= j

        cs &= 0x7f
        ret.append(cs)
        ret.append(0xf7)
        return ret

    @staticmethod
    def __fractal_models__(model=None):
        models = {
            "AXEFXSTD": 0x00,
            "AXEFXULT": 0x01,
            "MFC101": 0x02,
            "AXEFX2": 0x03,
            "MFC101MK3": 0x04,
            "FX8": 0x05,
            "AXEFX2XL": 0x06,
            "AXEFX2XLP": 0x07,
            "AX8": 0x08,
            "FX8MK2": 0x0A,
            "AXEFX3": 0x10,
            "FM3": 0x11
        }
        return models.get(model, None)

    def parse_midi_in(self, data, delta_t):
        """
        This callback is triggered any time a midi message comes in
        on the interface
        @param data is tuple of (data_array, delta_t)
        @param delta_t is None
        """
        midi_data = data[0]
        delta_t = data[1]
        self.last_received = [hex(v) for v in midi_data]
        print("midi received: {}".format([hex(v) for v in midi_data]))
        i = 0
        while i != len(self.expected_response_buffer):
            expected_response, query, response_function = self.expected_response_buffer[i]
            print("checking buffer")
            # if response matches expected response:
            if midi_data[:len(expected_response)] == expected_response and \
               midi_data != query:  # ignores MIDI THRU
                if response_function:
                    response_function(midi_data[len(expected_response):-2])
                self.expected_response_buffer.pop(i)
                i = i - 1
            i = i + 1

    def set_preset_by_value(self, preset_val):
        """
        Generate Bank Select + Program Change messages based on bank
        @param preset_val:
        @return:
        """
        bank = 0
        pc = preset_val
        if 127 < pc < 256:
            bank = 1
            pc = pc - 128
        if 256 < pc < 384:
            bank = 2
            pc = pc - 256
        if 384 < pc:
            bank = 3
            pc = pc - 384
        self.midi_out.send_message(mido.Message('control_change', control=0, value=bank, channel=self.channel).bytes())
        self.midi_out.send_message(mido.Message('program_change', program=pc, channel=self.channel).bytes())
        self.get_current_preset_name()

    def get_firmware_version(self):
        request = self.header + [self.model_code] + [0x08]
        query = self.__create_checksum__(request)
        self.midi_out.send_message(query)
        self.expected_response_buffer.append((request, query, self.parse_firmware_version))


    def parse_firmware_version(self, data):
        firmware_major = data[0]
        firmware_minor = data[1]
        print("firmware version received: {}.{}".format(firmware_major, firmware_minor))

    def get_current_preset_name(self):
        request = self.header + [self.model_code] + [0x0D, 0x7F, 0x7F]
        expected_response = request[:-2]
        query = self.__create_checksum__(request)
        self.midi_out.send_message(query)
        self.expected_response_buffer.append((expected_response, query, self.parse_current_preset_name))

    def parse_current_preset_name(self, data):
        """
        [self.header self.model_code, 0x0D, 0x7F, 0x7F, LSB, MSB, Bytes...]
        LSB + MSB represent the preset number
        the rest of the bytes
        @param data: midi message
        @return:
        """
        current_preset_id = self.__lsb_msb_to_int__(data[:2])
        current_preset_name = (''.join([chr(k) for k in data[2:-1]])).rstrip().lstrip()
        print("present name received: {:03d}: {}".format(current_preset_id, current_preset_name))





if __name__=="__main__":

    INTERFACE = 'MD-BT01 Bluetooth'
    midiInput = rtmidi.MidiIn()
    midiOutput = rtmidi.MidiOut()
    interface_available = False

    while not interface_available:

        if INTERFACE in midiInput.get_ports() and \
                INTERFACE in midiOutput.get_ports():
            interface_available = True
        else:
            time.sleep(5)

    # open input port:
    midiRX = midiInput.open_port(midiInput.get_ports().index(INTERFACE))
    midiRX.ignore_types(sysex=False, timing=False)
    # open output port:
    midiTX = midiOutput.open_port(midiOutput.get_ports().index(INTERFACE))

    interface = FractalInterface(midi_in=midiRX, midi_out=midiTX)

    interface_functions = [m for m in interface.__dir__() if 'get_' in m]

    interface.get_current_preset_name()

    cmd = ""
    while cmd not in ['quit', 'q', 'exit']:
        cmd = input(">> ")
        if cmd in interface_functions:
            getattr(interface, cmd)()
