import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestVmPackState(unittest.TestCase):

    def test_pack_u8(self):
        st = apx.VmPackState(value=1)
        data = bytearray([0,0,0])
        data_offset = 0
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 1)
        self.assertEqual(data, bytearray([1,0,0]))
        st.value=0x12
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(data, bytearray([1,0x12,0]))
        st.value=255
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 3)
        self.assertEqual(data, bytearray([1,0x12,255]))

    def test_pack_u16(self):
        st = apx.VmPackState(value=0)
        data = bytearray([0,0])
        data_offset = st.pack_u16(data, 0)
        self.assertEqual(data_offset, apx.UINT16_LEN)
        self.assertEqual(data, bytearray([0x00, 0x00]))
        st.value=0x1234
        data_offset = st.pack_u16(data, 0)
        self.assertEqual(data_offset, apx.UINT16_LEN)
        self.assertEqual(data, bytearray([0x34, 0x12]))
        st.value=65535
        data_offset = st.pack_u16(data, 0)
        self.assertEqual(data_offset, apx.UINT16_LEN)
        self.assertEqual(data, bytearray([0xFF, 0xFF]))

    def test_pack_u32(self):
        st = apx.VmPackState(value=0)
        data = bytearray([0,0,0,0])
        data_offset = st.pack_u32(data, 0)
        self.assertEqual(data_offset, apx.UINT32_LEN)
        self.assertEqual(data, bytearray([0x00, 0x00, 0x00, 0x00]))
        st.value=0x12345678
        data_offset = st.pack_u32(data, 0)
        self.assertEqual(data_offset, apx.UINT32_LEN)
        self.assertEqual(data, bytearray([0x78, 0x56, 0x34, 0x12]))
        st.value=0xFFFFFFFF
        data_offset = st.pack_u32(data, 0)
        self.assertEqual(data_offset, apx.UINT32_LEN)
        self.assertEqual(data, bytearray([0xFF, 0xFF, 0xFF, 0xFF]))

    def test_pack_s8(self):
        st = apx.VmPackState(value=0)
        data = bytearray(1)
        data_offset = st.pack_s8(data, 0)
        self.assertEqual(data_offset, apx.UINT8_LEN)
        self.assertEqual(data, bytearray([0]))
        st.value=127
        data_offset = st.pack_s8(data, 0)
        self.assertEqual(data_offset, apx.UINT8_LEN)
        self.assertEqual(data, bytearray([127]))
        st.value=-1
        data_offset = st.pack_s8(data, 0)
        self.assertEqual(data_offset, apx.UINT8_LEN)
        self.assertEqual(data, bytearray([0xFF]))
        st.value=-128
        data_offset = st.pack_s8(data, 0)
        self.assertEqual(data_offset,  apx.UINT8_LEN)
        self.assertEqual(data, bytearray([0x80]))

    def test_pack_s16(self):
        st = apx.VmPackState(value=0)
        data = bytearray(2)
        data_offset = st.pack_s16(data, 0)
        self.assertEqual(data_offset, apx.SINT16_LEN)
        self.assertEqual(data, bytearray([0, 0]))
        st.value=32767
        data_offset = st.pack_s16(data, 0)
        self.assertEqual(data_offset, apx.SINT16_LEN)
        self.assertEqual(data, bytearray([0xFF, 0x7F]))
        st.value=-1
        data_offset = st.pack_s16(data, 0)
        self.assertEqual(data_offset, apx.SINT16_LEN)
        self.assertEqual(data, bytearray([0xFF, 0xFF]))
        st.value=-32768
        data_offset = st.pack_s16(data, 0)
        self.assertEqual(data_offset, apx.SINT16_LEN)
        self.assertEqual(data, bytearray([0x00, 0x80]))

    def test_pack_s32(self):
        st = apx.VmPackState(value=0)
        data = bytearray(4)
        data_offset = st.pack_s32(data, 0)
        self.assertEqual(data_offset, apx.SINT32_LEN)
        self.assertEqual(data, bytearray([0, 0, 0, 0]))
        st.value=2147483647
        data_offset = st.pack_s32(data, 0)
        self.assertEqual(data_offset, apx.SINT32_LEN)
        self.assertEqual(data, bytearray([0xFF, 0xFF, 0xFF, 0x7F]))
        st.value=-1
        data_offset = st.pack_s32(data, 0)
        self.assertEqual(data_offset, apx.SINT32_LEN)
        self.assertEqual(data, bytearray([0xFF, 0xFF, 0xFF, 0xFF]))
        st.value=-2147483648
        data_offset = st.pack_s32(data, 0)
        self.assertEqual(data_offset, apx.SINT32_LEN)
        self.assertEqual(data, bytearray([0x00, 0x00, 0x00, 0x80]))

    def test_pack_u8_array(self):
        st = apx.VmPackState(value=[1,2,3])
        data = bytearray(3)
        data_offset = 0
        data_offset = st.pack_u8(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT8_LEN*len(st.value))
        self.assertEqual(data, bytearray([1, 2, 3]))

    def test_pack_u16_array(self):
        st = apx.VmPackState(value=[1,2,3])
        data = bytearray(6)
        data_offset = 0
        data_offset = st.pack_u16(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT16_LEN*len(st.value))
        self.assertEqual(data, bytearray([1, 0, 2, 0, 3, 0]))

    def test_pack_u32_array(self):
        st = apx.VmPackState(value=[1,2,3])
        data = bytearray(12)
        data_offset = 0
        data_offset = st.pack_u32(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT32_LEN*len(st.value))
        self.assertEqual(data, bytearray([1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0]))

    def test_pack_s8_array(self):
        st = apx.VmPackState(value=[-1,-2,-3])
        data = bytearray(3)
        data_offset = 0
        data_offset = st.pack_s8(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT8_LEN*len(st.value))
        self.assertEqual(data, bytearray([0xFF, 0xFE, 0xFD]))

    def test_pack_s16_array(self):
        st = apx.VmPackState(value=[-1,-2,-3])
        data = bytearray(6)
        data_offset = 0
        data_offset = st.pack_s16(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT16_LEN*len(st.value))
        self.assertEqual(data, bytearray([0xFF, 0xFF, 0xFE, 0xFF, 0xFD, 0xFF]))

    def test_pack_s32_array(self):
        st = apx.VmPackState(value=[-1,-2,-3])
        data = bytearray(12)
        data_offset = 0
        data_offset = st.pack_s32(data, data_offset, len(st.value))
        self.assertEqual(data_offset, apx.UINT32_LEN*len(st.value))
        self.assertEqual(data, bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0xFF, 0xFF, 0xFF, 0xFD, 0xFF, 0xFF, 0xFF]))

    def test_pack_str_with_shorter_string_should_pad_with_zeros(self):
        data = bytearray(7)
        data_offset = 0
        st = apx.VmPackState(value='Select')
        data_offset = st.pack_str(data, data_offset, 7)
        self.assertEqual(data_offset, 7)
        self.assertEqual(data, bytearray('Select\0'.encode('utf-8')))

    def test_pack_str_which_fits_exactly_shall_not_pad_with_zeros(self):
        data = bytearray(7)
        data_offset = 0
        st = apx.VmPackState(value='Selects')
        data_offset = st.pack_str(data, data_offset, 7)
        self.assertEqual(data_offset, 7)
        self.assertEqual(data, bytearray('Selects'.encode('utf-8')))

    def test_pack_str_which_is_too_long_should_truncate_to_fit(self):
        data = bytearray(7)
        data_offset = 0
        st = apx.VmPackState(value='Selected')
        data_offset = st.pack_str(data, data_offset, 7)
        self.assertEqual(data_offset, 7)
        self.assertEqual(data, bytearray('Selecte'.encode('utf-8')))


    def test_pack_u8_to_record(self):
        st = apx.VmPackState(value={'a': 255, 'b': 7})
        data = bytearray([0,0])
        data_offset=0
        st.record_enter()
        st.record_select('a')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 1)
        self.assertEqual(data, bytearray([255,0]))
        st.record_select('b')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(data, bytearray([255,7]))

    def test_pack_array_of_records(self):
        st = apx.VmPackState(value=[
            {'a': 255, 'b': 7},
            {'a': 29, 'b': 4},
            {'a': 0, 'b': 200},
            ])
        data = bytearray(6)
        data_offset=0
        self.assertIsNone(st.array_index)
        st.array_enter()
        self.assertEqual(st.array_index, 0)
        self.assertEqual(len(st.stack), 0)
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {'a': 255, 'b': 7})
        st.record_select('a')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data, bytearray([255,0,0,0,0,0]))
        st.record_select('b')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(data, bytearray([255,7,0,0,0,0]))
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.array_index, 1)
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {'a': 29, 'b': 4})
        st.record_select('a')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data, bytearray([255,7,29,0,0,0]))
        st.record_select('b')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(data, bytearray([255,7,29,4,0,0]))
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.array_index, 2)
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {'a': 0, 'b': 200})
        st.record_select('a')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data, bytearray([255,7,29,4,0,0]))
        st.record_select('b')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 6)
        self.assertEqual(data, bytearray([255,7,29,4,0,200]))
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.array_index, 3)
        st.array_leave()
        self.assertIsNone(st.array_index)

    def test_pack_array_of_records_in_record(self):
        st = apx.VmPackState(value={'customers': [{'id': 1, 'amount': 2}, {'id': 2, 'amount': 10}],
                                    'priority': 4})
        data = bytearray(5)
        data_offset=0
        st.record_enter()
        st.record_select('customers')
        self.assertEqual(st.key, 'customers')
        self.assertEqual(len(st.stack), 0)
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        self.assertIsNone(st.key)
        st.record_enter()
        self.assertEqual(st.value, {'id': 1, 'amount': 2})
        st.record_select('id')
        data_offset = st.pack_u8(data, data_offset)
        st.record_select('amount')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data, bytearray([1,2,0,0,0]))
        st.record_leave()
        self.assertEqual(st.array_index, 1)
        st.record_enter()
        self.assertEqual(st.value, {'id': 2, 'amount': 10})
        st.record_select('id')
        data_offset = st.pack_u8(data, data_offset)
        st.record_select('amount')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data, bytearray([1,2,2,10,0]))
        st.record_leave()
        st.array_leave()
        self.assertEqual(len(st.stack), 0)
        st.record_select('priority')
        data_offset = st.pack_u8(data, data_offset)
        self.assertEqual(data_offset, 5)
        self.assertEqual(data, bytearray([1,2,2,10,4]))
        self.assertEqual(st.key, 'priority')
        st.record_leave()
        self.assertIsNone(st.key)

    def test_pack_array_inside_array(self):
        st = apx.VmPackState(value=[ [1,2], [3,4] ])
        data = bytearray(4)
        data_offset=0
        st.array_enter()
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        data_offset = st.pack_u8(data, data_offset, 2)
        self.assertEqual(data_offset, 2)
        self.assertEqual(data, bytearray([1,2,0,0]))
        st.array_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.array_index, 1)
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        data_offset = st.pack_u8(data, data_offset, 2)
        self.assertEqual(data_offset, 4)
        self.assertEqual(data, bytearray([1,2,3,4]))
        st.array_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.array_index, 2)
        st.array_leave()
        self.assertIsNone(st.array_index)

