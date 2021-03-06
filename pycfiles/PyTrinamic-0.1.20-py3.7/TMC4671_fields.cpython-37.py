# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4671\TMC4671_fields.py
# Compiled at: 2019-12-05 09:47:54
# Size of source mod 2**32: 40150 bytes
"""
Created on 02.01.2019

@author: ED , JM
"""

class TMC4671_fields(object):
    __doc__ = '\n    Define all register bitfields of the TMC4671.\n\n    Each field is defined as a tuple consisting of ( Address, Mask, Shift ).\n\n    The name of the register is written as a comment behind each tuple. This is\n    intended for IDE users viewing the definition of a field by hovering over\n    it. This allows the user to see the corresponding register name of a field\n    without opening this file and searching for the definition.\n    '
    SI_TYPE = (0, 4294967295, 0)
    SI_VERSION = (0, 4294967295, 0)
    SI_DATE = (0, 4294967295, 0)
    SI_TIME = (0, 4294967295, 0)
    SI_VARIANT = (0, 4294967295, 0)
    SI_BUILD = (0, 4294967295, 0)
    CHIP_INFO_ADDRESS = (1, 255, 0)
    ADC_I0_RAW = (2, 65535, 0)
    ADC_I1_RAW = (2, 4294901760, 16)
    ADC_VM_RAW = (2, 65535, 0)
    ADC_AGPI_A_RAW = (2, 4294901760, 16)
    ADC_AGPI_B_RAW = (2, 65535, 0)
    ADC_AENC_UX_RAW = (2, 4294901760, 16)
    ADC_AENC_VN_RAW = (2, 65535, 0)
    ADC_AENC_WY_RAW = (2, 4294901760, 16)
    ADC_RAW_ADDR = (3, 255, 0)
    CFG_DSMODULATOR_A = (4, 3, 0)
    MCLK_POLARITY_A = (4, 4, 2)
    MDAT_POLARITY_A = (4, 8, 3)
    SEL_NCLK_MCLK_I_A = (4, 16, 4)
    BLANKING_A = (4, 65280, 8)
    CFG_DSMODULATOR_B = (4, 196608, 16)
    MCLK_POLARITY_B = (4, 262144, 18)
    MDAT_POLARITY_B = (4, 524288, 19)
    SEL_NCLK_MCLK_I_B = (4, 1048576, 20)
    BLANKING_B = (4, 4278190080, 24)
    DSADC_MCLK_A = (5, 4294967295, 0)
    DSADC_MCLK_B = (6, 4294967295, 0)
    DSADC_MDEC_A = (7, 65535, 0)
    DSADC_MDEC_B = (7, 4294901760, 16)
    ADC_I1_OFFSET = (8, 65535, 0)
    ADC_I1_SCALE = (8, 4294901760, 16)
    ADC_I0_OFFSET = (9, 65535, 0)
    ADC_I0_SCALE = (9, 4294901760, 16)
    ADC_I0_SELECT = (10, 255, 0)
    ADC_I1_SELECT = (10, 65280, 8)
    ADC_I_UX_SELECT = (10, 50331648, 24)
    ADC_I_V_SELECT = (10, 201326592, 26)
    ADC_I_WY_SELECT = (10, 805306368, 28)
    ADC_I0_EXT = (11, 65535, 0)
    ADC_I1_EXT = (11, 4294901760, 16)
    ADC_I0 = (12, 15, 0)
    ADC_I1 = (12, 240, 4)
    ADC_VM = (12, 3840, 8)
    ADC_AGPI_A = (12, 61440, 12)
    ADC_AGPI_B = (12, 983040, 16)
    ADC_AENC_UX = (12, 15728640, 20)
    ADC_AENC_VN = (12, 251658240, 24)
    ADC_AENC_WY = (12, 4026531840, 28)
    AENC_0_OFFSET = (13, 65535, 0)
    AENC_0_SCALE = (13, 4294901760, 16)
    AENC_1_OFFSET = (14, 65535, 0)
    AENC_1_SCALE = (14, 4294901760, 16)
    AENC_2_OFFSET = (15, 65535, 0)
    AENC_2_SCALE = (15, 4294901760, 16)
    AENC_0_SELECT = (17, 255, 0)
    AENC_1_SELECT = (17, 65280, 8)
    AENC_2_SELECT = (17, 16711680, 16)
    ADC_IUX = (18, 65535, 0)
    ADC_IWY = (18, 4294901760, 16)
    ADC_IV = (19, 65535, 0)
    AENC_UX = (21, 65535, 0)
    AENC_WY = (21, 4294901760, 16)
    AENC_VN = (22, 65535, 0)
    PWM_POLARITIES__ = (23, 1, 0)
    PWM_POLARITIES__ = (23, 2, 1)
    PWM_MAXCNT = (24, 65535, 0)
    PWM_BBM_L = (25, 255, 0)
    PWM_BBM_H = (25, 65280, 8)
    PWM_CHOP = (26, 255, 0)
    PWM_SV = (26, 256, 8)
    N_POLE_PAIRS = (27, 65535, 0)
    MOTOR_TYPE = (27, 16711680, 16)
    PHI_E_EXT = (28, 65535, 0)
    PHI_M_EXT = (29, 65535, 0)
    POSITION_EXT = (30, 4294967295, 0)
    OPENLOOP_PHI_DIRECTION = (31, 4096, 12)
    OPENLOOP_ACCELERATION = (32, 4294967295, 0)
    OPENLOOP_VELOCITY_TARGET = (33, 4294967295, 0)
    OPENLOOP_VELOCITY_ACTUAL = (34, 4294967295, 0)
    OPENLOOP_PHI = (35, 65535, 0)
    UD_EXT = (36, 65535, 0)
    UQ_EXT = (36, 4294901760, 16)
    APOL = (37, 1, 0)
    BPOL = (37, 2, 1)
    NPOL = (37, 4, 2)
    USE_ABN_AS_N = (37, 8, 3)
    CLN = (37, 256, 8)
    DIRECTION = (37, 4096, 12)
    ABN_DECODER_PPR = (38, 16777215, 0)
    ABN_DECODER_COUNT = (39, 16777215, 0)
    ABN_DECODER_COUNT_N = (40, 16777215, 0)
    ABN_DECODER_PHI_M_OFFSET = (41, 65535, 0)
    ABN_DECODER_PHI_E_OFFSET = (41, 4294901760, 16)
    ABN_DECODER_PHI_M = (42, 65535, 0)
    ABN_DECODER_PHI_E = (42, 4294901760, 16)
    APOL = (44, 1, 0)
    BPOL = (44, 2, 1)
    NPOL = (44, 4, 2)
    USE_ABN_AS_N = (44, 8, 3)
    CLN = (44, 256, 8)
    DIRECTION = (44, 4096, 12)
    ABN_2_DECODER_PPR = (45, 16777215, 0)
    ABN_2_DECODER_COUNT = (46, 16777215, 0)
    ABN_2_DECODER_COUNT_N = (47, 16777215, 0)
    ABN_2_DECODER_PHI_M_OFFSET = (48, 65535, 0)
    ABN_2_DECODER_PHI_M = (49, 65535, 0)
    POLARITY = (51, 1, 0)
    INTERPOLATION = (51, 256, 8)
    DIRECTION = (51, 4096, 12)
    HALL_BLANK = (51, 268369920, 16)
    HALL_POSITION_000 = (52, 65535, 0)
    HALL_POSITION_060 = (52, 4294901760, 16)
    HALL_POSITION_120 = (53, 65535, 0)
    HALL_POSITION_180 = (53, 4294901760, 16)
    HALL_POSITION_240 = (54, 65535, 0)
    HALL_POSITION_300 = (54, 4294901760, 16)
    HALL_PHI_M_OFFSET = (55, 65535, 0)
    HALL_PHI_E_OFFSET = (55, 4294901760, 16)
    HALL_DPHI_MAX = (56, 65535, 0)
    HALL_PHI_E = (57, 65535, 0)
    HALL_PHI_E_INTERPOLATED = (57, 4294901760, 16)
    HALL_PHI_M = (58, 65535, 0)
    AENC_DECODER_MODE__ = (59, 1, 0)
    AENC_DECODER_MODE__ = (59, 4096, 12)
    AENC_DECODER_N_THRESHOLD = (60, 65535, 0)
    AENC_DECODER_N_MASK = (60, 4294901760, 16)
    AENC_DECODER_PHI_A_RAW = (61, 65535, 0)
    AENC_DECODER_PHI_A_OFFSET = (62, 65535, 0)
    AENC_DECODER_PHI_A = (63, 65535, 0)
    AENC_DECODER_PPR = (64, 65535, 0)
    AENC_DECODER_COUNT = (65, 4294967295, 0)
    AENC_DECODER_COUNT_N = (66, 4294967295, 0)
    AENC_DECODER_PHI_M_OFFSET = (69, 65535, 0)
    AENC_DECODER_PHI_E_OFFSET = (69, 4294901760, 16)
    AENC_DECODER_PHI_M = (70, 65535, 0)
    AENC_DECODER_PHI_E = (70, 4294901760, 16)
    AENC_DECODER_POSITION = (71, 4294967295, 0)
    PIDIN_VELOCITY_TARGET = (75, 4294967295, 0)
    PIDIN_POSITION_TARGET = (76, 4294967295, 0)
    BIQUAD_X_A_1 = (77, 4294967295, 0)
    BIQUAD_X_A_2 = (77, 4294967295, 0)
    BIQUAD_X_B_0 = (77, 4294967295, 0)
    BIQUAD_X_B_1 = (77, 4294967295, 0)
    BIQUAD_X_B_2 = (77, 4294967295, 0)
    BIQUAD_X_ENABLE = (77, 4294967295, 0)
    BIQUAD_V_A_1 = (77, 4294967295, 0)
    BIQUAD_V_A_2 = (77, 4294967295, 0)
    BIQUAD_V_B_0 = (77, 4294967295, 0)
    BIQUAD_V_B_1 = (77, 4294967295, 0)
    BIQUAD_V_B_2 = (77, 4294967295, 0)
    BIQUAD_V_ENABLE = (77, 4294967295, 0)
    BIQUAD_T_A_1 = (77, 4294967295, 0)
    BIQUAD_T_A_2 = (77, 4294967295, 0)
    BIQUAD_T_B_0 = (77, 4294967295, 0)
    BIQUAD_T_B_1 = (77, 4294967295, 0)
    BIQUAD_T_B_2 = (77, 4294967295, 0)
    BIQUAD_T_ENABLE = (77, 4294967295, 0)
    BIQUAD_F_A_1 = (77, 4294967295, 0)
    BIQUAD_F_A_2 = (77, 4294967295, 0)
    BIQUAD_F_B_0 = (77, 4294967295, 0)
    BIQUAD_F_B_1 = (77, 4294967295, 0)
    BIQUAD_F_B_2 = (77, 4294967295, 0)
    BIQUAD_F_ENABLE = (77, 4294967295, 0)
    PRBS_AMPLITUDE = (77, 4294967295, 0)
    PRBS_DOWN_SAMPLING_RATIO = (77, 4294967295, 0)
    FEED_FORWARD_VELOCITY_GAIN = (77, 4294967295, 0)
    FEED_FORWARD_VELICITY_FILTER_CONSTANT = (77, 4294967295, 0)
    FEED_FORWARD_TORQUE_GAIN = (77, 4294967295, 0)
    FEED_FORWARD_TORGUE_FILTER_CONSTANT = (77, 4294967295, 0)
    VELOCITY_METER_PPTM_MIN_POS_DEV = (77, 65535, 0)
    REF_SWITCH_CONFIG = (77, 65535, 0)
    ENCODER_INIT_HALL_ENABLE = (77, 1, 0)
    SINGLE_PIN_IF_CFG = (77, 255, 0)
    SINGLE_PIN_IF_STATUS = (77, 4294901760, 16)
    SINGLE_PIN_IF_OFFSET = (77, 65535, 0)
    SINGLE_PIN_IF_SCALE = (77, 4294901760, 16)
    CONFIG_ADDR = (78, 4294967295, 0)
    VELOCITY_SELECTION = (80, 255, 0)
    VELOCITY_METER_SELECTION = (80, 65280, 8)
    POSITION_SELECTION = (81, 255, 0)
    PHI_E_SELECTION = (82, 255, 0)
    PHI_E = (83, 65535, 0)
    PID_FLUX_I = (84, 65535, 0)
    PID_FLUX_P = (84, 4294901760, 16)
    PID_TORQUE_I = (86, 65535, 0)
    PID_TORQUE_P = (86, 4294901760, 16)
    PID_VELOCITY_I = (88, 65535, 0)
    PID_VELOCITY_P = (88, 4294901760, 16)
    PID_POSITION_I = (90, 65535, 0)
    PID_POSITION_P = (90, 4294901760, 16)
    PID_TORQUE_FLUX_TARGET_DDT_LIMITS = (92, 4294967295, 0)
    PIDOUT_UQ_UD_LIMITS = (93, 65535, 0)
    PID_TORQUE_FLUX_LIMITS = (94, 65535, 0)
    PID_ACCELERATION_LIMIT = (95, 4294967295, 0)
    PID_VELOCITY_LIMIT = (96, 4294967295, 0)
    PID_POSITION_LIMIT_LOW = (97, 4294967295, 0)
    PID_POSITION_LIMIT_HIGH = (98, 4294967295, 0)
    MODE_MOTION = (99, 255, 0)
    MODE_RAMP = (99, 65280, 8)
    MODE_FF = (99, 16711680, 16)
    MODE_PID_SMPL = (99, 2130706432, 24)
    MODE_PID_TYPE = (99, 2147483648, 31)
    PID_FLUX_TARGET = (100, 65535, 0)
    PID_TORQUE_TARGET = (100, 4294901760, 16)
    PID_FLUX_OFFSET = (101, 65535, 0)
    PID_TORQUE_OFFSET = (101, 4294901760, 16)
    PID_VELOCITY_TARGET = (102, 4294967295, 0)
    PID_VELOCITY_OFFSET = (103, 4294967295, 0)
    PID_POSITION_TARGET = (104, 4294967295, 0)
    PID_FLUX_ACTUAL = (105, 65535, 0)
    PID_TORQUE_ACTUAL = (105, 4294901760, 16)
    PID_VELOCITY_ACTUAL = (106, 4294967295, 0)
    PID_POSITION_ACTUAL = (107, 4294967295, 0)
    PID_TORQUE_ERROR = (108, 4294967295, 0)
    PID_FLUX_ERROR = (108, 4294967295, 0)
    PID_VELOCITY_ERROR = (108, 4294967295, 0)
    PID_POSITION_ERROR = (108, 4294967295, 0)
    PID_TORQUE_ERROR_SUM = (108, 4294967295, 0)
    PID_FLUX_ERROR_SUM = (108, 4294967295, 0)
    PID_VELOCITY_ERROR_SUM = (108, 4294967295, 0)
    PID_POSITION_ERROR_SUM = (108, 4294967295, 0)
    PID_ERROR_ADDR = (109, 255, 0)
    PIDIN_TARGET_TORQUE = (110, 4294967295, 0)
    PIDIN_TARGET_FLUX = (110, 4294967295, 0)
    PIDIN_TARGET_VELOCITY = (110, 4294967295, 0)
    PIDIN_TARGET_POSITION = (110, 4294967295, 0)
    PIDOUT_TARGET_TORQUE = (110, 4294967295, 0)
    PIDOUT_TARGET_FLUX = (110, 4294967295, 0)
    PIDOUT_TARGET_VELOCITY = (110, 4294967295, 0)
    PIDOUT_TARGET_POSITION = (110, 4294967295, 0)
    FOC_IUX = (110, 65535, 0)
    FOC_IWY = (110, 4294901760, 16)
    FOC_IV = (110, 65535, 0)
    FOC_IA = (110, 65535, 0)
    FOC_IB = (110, 4294901760, 16)
    FOC_ID = (110, 65535, 0)
    FOC_IQ = (110, 4294901760, 16)
    FOC_UD = (110, 65535, 0)
    FOC_UQ = (110, 4294901760, 16)
    FOC_UD_LIMITED = (110, 65535, 0)
    FOC_UQ_LIMITED = (110, 4294901760, 16)
    FOC_UA = (110, 65535, 0)
    FOC_UB = (110, 4294901760, 16)
    FOC_UUX = (110, 65535, 0)
    FOC_UWY = (110, 4294901760, 16)
    FOC_UV = (110, 65535, 0)
    PWM_UX = (110, 65535, 0)
    PWM_WY = (110, 4294901760, 16)
    PWM_V = (110, 65535, 0)
    ADC_I_0 = (110, 65535, 0)
    ADC_I_1 = (110, 4294901760, 16)
    PID_FLUX_ACTUAL_DIV256 = (110, 255, 0)
    PID_TORQUE_ACTUAL_DIV256 = (110, 65280, 8)
    PID_FLUX_TARGET_DIV256 = (110, 16711680, 16)
    PID_TORQUE_TARGET_DIV256 = (110, 4278190080, 24)
    PID_TORQUE_ACTUAL = (110, 65535, 0)
    PID_TORQUE_TARGET = (110, 4294901760, 16)
    PID_FLUX_ACTUAL = (110, 65535, 0)
    PID_FLUX_TARGET = (110, 4294901760, 16)
    PID_VELOCITY_ACTUAL_DIV256 = (110, 65535, 0)
    PID_VELOCITY_TARGET_DIV256 = (110, 4294901760, 16)
    PID_VELOCITY_ACTUAL_LSB = (110, 65535, 0)
    PID_VELOCITY_TARGET_LSB = (110, 4294901760, 16)
    PID_POSITION_ACTUAL_DIV256 = (110, 65535, 0)
    PID_POSITION_TARGET_DIV256 = (110, 4294901760, 16)
    PID_POSITION_ACTUAL_LSB = (110, 65535, 0)
    PID_POSITION_TARGET_LSB = (110, 4294901760, 16)
    FF_VELOCITY = (110, 4294967295, 0)
    FF_TORQUE = (110, 65535, 0)
    ACTUAL_VELOCITY_PPTM = (110, 4294967295, 0)
    REF_SWITCH_STATUS = (110, 65535, 0)
    HOME_POSITION = (110, 4294967295, 0)
    LEFT_POSITION = (110, 4294967295, 0)
    RIGHT_POSITION = (110, 4294967295, 0)
    ENC_INIT_HALL_STATUS = (110, 65535, 0)
    ENC_INIT_HALL_PHI_E_ABN_OFFSET = (110, 65535, 0)
    ENC_INIT_HALL_PHI_E_AENC_OFFSET = (110, 65535, 0)
    ENC_INIT_HALL_PHI_A_AENC_OFFSET = (110, 65535, 0)
    ENC_INIT_MINI_MOVE_STATUS = (110, 65535, 0)
    ENC_INIT_MINI_MOVE_U_D = (110, 4294901760, 16)
    ENC_INIT_MINI_MOVE_PHI_E_OFFSET = (110, 65535, 0)
    ENC_INIT_MINI_MOVE_PHI_E = (110, 4294901760, 16)
    SINGLE_PIN_IF_TARGET_TORQUE = (110, 65535, 0)
    SINGLE_PIN_IF_PWM_DUTY_CYCLE = (110, 4294901760, 16)
    SINGLE_PIN_IF_TARGET_VELOCITY = (110, 4294967295, 0)
    SINGLE_PIN_IF_TARGET_POSITION = (110, 4294967295, 0)
    DEBUG_VALUE_0 = (110, 65535, 0)
    DEBUG_VALUE_1 = (110, 4294901760, 16)
    DEBUG_VALUE_2 = (110, 65535, 0)
    DEBUG_VALUE_3 = (110, 4294901760, 16)
    DEBUG_VALUE_4 = (110, 65535, 0)
    DEBUG_VALUE_5 = (110, 4294901760, 16)
    DEBUG_VALUE_6 = (110, 65535, 0)
    DEBUG_VALUE_7 = (110, 4294901760, 16)
    DEBUG_VALUE_8 = (110, 65535, 0)
    DEBUG_VALUE_9 = (110, 4294901760, 16)
    DEBUG_VALUE_10 = (110, 65535, 0)
    DEBUG_VALUE_11 = (110, 4294901760, 16)
    DEBUG_VALUE_12 = (110, 65535, 0)
    DEBUG_VALUE_13 = (110, 4294901760, 16)
    DEBUG_VALUE_14 = (110, 65535, 0)
    DEBUG_VALUE_15 = (110, 4294901760, 16)
    DEBUG_VALUE_16 = (110, 4294967295, 0)
    DEBUG_VALUE_17 = (110, 4294967295, 0)
    DEBUG_VALUE_18 = (110, 4294967295, 0)
    DEBUG_VALUE_19 = (110, 4294967295, 0)
    CONFIG_REG_0 = (110, 4294967295, 0)
    CONFIG_REG_1 = (110, 4294967295, 0)
    CTRL_PARAM_0 = (110, 65535, 0)
    CTRL_PARAM_1 = (110, 4294901760, 16)
    CTRL_PARAM_2 = (110, 65535, 0)
    CTRL_PARAM_3 = (110, 4294901760, 16)
    STATUS_REG_0 = (110, 4294967295, 0)
    STATUS_REG_1 = (110, 4294967295, 0)
    STATUS_PARAM_0 = (110, 65535, 0)
    STATUS_PARAM_1 = (110, 4294901760, 16)
    STATUS_PARAM_2 = (110, 65535, 0)
    STATUS_PARAM_3 = (110, 4294901760, 16)
    INTERIM_ADDR = (111, 255, 0)
    WATCHDOG_CFG = (116, 3, 0)
    ADC_VM_LIMIT_LOW = (117, 65535, 0)
    ADC_VM_LIMIT_HIGH = (117, 4294901760, 16)
    A_OF_ABN_RAW = (118, 1, 0)
    B_OF_ABN_RAW = (118, 2, 1)
    N_OF_ABN_RAW = (118, 4, 2)
    _ = (118, 8, 3)
    A_OF_ABN_2_RAW = (118, 16, 4)
    B_OF_ABN_2_RAW = (118, 32, 5)
    N_OF_ABN_2_RAW = (118, 64, 6)
    _ = (118, 128, 7)
    HALL_UX_OF_HALL_RAW = (118, 256, 8)
    HALL_V_OF_HALL_RAW = (118, 512, 9)
    HALL_WY_OF_HALL_RAW = (118, 1024, 10)
    _ = (118, 2048, 11)
    REF_SW_R_RAW = (118, 4096, 12)
    REF_SW_H_RAW = (118, 8192, 13)
    REF_SW_L_RAW = (118, 16384, 14)
    ENABLE_IN_RAW = (118, 32768, 15)
    STP_OF_DIRSTP_RAW = (118, 65536, 16)
    DIR_OF_DIRSTP_RAW = (118, 131072, 17)
    PWM_IN_RAW = (118, 262144, 18)
    _ = (118, 524288, 19)
    HALL_UX_FILT = (118, 1048576, 20)
    HALL_V_FILT = (118, 2097152, 21)
    HALL_WY_FILT = (118, 4194304, 22)
    _ = (118, 8388608, 23)
    _ = (118, 16777216, 24)
    _ = (118, 33554432, 25)
    _ = (118, 67108864, 26)
    _ = (118, 134217728, 27)
    PWM_IDLE_L_RAW = (118, 268435456, 28)
    PWM_IDLE_H_RAW = (118, 536870912, 29)
    _ = (118, 1073741824, 30)
    _ = (118, 2147483648, 31)
    TMC4671_OUTPUTS_RAW__ = (119, 1, 0)
    TMC4671_OUTPUTS_RAW__ = (119, 2, 1)
    TMC4671_OUTPUTS_RAW__ = (119, 4, 2)
    TMC4671_OUTPUTS_RAW__ = (119, 8, 3)
    TMC4671_OUTPUTS_RAW__ = (119, 16, 4)
    TMC4671_OUTPUTS_RAW__ = (119, 32, 5)
    TMC4671_OUTPUTS_RAW__ = (119, 64, 6)
    TMC4671_OUTPUTS_RAW__ = (119, 128, 7)
    STEP_WIDTH = (120, 4294967295, 0)
    UART_BPS = (121, 16777215, 0)
    ADDR_A = (122, 255, 0)
    ADDR_B = (122, 65280, 8)
    ADDR_C = (122, 16711680, 16)
    ADDR_D = (122, 4278190080, 24)
    GPIO_DSADCI_CONFIG__ = (123, 1, 0)
    GPIO_DSADCI_CONFIG__ = (123, 2, 1)
    GPIO_DSADCI_CONFIG__ = (123, 4, 2)
    GPIO_DSADCI_CONFIG__ = (123, 8, 3)
    GPIO_DSADCI_CONFIG__ = (123, 16, 4)
    GPIO_DSADCI_CONFIG__ = (123, 32, 5)
    GPIO_DSADCI_CONFIG__ = (123, 64, 6)
    GPO = (123, 16711680, 16)
    GPI = (123, 4278190080, 24)
    STATUS_FLAGS__ = (124, 1, 0)
    STATUS_FLAGS__ = (124, 2, 1)
    STATUS_FLAGS__ = (124, 4, 2)
    STATUS_FLAGS__ = (124, 8, 3)
    STATUS_FLAGS__ = (124, 16, 4)
    STATUS_FLAGS__ = (124, 32, 5)
    STATUS_FLAGS__ = (124, 64, 6)
    STATUS_FLAGS__ = (124, 128, 7)
    STATUS_FLAGS__ = (124, 256, 8)
    STATUS_FLAGS__ = (124, 512, 9)
    STATUS_FLAGS__ = (124, 1024, 10)
    STATUS_FLAGS__ = (124, 2048, 11)
    STATUS_FLAGS__ = (124, 4096, 12)
    STATUS_FLAGS__ = (124, 8192, 13)
    STATUS_FLAGS__ = (124, 16384, 14)
    STATUS_FLAGS__ = (124, 32768, 15)
    STATUS_FLAGS__ = (124, 65536, 16)
    STATUS_FLAGS__ = (124, 131072, 17)
    STATUS_FLAGS__ = (124, 262144, 18)
    STATUS_FLAGS__ = (124, 524288, 19)
    STATUS_FLAGS__ = (124, 1048576, 20)
    STATUS_FLAGS__ = (124, 2097152, 21)
    STATUS_FLAGS__ = (124, 4194304, 22)
    STATUS_FLAGS__ = (124, 8388608, 23)
    STATUS_FLAGS__ = (124, 16777216, 24)
    STATUS_FLAGS__ = (124, 33554432, 25)
    STATUS_FLAGS__ = (124, 67108864, 26)
    STATUS_FLAGS__ = (124, 134217728, 27)
    STATUS_FLAGS__ = (124, 268435456, 28)
    STATUS_FLAGS__ = (124, 536870912, 29)
    STATUS_FLAGS__ = (124, 1073741824, 30)
    STATUS_FLAGS__ = (124, 2147483648, 31)
    WARNING_MASK = (125, 4294967295, 0)