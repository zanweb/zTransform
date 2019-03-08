import unittest

from DTRGen import Customer

class TestCustomer(unittest.TestCase):
    def test_single_customer(self):
        expected = '"A",124,"Bob\'s Buildings","12180 Prichard Farm Road","","Maryland Heights","MO","63043","US","Deliver to side door.",500,"+1 (314) 344-3144",""'
        customer_item = Customer.Customer('A', 124, "Bob's Buildings", '12180 Prichard Farm Road', customer_city='Maryland Heights', customer_state='MO', customer_zip='63043', customer_country='US', customer_instructions='Deliver to side door.', max_bundle_weight=500, delivery_phone='+1 (314) 344-3144')
        self.assertEqual(str(customer_item), expected)

    def test_customers(self):
        customer_list = Customer.Customers()
        expected = '"A",124,"Bob\'s Buildings","12180 Prichard Farm Road","","Maryland Heights","MO","63043","US","Deliver to side door.",500,"+1 (314) 344-3144",""\n' \
                    '"C",50,"","","","","","","","Do not deliver to front!",,"",""'
        customer_item = Customer.Customer('A', 124, "Bob's Buildings", '12180 Prichard Farm Road', customer_city='Maryland Heights', customer_state='MO', customer_zip='63043', customer_country='US', customer_instructions='Deliver to side door.', max_bundle_weight=500, delivery_phone='+1 (314) 344-3144')
        customer_list.append(customer_item)
        customer_item = Customer.Customer('C', 50, customer_instructions='Do not deliver to front!')
        customer_list.append(customer_item)

        self.assertEqual(str(customer_list), expected)
