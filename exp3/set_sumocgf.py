import xml.etree.ElementTree as ET

def set_netfile_value(cfg_file,new_value):
    tree = ET.parse(cfg_file)
    root = tree.getroot()

    for input_element in root.iter('input'):
        for netfile_element in input_element.iter('net-file'):
            netfile_element.set('value', new_value)

    tree.write(cfg_file)

def set_route_file_value(cfg_file,new_value):
    tree = ET.parse(cfg_file)
    root = tree.getroot()

    for input_element in root.iter('input'):
        for netfile_element in input_element.iter('route-files'):
            netfile_element.set('value', new_value)

    tree.write(cfg_file)

def set_routing_algo_value(cfg_file,new_value):
    tree = ET.parse(cfg_file)
    root = tree.getroot()

    for input_element in root.iter('routing'):
        for netfile_element in input_element.iter('routing-algorithm'):
            netfile_element.set('value', new_value)

    tree.write(cfg_file)

def set_output_file_value(cfg_file,new_value):
    tree = ET.parse(cfg_file)
    root = tree.getroot()

    for input_element in root.iter('output'):
        for netfile_element in input_element.iter('vehroute-output'):
            netfile_element.set('value', new_value)

    tree.write(cfg_file)

if __name__ == "__main__":
    

    # Example usage
    config_file = "sim_files/test.sumocfg"
    set_netfile_value(config_file,"new.net.xml")
    set_route_file_value(config_file, "new_val")
    set_routing_algo_value(config_file,"test")
    set_output_file_value(config_file,"new_output")

