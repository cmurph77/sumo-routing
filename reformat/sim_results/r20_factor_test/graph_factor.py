import csv
import matplotlib.pyplot as plt

def analyze_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Assuming the first row is the header
        sum_of_averages = {}
        factor = 1
        for i in range(1,22):
            sum_of_averages[str(round(factor,3))] = 0
            factor = factor + 0.005
            i = i+1
        
        for line_number, line in enumerate(reader, start=2):  # Start at line 2 (since we already read the header)
            # Example analysis: Counting the number of columns in each line
            num_columns = len(line)
            # print(line)
            avg_time = float(line[5])
            trip_size = float(line[4])
            factor = str(line[6])
            sum_of_averages[factor] = sum_of_averages[factor] + avg_time


        print(sum_of_averages)

        # print(sum_of_averages)
        for key in sum_of_averages:
            value = sum_of_averages[key]
            sum_of_averages[key] = value / 10
            # print(f"Key: {key}, Value: {value}")
        # print(sum_of_averages)

        # Extracting x and y data
        x_data = [float(key) for key in sum_of_averages.keys()]
        y_data = list(sum_of_averages.values())

        # Plotting the line graph
        plt.plot(x_data, y_data, marker='o', linestyle='-')

        # Adding labels and title
        plt.xlabel('X-axis label')
        plt.ylabel('Y-axis label')
        plt.title('Line Graph')

        # Displaying the graph
        plt.grid(True)
        plt.savefig('r20_p05_factor.png')  # Saving the plot as a PNG file
        plt.show()

            
            
# Usage example
if __name__ == "__main__":
    csv_file_path = "r20_p05_factor.csv"  # Provide the path to your CSV file here
    analyze_csv(csv_file_path)
