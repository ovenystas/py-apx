import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import time
import shutil

class TestApxGenerator(unittest.TestCase):
    
    def test_ctypename(self):
        dsg = apx.DataSignature('C')
        self.assertEqual(dsg.ctypename(),'uint8')
        dsg = apx.DataSignature('c')
        self.assertEqual(dsg.ctypename(),'sint8')
        dsg = apx.DataSignature('S')
        self.assertEqual(dsg.ctypename(),'uint16')
        dsg = apx.DataSignature('s')
        self.assertEqual(dsg.ctypename(),'sint16')
        dsg = apx.DataSignature('L')
        self.assertEqual(dsg.ctypename(),'uint32')
        dsg = apx.DataSignature('l')
        self.assertEqual(dsg.ctypename(),'sint32')
    
    def test_code_generator(self):
        node = apx.Node("Test")
        node.append(apx.RequirePort('U8Port','C','=255'))
        node.append(apx.RequirePort('U8ARPort','C[3]','={255, 255, 255}'))
        output_dir = 'derived'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        apx.NodeGenerator().generate(output_dir, node)
        #shutil.rmtree(output_dir)

if __name__ == '__main__':
    unittest.main()
