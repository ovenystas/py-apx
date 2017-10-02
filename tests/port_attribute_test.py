import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestPortAttribute(unittest.TestCase):

   def test_integer_init_value(self):
      attr = apx.base.PortAttribute('=0')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'integer', 'value': 0})
      attr = apx.base.PortAttribute('=255')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'integer', 'value': 255})
      attr = apx.base.PortAttribute('={3,3,7}')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'record', 'elements': [
                                       {'type': 'integer', 'value': 3},
                                       {'type': 'integer', 'value': 3},
                                       {'type': 'integer', 'value': 7}]
                                       })

   def test_integer_init_value(self):
      attr = apx.base.PortAttribute('="InitValue"')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'string', 'value': 'InitValue'})
      attr = apx.base.PortAttribute('=""')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'string', 'value': ''})
      attr = apx.base.PortAttribute('={"a","b","", "c"}')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue, {'type':'record', 'elements': [
                                       {'type': 'string', 'value': 'a'},
                                       {'type': 'string', 'value': 'b'},
                                       {'type': 'string', 'value': ''},
                                       {'type': 'string', 'value': 'c'}]
                                       })


if __name__ == '__main__':
    unittest.main()