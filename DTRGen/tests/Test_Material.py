import unittest

from DTRGen import Material

class TestMaterial(unittest.TestCase):
    def test_single_material(self):
        expected = '"A","Material Code",18,0.0478,9.000,"","Steel","","18 Ga Steel",0.96,1.06,,1000'
        material = Material.Material('A', 'Material Code', 18, 0.0478, 9.000, material_type='Steel', material_description='18 Ga Steel', pound_per_foot=0.96, cost_per_pound=1.06, recorder_point=1000)
        self.assertEqual(str(material), expected)
    def test_material(self):
        materials = Material.Materials()
        expected = '"A","Material Code",18,0.0478,9.000,"","Steel","","18 Ga Steel",0.96,1.06,,1000\n' \
                    '"D","Material Code 6",,,,"","","","",,,,'
        material = Material.Material('A', 'Material Code', 18, 0.0478, 9.000, material_type='Steel', material_description='18 Ga Steel', pound_per_foot=0.96, cost_per_pound=1.06, recorder_point=1000)
        materials.append(material)
        material = Material.Material('D', 'Material Code 6')
        materials.append(material)
        self.assertEqual(str(materials), expected)

