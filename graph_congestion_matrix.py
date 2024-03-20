import csv
import matplotlib.pyplot as plt
import argparse

def calculate_column_averages(csv_file):
    # Initialize lists to store column data
    columns = []

    # Read the CSV file and extract column data
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if not columns:
                columns = [[] for _ in range(len(row))]
            for i, value in enumerate(row):
                columns[i].append(float(value))

    # Calculate column averages
    column_averages = [sum(column) / len(column) for column in columns]

    return column_averages

# def calculate_column_sum(csv_file):
#     # Initialize lists to store column data
#     columns = []

#     # Read the CSV file and extract column data
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             if not columns:
#                 columns = [[] for _ in range(len(row))]
#             for i, value in enumerate(row):
#                 columns[i].append(float(value))

#     # Calculate column averages
#     column_sums = [sum(column) / len(column) for column in columns]

#     return column_sums

def plot_column_averages(column_averages, column_labels,trip_count,net,algorithm):
    # Plot the column averages
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(column_averages)), column_averages, color='skyblue')
    plt.xlabel('Columns')
    plt.ylabel('Average')
    plt.title('Average Congestion for ' + str(trip_count) + ' trips on Network: ' + net +' using algorithm: ' + algorithm)
    plt.xticks(range(len(column_averages)), column_labels)
    plt.grid(axis='y')
    plt.show()

def main():
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Description of your script.')

    # Add arguments
    parser.add_argument('arg1', type=str, help='Description of argument 1')
    parser.add_argument('arg2', type=int, help='Description of argument 2')

    # Parse arguments
    args = parser.parse_args()

    # # Access parsed arguments
    net = args.arg1
    trip_count = args.arg2
    algorithm = 'astar'

    exp_a = 1
    exp_b = 2

    csv_file = "/Users/cianmurphy/code_directories/final_year_project/experiments/central_routing/cr_exp1/"+net+"_output_files/congestion_matrices/"+str(trip_count)+"tr_"+algorithm+"_cm.csv"
    column_averages = calculate_column_averages(csv_file)
    
    # Extract column labels from the header row
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        column_labels = next(reader)

    # Plot column averages with column labels
    plot_column_averages(column_averages, column_labels,trip_count,net,algorithm)

if __name__ == "__main__":
    main()

