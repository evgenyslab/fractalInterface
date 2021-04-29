from enum import Enum

SYSEX_HEADER = [0xF0, 0x00, 0x01, 0x74]

class FX(Enum):

    # tap tempo
    tapTempo = 0x10
    # tuner (on/off bit requred)
    tuner = 0x11

    # 0x12 what is here?

    # Current preset block dump
    getDump = 0x13

    # GET/SET
    temp = 0x14

    # GET/SET
    bypass = 0x0A
    channel = 0x0B
    scene = 0x0C

    # GET Only
    getPresetName = 0x0D
    getSceneName = 0x0E

    # GET/SET
    looper = 0x0F


class ID(Enum):
    # enum of IDs
    CONTROL = 2
    TUNER = 35
    IRCAPTURE = 36
    INPUT1 = 37
    INPUT2 = 38
    INPUT3 = 39
    INPUT4 = 40
    INPUT5 = 41
    OUTPUT1 = 42
    OUTPUT2 = 43
    OUTPUT3 = 44
    OUTPUT4 = 45
    COMP1 = 46
    COMP2 = 47
    COMP3 = 48
    COMP4 = 49
    GRAPHEQ1 = 50
    GRAPHEQ2 = 51
    GRAPHEQ3 = 52
    GRAPHEQ4 = 53
    PARAEQ1 = 54
    PARAEQ2 = 55
    PARAEQ3 = 56
    PARAEQ4 = 57
    DISTORT1 = 58  # AMPS
    DISTORT2 = 59
    DISTORT3 = 60
    DISTORT4 = 61
    CAB1 = 62
    CAB2 = 63
    CAB3 = 64
    CAB4 = 65
    REVERB1 = 66
    REVERB2 = 67
    REVERB3 = 68
    REVERB4 = 69
    DELAY1 = 70
    DELAY2 = 71
    DELAY3 = 72
    DELAY4 = 73
    MULTITAP1 = 74
    MULTITAP2 = 75
    MULTITAP3 = 76
    MULTITAP4 = 77
    CHORUS1 = 78
    CHORUS2 = 79
    CHORUS3 = 80
    CHORUS4 = 81
    FLANGER1 = 82
    FLANGER2 = 83
    FLANGER3 = 84
    FLANGER4 = 85
    ROTARY1 = 86
    ROTARY2 = 87
    ROTARY3 = 88
    ROTARY4 = 89
    PHASER1 = 90
    PHASER2 = 91
    PHASER3 = 92
    PHASER4 = 93
    WAH1 = 94
    WAH2 = 95
    WAH3 = 96
    WAH4 = 97
    FORMANT1 = 98
    FORMANT2 = 99
    FORMANT3 = 100
    FORMANT4 = 101
    VOLUME1 = 102
    VOLUME2 = 103
    VOLUME3 = 104
    VOLUME4 = 105
    TREMOLO1 = 106
    TREMOLO2 = 107
    TREMOLO3 = 108
    TREMOLO4 = 109
    PITCH1 = 110
    PITCH2 = 111
    PITCH3 = 112
    PITCH4 = 113
    FILTER1 = 114
    FILTER2 = 115
    FILTER3 = 116
    FILTER4 = 117
    FUZZ1 = 118  # DRIVE BLOCKS
    FUZZ2 = 119
    FUZZ3 = 120
    FUZZ4 = 121
    ENHANCER1 = 122
    ENHANCER2 = 123
    ENHANCER3 = 124
    ENHANCER4 = 125
    MIXER1 = 126
    MIXER2 = 127
    MIXER3 = 128
    MIXER4 = 129
    SYNTH1 = 130
    SYNTH2 = 131
    SYNTH3 = 132
    SYNTH4 = 133
    VOCODER1 = 134
    VOCODER2 = 135
    VOCODER3 = 136
    VOCODER4 = 137
    MEGATAP1 = 138
    MEGATAP2 = 139
    MEGATAP3 = 140
    MEGATAP4 = 141
    CROSSOVER1 = 142
    CROSSOVER2 = 143
    CROSSOVER3 = 144
    CROSSOVER4 = 145
    GATE1 = 146
    GATE2 = 147
    GATE3 = 148
    GATE4 = 149
    RINGMOD1 = 150
    RINGMOD2 = 151
    RINGMOD3 = 152
    RINGMOD4 = 153
    MULTICOMP1 = 154
    MULTICOMP2 = 155
    MULTICOMP3 = 156
    MULTICOMP4 = 157
    TENTAP1 = 158
    TENTAP2 = 159
    TENTAP3 = 160
    TENTAP4 = 161
    RESONATOR1 = 162
    RESONATOR2 = 163
    RESONATOR3 = 164
    RESONATOR4 = 165
    LOOPER1 = 166
    LOOPER2 = 167
    LOOPER3 = 168
    LOOPER4 = 169
    TONEMATCH1 = 170
    TONEMATCH2 = 171
    TONEMATCH3 = 172
    TONEMATCH4 = 173
    RTA1 = 174
    RTA2 = 175
    RTA3 = 176
    RTA4 = 177
    PLEX1 = 178
    PLEX2 = 179
    PLEX3 = 180
    PLEX4 = 181
    FBSEND1 = 182
    FBSEND2 = 183
    FBSEND3 = 184
    FBSEND4 = 185
    FBRETURN1 = 186
    FBRETURN2 = 187
    FBRETURN3 = 188
    FBRETURN4 = 189
    MIDIBLOCK = 190
    MULTIPLEXER1 = 191
    MULTIPLEXER2 = 192
    MULTIPLEXER3 = 193
    MULTIPLEXER4 = 194
    IRPLAYER1 = 195
    IRPLAYER2 = 196
    IRPLAYER3 = 197
    IRPLAYER4 = 198
    FOOTCONTROLLER = 199
    PRESET_FC = 200

