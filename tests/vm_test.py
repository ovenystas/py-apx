import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestApxVM(unittest.TestCase):

    def test_parse_prog_header(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PROG_HEADER, apx.UNPACK_PROG, apx.VTYPE_MAP, 0x12, 0x34, 0x56])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.ProgHeaderInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.prog_type, apx.UNPACK_PROG)
        self.assertEqual(instruction.variant_type, apx.VTYPE_MAP)
        self.assertEqual(instruction.length, 0x123456)

        prog = bytes([0, 0, 0, apx.OPCODE_PROG_HEADER, apx.PACK_PROG, apx.VTYPE_SCALAR, 0, 0, 1])
        instruction, code_next = vm.parse_next_instruction(prog, 3, len(prog))
        self.assertIsInstance(instruction, apx.ProgHeaderInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.prog_type, apx.PACK_PROG)
        self.assertEqual(instruction.variant_type, apx.VTYPE_SCALAR)
        self.assertEqual(instruction.length, 1)

    def test_parse_pack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8)
        self.assertIsNone(instruction.length)

    def test_parse_pack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16)
        self.assertIsNone(instruction.length)

    def test_parse_pack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32)
        self.assertIsNone(instruction.length)

    def test_parse_pack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8)
        self.assertIsNone(instruction.length)

    def test_parse_pack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16)
        self.assertIsNone(instruction.length)

    def test_parse_pack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32)

    def test_parse_unpack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S16])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32)
        self.assertIsNone(instruction.length)

    def test_parse_pack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_STR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_STR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_STR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_STR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_U32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_U32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_pack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_PACK_S32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_PACK_S32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_STR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_STR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_STR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_STR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_U32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_U32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S8AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S8AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S16AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S16AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S16AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32AR, 0x12, 0x34])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32AR)
        self.assertEqual(instruction.length, 0x1234)

        prog = bytes([apx.OPCODE_UNPACK_S32AR, 0xFF, 0xFF])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_UNPACK_S32AR)
        self.assertEqual(instruction.length, 0xFFFF)

    def test_parse_unpack_record_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_ENTER])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_RECORD_ENTER)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_record_select(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_SELECT, ord('S'),ord('o'),ord('u'),ord('n'),ord('d'),ord('I'),ord('d'),0])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.SelectInstruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.name, "SoundId")

        prog = bytes([apx.OPCODE_RECORD_SELECT, ord('A'),ord('l'),ord('e'),ord('r'),ord('t'),0, apx.OPCODE_UNPACK_U8])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.SelectInstruction)
        self.assertEqual(code_next, len(prog)-1)
        self.assertEqual(instruction.name, "Alert")

    def test_parse_unpack_record_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_LEAVE])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_RECORD_LEAVE)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_ENTER])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_ENTER)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_next(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_NEXT])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_NEXT)
        self.assertIsNone(instruction.length)

    def test_parse_unpack_array_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_LEAVE])
        instruction, code_next = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertIsInstance(instruction, apx.Instruction)
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction.opcode, apx.OPCODE_ARRAY_LEAVE)
        self.assertIsNone(instruction.length)

    def test_parse_end_of_program(self):
        """
        Return None when end of program
        """
        vm = apx.VM()
        prog = bytes([0,0,0])
        instruction, code_next = vm.parse_next_instruction(prog, len(prog), len(prog))
        self.assertIsNone(instruction)
        self.assertEqual(code_next, len(prog))

    def test_verify_value_type(self):
        vm = apx.VM()
        vm.value=1
        self.assertTrue(vm.verify_value_type(apx.VTYPE_SCALAR))
        vm.value='Test'
        self.assertTrue(vm.verify_value_type(apx.VTYPE_SCALAR))
        with self.assertRaises(apx.InvalidValueTypeError) as context:
            vm.value=1.23
            self.assertTrue(vm.verify_value_type(apx.VTYPE_SCALAR))
        self.assertEqual("Expected int or str, got '<class 'float'>'", str(context.exception))
        vm.value=int(1.23)
        self.assertTrue(vm.verify_value_type(apx.VTYPE_SCALAR))
        vm.value=[1,2,3]
        self.assertTrue(vm.verify_value_type(apx.VTYPE_LIST))
        with self.assertRaises(apx.InvalidValueTypeError) as context:
            vm.value=1
            self.assertTrue(vm.verify_value_type(apx.VTYPE_LIST))
        self.assertEqual("Expected list, got '<class 'int'>'", str(context.exception))
        vm.value={'a':1, 'b':2, 'c':3}
        self.assertTrue(vm.verify_value_type(apx.VTYPE_MAP))
        with self.assertRaises(apx.InvalidValueTypeError) as context:
            vm.value='a'
            self.assertTrue(vm.verify_value_type(apx.VTYPE_MAP))
        self.assertEqual("Expected dict, got '<class 'str'>'", str(context.exception))

    def test_verify_data_len(self):
        vm = apx.VM()
        vm.set_state_internal(bytes([0,1]), 0)
        self.assertTrue(vm.verify_data_len(2))
        self.assertFalse(vm.verify_data_len(3))
        vm.data_offset=1
        self.assertFalse(vm.verify_data_len(2))
        self.assertTrue(vm.verify_data_len(1))

    def test_exec_pack_u8(self):
        vm = apx.VM()
        data = bytearray([0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_U8)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0]))
        self.assertEqual(vm.data_offset, 1)
        vm.value=0xAB
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0xAB,0]))
        self.assertEqual(vm.data_offset, 2)
        vm.value=0xFF
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0xAB,0xFF]))
        self.assertEqual(vm.data_offset, 3)


    def test_exec_unpack_u8(self):
        vm = apx.VM()
        data = bytearray([0,0xAB,0xFF])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_U8)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 1)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0xAB)
        self.assertEqual(vm.data_offset, 2)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0xFF)
        self.assertEqual(vm.data_offset, 3)

    def test_exec_pack_u16(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_U16)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0,0]))
        self.assertEqual(vm.data_offset, 2)
        vm.value=0x1234
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0x34,0x12,0,0]))
        self.assertEqual(vm.data_offset, 4)
        vm.value=0xFFFF
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0x34,0x12,0xFF,0xFF]))
        self.assertEqual(vm.data_offset, 6)

    def test_exec_unpack_u16(self):
        vm = apx.VM()
        data = bytearray([0,0,0x34,0x12,0xFF,0xFF])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_U16)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 2)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0x1234)
        self.assertEqual(vm.data_offset, 4)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0xFFFF)
        self.assertEqual(vm.data_offset, 6)

    def test_exec_pack_u32(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_U32)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0,0,0,0,0,0,0,0]))
        self.assertEqual(vm.data_offset, 4)
        vm.value=0x12345678
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0x78,0x56,0x34,0x12,0,0,0,0]))
        self.assertEqual(vm.data_offset, 8)
        vm.value=0xFFFFFFFF
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0x78,0x56,0x34,0x12,0xFF,0xFF,0xFF,0xFF]))
        self.assertEqual(vm.data_offset, 12)

    def test_exec_unpack_u32(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0x78,0x56,0x34,0x12,0xFF,0xFF,0xFF,0xFF])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_U32)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 4)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0x12345678)
        self.assertEqual(vm.data_offset, 8)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0xFFFFFFFF)
        self.assertEqual(vm.data_offset, 12)

    def test_exec_pack_s8(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_S8)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0]))
        self.assertEqual(vm.data_offset, 1)
        vm.value=127
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0x7F,0,0]))
        self.assertEqual(vm.data_offset, 2)
        vm.value=-1
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0x7F,0xFF,0]))
        self.assertEqual(vm.data_offset, 3)
        vm.value=-128
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0x7F,0xFF,0x80]))
        self.assertEqual(vm.data_offset, 4)


    def test_exec_unpack_s8(self):
        vm = apx.VM()
        data = bytearray([0,0x7F,0xFF,0x80])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_S8)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 1)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 127)
        self.assertEqual(vm.data_offset, 2)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -1)
        self.assertEqual(vm.data_offset, 3)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -128)
        self.assertEqual(vm.data_offset, 4)

    def test_exec_pack_s16(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0,0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_S16)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0,0,0,0]))
        self.assertEqual(vm.data_offset, 2)
        vm.value=32767
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0xFF,0x7F,0,0,0,0]))
        self.assertEqual(vm.data_offset, 4)
        vm.value=-1
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0xFF,0x7F,0xFF,0xFF,0,0]))
        self.assertEqual(vm.data_offset, 6)
        vm.value=-32768
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0xFF,0x7F,0xFF,0xFF,0,0x80]))
        self.assertEqual(vm.data_offset, 8)

    def test_exec_unpack_s16(self):
        vm = apx.VM()
        data = bytearray([0,0,0xFF,0x7F,0xFF,0xFF,0,0x80])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_S16)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 2)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 32767)
        self.assertEqual(vm.data_offset, 4)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -1)
        self.assertEqual(vm.data_offset, 6)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -32768)
        self.assertEqual(vm.data_offset, 8)

    def test_exec_pack_s32(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0, value = 0)
        instruction = apx.Instruction(apx.OPCODE_PACK_S32)
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
        self.assertEqual(vm.data_offset, 4)
        vm.value=2147483647
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0xFF,0xFF,0xFF,0x7F,0,0,0,0,0,0,0,0]))
        self.assertEqual(vm.data_offset, 8)
        vm.value=-1
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0xFF,0xFF,0xFF,0x7F,0xFF,0xFF,0xFF,0xFF,0,0,0,0]))
        self.assertEqual(vm.data_offset, 12)
        vm.value=-2147483648
        vm.exec_instruction(instruction)
        self.assertEqual(data, bytearray([0,0,0,0,0xFF,0xFF,0xFF,0x7F,0xFF,0xFF,0xFF,0xFF,0,0,0,0x80]))
        self.assertEqual(vm.data_offset, 16)

    def test_exec_unpack_s32(self):
        vm = apx.VM()
        data = bytearray([0,0,0,0,0xFF,0xFF,0xFF,0x7F,0xFF,0xFF,0xFF,0xFF,0,0,0,0x80])
        self.assertIsNone(vm.value)
        vm.set_state_internal(data, 0)
        instruction = apx.Instruction(apx.OPCODE_UNPACK_S32)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 0)
        self.assertEqual(vm.data_offset, 4)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, 2147483647)
        self.assertEqual(vm.data_offset, 8)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -1)
        self.assertEqual(vm.data_offset, 12)
        vm.exec_instruction(instruction)
        self.assertEqual(vm.value, -2147483648)
        self.assertEqual(vm.data_offset, 16)


if __name__ == '__main__':
    unittest.main()
