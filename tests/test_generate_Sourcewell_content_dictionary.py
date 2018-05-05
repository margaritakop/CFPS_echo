from unittest import TestCase
import generate_protocol
import collections

class TestGenerate_Sourcewell_content_dictionary(TestCase):
    def test_generate_Sourcewell_content_dictionary(self):
        result_dict = generate_protocol.generate_Sourcewell_content_dictionary({'ID_01':{'A':10000}}, {'ID_01': ['A01', 'A02', 'A03', 'A04' ]})
        self.assertEqual(result_dict, collections.OrderedDict([('A', 60000)]))
        with self.assertRaises(SystemExit):
            generate_protocol.generate_Sourcewell_content_dictionary({'ID_01':{'A':20000}}, {'ID_01': ['A01', 'A02', 'A03', 'A04' ]})