class MODEL(Enum):
    AXEFXSTD = 0x00
    AXEFXULT = 0x01
    MFC101 = 0x02
    AXEFX2 = 0x03
    MFC101MK3 = 0x04
    FX8 = 0x05
    AXEFX2XL = 0x06
    AXEFX2XLP = 0x07
    AX8 = 0x08
    FX8MK2 = 0x0A
    AXEFX3 = 0x10
    FM3 = 0x11


"""
Midi Function list

FM# seems to respond with 100 or 0x64 when things don't match in fx position (5th)

0x00 ->
0x01 -> tested with block ID, got back longer sysex


header = 5 bytes

fx  
[header] + [fID] + [cs 0xf7]
    0x00 ->
        [header] [0x64] [0x00, 0x05] [cs 0xf7]
    0x01 -> 
        [header] [fID] [15 bytes] [cs 0xf7]
    0x02 -> 
        [header] [0x64] [0x02, 0x05] [cs 0xf7]
    0x03 ->
        [header] [0x64] [0x03, 0x0f] [cs 0xf7]
    0x04 ->
        NO RESPONSE
    0x08 -> returns something
    
    
fx + block ID
[header] + [fID] + [idLSB, idMSB] + [cs 0xf7]
    0x00 ->
        [header] [0x64] [0x00, 0x05] [cs 0xf7]
    0x01 ->
        [header] [fID] [idLSB, idMSB] [13 bytes] [cs 0xf7]
    0x02 -> 
        [header] [0x64] [0x02, 0x05] [cs 0xf7]
    0x03 ->
        [header] [0x64] [0x03, 0x0f] [cs 0xf7]
    0x04 ->
        NO RESPONSE
    0x05 ->
        [header] [0x64] [0x05, 0x05] [cs 0xf7]
    0x06 ->
        [header] [0x64] [0x06, 0x05] [cs 0xf7]
    0x07 ->
        [header] [0x64] [0x07, 0x05] [cs 0xf7]
    0x08 ->
        [header] [fID] [4 bytes] [cs 0xf7]
    0x09 ->
        [header] [0x64] [0x09, 0x05] [cs 0xf7]
    
    0x12 -> changed page on front to midi settings... Seems to control change of pages; depends on extra bytes sent
    
    DIFFERENT RESPONSE PER ID QUERY
    0x19 -> 
        [header] [122] [idLSB, idMSB] [0, 16]? [cs 0xf7]
        8x
        [header] [123] [] [cs 0xf7]
        
        [header] [124] [4 bytes] [cs 0xf7]
        
    
    fID 122, with effect ID, returned 2 bytes; then another set of a lot of data...
            then sent a whole set of packges of length 1290 (FID 123) [8 sets of 1290]
            then finished with fID 124

    DIFFERENT RESPONSE PER ID QUERY
    0x1f ->
        [header] [116] [idLSB, idMSB] [20, 4]? [cs 0xf7]
        
        /// INPUT1 had first msg at 20,4 with 4x 117 messages after, then 118 messgae
        /// FUZZ1 had first msg at 20,1 with 1x 117 messages after, then 118 message
        
        [header] [118] [cd 0x7f]
    
"""