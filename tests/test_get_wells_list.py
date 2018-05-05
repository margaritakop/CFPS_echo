from unittest import TestCase


class TestGet_wells_list(TestCase):
    def test_get_wells_list(self):
        from src.generate_protocol import get_wells_list
        wells_list = get_wells_list({'start_destwell':'P22'})
        self.assertEqual(wells_list, ['P22', 'P23', 'P24'])
        wells_list = get_wells_list({'start_destwell':'P01'})[0:3]
        self.assertEqual(wells_list, ['P01','P02','P03'])
        wells_list = get_wells_list({'start_destwell':'P1'})[0:3]
        self.assertEqual(wells_list, ['P01','P02','P03'])

        with self.assertRaises(SystemExit):
            get_wells_list({'start_destwell':'Q1'})
        with self.assertRaises(SystemExit):
            get_wells_list({'start_destwell':'A25'})