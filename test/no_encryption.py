'''
/********************/
/*    unittest      */
/* no_encryption.py */
/*   Version 1.0    */
/*    2025/03/23    */
/********************/
'''
import json
import os
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from encryptlib import NoEncryption  # noqa

with open('config.json', 'r') as f:
    cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))


class TestNoEncryption(unittest.TestCase):
    def setUp(self):
        self.enc = NoEncryption(cfg.NoEncryption)

    def test_protocol(self):
        EXPECTED = 'No Protocol'
        COMPUTED = self.enc.protocol
        self.assertEqual(COMPUTED, EXPECTED)

    def test_generate_key(self):
        self.enc._generateKey(seed=8033)
        self.assertEqual(self.enc.key_bits[0:16], '0110011100111001')
        self.assertEqual(self.enc.key_bits[1024:1048],
                         '001011000001110101100011')

    def test_key_valid(self):
        self.assertFalse(self.enc.isKeyValid())
        self.enc._generateKey()
        self.assertTrue(self.enc.isKeyValid())

    def test_encode_message(self):
        self.enc._generateKey(seed=8033)
        EXPECTED = 'This is a test message'
        message = self.enc.encrypt(EXPECTED)
        message_bits = ''.join(format(byte, '08b') for byte in message)
        self.assertEqual(message_bits[0:16], '0011001101010001')
        COMPUTED = self.enc.decrypt(message)
        self.assertEqual(COMPUTED, EXPECTED)


if __name__ == '__main__':
    unittest.main()
