import unittest

from DTRGen import Order


class TestOrder(unittest.TestCase):
    def test_single_cutitem(self):
        cut_item = Order.CutItem('Order 1234', 1, 10, 60.0, 'material code', 'product code', 'R', 'ABC-123', "C")
        expected = '"Order 1234",1,10,60.000,"material code","","product code","","R","","","","ABC-123","C","",,"","",,,"","","","","","",""'
        self.assertEqual(str(cut_item), expected)

    def test_cut_list(self):
        cut_list = Order.CutList()
        expected = 'UNITS=.39370078\n' \
                   '"Order 1234",1,10,60.000,"material code","","product code","","R","","","","ABC-123","C","",,"","",,,"","","","","","",""\n' \
                   '"Order 1234",2,5,120.000,"material code","","product code","","R","","","","ABC-124","C","",,"","",,,"","","","","","",""\n' \
                   '"Order 5678",1,100,24.875,"material code","","product code","","R","","","","ABC-123","C","",,"","",,,"","","","","","",""'
        cut_item = Order.CutItem('Order 1234', 1, 10, 60.0, 'material code', 'product code', 'R', 'ABC-123', "C")
        cut_list.append(cut_item)
        cut_item = Order.CutItem('Order 1234', 2, 5, 120.0, "material code", "product code", "R", "ABC-124", "C")
        cut_list.append(cut_item)
        cut_item = Order.CutItem('Order 5678', 1, 100, 24.875, 'material code', 'product code', 'R', 'ABC-123', 'C')
        cut_list.append(cut_item)
        self.assertEqual(str(cut_list), expected)
        cut_list.save_as('test_order.ORD')


if __name__ == '__main__':
    unittest.main()
