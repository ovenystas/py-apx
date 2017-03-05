import os, sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile

class TestRemoteFile(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_packHeader(self):      
      result = remotefile.packHeader(0,False)
      self.assertEqual( result, bytes([0,0]))
      result = remotefile.packHeader(0,True)
      self.assertEqual( result, bytes([0x40,0]))
      result = remotefile.packHeader(1234,True)
      self.assertEqual( result, bytes([0x44,0xD2]))
      result = remotefile.packHeader(16383,False)
      self.assertEqual( result, bytes([0x3F,0xFF]))
      result = remotefile.packHeader(16383,True)
      self.assertEqual( result, bytes([0x7F,0xFF]))
      result = remotefile.packHeader(16384,False)      
      self.assertEqual( result, bytes([0x80,0x00,0x40,0x00]))
      result = remotefile.packHeader(16384,True)
      self.assertEqual( result, bytes([0xC0,0x00,0x40,0x00]))
      result = remotefile.packHeader(1073741823,False)
      self.assertEqual( result, bytes([0xBF,0xFF,0xFF,0xFF]))
      result = remotefile.packHeader(1073741823,True)
      self.assertEqual( result, bytes([0xFF,0xFF,0xFF,0xFF]))
      with self.assertRaises(ValueError):
         remotefile.packHeader(1073741824,False)
         remotefile.packHeader(1073741824,True)

   def test_File(self):
      info = remotefile.File("test.txt",100)      
      self.assertEqual(info.name, "test.txt")
      self.assertEqual(info.length, 100)
      self.assertEqual(info.digestType, remotefile.RMF_DIGEST_TYPE_NONE)
      self.assertEqual(info.digestData, bytes([0]*32))


   def test_packFileInfo(self):
      file1 = remotefile.File("test.txt",100, address=10000)
      data = remotefile.packFileInfo(file1)
      self.assertIsInstance(data, bytes)
      self.assertEqual(len(data), 48+len(file1.name))
      self.assertEqual(data[0:4],b'\x03\x00\x00\x00')
      self.assertEqual(data[4:8],b'\x10\x27\x00\x00')
      self.assertEqual(data[8:12],b'\x64\x00\x00\x00')
      self.assertEqual(data[12:16],b'\x00\x00\x00\x00')
      self.assertEqual(data[16:48],bytes([0]*32))
      self.assertEqual(data[48:],b"test.txt")
      
      file2 = remotefile.unpackFileInfo(data)
      self.assertEqual(file1.name, file2.name)
      self.assertEqual(file1.address, file2.address)
      self.assertEqual(file1.length, file2.length)
      self.assertEqual(file1.fileType, file2.fileType)
      self.assertEqual(file1.digestType, file2.digestType)
      self.assertEqual(file1.digestData, file2.digestData)
      

   def test_readLine(self):
      buf=b"RMF/1.0\nNumHeader-Format:32\n\n"
      iNext=remotefile.readLine(buf,0,len(buf))
      self.assertEqual(iNext, 7)
      iNext=remotefile.readLine(buf,8,len(buf))
      self.assertEqual(iNext, 27)
      iNext=remotefile.readLine(buf,28,len(buf))
      self.assertEqual(iNext, 28)
   
   def test_packFileOpen(self):
      data = remotefile.packFileOpen(0x12345678)
      self.assertEqual(len(data), 8)
   
if __name__ == '__main__':
    unittest.main()