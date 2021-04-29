import rtmidi
import time

from fractalInterface.fractalConstants import *

"""
0xF0 sysex start
0x00 Manf. ID byte0
0x01 Manf. ID byte1
0x74 Manf. ID byte2
0xdd Model #

Models:
0x10 Axe-Fx III
0x11 FM3

"""


def injectChecksum(msg):
    cs = msg[0]
    for j in msg[1:]:
        cs ^= j

    cs &= 0x7f
    msg.append(cs)
    msg.append(0xf7)
    return msg


def int2LSBMSB(val):
    return [val & 0x7f, val >> 7]

def LSBMSB2Int(arr):
    return arr[-1] << 7 ^ arr[0]

def getCurrentPresetName(midiRX, midiTX, model=0x11):
    query = SYSEX_HEADER + [model] + [FX.getPresetName] + [0x7F, 0x7F]
    midiTX.send_message(injectChecksum(query))
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:5] == query[:5]:
        # need to make sure we're getting same preset we asked for
        preset = LSBMSB2Int(rx[0][6:8])  # LSB, MSB -> int (shift + XOR)
        name = (''.join([chr(k) for k in rx[0][8:-3]])).rstrip()  # ignore checksum and 0x00
        print("{:}: {:}".format(preset, name))


def getPresetNameByID(id=0, midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [FX.getPresetName] + int2LSBMSB(id)
    midiTX.send_message(injectChecksum(query))
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:7] == query[:7]:
        preset = LSBMSB2Int(rx[0][6:8])  # LSB, MSB -> int (shift + XOR)
        name = (''.join([chr(k) for k in rx[0][8:-3]])).rstrip()  # ignore checksum and 0x00
        print("{:}: {:}".format(preset, name))


def getBypassStateByID(id=0, midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [FX.bypass] + int2LSBMSB(id) + [0x7F]  # last byte is set to 7F for Query
    midiTX.send_message(injectChecksum(query))
    time.sleep(0.1)
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:7] == query[:7]:
        bypassState = rx[0][8]
        print("Effect {:} is {:}".format(id, 'Bypassed' if bypassState else 'Engaged'))


def setBypassStateTrue(id=0, midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [FX.bypass] + int2LSBMSB(id) + [0x01]  # last byte is set to 7F for Query
    midiTX.send_message(injectChecksum(query))
    time.sleep(0.1)
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:7] == query[:7]:
        bypassState = rx[0][8]
        print("Effect {:} is {:}".format(id, 'Bypassed' if bypassState else 'Engaged'))


def setBypassStateFalse(id=0, midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [FX.bypass] + int2LSBMSB(id) + [0x00]  # last byte is set to 7F for Query
    midiTX.send_message(injectChecksum(query))
    time.sleep(0.1)
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:7] == query[:7]:
        bypassState = rx[0][8]
        print("Effect {:} is {:}".format(id, 'Bypassed' if bypassState else 'Engaged'))

def getStatusDump(midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [0x13]
    midiTX.send_message(injectChecksum(query))
    time.sleep(0.1)
    # really need to check if there is a buffer of messages before processing; maybe async function?
    # packet -> [id_lsb, id_msb, dd],
    rx = midiRX.get_message()
    if rx is not None and rx[0][:5] == query[:5]:
        packets = rx[0][6:-2]
        numEffects = int(len(packets)/3)
        # [Effect Name, ID, BypassState, channel, num channels]
        for i in range(0, numEffects):
            effectID = LSBMSB2Int(packets[3*i:(3*i)+2])
            effectName = ID(LSBMSB2Int(packets[3*i:(3*i)+2])).name
            latent = packets[3*i+2]
            bypassState = latent & 0x01  # 1 bypass, 0 engaged
            channel = ((latent >> 1) & 7)
            channelsSupported = ((latent >> 4) & 7)
            print("Block: {:}, ID: {:}, CH: {:}, State: {:}".format(
                effectName, effectID, channel, 'Bypassed' if bypassState else 'Engaged'
            ))


# NOT SRE THIS WORKS
def getCPU(midiRX=None, midiTX=None, model=0x11):
    query = SYSEX_HEADER + [model] + [0x11]
    midiTX.send_message(injectChecksum(query))
    time.sleep(0.1)
    # really need to check if there is a buffer of messages before processing; maybe async function?
    rx = midiRX.get_message()
    if rx is not None and rx[0][:5] == query[:5]:
        pass

def clearMidiInputBuffer(midiRX):
    while midiRX.get_message():
        midiRX.get_message()


model = MODEL.FM3.value


midiInput = rtmidi.MidiIn()
midiOutput = rtmidi.MidiOut()

availableInputPorts = midiInput.get_ports()
availableOutputPorts = midiOutput.get_ports()

# open input port:
midiRX = midiInput.open_port(availableInputPorts.index('mio'))
midiRX.ignore_types(sysex=False, timing=False)
# open output port:
midiTX = midiOutput.open_port(availableOutputPorts.index('mio'))



for fID in range(70, 127):
    if fID in [0x10, 0x11, 0x13, 0x14, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0xF]:
        continue #skip these..
    clearMidiInputBuffer(midiRX)
    query = SYSEX_HEADER + [model] + [fID] + int2LSBMSB(ID.FUZZ1.value)
    injectChecksum(query)
    midiTX.send_message(query)
    time.sleep(0.1)
    rx = midiRX.get_message()
    if rx is not None:
        if rx[0][5:7] == [100, fID]:
            print('fID: {:} did not work'.format(fID))
        else:
            print(print('fID: {:} MIGHT HAVE WORKED, returned {:} Bytes'.format(fID, len(rx[0])-8)))
    else:
        print('fID: {:} NO RESPONSE'.format(fID))