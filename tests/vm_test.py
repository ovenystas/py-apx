import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestApxVM(unittest.TestCase):

    def test_parse_prog_header(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PROG_HEADER, apx.UNPACK_PROG, apx.VTYPE_MAP, 0x12, 0x34, 0x56])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.ProgHeaderInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.prog_type, apx.UNPACK_PROG)
        self.assertEqual(instruction.variant_type, apx.VTYPE_MAP)
        self.assertEqual(instruction.length, 0x123456)

        prog = bytes([0, 0, 0, apx.OPCODE_PROG_HEADER, apx.PACK_PROG, apx.VTYPE_SCALAR, 0, 0, 1])
        instruction, code_next = vm.parseNextInstruction(prog, 3, len(prog))
        self.assertIsInstance(instruction, apx.ProgHeaderInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.prog_type, apx.PACK_PROG)
        self.assertEqual(instruction.variant_type, apx.VTYPE_SCALAR)
        self.assertEqual(instruction.length, 1)
    
    def test_parse_pack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8)
        self.assertIsNone(instruction.length)

    def test_parse_pack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16)
        self.assertIsNone(instruction.length)

    def test_parse_pack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32)
        self.assertIsNone(instruction.length)
    
    def test_parse_pack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8)
        self.assertIsNone(instruction.length)

    def test_parse_pack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16)
        self.assertIsNone(instruction.length)
    
    def test_parse_pack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32)
    
    def test_parse_unpack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S16])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16)
        self.assertIsNone(instruction.length)
    
    def test_parse_unpack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))        
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32)
        self.assertIsNone(instruction.length)

    def test_parse_pack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_STR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_STR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_STR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_STR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_STR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_STR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_STR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_STR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S16AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32AR, 0x12, 0x34])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_record_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_ENTER])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_RECORD_ENTER)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_record_select(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_SELECT, ord('S'),ord('o'),ord('u'),ord('n'),ord('d'),ord('I'),ord('d'),0])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.SelectInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.name, "SoundId")

        prog = bytes([apx.OPCODE_RECORD_SELECT, ord('A'),ord('l'),ord('e'),ord('r'),ord('t'),0, apx.OPCODE_UNPACK_U8])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.SelectInstruction)
        self.assertEqual(code_next, len(prog)-1)
        self.assertEqual(instruction.name, "Alert")
        
    def test_parse_unpack_record_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_LEAVE])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_RECORD_LEAVE)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_ENTER])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_ENTER)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_next(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_NEXT])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_NEXT)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_LEAVE])
        instruction, code_next = vm.parseNextInstruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_LEAVE)
        self.assertIsNone(instruction.length)

if __name__ == '__main__':
    unittest.main()
