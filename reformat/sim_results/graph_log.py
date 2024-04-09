import re
import matplotlib.pyplot as plt
import argparse

def parse_line(line):
    match = re.match(r'(\w+)--\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] , Network: .* Trip Size: (\d+), Average Time: (\d+\.\d+)', line)
    if match:
        algo = match.group(1)
        trip_size = int(match.group(2))
        avg_time = float(match.group(3))
        return algo, trip_size, avg_time
    else:
        return None, None, None

def main():
    # -------- read args
    parser = argparse.ArgumentParser(description="Description of your script.")
    parser.add_argument("arg1", help="set the trip count")
    args = parser.parse_args()

    fname = args.arg1
    
    # trip_data = {'so_simple': {}, 'ue_simple': {}}
    # total_avg_times = {'so_simple': [], 'ue_simple': []}

    trip_data = {'system_optimum': {}, 'user_equilibrium': {}}
    total_avg_times = {'system_optimum': [], 'user_equilibrium': []}

    # fname = 'soVue_r20.txt'
    # fname = 'r20_compare/r20_p1_results.txt'
    with open(fname, 'r') as file:
        for line in file:
            algo, trip_size, avg_time = parse_line(line)
            if algo and trip_size and avg_time:
                trip_data[algo][trip_size] = trip_data[algo].get(trip_size, []) + [avg_time]
                total_avg_times[algo].append(avg_time)

    line_colors = ['blue', 'red', 'green']  # Change this to your desired sequence of colors
    
    
    i = 1
    for algo, sizes in trip_data.items():
        if i == 1: plot_colour = 'green'
        elif i == 2 : plot_colour = 'red'
        i = i+1
        plt.scatter(list(sizes.keys()), [sum(times)/len(times) for times in sizes.values()], label=algo,color=plot_colour )

    plt.xlabel('Trip Files')
    plt.ylabel('Average Time')
    plt.title(' ')
    plt.legend()
    plt.grid(True)
    i = 1
    so_avg = 0
    ue_avg = 0
    for algo, avg_times in total_avg_times.items():
        avg_of_avg = sum(avg_times) / len(avg_times)
        if i == 1: ue_avg = avg_of_avg
        elif i == 2 : so_avg = avg_of_avg
        i = i +1;
        print(f"Average of the average times for {algo}: {avg_of_avg}")

    
    plt.axhline(ue_avg, color='green')
    plt.axhline(so_avg, color= 'red')

    plt.savefig(fname + '.png')  # Saving the plot as a PNG file
    plt.show()



if __name__ == "__main__":
    main()
