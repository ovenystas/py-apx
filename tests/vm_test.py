import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestApxVM(unittest.TestCase):

    def test_parse_pack_prog_header(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_PROG, 0x78, 0x56, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_prog)
        self.assertEqual(args, [0x12345678])

    def test_parse_unpack_prog_header(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_PROG, 0x78, 0x56, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_prog)
        self.assertEqual(args, [0x12345678])
    
    def test_parse_pack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u8)
        self.assertIsNone(args)

    def test_parse_pack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u16)
        self.assertIsNone(args)

    def test_parse_pack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u32)
        self.assertIsNone(args)
    
    def test_parse_pack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s8)
        self.assertIsNone(args)

    def test_parse_pack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s16)
        self.assertIsNone(args)

    def test_parse_pack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s32)
        self.assertIsNone(args)

    def test_parse_unpack_u8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u8)
        self.assertIsNone(args)

    def test_parse_unpack_u16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u16)
        self.assertIsNone(args)

    def test_parse_unpack_u32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u32)
        self.assertIsNone(args)
    
    def test_parse_unpack_s8(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_s8)
        self.assertIsNone(args)

    def test_parse_unpack_s16(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S16])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_s16)
        self.assertIsNone(args)

    def test_parse_unpack_s32(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_s32)
        self.assertIsNone(args)

    def test_parse_pack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_STR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_str)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_str(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_STR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_str)
        self.assertEqual(args, [0x1234])

    def test_parse_pack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U8AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u8)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_u8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U8AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u8)
        self.assertEqual(args, [0x1234])

    def test_parse_pack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U16AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u16)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u16)
        self.assertEqual(args, [0x1234])
    
    def test_parse_pack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_U32AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_u32)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_u32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U32AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u32)
        self.assertEqual(args, [0x1234])
        
    def test_parse_pack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S8AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s8)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_s8_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S8AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_s8)
        self.assertEqual(args, [0x1234])

    def test_parse_pack_s16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S16AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s16)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_u16_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_U16AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_u16)
        self.assertEqual(args, [0x1234])
    
    def test_parse_pack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_PACK_S32AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_pack_s32)
        self.assertEqual(args, [0x1234])

    def test_parse_unpack_s32_array(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_UNPACK_S32AR, 0x34, 0x12])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_unpack_s32)
        self.assertEqual(args, [0x1234])
    
    def test_parse_record_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_ENTER])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_record_enter)
        self.assertIsNone(args)

    def test_parse_record_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_LEAVE])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_record_leave)
        self.assertIsNone(args)

    def test_parse_array_enter(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_ENTER])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_array_enter)
        self.assertIsNone(args)

    def test_parse_array_leave(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_ARRAY_LEAVE])
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_array_leave)
        self.assertIsNone(args)

    def test_parse_record_select(self):
        vm = apx.VM()
        prog = bytes([apx.OPCODE_RECORD_SELECT])+'Selection\0'.encode('ascii')
        code_next, instruction, args = vm.parse_next_instruction(prog, 0, len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertEqual(instruction, vm.exec_record_select)
        self.assertEqual(args, ['Selection'])
  
    def test_parse_end_of_program(self):
        """
        Return None when end of program
        """
        vm = apx.VM()
        prog = bytes([0,0,0])
        code_next, instruction, args = vm.parse_next_instruction(prog, len(prog), len(prog))
        self.assertEqual(code_next, len(prog))
        self.assertIsNone(instruction)
        self.assertIsNone(args)
    
    def test_exec_pack_u8(self):
        vm = apx.VM()
        data = bytearray(3)
        vm.init_pack_prog(value=0, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u8, None)
        self.assertEqual(data, bytearray([0,0,0]))
        vm.value = 128
        vm.exec_instruction(vm.exec_pack_u8, None)
        self.assertEqual(data, bytearray([0,128,0]))
        vm.value = 255
        vm.exec_instruction(vm.exec_pack_u8, None)
        self.assertEqual(data, bytearray([0,128,255]))

    def test_exec_pack_u16(self):
        vm = apx.VM()
        data = bytearray(6)
        vm.init_pack_prog(value=0, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u16, None)
        self.assertEqual(data, bytearray([0, 0, 0, 0, 0, 0]))
        vm.value = 0x1234
        vm.exec_instruction(vm.exec_pack_u16, None)
        self.assertEqual(data, bytearray([0, 0, 0x34, 0x12, 0, 0]))
        vm.value = 65535
        vm.exec_instruction(vm.exec_pack_u16, None)
        self.assertEqual(data, bytearray([0, 0, 0x34, 0x12, 0xFF, 0xFF]))

    def test_exec_pack_u32(self):
        vm = apx.VM()
        data = bytearray(12)
        vm.init_pack_prog(value=0, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u32, None)
        self.assertEqual(data, bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        vm.value = 0x12345678
        vm.exec_instruction(vm.exec_pack_u32, None)
        self.assertEqual(data, bytearray([0, 0, 0, 0, 0x78, 0x56, 0x34, 0x12, 0, 0, 0, 0]))
        vm.value = 0xFFFFFFFF
        vm.exec_instruction(vm.exec_pack_u32, None)
        self.assertEqual(data, bytearray([0, 0, 0, 0, 0x78, 0x56, 0x34, 0x12, 0xFF, 0xFF, 0xFF, 0xFF]))

    def test_exec_pack_s8(self):
        vm = apx.VM()
        data = bytearray(4)
        vm.init_pack_prog(value=-128, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s8, None)
        self.assertEqual(data, bytearray([0x80,0,0,0]))
        vm.value = -1
        vm.exec_instruction(vm.exec_pack_s8, None)
        self.assertEqual(data, bytearray([0x80,0xFF,0,0]))
        vm.value = 0
        vm.exec_instruction(vm.exec_pack_s8, None)
        self.assertEqual(data, bytearray([0x80,0xFF,0,0]))
        vm.value = 127
        vm.exec_instruction(vm.exec_pack_s8, None)
        self.assertEqual(data, bytearray([0x80,0xFF,0,127]))

    def test_exec_pack_s16(self):
        vm = apx.VM()
        data = bytearray(8)
        vm.init_pack_prog(value=-32768, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s16, None)
        self.assertEqual(data, bytearray([0,0x80,0,0,0,0,0,0]))
        vm.value = -1
        vm.exec_instruction(vm.exec_pack_s16, None)
        self.assertEqual(data, bytearray([0,0x80,0xFF,0xFF,0,0,0,0]))
        vm.value = 0
        vm.exec_instruction(vm.exec_pack_s16, None)
        self.assertEqual(data, bytearray([0,0x80,0xFF,0xFF,0,0,0,0]))
        vm.value = 32767
        vm.exec_instruction(vm.exec_pack_s16, None)
        self.assertEqual(data, bytearray([0,0x80,0xFF,0xFF,0,0,0xFF,0x7F]))

    def test_exec_pack_s32(self):
        vm = apx.VM()
        data = bytearray(16)
        vm.init_pack_prog(value=-2147483648, data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s32, None)
        self.assertEqual(data, bytearray([0,0,0,0x80, 0,0,0,0, 0,0,0,0, 0,0,0,0]))
        vm.value = -1
        vm.exec_instruction(vm.exec_pack_s32, None)
        self.assertEqual(data, bytearray([0,0,0,0x80, 0xFF,0xFF,0xFF,0xFF, 0,0,0,0, 0,0,0,0]))
        vm.value = 0
        vm.exec_instruction(vm.exec_pack_s32, None)
        self.assertEqual(data, bytearray([0,0,0,0x80, 0xFF,0xFF,0xFF,0xFF, 0,0,0,0, 0,0,0,0]))
        vm.value = 2147483647
        vm.exec_instruction(vm.exec_pack_s32, None)
        self.assertEqual(data, bytearray([0,0,0,0x80, 0xFF,0xFF,0xFF,0xFF, 0,0,0,0, 0xFF,0xFF,0xFF,0x7F]))

    def test_exec_pack_u8_array(self):
        vm = apx.VM()
        data = bytearray(4)
        vm.init_pack_prog(value=[1,2,3,4], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u8, [4])
        self.assertEqual(data, bytearray([1,2,3,4]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u8, [5])

    def test_exec_pack_u16_array(self):
        vm = apx.VM()
        data = bytearray(8)
        vm.init_pack_prog(value=[0x0A,0x1234,65535,22], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u16, [4])
        self.assertEqual(data, bytearray([0x0A,0, 0x34,0x12, 0xFF,0xFF, 22,0]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u16, [5])

    def test_exec_pack_u32_array(self):
        vm = apx.VM()
        data = bytearray(16)
        vm.init_pack_prog(value=[19, 12345678, 0x12345678, 900], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_u32, [4])
        self.assertEqual(data, bytearray([19,0,0,0, 0x4e,0x61,0xbc,0, 0x78,0x56,0x34,0x12, 0x84,0x03,0,0]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u32, [5])

    def test_exec_pack_s8_array(self):
        vm = apx.VM()
        data = bytearray(4)
        vm.init_pack_prog(value=[1,-23,18,-94], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s8, [4])
        self.assertEqual(data, bytearray([1, 0xe9, 18, 0xa2]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u8, [5])

    def test_exec_pack_s16_array(self):
        vm = apx.VM()
        data = bytearray(6)
        vm.init_pack_prog(value=[-918, 600, 42], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s16, [3])
        self.assertEqual(data, bytearray([0x6a,0xfc, 0x58,0x02, 42,0]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u8, [4])

    def test_exec_pack_s32_array(self):
        vm = apx.VM()
        data = bytearray(8)
        vm.init_pack_prog(value=[-100000, 100000], data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_s32, [2])
        self.assertEqual(data, bytearray([0x60,0x79,0xfe,0xff, 0xa0, 0x86,0x01,0x00]))
        with self.assertRaises(ValueError) as context:
            vm.exec_instruction(vm.exec_pack_u8, [3])

    def test_exec_pack_str(self):
        vm = apx.VM()
        data = bytearray(8)
        vm.init_pack_prog(value='Hello', data_len=len(data), data=data, data_offset=0)
        vm.exec_instruction(vm.exec_pack_str, [6])
        self.assertEqual(data, bytearray('Hello\0\0\0'.encode('utf-8')))

if __name__ == '__main__':
    unittest.main()
