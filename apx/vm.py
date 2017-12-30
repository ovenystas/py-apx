from apx.base import *
from apx.vm_base import *
import struct

class VM:
    """
    APX Virtual Machine
    """
    def __init__(self, little_endian_format=True):
        def prog_header(opcode, code, code_next, code_end):
            if code_next+5 <= code_end:
                prog_type = code[code_next]; code_next+=1
                variant_type = code[code_next]; code_next+=1
                length = (int(code[code_next])<<16) | (int(code[code_next+1])<<8) | (int(code[code_next+2])); code_next+=3
                return ProgHeaderInstruction(prog_type, variant_type, length), code_next                    
            else:
                raise InvalidInstructionError('Expected 5 additional bytes after the opcode')
        def simple(opcode, code, code_next, code_end): return Instruction(opcode), code_next
        def array(opcode, code, code_next, code_end):
            if code_next+2 <= code_end:
                return Instruction(opcode, (int(code[code_next])<<8)|int(code[code_next+1])), code_next+2
            else:
                raise InvalidInstructionError('Expected 2 additional bytes after the opcode')
        
        def select(opcode, code, code_next, code_end):
            begin = code_next
            while(code_next<code_end):                
                if code[code_next] == 0:
                    end = code_next                    
                    code_next+=1
                    return SelectInstruction(code[begin:end].decode("ascii")), code_next
                code_next+=1
            raise InvalidInstructionError('Expected NULL terminator before end of program')
        
        self.opcode_map = {
            OPCODE_PROG_HEADER: prog_header,
            OPCODE_PACK_U8: simple,
            OPCODE_PACK_U16: simple,
            OPCODE_PACK_U32: simple,
            OPCODE_PACK_S8: simple,
            OPCODE_PACK_S16: simple,
            OPCODE_PACK_S32: simple,
            OPCODE_PACK_STR: array,
            OPCODE_PACK_U8AR: array,
            OPCODE_PACK_U16AR: array,
            OPCODE_PACK_U32AR: array,
            OPCODE_PACK_S8AR: array,
            OPCODE_PACK_S16AR: array,
            OPCODE_PACK_S32AR: array,
            OPCODE_UNPACK_U8: simple,
            OPCODE_UNPACK_U16: simple,
            OPCODE_UNPACK_U32: simple,
            OPCODE_UNPACK_S8: simple,
            OPCODE_UNPACK_S16: simple,
            OPCODE_UNPACK_S32: simple,
            OPCODE_UNPACK_STR: array,
            OPCODE_UNPACK_U8AR: array,
            OPCODE_UNPACK_U16AR: array,
            OPCODE_UNPACK_U32AR: array,
            OPCODE_UNPACK_S8AR: array,
            OPCODE_UNPACK_S16AR: array,
            OPCODE_UNPACK_S32AR: array,
            OPCODE_RECORD_ENTER: simple,
            OPCODE_RECORD_SELECT: select,
            OPCODE_RECORD_LEAVE: simple,
            OPCODE_ARRAY_ENTER: simple,
            OPCODE_ARRAY_NEXT: simple,
            OPCODE_ARRAY_LEAVE: simple,
        }
        
        self.exec_map = {
            OPCODE_PACK_STR: self._exec_pack_str,
            OPCODE_UNPACK_STR: self._exec_unpack_str
        }
        if little_endian_format:
            u8_pack = (self._exec_pack_struct, struct.Struct("B"), 1)
            u16_pack = (self._exec_pack_struct, struct.Struct("<H"),2)
            u32_pack = (self._exec_pack_struct, struct.Struct("<I"),4)
            s8_pack = (self._exec_pack_struct, struct.Struct("b"),1)
            s16_pack = (self._exec_pack_struct, struct.Struct("<h"),2)
            s32_pack = (self._exec_pack_struct, struct.Struct("<i"),4)
            u8_unpack = (self._exec_unpack_struct, struct.Struct("B"),1)
            u16_unpack = (self._exec_unpack_struct, struct.Struct("<H"),2)
            u32_unpack = (self._exec_unpack_struct, struct.Struct("<I"),4)
            s8_unpack = (self._exec_unpack_struct, struct.Struct("b"),1)
            s16_unpack = (self._exec_unpack_struct, struct.Struct("<h"),2)
            s32_unpack = (self._exec_unpack_struct, struct.Struct("<i"),4)
            self.struct_map = {
                #tuple: handler, struct, data length
                OPCODE_PACK_U8: u8_pack,
                OPCODE_PACK_U16: u16_pack,
                OPCODE_PACK_U32: u32_pack,
                OPCODE_PACK_S8: s8_pack,
                OPCODE_PACK_S16: s16_pack,
                OPCODE_PACK_S32: s32_pack,
                OPCODE_PACK_U8AR: u8_pack,
                OPCODE_PACK_U16AR: u16_pack,
                OPCODE_PACK_U32AR: u32_pack,
                OPCODE_PACK_S8AR: s8_pack,
                OPCODE_PACK_S16AR: s16_pack,
                OPCODE_PACK_S32AR: s32_pack,                
                
                OPCODE_UNPACK_U8: u8_unpack,
                OPCODE_UNPACK_U16: u16_unpack,
                OPCODE_UNPACK_U32: u32_unpack,
                OPCODE_UNPACK_S8: s8_unpack,
                OPCODE_UNPACK_S16: s16_unpack,
                OPCODE_UNPACK_S32: s32_unpack,
                OPCODE_UNPACK_U8AR: u8_unpack,
                OPCODE_UNPACK_U16AR: u16_unpack,
                OPCODE_UNPACK_U32AR: u32_unpack,
                OPCODE_UNPACK_S8AR: s8_unpack,
                OPCODE_UNPACK_S16AR: s16_unpack,
                OPCODE_UNPACK_S32AR: s32_unpack,
            }
        else:
            raise NotImplementedError("Big endian format")
        
        self.reset()

    def reset(self):
        """ Resets internal state"""
        self.value = None
        self.data = None
        self.data_offset=None
        self.prog_type = NO_PROG

    def set_state_internal(self, data, data_offset, first_instruction = False, value = None):
        self.value = value
        self.data=data
        self.data_offset=data_offset
        self.first_instruction = first_instruction
    
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
        self.prog_type = PACK_PROG
        self.data=data
        self.data_offset=data_offset
        self.value=value
        self.first_instruction=True
        while True:
            instruction, code_result = self.parse_next_instruction(code, code_next, code_end)
            if instruction is None:
                break
            else:
                self.exec_instruction(instruction)
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
                handler = self.opcode_map[opcode]
                return handler(opcode, code, code_next, code_end)
            except KeyError:
                raise UnknownOpCodeError('op_code = %d'%code[code_next])
        return None, code_next

    def exec_instruction(self, instruction):
        if self.first_instruction:
            if isinstance(instruction, ProgHeaderInstruction):
                self.first_instruction = False                
                if instruction.prog_type == PACK_PROG:
                    self.verify_value_compatibility(instruction.variant_type)
                if not self.verify_data_len(instruction.length):
                    raise RuntimeError('Not enough bytes in data buffer. Expected %d bytes, got %d'%(instruction.length, len(self.data)-self.data_offset))
            else:
                raise RuntimeError('first instructionm must be of type OPCODE_PROG_HEADER')
        else:
            if isinstance(instruction, SelectInstruction):
                raise NotImplementedError('SelectInstruction')
            elif isinstance(instruction, Instruction):
                if instruction.opcode in self.struct_map:
                    handler, struct_obj, data_len = self.struct_map[instruction.opcode]
                    handler(struct_obj, data_len, instruction.length)
                else:
                    handler = self.exec_map[instruction.opcode]
                    handler(instruction.length)
                

    def verify_value_type(self, value_type):
        if value_type == VTYPE_INVALID:
            raise InvalidValueTypeError(value_type)
        elif value_type == VTYPE_SCALAR and not isinstance(self.value, (str, int)):
            raise InvalidValueTypeError("Expected int or str, got '%s'"%type(self.value))
        elif value_type == VTYPE_LIST and not isinstance(self.value, list):
            raise InvalidValueTypeError("Expected list, got '%s'"%type(self.value))
        elif value_type == VTYPE_MAP and not isinstance(self.value, dict):
            raise InvalidValueTypeError("Expected dict, got '%s'"%type(self.value))
        return True

    def prepare_value(self, value_type):
        """
        Creates the initial container before unpacking value
        """
        if value_type == VTYPE_LIST:
            self.value = []
        elif value_type == VTYPE_MAP:
            self.value = {}
    
    def verify_data_len(self, length):
        return (len(self.data)-self.data_offset)>=length
    
    def _exec_pack_struct(self, obj, data_len, array_len):
        if array_len is None:
            obj.pack_into(self.data, self.data_offset, self.value)
            self.data_offset+=data_len
        else:
            for i in range(array_len):
                obj.pack_into(self.data, self.data_offset, self.value[i])
                self.data_offset+=data_len

    def _exec_unpack_struct(self, obj, data_len, array_len):
        if array_len is None:
            (self.value,) = obj.unpack_from(self.data, self.data_offset)
            self.data_offset+=data_len
        else:
            self.value=[]
            for i in range(array_len):
                (tmp,) = obj.unpack_from(self.data, self.data_offset)
                self.value.append(tmp)
                self.data_offset+=data_len
                    
    def _exec_pack_str(self, data_len):
        struct.pack_into('{:d}s'.format(data_len+1), self.data, self.data_offset, bytes(self.value, encoding='ascii'))
        self.data_offset+=data_len+1 #Python adds a null-terminator

    def _exec_unpack_str(self, data_len):
        (tmp,) = struct.unpack_from('{:d}s'.format(data_len), self.data, self.data_offset)
        self.value=tmp.decode("ascii")
        self.data_offset+=data_len+1
