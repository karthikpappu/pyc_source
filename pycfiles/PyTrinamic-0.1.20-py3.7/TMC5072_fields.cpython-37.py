# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5072\TMC5072_fields.py
# Compiled at: 2019-12-05 09:50:08
# Size of source mod 2**32: 37349 bytes
"""
Created on 20.09.2019

@author: JM
"""

class TMC5072_fields(object):
    __doc__ = '\n\tDefine all register bitfields of the TMC5072.\n\n\tEach field is defined as a tuple consisting of ( Address, Mask, Shift ).\n\tFields that are present multiple times in different registers (for multiple\n\tmotors) all of the bitfield tuples are bundled together into another tuple.\n\n\tThe name of the register is written as a comment behind each tuple. This is\n\tintended for IDE users viewing the definition of a field by hovering over\n\tit. This allows the user to see the corresponding register name of a field\n\twithout opening this file and searching for the definition.\n\t'
    SINGLE_DRIVER = (0, 1, 0)
    STEPDIR1_ENABLE = (0, 2, 1)
    STEPDIR2_ENABLE = (0, 4, 2)
    POSCMP_ENABLE = (0, 8, 3)
    ENC1_REFSEL = (0, 16, 4)
    ENC2_ENABLE = (0, 32, 5)
    ENC2_REFSEL = (0, 64, 6)
    TEST_MODE = (0, 128, 7)
    SHAFT1 = (0, 256, 8)
    SHAFT2 = (0, 512, 9)
    LOCK_GCONF = (0, 1024, 10)
    DC_SYNC = (0, 2048, 11)
    RESET = (1, 1, 0)
    DRV_ERR1 = (1, 2, 1)
    DRV_ERR1 = (1, 4, 2)
    UV_CP = (1, 8, 3)
    IFCNT = (2, 255, 0)
    SLAVEADDR = (3, 15, 0)
    SENDDELAY = (3, 240, 4)
    TEST_SEL = (3, 15, 0)
    SENDDELAY = (3, 240, 4)
    IO0_IN = (4, 1, 0)
    IO1_IN = (4, 2, 1)
    IO2_IN = (4, 4, 2)
    IO3_IN = (4, 8, 3)
    IOP_IN = (4, 16, 4)
    ION_IN = (4, 32, 5)
    NEXTADDR_IN = (4, 64, 6)
    DRV_ENN = (4, 128, 7)
    SW_COMP_IN = (4, 256, 8)
    VERSION = (4, 4278190080, 24)
    IO0_OUT = (4, 1, 0)
    IO1_OUT = (4, 2, 1)
    IO2_OUT = (4, 4, 2)
    IODDR0 = (4, 256, 8)
    IODDR1 = (4, 512, 9)
    IODDR2 = (4, 1024, 10)
    X_COMPARE = (5, 4294967295, 0)
    PWM_AMPL = (16, 255, 0)
    PWM_GRAD = (16, 65280, 8)
    PWM_FREQ = (16, 196608, 16)
    PWM_AUTOSCALE = (16, 262144, 18)
    PWM_SYMMETRIC = (16, 524288, 19)
    FREEWHEEL = (16, 3145728, 20)
    PWM_AMPL = (16, 255, 0)
    PWM_GRAD = (16, 65280, 8)
    PWM_FREQ = (16, 196608, 16)
    PWM_AUTOSCALE = (16, 262144, 18)
    PWM_SYMMETRIC = (16, 524288, 19)
    FREEWHEEL = (16, 3145728, 20)
    PWM_STATUS = (17, 255, 0)
    PWM_AMPL = (24, 255, 0)
    PWM_GRAD = (24, 65280, 8)
    PWM_FREQ = (24, 196608, 16)
    PWM_AUTOSCALE = (24, 262144, 18)
    PWM_SYMMETRIC = (24, 524288, 19)
    FREEWHEEL = (24, 3145728, 20)
    PWM_AMPL = (24, 255, 0)
    PWM_GRAD = (24, 65280, 8)
    PWM_FREQ = (24, 196608, 16)
    PWM_AUTOSCALE = (24, 262144, 18)
    PWM_SYMMETRIC = (24, 524288, 19)
    FREEWHEEL = (24, 3145728, 20)
    PWM_STATUS = (25, 255, 0)
    RAMPMODE = (32, 3, 0)
    XACTUAL = (33, 4294967295, 0)
    VACTUAL = (34, 16777215, 0)
    VSTART = (35, 262143, 0)
    A1 = (36, 65535, 0)
    V1_ = (37, 1048575, 0)
    AMAX = (38, 65535, 0)
    VMAX = (39, 8388607, 0)
    DMAX = (40, 65535, 0)
    D1 = (42, 65535, 0)
    VSTOP = (43, 262143, 0)
    TZEROWAIT = (44, 65535, 0)
    XTARGET = (45, 4294967295, 0)
    RAMPMODE = (64, 3, 0)
    XACTUAL = (65, 4294967295, 0)
    VACTUAL = (66, 16777215, 0)
    VSTART = (67, 262143, 0)
    A1 = (68, 65535, 0)
    V1_ = (69, 1048575, 0)
    AMAX = (70, 65535, 0)
    VMAX = (71, 8388607, 0)
    DMAX = (72, 65535, 0)
    D1 = (74, 65535, 0)
    VSTOP = (75, 262143, 0)
    TZEROWAIT = (76, 65535, 0)
    XTARGET = (77, 4294967295, 0)
    IHOLD = (48, 31, 0)
    IRUN = (48, 7936, 8)
    IHOLDDELAY = (48, 983040, 16)
    VCOOLTHRS = (49, 8388607, 0)
    VHIGH = (50, 8388607, 0)
    VDCMIN = (51, 8388607, 0)
    STOP_L_ENABLE = (52, 1, 0)
    STOP_R_ENABLE = (52, 2, 1)
    POL_STOP_L = (52, 4, 2)
    POL_STOP_R = (52, 8, 3)
    SWAP_LR = (52, 16, 4)
    LATCH_L_ACTIVE = (52, 32, 5)
    LATCH_L_INACTIVE = (52, 64, 6)
    LATCH_R_ACTIVE = (52, 128, 7)
    LATCH_R_INACTIVE = (52, 256, 8)
    EN_LATCH_ENCODER = (52, 512, 9)
    SG_STOP = (52, 1024, 10)
    EN_SOFTSTOP = (52, 2048, 11)
    STATUS_STOP_L = (53, 1, 0)
    STATUS_STOP_R = (53, 2, 1)
    STATUS_LATCH_L = (53, 4, 2)
    STATUS_LATCH_R = (53, 8, 3)
    EVENT_STOP_L = (53, 16, 4)
    EVENT_STOP_R = (53, 32, 5)
    EVENT_STOP_SG = (53, 64, 6)
    EVENT_POS_REACHED = (53, 128, 7)
    VELOCITY_REACHED = (53, 256, 8)
    POSITION_REACHED = (53, 512, 9)
    VZERO = (53, 1024, 10)
    T_ZEROWAIT_ACTIVE = (53, 2048, 11)
    SECOND_MOVE = (53, 4096, 12)
    STATUS_SG = (53, 8192, 13)
    XLATCH = (54, 4294967295, 0)
    IHOLD = (80, 31, 0)
    IRUN = (80, 7936, 8)
    IHOLDDELAY = (80, 983040, 16)
    VCOOLTHRS = (81, 8388607, 0)
    VHIGH = (82, 8388607, 0)
    VDCMIN = (83, 8388607, 0)
    STOP_L_ENABLE = (84, 1, 0)
    STOP_R_ENABLE = (84, 2, 1)
    POL_STOP_L = (84, 4, 2)
    POL_STOP_R = (84, 8, 3)
    SWAP_LR = (84, 16, 4)
    LATCH_L_ACTIVE = (84, 32, 5)
    LATCH_L_INACTIVE = (84, 64, 6)
    LATCH_R_ACTIVE = (84, 128, 7)
    LATCH_R_INACTIVE = (84, 256, 8)
    EN_LATCH_ENCODER = (84, 512, 9)
    SG_STOP = (84, 1024, 10)
    EN_SOFTSTOP = (84, 2048, 11)
    STATUS_STOP_L = (85, 1, 0)
    STATUS_STOP_R = (85, 2, 1)
    STATUS_LATCH_L = (85, 4, 2)
    STATUS_LATCH_R = (85, 8, 3)
    EVENT_STOP_L = (85, 16, 4)
    EVENT_STOP_R = (85, 32, 5)
    EVENT_STOP_SG = (85, 64, 6)
    EVENT_POS_REACHED = (85, 128, 7)
    VELOCITY_REACHED = (85, 256, 8)
    POSITION_REACHED = (85, 512, 9)
    VZERO = (85, 1024, 10)
    T_ZEROWAIT_ACTIVE = (85, 2048, 11)
    SECOND_MOVE = (85, 4096, 12)
    STATUS_SG = (85, 8192, 13)
    XLATCH = (86, 4294967295, 0)
    POL_A = (56, 1, 0)
    POL_B = (56, 2, 1)
    POL_N = (56, 4, 2)
    IGNORE_AB = (56, 8, 3)
    CLR_CONT = (56, 16, 4)
    CLR_ONCE = (56, 32, 5)
    POS_EDGE_NEG_EDGE = (56, 192, 6)
    CLR_ENC_X = (56, 256, 8)
    LATCH_X_ACT = (56, 512, 9)
    ENC_SEL_DECIMAL = (56, 1024, 10)
    LATCH_NOW_ = (56, 2048, 11)
    X_ENC = (57, 4294967295, 0)
    INTEGER = (58, 4294901760, 16)
    FRACTIONAL = (58, 65535, 0)
    ENC_STATUS = (59, 1, 0)
    ENC_LATCH = (60, 4294967295, 0)
    POL_A = (88, 1, 0)
    POL_B = (88, 2, 1)
    POL_N = (88, 4, 2)
    IGNORE_AB = (88, 8, 3)
    CLR_CONT = (88, 16, 4)
    CLR_ONCE = (88, 32, 5)
    POS_EDGE_NEG_EDGE = (88, 192, 6)
    CLR_ENC_X = (88, 256, 8)
    LATCH_X_ACT = (88, 512, 9)
    ENC_SEL_DECIMAL = (88, 1024, 10)
    LATCH_NOW_ = (88, 2048, 11)
    X_ENC = (89, 4294967295, 0)
    INTEGER = (90, 4294901760, 16)
    FRACTIONAL = (90, 65535, 0)
    ENC_STATUS = (91, 1, 0)
    ENC_LATCH = (92, 4294967295, 0)
    OFS0 = (96, 1, 0)
    OFS1 = (96, 2, 1)
    OFS2 = (96, 4, 2)
    OFS3 = (96, 8, 3)
    OFS4 = (96, 16, 4)
    OFS5 = (96, 32, 5)
    OFS6 = (96, 64, 6)
    OFS7 = (96, 128, 7)
    OFS8 = (96, 256, 8)
    OFS9 = (96, 512, 9)
    OFS10 = (96, 1024, 10)
    OFS11 = (96, 2048, 11)
    OFS12 = (96, 4096, 12)
    OFS13 = (96, 8192, 13)
    OFS14 = (96, 16384, 14)
    OFS15 = (96, 32768, 15)
    OFS16 = (96, 65536, 16)
    OFS17 = (96, 131072, 17)
    OFS18 = (96, 262144, 18)
    OFS19 = (96, 524288, 19)
    OFS20 = (96, 1048576, 20)
    OFS21 = (96, 2097152, 21)
    OFS22 = (96, 4194304, 22)
    OFS23 = (96, 8388608, 23)
    OFS24 = (96, 16777216, 24)
    OFS25 = (96, 33554432, 25)
    OFS26 = (96, 67108864, 26)
    OFS27 = (96, 134217728, 27)
    OFS28 = (96, 268435456, 28)
    OFS29 = (96, 536870912, 29)
    OFS30 = (96, 1073741824, 30)
    OFS31 = (96, 2147483648, 31)
    OFS32 = (97, 1, 0)
    OFS33 = (97, 2, 1)
    OFS34 = (97, 4, 2)
    OFS35 = (97, 8, 3)
    OFS36 = (97, 16, 4)
    OFS37 = (97, 32, 5)
    OFS38 = (97, 64, 6)
    OFS39 = (97, 128, 7)
    OFS40 = (97, 256, 8)
    OFS41 = (97, 512, 9)
    OFS42 = (97, 1024, 10)
    OFS43 = (97, 2048, 11)
    OFS44 = (97, 4096, 12)
    OFS45 = (97, 8192, 13)
    OFS46 = (97, 16384, 14)
    OFS47 = (97, 32768, 15)
    OFS48 = (97, 65536, 16)
    OFS49 = (97, 131072, 17)
    OFS50 = (97, 262144, 18)
    OFS51 = (97, 524288, 19)
    OFS52 = (97, 1048576, 20)
    OFS53 = (97, 2097152, 21)
    OFS54 = (97, 4194304, 22)
    OFS55 = (97, 8388608, 23)
    OFS56 = (97, 16777216, 24)
    OFS57 = (97, 33554432, 25)
    OFS58 = (97, 67108864, 26)
    OFS59 = (97, 134217728, 27)
    OFS60 = (97, 268435456, 28)
    OFS61 = (97, 536870912, 29)
    OFS62 = (97, 1073741824, 30)
    OFS63 = (97, 2147483648, 31)
    OFS64 = (98, 1, 0)
    OFS65 = (98, 2, 1)
    OFS66 = (98, 4, 2)
    OFS67 = (98, 8, 3)
    OFS68 = (98, 16, 4)
    OFS69 = (98, 32, 5)
    OFS70 = (98, 64, 6)
    OFS71 = (98, 128, 7)
    OFS72 = (98, 256, 8)
    OFS73 = (98, 512, 9)
    OFS74 = (98, 1024, 10)
    OFS75 = (98, 2048, 11)
    OFS76 = (98, 4096, 12)
    OFS77 = (98, 8192, 13)
    OFS78 = (98, 16384, 14)
    OFS79 = (98, 32768, 15)
    OFS80 = (98, 65536, 16)
    OFS81 = (98, 131072, 17)
    OFS82 = (98, 262144, 18)
    OFS83 = (98, 524288, 19)
    OFS84 = (98, 1048576, 20)
    OFS85 = (98, 2097152, 21)
    OFS86 = (98, 4194304, 22)
    OFS87 = (98, 8388608, 23)
    OFS88 = (98, 16777216, 24)
    OFS89 = (98, 33554432, 25)
    OFS90 = (98, 67108864, 26)
    OFS91 = (98, 134217728, 27)
    OFS92 = (98, 268435456, 28)
    OFS93 = (98, 536870912, 29)
    OFS94 = (98, 1073741824, 30)
    OFS95 = (98, 2147483648, 31)
    OFS96 = (99, 1, 0)
    OFS97 = (99, 2, 1)
    OFS98 = (99, 4, 2)
    OFS99 = (99, 8, 3)
    OFS100 = (99, 16, 4)
    OFS101 = (99, 32, 5)
    OFS102 = (99, 64, 6)
    OFS103 = (99, 128, 7)
    OFS104 = (99, 256, 8)
    OFS105 = (99, 512, 9)
    OFS106 = (99, 1024, 10)
    OFS107 = (99, 2048, 11)
    OFS108 = (99, 4096, 12)
    OFS109 = (99, 8192, 13)
    OFS110 = (99, 16384, 14)
    OFS111 = (99, 32768, 15)
    OFS112 = (99, 65536, 16)
    OFS113 = (99, 131072, 17)
    OFS114 = (99, 262144, 18)
    OFS115 = (99, 524288, 19)
    OFS116 = (99, 1048576, 20)
    OFS117 = (99, 2097152, 21)
    OFS118 = (99, 4194304, 22)
    OFS119 = (99, 8388608, 23)
    OFS120 = (99, 16777216, 24)
    OFS121 = (99, 33554432, 25)
    OFS122 = (99, 67108864, 26)
    OFS123 = (99, 134217728, 27)
    OFS124 = (99, 268435456, 28)
    OFS125 = (99, 536870912, 29)
    OFS126 = (99, 1073741824, 30)
    OFS127 = (99, 2147483648, 31)
    OFS128 = (100, 1, 0)
    OFS129 = (100, 2, 1)
    OFS130 = (100, 4, 2)
    OFS131 = (100, 8, 3)
    OFS132 = (100, 16, 4)
    OFS133 = (100, 32, 5)
    OFS134 = (100, 64, 6)
    OFS135 = (100, 128, 7)
    OFS136 = (100, 256, 8)
    OFS137 = (100, 512, 9)
    OFS138 = (100, 1024, 10)
    OFS139 = (100, 2048, 11)
    OFS140 = (100, 4096, 12)
    OFS141 = (100, 8192, 13)
    OFS142 = (100, 16384, 14)
    OFS143 = (100, 32768, 15)
    OFS144 = (100, 65536, 16)
    OFS145 = (100, 131072, 17)
    OFS146 = (100, 262144, 18)
    OFS147 = (100, 524288, 19)
    OFS148 = (100, 1048576, 20)
    OFS149 = (100, 2097152, 21)
    OFS150 = (100, 4194304, 22)
    OFS151 = (100, 8388608, 23)
    OFS152 = (100, 16777216, 24)
    OFS153 = (100, 33554432, 25)
    OFS154 = (100, 67108864, 26)
    OFS155 = (100, 134217728, 27)
    OFS156 = (100, 268435456, 28)
    OFS157 = (100, 536870912, 29)
    OFS158 = (100, 1073741824, 30)
    OFS159 = (100, 2147483648, 31)
    OFS160 = (101, 1, 0)
    OFS161 = (101, 2, 1)
    OFS162 = (101, 4, 2)
    OFS163 = (101, 8, 3)
    OFS164 = (101, 16, 4)
    OFS165 = (101, 32, 5)
    OFS166 = (101, 64, 6)
    OFS167 = (101, 128, 7)
    OFS168 = (101, 256, 8)
    OFS169 = (101, 512, 9)
    OFS170 = (101, 1024, 10)
    OFS171 = (101, 2048, 11)
    OFS172 = (101, 4096, 12)
    OFS173 = (101, 8192, 13)
    OFS174 = (101, 16384, 14)
    OFS175 = (101, 32768, 15)
    OFS176 = (101, 65536, 16)
    OFS177 = (101, 131072, 17)
    OFS178 = (101, 262144, 18)
    OFS179 = (101, 524288, 19)
    OFS180 = (101, 1048576, 20)
    OFS181 = (101, 2097152, 21)
    OFS182 = (101, 4194304, 22)
    OFS183 = (101, 8388608, 23)
    OFS184 = (101, 16777216, 24)
    OFS185 = (101, 33554432, 25)
    OFS186 = (101, 67108864, 26)
    OFS187 = (101, 134217728, 27)
    OFS188 = (101, 268435456, 28)
    OFS189 = (101, 536870912, 29)
    OFS190 = (101, 1073741824, 30)
    OFS191 = (101, 2147483648, 31)
    OFS192 = (102, 1, 0)
    OFS193 = (102, 2, 1)
    OFS194 = (102, 4, 2)
    OFS195 = (102, 8, 3)
    OFS196 = (102, 16, 4)
    OFS197 = (102, 32, 5)
    OFS198 = (102, 64, 6)
    OFS199 = (102, 128, 7)
    OFS200 = (102, 256, 8)
    OFS201 = (102, 512, 9)
    OFS202 = (102, 1024, 10)
    OFS203 = (102, 2048, 11)
    OFS204 = (102, 4096, 12)
    OFS205 = (102, 8192, 13)
    OFS206 = (102, 16384, 14)
    OFS207 = (102, 32768, 15)
    OFS208 = (102, 65536, 16)
    OFS209 = (102, 131072, 17)
    OFS210 = (102, 262144, 18)
    OFS211 = (102, 524288, 19)
    OFS212 = (102, 1048576, 20)
    OFS213 = (102, 2097152, 21)
    OFS214 = (102, 4194304, 22)
    OFS215 = (102, 8388608, 23)
    OFS216 = (102, 16777216, 24)
    OFS217 = (102, 33554432, 25)
    OFS218 = (102, 67108864, 26)
    OFS219 = (102, 134217728, 27)
    OFS220 = (102, 268435456, 28)
    OFS221 = (102, 536870912, 29)
    OFS222 = (102, 1073741824, 30)
    OFS223 = (102, 2147483648, 31)
    OFS224 = (103, 1, 0)
    OFS225 = (103, 2, 1)
    OFS226 = (103, 4, 2)
    OFS227 = (103, 8, 3)
    OFS228 = (103, 16, 4)
    OFS229 = (103, 32, 5)
    OFS230 = (103, 64, 6)
    OFS231 = (103, 128, 7)
    OFS232 = (103, 256, 8)
    OFS233 = (103, 512, 9)
    OFS234 = (103, 1024, 10)
    OFS235 = (103, 2048, 11)
    OFS236 = (103, 4096, 12)
    OFS237 = (103, 8192, 13)
    OFS238 = (103, 16384, 14)
    OFS239 = (103, 32768, 15)
    OFS240 = (103, 65536, 16)
    OFS241 = (103, 131072, 17)
    OFS242 = (103, 262144, 18)
    OFS243 = (103, 524288, 19)
    OFS244 = (103, 1048576, 20)
    OFS245 = (103, 2097152, 21)
    OFS246 = (103, 4194304, 22)
    OFS247 = (103, 8388608, 23)
    OFS248 = (103, 16777216, 24)
    OFS249 = (103, 33554432, 25)
    OFS250 = (103, 67108864, 26)
    OFS251 = (103, 134217728, 27)
    OFS252 = (103, 268435456, 28)
    OFS253 = (103, 536870912, 29)
    OFS254 = (103, 1073741824, 30)
    OFS255 = (103, 2147483648, 31)
    W0 = (104, 3, 0)
    W1 = (104, 12, 2)
    W2 = (104, 48, 4)
    W3 = (104, 192, 6)
    X1 = (104, 65280, 8)
    X2 = (104, 16711680, 16)
    X3 = (104, 4278190080, 24)
    START_SIN = (105, 255, 0)
    START_SIN90 = (105, 16711680, 16)
    MSCNT = (106, 1023, 0)
    CUR_A = (107, 511, 0)
    CUR_B = (107, 33488896, 16)
    TOFF = (108, 15, 0)
    TFD_2__0_ = (108, 112, 4)
    OFFSET = (108, 1920, 7)
    TFD__ = (108, 2048, 11)
    DISFDCC = (108, 4096, 12)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    MRES = (108, 251658240, 24)
    INTPOL = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    TOFF = (108, 15, 0)
    TFD_2__0_ = (108, 112, 4)
    OFFSET = (108, 1920, 7)
    TFD__ = (108, 2048, 11)
    DISFDCC = (108, 4096, 12)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    MRES = (108, 251658240, 24)
    INTPOL = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    TOFF = (108, 15, 0)
    HSTRT = (108, 112, 4)
    HEND = (108, 1920, 7)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    MRES = (108, 251658240, 24)
    INTPOL = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    SEMIN = (109, 15, 0)
    SEUP = (109, 96, 5)
    SEMAX = (109, 3840, 8)
    SEDN = (109, 24576, 13)
    SEIMIN = (109, 32768, 15)
    SGT = (109, 8323072, 16)
    SFILT = (109, 16777216, 24)
    DC_TIME = (110, 1023, 0)
    DC_SG = (110, 16711680, 16)
    SG_RESULT = (111, 1023, 0)
    FSACTIVE = (111, 32768, 15)
    CS_ACTUAL = (111, 2031616, 16)
    STALLGUARD = (111, 16777216, 24)
    OT = (111, 33554432, 25)
    OTPW = (111, 67108864, 26)
    S2GA = (111, 134217728, 27)
    S2GB = (111, 268435456, 28)
    OLA = (111, 536870912, 29)
    OLB = (111, 1073741824, 30)
    STST = (111, 2147483648, 31)
    MSCNT = (122, 1023, 0)
    CUR_A = (123, 511, 0)
    CUR_B = (123, 33488896, 16)
    TOFF = (124, 15, 0)
    TFD_2__0_ = (124, 112, 4)
    OFFSET = (124, 1920, 7)
    TFD__ = (124, 2048, 11)
    DISFDCC = (124, 4096, 12)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    MRES = (124, 251658240, 24)
    INTPOL = (124, 268435456, 28)
    DEDGE = (124, 536870912, 29)
    DISS2G = (124, 1073741824, 30)
    TOFF = (124, 15, 0)
    TFD_2__0_ = (124, 112, 4)
    OFFSET = (124, 1920, 7)
    TFD__ = (124, 2048, 11)
    DISFDCC = (124, 4096, 12)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    MRES = (124, 251658240, 24)
    INTPOL = (124, 268435456, 28)
    DEDGE = (124, 536870912, 29)
    DISS2G = (124, 1073741824, 30)
    TOFF = (124, 15, 0)
    HSTRT = (124, 112, 4)
    HEND = (124, 1920, 7)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    MRES = (124, 251658240, 24)
    INTPOL = (124, 268435456, 28)
    DEDGE = (124, 536870912, 29)
    DISS2G = (124, 1073741824, 30)
    SEMIN = (125, 15, 0)
    SEUP = (125, 96, 5)
    SEMAX = (125, 3840, 8)
    SEDN = (125, 24576, 13)
    SEIMIN = (125, 32768, 15)
    SGT = (125, 8323072, 16)
    SFILT = (125, 16777216, 24)
    DC_TIME = (126, 1023, 0)
    DC_SG = (126, 16711680, 16)
    SG_RESULT = (127, 1023, 0)
    FSACTIVE = (127, 32768, 15)
    CS_ACTUAL = (127, 2031616, 16)
    STALLGUARD = (127, 16777216, 24)
    OT = (127, 33554432, 25)
    OTPW = (127, 67108864, 26)
    S2GA = (127, 134217728, 27)
    S2GB = (127, 268435456, 28)
    OLA = (127, 536870912, 29)
    OLB = (127, 1073741824, 30)
    STST = (127, 2147483648, 31)