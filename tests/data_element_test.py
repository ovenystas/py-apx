import os, sys, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestDataSignature(unittest.TestCase):
    
    def test_create_empty(self):
        elem = apx.DataElement()
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.INVALID_TYPE_CODE)        
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)

    def test_create_u8(self):
        elem = apx.DataElement.UInt8(minVal=0, maxVal=3)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT8_TYPE_CODE)  
        self.assertEqual(elem.minVal, 0)
        self.assertEqual(elem.maxVal, 3)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)

    def test_create_u16(self):
        elem = apx.DataElement.UInt16(minVal=0, maxVal=10000)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT16_TYPE_CODE)  
        self.assertEqual(elem.minVal, 0)
        self.assertEqual(elem.maxVal, 10000)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)

    def test_create_u32(self):
        elem = apx.DataElement.UInt32()
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT32_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)
    
    def test_create_u8_array(self):
        elem = apx.DataElement.UInt8(minVal=0, maxVal=3, arrayLen=16)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT8_TYPE_CODE)  
        self.assertEqual(elem.minVal, 0)
        self.assertEqual(elem.maxVal, 3)
        self.assertEqual(elem.arrayLen, 16)
        self.assertIsNone(elem.elements)

    def test_create_u16_array(self):
        elem = apx.DataElement.UInt16(arrayLen = 20)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT16_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertEqual(elem.arrayLen, 20)
        self.assertIsNone(elem.elements)

    def test_create_u32_array(self):
        elem = apx.DataElement.UInt32(arrayLen = 4)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.UINT32_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertEqual(elem.arrayLen, 4)
        self.assertIsNone(elem.elements)
        
    def test_create_string(self):
        elem = apx.DataElement.String(arrayLen=20)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.STRING_TYPE_CODE)
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertEqual(elem.arrayLen, 20)
        self.assertIsNone(elem.elements)

    def test_create_s8(self):
        elem = apx.DataElement.SInt8(minVal=-3, maxVal=3)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT8_TYPE_CODE)  
        self.assertEqual(elem.minVal, -3)
        self.assertEqual(elem.maxVal, 3)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)

    def test_create_s16(self):
        elem = apx.DataElement.SInt16(minVal=-10000, maxVal=10000)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT16_TYPE_CODE)  
        self.assertEqual(elem.minVal, -10000)
        self.assertEqual(elem.maxVal, 10000)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)

    def test_create_s32(self):
        elem = apx.DataElement.SInt32()
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT32_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)
    
    def test_create_s8_array(self):
        elem = apx.DataElement.SInt8(minVal=-10, maxVal=10, arrayLen=16)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT8_TYPE_CODE)  
        self.assertEqual(elem.minVal, -10)
        self.assertEqual(elem.maxVal, 10)
        self.assertEqual(elem.arrayLen, 16)
        self.assertIsNone(elem.elements)

    def test_create_s16_array(self):
        elem = apx.DataElement.SInt16(arrayLen = 20)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT16_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertEqual(elem.arrayLen, 20)
        self.assertIsNone(elem.elements)

    def test_create_s32_array(self):
        elem = apx.DataElement.SInt32(arrayLen = 4)
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(elem.typeCode, apx.SINT32_TYPE_CODE)  
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertEqual(elem.arrayLen, 4)
        self.assertIsNone(elem.elements)

    def test_create_record(self):
        elem = apx.DataElement.Record()
        elem.append(apx.DataElement.String('Name', 20))
        elem.append(apx.DataElement.UInt32('UserId'))
        self.assertIsNone(elem.name)
        self.assertIsNone(elem.typeReference)
        self.assertEqual(len(elem.elements), 2)
        (child1,child2) = elem.elements[:]
        self.assertEqual(child1.name, "Name")
        self.assertEqual(child1.typeCode, apx.STRING_TYPE_CODE)
        self.assertEqual(child1.arrayLen, 20)
        self.assertEqual(child2.name, "UserId")
        self.assertEqual(child2.typeCode, apx.UINT32_TYPE_CODE)
        
    def test_create_typeref(self):
        dataType = apx.DataType('TestType_T', 'C(0,1)')
        elem = apx.DataElement.TypeReference(dataType)
        self.assertIsNone(elem.name)
        self.assertEqual(elem.typeCode, apx.REFERENCE_TYPE_CODE)
        self.assertIs(elem.typeReference, dataType)
        self.assertIsNone(elem.minVal)
        self.assertIsNone(elem.maxVal)
        self.assertIsNone(elem.arrayLen)
        self.assertIsNone(elem.elements)
        
        
if __name__ == '__main__':
    unittest.main()