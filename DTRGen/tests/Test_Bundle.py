import unittest

from DTRGen import Bundle


class TestBundle(unittest.TestCase):
    def test_single_bundle_item(self):
        expected = '"Order 1234","material code","product code",1,"special print data","","","","","","","","bformat 1",""'
        bundle_item = Bundle.BundleItem('Order 1234', 'material code', 'product code', 1, user1='special print data',
                                        bundle_format='bformat 1')
        self.assertEqual(str(bundle_item), expected)

    def test_single_bundle_item_all(self):
        expected = '"Order 1234","material code","product code",0,"","","","","","","","","","","customer name","","","","","","","","","","","",01/01/01,"",F'
        bundle_item_all = Bundle.BundleItemAll('Order 1234', 'material code', 'product code', 0,
                                               customer_name='customer name', required_date='01/01/01', hold=False)
        self.assertEqual(str(bundle_item_all), expected)

    def test_all_bundle(self):
        bundle_items = Bundle.BundleItems()
        expected = '"Order 1234","material code","product code",1,"special print data","","","","","","","","bformat 1",""\n' \
                   '"Order 1234","material code","product code",2,"different print data","","","","","","","","bformat 1",""\n' \
                   '"Order 1234","material code","product code",0,"","","","","","","","","","","customer name","","","","","","","","","","","",01/01/01,"",F\n' \
                   '"Order 5678","material code","product code",0,"","","","","","","","","","","customer name 2","","","","","","","","","","","",01/04/01,"",F'
        bundle_item = Bundle.BundleItem('Order 1234', 'material code', 'product code', 1, 'special print data',
                                        bundle_format='bformat 1')
        bundle_items.append(bundle_item)
        bundle_item = Bundle.BundleItem('Order 1234', 'material code', 'product code', 2, 'different print data', bundle_format='bformat 1')
        bundle_items.append(bundle_item)
        bundle_item = Bundle.BundleItemAll('Order 1234', 'material code', 'product code', 0, customer_name='customer name', required_date='01/01/01',hold=False)
        bundle_items.append(bundle_item)
        bundle_item = Bundle.BundleItemAll('Order 5678', 'material code', 'product code', 0, customer_name='customer name 2', required_date='01/04/01', hold=False)
        bundle_items.append(bundle_item)
        self.assertEqual(str(bundle_items), expected)
