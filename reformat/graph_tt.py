import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

# Function to extract travel times from XML file
def extract_travel_times(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    travel_times = []
    for vehicle in root.findall('vehicle'):
        depart_time = float(vehicle.attrib['depart'])
        arrival_time = float(vehicle.attrib['arrival'])
        travel_time = arrival_time - depart_time
        travel_times.append(travel_time)
    return travel_times

# Define function to calculate mean and add it to plot
def add_mean_to_plot(travel_times, ax):
    mean_travel_time = np.mean(travel_times)
    ax.axvline(x=mean_travel_time, color='green', linestyle='--', label=f'Mean: {mean_travel_time:.2f}')
    ax.legend()

# Define file paths
file1 = 'out/so_simple_out/rand_20_output_files/cr_1000tr.out.xml'
file2 = 'out/ue_simple_out/rand_20_output_files/cr_1000tr.out.xml'

# Extract travel times from both files
travel_times_file1 = extract_travel_times(file1)
travel_times_file2 = extract_travel_times(file2)

# Define bins for grouping travel times
bins = np.arange(0, max(max(travel_times_file1), max(travel_times_file2)) + 20, 20)

# Plotting the bar charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.hist(travel_times_file1, bins=bins, color='blue', edgecolor='black')
ax1.set_xlabel('Travel Time')
ax1.set_ylabel('Number of Vehicles')
ax1.set_title('Distribution of Travel Times (SO)')
ax1.grid(axis='y')
add_mean_to_plot(travel_times_file1, ax1)

ax2.hist(travel_times_file2, bins=bins, color='red', edgecolor='black')
ax2.set_xlabel('Travel Time')
ax2.set_ylabel('Number of Vehicles')
ax2.set_title('Distribution of Travel Times (UE)')
ax2.grid(axis='y')
add_mean_to_plot(travel_times_file2, ax2)

plt.tight_layout()
plt.show()
