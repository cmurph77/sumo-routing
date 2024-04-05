import random
import sys
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
    start = 0.0
    
    for i in range(num_trips):
        trip = SubElement(root, "trip")
        trip.set("id", str(i))
        trip.set("depart", str(start))
        trip.set("from", "E0")
        trip.set("to", f"E100")
        start = start + 0.1

    return prettify(root)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <num_trips>")
        sys.exit(1)

    num_trips = int(sys.argv[1])
    xml_content = generate_trip_xml(num_trips)
    out_fname = str(num_trips) + "tr_tree_23.trips.xml"
    
    with open(out_fname, "w") as xml_file:
        xml_file.write(xml_content)

    print("XML file " + out_fname + " has been generated successfully.")
