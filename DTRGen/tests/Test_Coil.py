import unittest

from DTRGen import Coil


class TestCoil(unittest.TestCase):
    def test_single_coil(self):
        coil_item = Coil.CoilItem('A', 'Coil 1234', date_in='01/01/01', starting_length=2500, status='I',
                                  vendor_name='steel vendor', material_code='material code', coil_material_type='steel',
                                  cost_per_pound=1.25, weight=1800, heat_number='ABC123', vendor_code='SV',
                                  purchase_order='PO5678')
        expected = '"A","Coil 1234","","01/01/01","","2500","","I","steel vendor","material code","steel","1.25","","","","1800","ABC123","SV","PO5678",""'
        self.assertEqual(str(coil_item), expected)

    def test_coils(self):
        coil_items = Coil.CoilItems()
        expected = '"A","Coil 1234","","01/01/01","","2500","","I","steel vendor","material code","steel","1.25","","","","1800","ABC123","SV","PO5678",""\n' \
                   '"A","Coil 5678","","01/01/01","","3600","","I","steel vendor","material code 2","aluminum","0.80","","","","1100","DEF456","SV","PO5678",""'
        coil_item = Coil.CoilItem('A', 'Coil 1234', date_in='01/01/01', starting_length=2500, status='I',
                                  vendor_name='steel vendor', material_code='material code', coil_material_type='steel',
                                  cost_per_pound=1.25, weight=1800, heat_number='ABC123', vendor_code='SV',
                                  purchase_order='PO5678')
        coil_items.append(coil_item)
        coil_item = Coil.CoilItem('A', 'Coil 5678', date_in='01/01/01', starting_length=3600, status='I',
                                  vendor_name='steel vendor', material_code='material code 2', coil_material_type='aluminum',
                                  cost_per_pound=0.80, weight=1100, heat_number='DEF456', vendor_code='SV',
                                  purchase_order='PO5678')
        coil_items.append(coil_item)

        self.assertEqual(str(coil_items), expected)
