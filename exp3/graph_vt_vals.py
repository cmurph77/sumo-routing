import matplotlib.pyplot as plt

def plot_dictionary_values_from_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            data[key.strip()] = value.strip()

    keys = list(map(float, data.keys()))
    values = list(map(float, data.values()))

    plt.bar(keys, values)
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Bar Chart of Dictionary Values')
    plt.grid(True)
    plt.show()

# File path containing the dictionary
file_path = '/Users/cianmurphy/code_directories/final_year_project/experiments/central_routing/cr_exp1/r20_1to50_ct_1500tr_.txt'

# Plotting the graph from file
plot_dictionary_values_from_file(file_path)
