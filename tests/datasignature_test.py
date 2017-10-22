import os, sys, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestDataSignatureParsing(unittest.TestCase):
    
    def test_uint8(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('C')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertIsNone(dataElement.arrayLen)
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,1)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 1)
        self.assertIsNone(dataElement.arrayLen)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,255)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 255)
        self.assertFalse(dataElement.isArray)
        self.assertIsNone(dataElement.arrayLen)

    def test_uint8_array(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('C[8]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 8)
        
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,1)[4]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 1)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 4)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,255)[10]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 255)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 10)
        
    def test_uint8_errors(self):
        with self.assertRaises(apx.ParseError):
            (dataElement, remain) = apx.DataSignature.parseDataSignature('C[8')

        with self.assertRaises(apx.ParseError):
            (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,1')
        
        with self.assertRaises(apx.ParseError):
            (dataElement, remain) = apx.DataSignature.parseDataSignature('C(0,1)[8')
        
    def test_uint16(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('S')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertFalse(dataElement.isArray)
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('S(0,400)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 400)
        self.assertFalse(dataElement.isArray)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('S(0,65535)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 65535)
        self.assertFalse(dataElement.isArray)
    
    def test_uint16_array(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('S[8]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 8)
        
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('S(0,400)[4]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 400)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 4)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('S(0,65535)[10]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT16_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 65535)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 10)        

    def test_uint32(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('L')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertFalse(dataElement.isArray)
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('L(0,100000)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 100000)
        self.assertFalse(dataElement.isArray)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('L(0,4294967295)')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 4294967295)
        self.assertFalse(dataElement.isArray)
    
    def test_uint32_array(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('L[8]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertIsNone(dataElement.minVal)
        self.assertIsNone(dataElement.maxVal)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 8)
        
        
        (dataElement, remain) = apx.DataSignature.parseDataSignature('L(0,1000000)[4]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 1000000)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 4)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('L(0,4294967295)[10]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.UINT32_TYPE_CODE)
        self.assertEqual(dataElement.minVal, 0)
        self.assertEqual(dataElement.maxVal, 4294967295)
        self.assertTrue(dataElement.isArray)
        self.assertEqual(dataElement.arrayLen, 10)
    
    def test_record_simple(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('{"Hours"C"Minutes"C"Seconds"C}')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.RECORD_TYPE_CODE)
        self.assertEqual(len(dataElement.elements), 3)
        (child1, child2, child3) = dataElement.elements[:]
        self.assertEqual(child1.name, "Hours")
        self.assertEqual(child1.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(child2.name, "Minutes")
        self.assertEqual(child2.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(child3.name, "Seconds")
        self.assertEqual(child3.typeCode, apx.UINT8_TYPE_CODE)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('{"Hours"C(0,23)"Minutes"C(0,59)"Seconds"C(0,59)}')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.RECORD_TYPE_CODE)
        self.assertEqual(len(dataElement.elements), 3)
        (child1, child2, child3) = dataElement.elements[:]
        self.assertEqual(child1.name, "Hours")
        self.assertEqual(child1.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(child1.minVal, 0)
        self.assertEqual(child1.maxVal, 23)
        self.assertEqual(child2.name, "Minutes")
        self.assertEqual(child2.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(child2.minVal, 0)
        self.assertEqual(child2.maxVal, 59)
        self.assertEqual(child3.name, "Seconds")
        self.assertEqual(child3.typeCode, apx.UINT8_TYPE_CODE)
        self.assertEqual(child3.minVal, 0)
        self.assertEqual(child3.maxVal, 59)
    
    def test_typeRef(self):
        (dataElement, remain) = apx.DataSignature.parseDataSignature('T[0]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.REFERENCE_TYPE_CODE)
        self.assertEqual(dataElement.typeReference, 0)

        (dataElement, remain) = apx.DataSignature.parseDataSignature('T["TypeName"]')
        self.assertIsInstance(dataElement, apx.DataElement)
        self.assertEqual(dataElement.typeCode, apx.REFERENCE_TYPE_CODE)
        self.assertEqual(dataElement.typeReference, "TypeName")

class TestDataSignatureInitValues(unittest.TestCase):
    
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