import xml.etree.ElementTree as ET

# extracts distances from net file in the form { edge_id : distance }
def get_distances_in_net(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    edge_lengths = {}

    for edge in root.findall('edge'):
        edge_id = edge.attrib['id']
        lane = edge.find('lane')
        if lane is not None:
            length = float(lane.attrib['length'])
            edge_lengths[edge_id] = length

    return edge_lengths




if __name__ == "__main__":
    edge_lengths = get_distances_in_net('random_20.net.xml' )
    print(edge_lengths)
    for edge,length in edge_lengths.items():
        print(str(edge) + "  " + str(length))
