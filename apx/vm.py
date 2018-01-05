from apx.base import *
from apx.vm_base import *
from apx.vm_state import *
from apx.vm_state import *
import struct
import functools

class VM:
    """
    APX Virtual Machine
    """
    def __init__(self, little_endian_format=True):
        self.opcode_parser_map = {
            OPCODE_PACK_PROG: self.parse_pack_prog,
            OPCODE_UNPACK_PROG: self.parse_unpack_prog,
            OPCODE_PACK_U8: self.parse_pack_u8,
            OPCODE_PACK_U16: self.parse_pack_u16,
            OPCODE_PACK_U32: self.parse_pack_u32,
            OPCODE_PACK_S8: self.parse_pack_s8,
            OPCODE_PACK_S16: self.parse_pack_s16,
            OPCODE_PACK_S32: self.parse_pack_s32,
            OPCODE_PACK_STR: self.parse_pack_str,
            OPCODE_PACK_U8AR: self.parse_pack_u8_array,
            OPCODE_PACK_U16AR: self.parse_pack_u16_array,
            OPCODE_PACK_U32AR: self.parse_pack_u32_array,
            OPCODE_PACK_S8AR: self.parse_pack_s8_array,
            OPCODE_PACK_S16AR: self.parse_pack_s16_array,
            OPCODE_PACK_S32AR: self.parse_pack_s32_array,
            OPCODE_UNPACK_U8: self.parse_unpack_u8,
            OPCODE_UNPACK_U16: self.parse_unpack_u16,
            OPCODE_UNPACK_U32: self.parse_unpack_u32,
            OPCODE_UNPACK_S8: self.parse_unpack_s8,
            OPCODE_UNPACK_S16: self.parse_unpack_s16,
            OPCODE_UNPACK_S32: self.parse_unpack_s32,
            OPCODE_UNPACK_STR: self.parse_unpack_str,
            OPCODE_UNPACK_U8AR: self.parse_unpack_u8_array,
            OPCODE_UNPACK_U16AR: self.parse_unpack_u16_array,
            OPCODE_UNPACK_U32AR: self.parse_unpack_u32_array,
            OPCODE_UNPACK_S8AR: self.parse_unpack_s8_array,
            OPCODE_UNPACK_S16AR: self.parse_unpack_s16_array,
            OPCODE_UNPACK_S32AR: self.parse_unpack_s32_array,
            OPCODE_RECORD_ENTER: self.parse_record_enter,
            OPCODE_RECORD_SELECT: self.parse_record_select,
            OPCODE_RECORD_LEAVE: self.parse_record_leave,
            OPCODE_ARRAY_ENTER: self.parse_array_enter,
            OPCODE_ARRAY_LEAVE: self.parse_array_leave,
        }
                        
        self.reset()
    
    @property
    def value(self):
        if self.state is None:
            raise RuntimeError('self.state is not initialized')
        return self.state.value
    
    @value.setter
    def value(self, value):
        if self.state is None:
            raise RuntimeError('self.state is not initialized')
        self.state.value = value

    def reset(self):
        """
        Resets internal state
        """
        self.data = None
        self.data_offset=None
        self.prog_type = NO_PROG
        self.state = None

    def init_pack_prog(self, value, data_len, data, data_offset=0):
        self.verify_data_len(data_len, data, data_offset)
        self.state = VmPackState(value)
        self.prog_type = PACK_PROG
        self.data=data
        self.data_offset = data_offset
            
    def init_unpack_prog(self, data_len, data, data_offset=0):
        self.verify_data_len(data_len, data, data_offset)
        self.state = VmUnpackState()
        self.prog_type = UNPACK_PROG
        self.data=data
        self.data_offset = data_offset
    
    def verify_data_len(self, data_len, data, data_offset):
        bytes_avail = len(data)-data_offset
        if bytes_avail < data_len:
            raise RuntimeError('Not enough bytes in bytearray (data). Require {:d} bytes, got {:d}'.format(data_len, bytes_avail))
    
    def parse_pack_prog(self, code, code_next, code_end):
        if code_next+4 <= code_end:
            data_len = (int(code[code_next])) | (int(code[code_next+1])<<8) | (int(code[code_next+2])<<16) | (int(code[code_next+3])<<24)
            return code_next+4, self.exec_pack_prog_instruction, [data_len]
        else:
            raise InvalidInstructionError('Expected 4 additional bytes after the opcode')

    def parse_unpack_prog(self, code, code_next, code_end):
        if code_next+4 <= code_end:
            data_len = (int(code[code_next])) | (int(code[code_next+1])<<8) | (int(code[code_next+2])<<16) | (int(code[code_next+3])<<24)
            return code_next+4, self.exec_unpack_prog_instruction, [data_len]
        else:
            raise InvalidInstructionError('Expected 4 additional bytes after the opcode')
    
    def parse_pack_u8(self, code, code_next, code_end):
        return code_next, self.exec_pack_u8, None
    
    def parse_pack_u16(self, code, code_next, code_end):
        return code_next, self.exec_pack_u16, None

    def parse_pack_u32(self, code, code_next, code_end):
        return code_next, self.exec_pack_u32, None

    def parse_pack_s8(self, code, code_next, code_end):
        return code_next, self.exec_pack_s8, None

    def parse_pack_s16(self, code, code_next, code_end):
        return code_next, self.exec_pack_s16, None

    def parse_pack_s32(self, code, code_next, code_end):
        return code_next, self.exec_pack_s32, None
    
    def parse_pack_u8_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_u8, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_pack_u16_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_u16, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')        

    def parse_pack_u32_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_u32, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')    

    def parse_pack_s8_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_s8, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_pack_s16_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_s16, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_pack_s32_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_s32, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_pack_str(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_pack_str, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_unpack_u8(self, code, code_next, code_end):
        return code_next, self.exec_unpack_u8, None
    
    def parse_unpack_u16(self, code, code_next, code_end):
        return code_next, self.exec_unpack_u16, None

    def parse_unpack_u32(self, code, code_next, code_end):
        return code_next, self.exec_unpack_u32, None

    def parse_unpack_s8(self, code, code_next, code_end):
        return code_next, self.exec_unpack_s8, None

    def parse_unpack_s16(self, code, code_next, code_end):
        return code_next, self.exec_unpack_s16, None

    def parse_unpack_s32(self, code, code_next, code_end):
        return code_next, self.exec_unpack_s32, None
    
    def parse_unpack_u8_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_u8, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_unpack_u16_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_u16, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')        

    def parse_unpack_u32_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_u32, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')    

    def parse_unpack_s8_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_s8, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_unpack_s16_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_s16, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_unpack_s32_array(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_s32, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')

    def parse_unpack_str(self, code, code_next, code_end):
        if code_next+2 <= code_end:
            array_len = (int(code[code_next])) | (int(code[code_next+1])<<8)            
            return code_next+2, self.exec_unpack_str, [array_len]
        else:
            raise InvalidInstructionError('Expected 2 additional bytes after the opcode')        

    def parse_record_enter(self, code, code_next, code_end):
        return code_next, self.exec_record_enter, None

    def parse_record_select(self, code, code_next, code_end):        
        begin = code_next
        while(code_next<code_end):
            if code[code_next] == 0:
                end = code_next                    
                code_next+=1
                return code_next, self.exec_record_select, [code[begin:end].decode("ascii")]                
            code_next+=1
        raise InvalidInstructionError('Expected NULL terminator before end of program')

    def parse_record_leave(self, code, code_next, code_end):
        return code_next, self.exec_record_leave, None

    def parse_array_enter(self, code, code_next, code_end):
        return code_next, self.exec_array_enter, None

    def parse_array_leave(self, code, code_next, code_end):
        return code_next, self.exec_array_leave, None

    def exec_pack_u8(self, array_len=0):
        self.data_offset=self.state.pack_u8(self.data, self.data_offset, array_len)
    
    def exec_pack_u16(self, array_len=0):
        self.data_offset=self.state.pack_u16(self.data, self.data_offset, array_len)

    def exec_pack_u32(self, array_len=0):
        self.data_offset=self.state.pack_u32(self.data, self.data_offset, array_len)

    def exec_pack_s8(self, array_len=0):
        self.data_offset=self.state.pack_s8(self.data, self.data_offset, array_len)
    
    def exec_pack_s16(self, array_len=0):
        self.data_offset=self.state.pack_s16(self.data, self.data_offset, array_len)

    def exec_pack_s32(self, array_len=0):
        self.data_offset=self.state.pack_s32(self.data, self.data_offset, array_len)

    def exec_pack_str(self, array_len=0):
        self.data_offset=self.state.pack_str(self.data, self.data_offset, array_len)

    def exec_unpack_u8(self, array_len=0):
        self.data_offset=self.state.unpack_u8(self.data, self.data_offset, array_len)
    
    def exec_unpack_u16(self, array_len=0):
        self.data_offset=self.state.unpack_u16(self.data, self.data_offset, array_len)

    def exec_unpack_u32(self, array_len=0):
        self.data_offset=self.state.unpack_u32(self.data, self.data_offset, array_len)

    def exec_unpack_s8(self, array_len=0):
        self.data_offset=self.state.unpack_s8(self.data, self.data_offset, array_len)
    
    def exec_unpack_s16(self, array_len=0):
        self.data_offset=self.state.unpack_s16(self.data, self.data_offset, array_len)

    def exec_unpack_s32(self, array_len=0):
        self.data_offset=self.state.unpack_s32(self.data, self.data_offset, array_len)

    def exec_unpack_str(self, array_len=0):
        self.data_offset=self.state.unpack_str(self.data, self.data_offset, array_len)

    def exec_record_enter(self):
        self.state.record_enter()

    def exec_record_select(self, name):
        self.state.record_select(name)

    def exec_record_leave(self):
        self.state.record_leave()

    def exec_array_enter(self):
        self.state.array_enter()

    def exec_array_leave(self):
        self.state.array_leave()

    def exec_pack_prog(self, code, data, data_offset, value):
        """
        Executes the pack program
        code: compiled program (bytes)
        data: data to operate on (bytearray)
        data_offset: start offset (int)
        value: the python value that shall be packed (int, string, list or dict)
        """
        code_next = 0
        code_end = len(code)
        self.reset()
        self.init_pack_prog(value, len(data)-data_offset, data, data_offset)
        self.first_instruction=True
        while True:
            code_next, instruction, args = self.parse_next_instruction(code, code_next, code_end)
            if instruction is None:
                break
            else:
                if self.first_instruction:
                    self.first_instruction = False
                    if instruction != self.exec_pack_prog_instruction:
                        raise RuntimeError('First instuction must be of type OPCODE_PACK_PROG')
                self.exec_instruction(instruction, args)
        
    
    def exec_unpack_prog(self, code, data, data_offset):
        """
        Executes the unpack program
        code: Compiled program (bytes)
        data: data to operate on (bytearray)
        data_offset: start offset (int)
        returns: unpacked python value (int, string, list or dict)
        """
        """
        Executes the pack program
        code: compiled program (bytes)
        data: data to operate on (bytearray)
        data_offset: start offset (int)
        value: the python value that shall be packed (int, string, list or dict)
        """
        code_next = 0
        code_end = len(code)
        self.reset()
        self.init_unpack_prog(len(data)-data_offset, data, data_offset)
        self.first_instruction=True
        while True:
            code_next, instruction, args = self.parse_next_instruction(code, code_next, code_end)
            if instruction is None:
                break
            else:
                if self.first_instruction:
                    self.first_instruction = False
                    if instruction != self.exec_unpack_prog_instruction:
                        raise RuntimeError('First instuction must be of type OPCODE_UNPACK_PROG')
                self.exec_instruction(instruction, args)        
        

    def parse_next_instruction(self, code, code_next, code_end):
        """
        Returns the next parsed instruction along with the next parse position        
        """
        if code_next < code_end:
            opcode = code[code_next]; code_next+=1
            try:
                parser_handler = self.opcode_parser_map[opcode]
                return parser_handler(code, code_next, code_end) #returns code_next, instruction, args
            except KeyError:
                raise UnknownOpCodeError('op_code = %d'%code[code_next])
        return code_next, None, None
    
    def exec_instruction(self, instruction, args):
        if args is None:
            instruction()
        else:
            instruction(*args)
    
    def exec_pack_prog_instruction(self, data_len):
        if self.prog_type == NO_PROG:
            raise RuntimeError('Virtual machine not properly initialized')
        elif self.prog_type != PACK_PROG:
            raise RuntimeError('Wrong type of program, expected pack program')
        self.verify_data_len(data_len, self.data, self.data_offset)
        
    def exec_unpack_prog_instruction(self, data_len):
        if self.prog_type == NO_PROG:
            raise RuntimeError('Virtual machine not properly initialized')
        elif self.prog_type != UNPACK_PROG:
            raise RuntimeError('Wrong type of program, expected unpack program')
        self.verify_data_len(data_len, self.data, self.data_offset)