class TestVmUnpackState(unittest.TestCase):

    def test_record_enter(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        self.assertIsNone(st.key)
        st.record_enter()
        self.assertEqual(st.value, {})

    def test_record_select(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        self.assertIsNone(st.key)
        with self.assertRaises(RuntimeError) as context:
            st.record_select('name')
        self.assertEqual("record_select performed before record_enter", str(context.exception))
        st.record_enter()
        self.assertEqual(st.value, {})
        st.record_select('name')
        self.assertEqual(st.key, 'name')

    def test_record_leave(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        self.assertIsNone(st.key)
        st.record_enter()
        self.assertEqual(st.value, {})
        st.record_select('name')
        self.assertEqual(st.key, 'name')
        st.record_leave()
        self.assertIsNone(st.key)

    def test_unpack_u8(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([3,15])
        data_offset = 0
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 1)
        self.assertEqual(st.value,3)
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value,15)

    def test_unpack_u8_array(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([1,3,7,15,31])
        data_offset = 0
        data_offset = st.unpack_u8(data, data_offset, 5)
        self.assertEqual(data_offset, 5)
        self.assertEqual(st.value, [1,3,7,15,31])

    def test_unpack_u8_from_record(self):
        st = apx.VmUnpackState()
        data = bytearray([255, 7])
        data_offset=0
        st.record_enter()
        st.record_select('a')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 1)
        st.record_select('b')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, {'a': 255, 'b': 7})

    def test_unpack_array_of_records(self):
        st = apx.VmUnpackState()
        data = bytearray([255,7,29,4,0,200])
        data_offset=0
        self.assertIsNone(st.value)
        self.assertIsNone(st.array_index)
        st.array_enter()
        self.assertEqual(st.value, [])
        self.assertEqual(st.array_index, 0)
        self.assertEqual(len(st.stack), 0)
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {})
        st.record_select('a')
        data_offset = st.unpack_u8(data, data_offset)
        st.record_select('b')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, {'a': 255, 'b': 7})
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.value, [{'a': 255, 'b': 7}])
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {})
        st.record_select('a')
        data_offset = st.unpack_u8(data, data_offset)
        st.record_select('b')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, {'a': 29, 'b': 4})
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.value, [{'a': 255, 'b': 7}, {'a': 29, 'b': 4}])
        self.assertEqual(st.array_index, 2)
        st.record_enter()
        self.assertIsNone(st.array_index)
        self.assertEqual(len(st.stack), 1)
        self.assertEqual(st.value, {})
        st.record_select('a')
        data_offset = st.unpack_u8(data, data_offset)
        st.record_select('b')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 6)
        self.assertEqual(st.value, {'a': 0, 'b': 200})
        st.record_leave()
        self.assertEqual(len(st.stack), 0)
        self.assertEqual(st.value, [{'a': 255, 'b': 7}, {'a': 29, 'b': 4}, {'a': 0, 'b': 200}])
        self.assertEqual(st.array_index, 3)
        st.array_leave()
        self.assertIsNone(st.array_index)

    def test_unpack_array_of_records_in_record(self):
        st = apx.VmUnpackState()
        data = bytearray([1,2,2,10,4])
        data_offset=0
        st.record_enter()
        st.record_select('customers')
        self.assertEqual(st.key, 'customers')
        self.assertEqual(len(st.stack), 0)
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        self.assertIsNone(st.key)
        self.assertEqual(st.array_index, 0)
        st.record_enter()
        self.assertEqual(st.value, {})
        st.record_select('id')
        data_offset = st.unpack_u8(data, data_offset)
        st.record_select('amount')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(st.value, {'id': 1, 'amount': 2})
        st.record_leave()
        self.assertEqual(st.array_index, 1)
        st.record_enter()
        self.assertEqual(st.value, {})
        st.record_select('id')
        data_offset = st.unpack_u8(data, data_offset)
        st.record_select('amount')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(st.value, {'id': 2, 'amount': 10})
        st.record_leave()
        st.array_leave()
        self.assertEqual(len(st.stack), 0)
        st.record_select('priority')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 5)
        st.record_leave()
        self.assertIsNone(st.key)
        self.assertEqual(st.value, {'customers': [{'id': 1, 'amount': 2}, {'id': 2, 'amount': 10}],
                                    'priority': 4})

    def test_unpack_array_inside_array(self):
        st = apx.VmUnpackState()
        data = bytearray([1,2,3,4])
        data_offset=0
        st.array_enter()
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        data_offset = st.unpack_u8(data, data_offset, 2)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, [1,2])
        st.array_leave()
        self.assertEqual(st.array_index, 1)
        st.array_enter()
        self.assertEqual(len(st.stack), 1)
        data_offset = st.unpack_u8(data, data_offset, 2)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, [3,4])
        st.array_leave()
        self.assertEqual(st.array_index, 2)
        st.array_leave()
        self.assertIsNone(st.array_index)
        self.assertEqual(st.value, [[1,2], [3,4]])

    def test_unpack_u16(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0, 0x34,0x12, 0xFF,0xFF])
        data_offset = 0
        data_offset = st.unpack_u16(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, 0)
        data_offset = st.unpack_u16(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, 0x1234)
        data_offset = st.unpack_u16(data, data_offset)
        self.assertEqual(data_offset, 6)
        self.assertEqual(st.value, 65535)

    def test_unpack_u32(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0,0,0, 0x78,0x56,0x34,0x12, 0xFF,0xFF,0xFF,0xFF])
        data_offset = 0
        data_offset = st.unpack_u32(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, 0)
        data_offset = st.unpack_u32(data, data_offset)
        self.assertEqual(data_offset, 8)
        self.assertEqual(st.value, 0x12345678)
        data_offset = st.unpack_u32(data, data_offset)
        self.assertEqual(data_offset, 12)
        self.assertEqual(st.value, 0xFFFFFFFF)

    def test_unpack_s8(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0x80,0xFF,0,127])
        data_offset = 0
        data_offset = st.unpack_s8(data, data_offset)
        self.assertEqual(data_offset, 1)
        self.assertEqual(st.value, -128)
        data_offset = st.unpack_s8(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, -1)
        data_offset = st.unpack_s8(data, data_offset)
        self.assertEqual(data_offset, 3)
        self.assertEqual(st.value, 0)
        data_offset = st.unpack_s8(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, 127)

    def test_unpack_s16(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0x80, 0xFF,0xFF, 0,0, 0xFF,0x7F])
        data_offset = 0
        data_offset = st.unpack_s16(data, data_offset)
        self.assertEqual(data_offset, 2)
        self.assertEqual(st.value, -32768)
        data_offset = st.unpack_s16(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, -1)
        data_offset = st.unpack_s16(data, data_offset)
        self.assertEqual(data_offset, 6)
        self.assertEqual(st.value, 0)
        data_offset = st.unpack_s16(data, data_offset)
        self.assertEqual(data_offset, 8)
        self.assertEqual(st.value, 32767)

    def test_unpack_s32(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0,0,0x80, 0xFF,0xFF,0xFF,0xFF, 0,0,0,0, 0xFF,0xFF,0xFF,0x7F])
        data_offset = 0
        data_offset = st.unpack_s32(data, data_offset)
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, -2147483648)
        data_offset = st.unpack_s32(data, data_offset)
        self.assertEqual(data_offset, 8)
        self.assertEqual(st.value, -1)
        data_offset = st.unpack_s32(data, data_offset)
        self.assertEqual(data_offset, 12)
        self.assertEqual(st.value, 0)
        data_offset = st.unpack_s32(data, data_offset)
        self.assertEqual(data_offset, 16)
        self.assertEqual(st.value, 2147483647)

    def test_unpack_s8_array(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0x80,0xFF,0,127])
        data_offset = 0
        data_offset = st.unpack_s8(data, data_offset, 4)        
        self.assertEqual(data_offset, 4)
        self.assertEqual(st.value, [-128,-1,0,127])

    def test_unpack_s16_array(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0x80, 0xFF,0xFF, 0,0, 0xFF,0x7F])
        data_offset = 0
        data_offset = st.unpack_s16(data, data_offset, 4)
        self.assertEqual(data_offset, 8)
        self.assertEqual(st.value, [-32768, -1, 0, 32767])
        
    def test_unpack_s32(self):
        st = apx.VmUnpackState()
        self.assertIsNone(st.value)
        data = bytearray([0,0,0,0x80, 0xFF,0xFF,0xFF,0xFF, 0,0,0,0, 0xFF,0xFF,0xFF,0x7F])
        data_offset = 0
        data_offset = st.unpack_s32(data, data_offset, 4)
        self.assertEqual(data_offset, 16)
        self.assertEqual(st.value, [-2147483648, -1, 0, 2147483647])
    
    def test_unpack_str(self):
        st = apx.VmUnpackState()
        data = bytearray('Hello\0World\0\0\0'.encode('utf-8'))
        data_offset = 0
        data_offset = st.unpack_str(data, data_offset, 6)
        self.assertEqual(data_offset, 6)
        self.assertEqual(st.value, 'Hello')
        data_offset = st.unpack_str(data, data_offset, 5)
        self.assertEqual(data_offset, 11)
        self.assertEqual(st.value, 'World')
        data_offset = st.unpack_str(data, data_offset, 3)
        self.assertEqual(data_offset, 14)
        self.assertEqual(st.value, '')
    
    def test_unpack_str_in_record(self):
        st = apx.VmUnpackState()
        data = bytearray(bytes([14,0])+"Selection\0".encode('utf-8')+bytes([0]))
        data_offset = 0
        st.record_enter()
        st.record_select('Position')
        data_offset = st.unpack_u16(data, data_offset)
        self.assertEqual(data_offset, 2)
        st.record_select('Label')
        data_offset = st.unpack_str(data, data_offset, 10)
        self.assertEqual(data_offset, 12)
        st.record_select('Index')
        data_offset = st.unpack_u8(data, data_offset)
        self.assertEqual(data_offset, 13)
        st.record_leave()
        self.assertEqual(st.value, {'Position': 14, 'Label': 'Selection', 'Index': 0})

        

if __name__ == '__main__':
    unittest.main()