# import adafruit_ble
# import adafruit_ble_midi
# import adafruit_midi
# from adafruit_midi.control_change import ControlChange
# from adafruit_midi.note_off import NoteOff
# from adafruit_midi.note_on import NoteOn
# from adafruit_midi.pitch_bend import PitchBend
# from adafruit_midi.program_change import ProgramChange
# from adafruit_midi.system_exclusive import SystemExclusive
# from fractalInterface.fractalConstants import *
# from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
#
# def int2LSBMSB(val):
#     return [val & 0x7f, val >> 7]
#
#
# def LSBMSB2Int(arr):
#     return arr[-1] << 7 ^ arr[0]
#
#
# def inject_checksum(msg):
#     cs = msg[0]
#     for j in msg[1:]:
#         cs ^= j
#
#     cs &= 0x7f
#     msg.append(cs)
#     # msg.append(0xf7)
#     return msg
#
# # setup BLE
# ble = adafruit_ble.BLERadio()
#
# # how to run the scan/stop in background?
# # and how to get the device list cleaner?
# r = ble.start_scan()
# ble.stop_scan()
#
# t = r.__next__()
# while t.complete_name != 'MD-BT01':
#     t = r.__next__()
#
#
# conn = ble.connect(t)
# # create MIDIService object through the connection:
# serv = conn[adafruit_ble_midi.MIDIService]
# # create MIDI Device using the service:
# midi = adafruit_midi.MIDI(midi_in=serv, midi_out=serv, in_channel=0, out_channel=0, in_buf_size=512, debug=True)
# advertisement = ProvideServicesAdvertisement(serv)
# ble.start_advertising(advertisement)
#
# a = SolicitServicesAdvertisement()
# a.solicited_services.append(adafruit_ble_midi.MIDIService)
# ble.start_advertising(a)
#
#
# pc = ProgramChange(10, channel=0)
# # Now can communicate
# midi.send(ProgramChange(10, channel=0))
# # BUT CAN"t Seem to receive on MAC. Sad. seems like the connection is not complete;
# # on BT-01 the red connection light is solid for connection, but doesnt blink green when sending;
# # is this a mac issue? or a connection issue?
# midi._send()
#
# model = 0x11  # FM3
# SYSEX_HEADER_B = [0x01, 0x74]
# query = SYSEX_HEADER_B + [model] + [FX.getPresetName.value] + [0x7F, 0x7F]
# data = inject_checksum(query)
# sysex = SystemExclusive(0x00, data)
#
# midi._send(data, len(data))
# # really need to check if there is a buffer of messages before processing; maybe async function?
# rx = midi.receive()
# if rx is not None and rx[0][:5] == query[:5]:
#     # need to make sure we're getting same preset we asked for
#     preset = LSBMSB2Int(rx[0][6:8])  # LSB, MSB -> int (shift + XOR)
#     name = (''.join([chr(k) for k in rx[0][8:-3]])).rstrip()  # ignore checksum and 0x00
#     print("{:}: {:}".format(preset, name))