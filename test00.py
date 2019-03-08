from CamGen import DataTransform
from LysaghtPurlin.Bundle import *
from LysaghtPurlin.Order import *
from LysaghtPurlin.Part import *

data = DataTransform.LysaghtDTRData()
reader = data.get_data()
writer = data.set_data()

part = Part('abc123', 8265, 2.4, 21, 'C200190', 'Material code')
part.add_hole(Hole('OF', 35.0, 158.0, 8.0))
part.add_hole(Hole('OF', 635.0, 158.0, 8.0))
part.add_hole(Hole('OF', 1235.0, 158.0, 8.0))
part.add_hole(Hole('OF', 1835.0, 158.0, 8.0))
part.add_hole(Hole('WEB', 2000.0, 115.0, 16.0))
part.add_hole(Hole('WEB', 2000.0, -115.0, 16.0))
part.add_hole(Hole('WEB', 2500.0, 115.0, 16.0))
part.add_hole(Hole('WEB', 2500.0, -115.0, 16.0))
part.add_hole(Hole('WEB', 3000.0, 0.0, 22.0))
part.add_hole(Hole('IF', 7000.0, 90.0, 14.0))
part.add_hole(Hole('IF', 7000.0, -90.0, 14.0))
part.sort_holes()
part.group_holes_by_y()
part.convert_to_dtr_holes()

order = Order('O123456', 'LKQ', 'product code 1')
batch = Batch(123456)
order.add_batch(batch)
bundle = Bundle(1)
batch.add_bundle(bundle)
bundle.add_part(part)

writer.write(order, 'd:\\')
# print(order)
