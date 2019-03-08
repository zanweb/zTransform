import unittest

from DTRGen import Part


class TestPart(unittest.TestCase):
    def test_single_part(self):
        part = Part.Part("Part 5678", 2, 0.0, False, 4)
        expected = '"Part 5678",,"",4,2,0.000,F,"",,'
        self.assertEqual(str(part), expected)

    def test_parts(self):
        parts = Part.Parts()
        expected = 'UNITS=.39370078\n' \
                   '"Part 1234",,"",1,0,12.000,T,"",,\n' \
                   '"Part 1234",,"",1,4,24.000,T,"",,\n' \
                   '"Part 1234",,"",1,5,10.000,T,"",,\n' \
                   '"Part 5678",,"",4,2,0.000,F,"",,'
        part = Part.Part("Part 1234", 0, 12.0, True, 1)
        parts.append(part)
        part = Part.Part("Part 1234", 4, 24.0, True, 1)
        parts.append(part)
        part = Part.Part("Part 1234", 5, 10.0, True, 1)
        parts.append(part)
        part = Part.Part("Part 5678", 2, 0.0, False, 4)
        parts.append(part)
        self.assertEqual(str(parts), expected)
        parts.save_as("test_part.PRT")

    def test_part_shape(self):
        expected = '"PD","Part 1234",,"pg-1",,"S","sp-1",100.0,50.0,100.0,"LE",0.0,"CP"'
        part_shape = Part.PartShape("Part 1234", "pg-1", "S", "sp-1", 100.0, 50.0, "LE", 100.0, "CP", 0.0)
        self.assertEqual(str(part_shape), expected)


if __name__ == '__main__':
    unittest.main()
