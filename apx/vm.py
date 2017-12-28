from apx.base import *
from apx.vm_base import *

class VM:
    """
    APX Virtual Machine
    """
    def __init__(self):
        self.value = None
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
        instruction, code_result = self.parseNextInstruction(code, code_next, code_end)
    
    def exec_unpack_prog(self, code, data, data_offset):
        """
        Executes the unpack program
        code: Compiled program (bytes)
        data: data to operate on (bytearray)
        data_offset: start offset (int)
        returns: unpacked python value (int, string, list or dict)
        """
        pass
        

    def parseNextInstruction(self, code, code_next, code_end):
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

