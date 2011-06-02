#!/usr/bin/env python
import unittest

import vlc_rc


class FactoryTestCase(unittest.TestCase):
    def test_telnet(self):
        from vlc_rc.interfaces.telnet import Interface
        iface = vlc_rc.interface(vlc_rc.INTERFACE_TELNET)
        self.assertEqual(Interface, iface)

    def test_invalid(self):
        self.assertRaises(vlc_rc.interfaces.InvalidInterfaceException,
                          vlc_rc.interface, 'telephaty')


class TelnetTestCase(unittest.TestCase):
    class MyTelnet(object):
        def __init__(self, *args, **kwargs):
            self.open = True
            self.logged_in = False
            self.password = 'peace'
            self.buffer = 'Password:'

        def close(self):
            self.open = False

        def write(self, string):
            string = string.strip()
            if not self.logged_in:
                data = self.authenticate(string)
            else:
                data = self.execute(string)
            self.buffer += data

        def read_until(self, string, *args, **kwargs):
            pos = self.buffer.index(string)
            read = self.buffer[0:pos + len(string)]
            self.buffer = self.buffer[pos + len(string):]
            return read

        def expect(self, expects, *args, **kwargs):
            string = None
            for string in expects:
                try:
                    string = self.read_until(string)
                except ValueError:
                    pass
                else:
                    break
            if string:
                return (expects.index(string), string, string)
            raise ValueError

        def read_some(self, *args, **kwargs):
            read = self.buffer
            self.buffer = ''
            return read

        def authenticate(self, password):
            if password == self.password:
                self.logged_in = True
                return vlc_rc.interfaces.telnet.Interface.WELCOME_STRING
            else:
                return vlc_rc.interfaces.telnet.Interface.WRONG_PASSWORD

        def execute(self, string):
            return ''

    def setUp(self):
        vlc_rc.interfaces.telnet.telnetlib.Telnet = self.MyTelnet
        self.iface = vlc_rc.interfaces.telnet.Interface(None, None)

    def test_connect_wrong_passwd(self):
        self.assertRaises(vlc_rc.interfaces.telnet.InvalidPasswordException,
                          self.iface.connect, 'emotion')

    def test_connect_successful(self):
        self.iface.connect(password='peace')


if __name__ == '__main__':
    unittest.main()
