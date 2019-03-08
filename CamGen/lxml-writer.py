from lxml import etree

if __name__ == '__main__':
    # root = etree.Element("root")

    root = etree.Element("root", nsmap={'xsi': 'http://b.c/d'})

    root.set("xsiinteresting", "totally")
    child1 = etree.SubElement(root, "child1")
    child1.set("interesting", "totally")
    child1.text = "TEXT"

    child2 = etree.SubElement(root, "child2")
    child2.set("name", "myattr1")
    child2.set("auto", "myattr2")

    child3 = etree.SubElement(child2, "child3")
    child3.text = "TEXT"
    child4 = etree.SubElement(child2, "child4")
    child4.text = "TEXT"
    child5 = etree.SubElement(child2, "child5")

    child6 = etree.SubElement(child5, "child6")
    child6.text = "TEXT"
    child7 = etree.SubElement(child5, "child7")
    child7.text = "TEXT"
    # root.append( etree.Element("child1") )
    # root.append( etree.Element("child1", interesting="totally"))
    # child2 = etree.SubElement(root, "child2")

    # child3 = etree.SubElement(root, "child3")
    # root.insert(0, etree.Element("child0"))

    print(etree.tostring(root, pretty_print=True))

    # write to file:
    tree = etree.ElementTree(root)
    tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding=u'utf-8')
