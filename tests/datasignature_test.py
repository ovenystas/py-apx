import os, sys, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestDataSignature(unittest.TestCase):
    
    def test_create_init_data_u8(self):
        dsg = apx.base.DataSignature('C')
        
        attr = apx.base.PortAttribute('=0')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x00', bytes(data))
        
        attr = apx.base.PortAttribute('=0x12')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x12', bytes(data))
        
        attr = apx.base.PortAttribute('=255')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF', bytes(data))
        
        attr = apx.base.PortAttribute('=0xFF')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\xFF', bytes(data))
    
    def test_create_init_data_u16(self):
        dsg = apx.base.DataSignature('S')
        
        attr = apx.base.PortAttribute('=0')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x00\x00', bytes(data))
        
        attr = apx.base.PortAttribute('=0x1234')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x34\x12', bytes(data))
        
        attr = apx.base.PortAttribute('=65535')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF\xFF', bytes(data))

    def test_create_init_data_u32(self):
        dsg = apx.base.DataSignature('L')
        
        attr = apx.base.PortAttribute('=0')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x00\x00\x00\x00', bytes(data))
        
        attr = apx.base.PortAttribute('=0x12345678')
        data = dsg.createInitData(attr.initValue)        
        self.assertEqual(b'\x78\x56\x34\x12', bytes(data))
        
        attr = apx.base.PortAttribute('=0xFFFFFFFF')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF\xFF\xFF\xFF', bytes(data))

    def test_create_init_data_record(self):
        dsg = apx.base.DataSignature('{"first"C"second"S"third"L}')
        
        attr = apx.base.PortAttribute('={0,0,0}')
        data = dsg.createInitData(attr.initValue)
        (first, second, third) = (b'\x00', b'\x00\x00', b'\x00\x00\x00\x00')        
        self.assertEqual(first+second+third, bytes(data))

        attr = apx.base.PortAttribute('={0x11,0x22,0x33}')
        data = dsg.createInitData(attr.initValue)
        (first, second, third) = (b'\x11', b'\x22\x00', b'\x33\x00\x00\x00')
        self.assertEqual(first+second+third, bytes(data))

        attr = apx.base.PortAttribute('={0x01,0x1234,0x5678}')
        data = dsg.createInitData(attr.initValue)
        (first, second, third) = (b'\x01', b'\x34\x12', b'\x78\x56\x00\x00')
        self.assertEqual(first+second+third, bytes(data))

        attr = apx.base.PortAttribute('={0xFF,0xFFFF,0xFFFFFFFF}')
        data = dsg.createInitData(attr.initValue)
        (first, second, third) = (b'\xFF', b'\xFF\xFF', b'\xFF\xFF\xFF\xFF')
        self.assertEqual(first+second+third, bytes(data))
    
    def test_create_init_data_string(self):
        dsg = apx.base.DataSignature('a[6]')
        
        attr = apx.base.PortAttribute('=""')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x00\x00\x00\x00\x00\x00', bytes(data))

        attr = apx.base.PortAttribute('="Hello"')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'Hello\x00', bytes(data))
        
        attr = apx.base.PortAttribute('="HelloWorld"')
        old, capture = sys.stderr, io.StringIO()
        sys.stderr=capture
        data = dsg.createInitData(attr.initValue)
        sys.stderr = old
        self.assertEqual(capture.getvalue(), 'Warning: init value "HelloWorld" will be truncated to 6 bytes\n')
        self.assertEqual(b'HelloW', bytes(data))

        attr = apx.base.PortAttribute('="AaA"')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'AaA\x00\x00\x00', bytes(data))

    def test_create_init_data_arrayU8(self):
        dsg = apx.base.DataSignature('C[2]')
        
        attr = apx.base.PortAttribute('={1,2}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x01\x02', bytes(data))

        attr = apx.base.PortAttribute('={0,0}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x00\x00', bytes(data))

        attr = apx.base.PortAttribute('={0xFF, 0xFF}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF\xFF', bytes(data))

    def test_create_init_data_arrayU16(self):
        dsg = apx.base.DataSignature('S[3]')
        
        attr = apx.base.PortAttribute('={0x100,0x1234,0x60}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x00\x01\x34\x12\x60\x00', bytes(data))

        attr = apx.base.PortAttribute('={0,0,0}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x00\x00\x00\x00\x00\x00', bytes(data))

        attr = apx.base.PortAttribute('={0xFFFF, 0xFFFF, 0xFFFF}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF\xFF\xFF\xFF\xFF\xFF', bytes(data))

    def test_create_init_data_arrayU32(self):
        dsg = apx.base.DataSignature('L[2]')
        
        attr = apx.base.PortAttribute('={0x12345678, 0x630001}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x78\x56\x34\x12\x01\x00\x63\x00', bytes(data))

        attr = apx.base.PortAttribute('={0,0}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\x00\x00\x00\x00\x00\x00\x00\x00', bytes(data))

        attr = apx.base.PortAttribute('={0xFFFFFFFF, 0xFFFFFFFF}')
        data = dsg.createInitData(attr.initValue)
        self.assertEqual(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF', bytes(data))
        
if __name__ == '__main__':
    unittest.main()