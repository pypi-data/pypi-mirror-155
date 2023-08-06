from lxml import etree


def clean_transaction_xml(transaction_xml_payload):
    root = etree.fromstring(transaction_xml_payload)
    xml_root = etree.iterwalk(root)

    for action, xml_element in xml_root:
        parent = xml_element.getparent()
        if recursively_empty(xml_element):
            parent.remove(xml_element)

        recurvisely_remove_parent(parent)

    str_xml = etree.tostring(root, encoding="utf-8", pretty_print=True)
    return str_xml


def recurvisely_remove_parent(parent):
    if parent is not None and len(list(parent)) < 1:
        parents_parent = parent.getparent()
        if parents_parent is not None and len(list(parent)) < 1:
            parents_parent.remove(parent)
            recurvisely_remove_parent(parents_parent)


def recursively_empty(xml_element):
    if xml_element.text:
        return False
    return all((recursively_empty(xe) for xe in xml_element.iterchildren()))
