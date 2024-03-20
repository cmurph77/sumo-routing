import random
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def generate_trip_xml(num_trips):
    root = Element("routes")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")

    for i in range(num_trips):
        trip = SubElement(root, "trip")
        trip.set("id", str(i))
        trip.set("depart", str(i))
        trip.set("from", "E0")
        trip.set("to", f"F{random.randint(1, 22)}")

    return prettify(root)

if __name__ == "__main__":
    num_trips = 50
    xml_content = generate_trip_xml(num_trips)

    with open(str(num_trips) + "tr_tree_23.trips.xml", "w") as xml_file:
        xml_file.write(xml_content)

    print("XML file 'trips.xml' has been generated successfully.")
