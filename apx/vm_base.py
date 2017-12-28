OPCODE_NOP = 0
OPCODE_PROG_HEADER = 1
OPCODE_PACK_U8 = 2
OPCODE_PACK_U16 = 3
OPCODE_PACK_U32 = 4
OPCODE_PACK_S8 = 5
OPCODE_PACK_S16 = 6
OPCODE_PACK_S32 = 7
OPCODE_PACK_STR = 8
OPCODE_PACK_U8AR = 9
OPCODE_PACK_U16AR = 10
OPCODE_PACK_U32AR = 11
OPCODE_PACK_S8AR = 12
OPCODE_PACK_S16AR = 13
OPCODE_PACK_S32AR = 14
OPCODE_UNPACK_U8 = 15
OPCODE_UNPACK_U16 = 16
OPCODE_UNPACK_U32 = 17
OPCODE_UNPACK_S8 = 18
OPCODE_UNPACK_S16 = 19
OPCODE_UNPACK_S32 = 20
OPCODE_UNPACK_STR = 21
OPCODE_UNPACK_U8AR = 22
OPCODE_UNPACK_U16AR = 23
OPCODE_UNPACK_U32AR = 24
OPCODE_UNPACK_S8AR = 25
OPCODE_UNPACK_S16AR = 26
OPCODE_UNPACK_S32AR = 27
OPCODE_RECORD_ENTER = 28
OPCODE_RECORD_SELECT = 29
OPCODE_RECORD_LEAVE = 30
OPCODE_ARRAY_ENTER = 31
OPCODE_ARRAY_NEXT = 32
OPCODE_ARRAY_LEAVE = 33

PACK_PROG = 0
UNPACK_PROG = 1

UINT8_LEN   = 1
UINT16_LEN  = 2
UINT32_LEN  = 4
SINT8_LEN   = 1
SINT16_LEN  = 2
SINT32_LEN  = 4

#Errors
class InvalidInstructionError(RuntimeError):
    pass

class UnknownOpCodeError(RuntimeError):
    pass

#Instructions
class ProgHeaderInstruction:
    __slots__ = ['prog_type', 'variant_type', 'length']
    def __init__(self, prog_type, variant_type, length):
        self.prog_type = prog_type
        self.variant_type=variant_type
        self.length = length

class Instruction:
    """
    For all other instructions
    """
    __slots__ = ['opcode', 'length']
    def __init__(self, opcode, length=None):
        self.opcode = opcode
        self.length = length

class SelectInstruction:
    """
    For all other instructions
    """
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name