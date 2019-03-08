import unittest

from DTRGen import Product


class TestProduct(unittest.TestCase):
    def test_single_product(self):
        expected = '"A",1,"Product Code","Roll Formed Part",12.125,"","",,F,F,1.500,"",12,80,225'
        product_item = Product.Product('A', 1, 'Product Code', 'Roll Formed Part', 12.125, calculate_length=False,
                                       hole_count=False, leg_height=1.5, coil_change_minutes=12.0,
                                       tooling_change_minutes=80.0, feet_per_minute=225)
        self.assertEqual(str(product_item), expected)

    def test_products(self):
        product_list = Product.Products()
        expected = '"A",1,"Product Code","Roll Formed Part",12.125,"","",,F,F,1.500,"",12,80,225\n' \
                   '"A",2,"Product Code","Roll Formed Part",12.125,"","",,F,F,1.500,"",12,25,225'
        product_item = Product.Product('A', 1, 'Product Code', 'Roll Formed Part', 12.125, calculate_length=False,
                                       hole_count=False, leg_height=1.5, coil_change_minutes=12.0,
                                       tooling_change_minutes=80.0, feet_per_minute=225)
        product_list.append(product_item)
        product_item = Product.Product('A', 2, 'Product Code', 'Roll Formed Part', 12.125, calculate_length=False,
                                       hole_count=False, leg_height=1.5, coil_change_minutes=12.0,
                                       tooling_change_minutes=25., feet_per_minute=225)
        product_list.append(product_item)
        self.assertEqual(str(product_list), expected)
