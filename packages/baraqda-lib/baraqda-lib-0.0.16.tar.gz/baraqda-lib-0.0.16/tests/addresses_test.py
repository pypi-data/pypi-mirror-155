import unittest
import os
from baraqdalib.addresses import Addresses


class AddressesTestCase(unittest.TestCase):
    def test_sym(self):
        os.chdir('../')
        a = Addresses()
        self.assertEqual([a._get_sym_city('Piorunów'), a._get_sym_city('Regut'), a._get_sym_city('Tłuste'), a._get_sym_city('Brzozówka'),
                          a._get_sym_city('Siemierz Górny'), a._get_sym_city('Horyszów-Nowa Kolonia')],
                         ['307', '1063', '2536', '1146', '896829', '898030'])


if __name__ == '__main__':
    unittest.main()
