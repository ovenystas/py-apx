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
            return code_next+4, self.exec_pack_prog, [data_len]
        else:
            raise InvalidInstructionError('Expected 4 additional bytes after the opcode')

    def parse_unpack_prog(self, code, code_next, code_end):
        if code_next+4 <= code_end:
            data_len = (int(code[code_next])) | (int(code[code_next+1])<<8) | (int(code[code_next+2])<<16) | (int(code[code_next+3])<<24)
            return code_next+4, self.exec_unpack_prog, [data_len]
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
        self.init_pack_prog(value, len(data), data, data_offset)
        self.first_instruction=True
        while True:
            code_next, instruction, args = self.parse_next_instruction(code, code_next, code_end)
            if instruction is None:
                break
            else:
                self.exec_instruction(instruction, args)
        self.reset()
    
    def exec_unpack_prog(self, code, data, data_offset):
        """
        Executes the unpack program
        code: Compiled program (bytes)
        data: data to operate on (bytearray)
        data_offset: start offset (int)
        returns: unpacked python value (int, string, list or dict)
        """
        pass
        

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

    # def exec_instruction(self, instruction):
    #     if self.first_instruction:
    #         if isinstance(instruction, PackProgInstruction):
    #             self.verify_data_len(instruction.data_len, self.data, self.data_offset)
    #             self.first_instruction = False                
    #             self.prog_type = PACK_PROG
    #         elif isinstance(instruction, UnpackProgInstruction):
    #             self.verify_data_len(instruction.data_len, self.data, self.data_offset)
    #             self.first_instruction = False
    #             self.prog_type = UNPACK_PROG
    #             self.data=bytearray(instruction.data_len)
    #             self.data_offset = 0
    #         else:
    #             raise RuntimeError('first instructionm must be of type OPCODE_PROG_HEADER')
    #     else:
    #         if isinstance(instruction, RecordSelectInstruction):
    #             self._exec_record_select(instruction.name)
    #         elif isinstance(instruction, GenericInstruction):
    #             if instruction.opcode in self.struct_map:
    #                 handler, struct_obj, data_len = self.struct_map[instruction.opcode]
    #                 handler(struct_obj, data_len, instruction.length)
    #             else:
    #                 handler = self.exec_map[instruction.opcode]
    #                 handler(instruction.length)
                

    # def verify_value_type(self, value_type):
    #     if value_type == VTYPE_INVALID:
    #         raise InvalidValueTypeError(value_type)
    #     elif value_type == VTYPE_SCALAR and not isinstance(self.value, (str, int)):
    #         raise InvalidValueTypeError("Expected int or str, got '%s'"%type(self.value))
    #     elif value_type == VTYPE_LIST and not isinstance(self.value, list):
    #         raise InvalidValueTypeError("Expected list, got '%s'"%type(self.value))
    #     elif value_type == VTYPE_MAP and not isinstance(self.value, dict):
    #         raise InvalidValueTypeError("Expected dict, got '%s'"%type(self.value))
    #     return True


    # def _exec_pack_struct(self, obj, data_len, array_len):
    #     if array_len is None:
    #         obj.pack_into(self.data, self.data_offset, self.value)
    #         self.data_offset+=data_len
    #     else:
    #         for i in range(array_len):
    #             obj.pack_into(self.data, self.data_offset, self.value[i])
    #             self.data_offset+=data_len
    # 
    # def _exec_unpack_struct(self, obj, data_len, array_len):
    #     if array_len is None:
    #         (self.value,) = obj.unpack_from(self.data, self.data_offset)
    #         self.data_offset+=data_len
    #     else:
    #         self.value=[]
    #         for i in range(array_len):
    #             (tmp,) = obj.unpack_from(self.data, self.data_offset)
    #             self.value.append(tmp)
    #             self.data_offset+=data_len
    #                 
    # def _exec_pack_str(self, data_len):
    #     struct.pack_into('{:d}s'.format(data_len+1), self.data, self.data_offset, bytes(self.value, encoding='ascii'))
    #     self.data_offset+=data_len+1 #Python adds a null-terminator
    # 
    # def _exec_unpack_str(self, data_len):
    #     (tmp,) = struct.unpack_from('{:d}s'.format(data_len), self.data, self.data_offset)
    #     self.value=tmp.decode("ascii")
    #     self.data_offset+=data_len+1
    # 
    # def _exec_record_select(self, name):
    #     pass
    
