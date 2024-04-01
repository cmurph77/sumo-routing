import re
import matplotlib.pyplot as plt

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
    trip_data = {'so_simple': {}, 'ue_simple': {}}
    total_avg_times = {'so_simple': [], 'ue_simple': []}

    # fname = 'soVue_r20.txt'
    fname = 'net1_log.txt'
    with open(fname, 'r') as file:
        for line in file:
            algo, trip_size, avg_time = parse_line(line)
            if algo and trip_size and avg_time:
                trip_data[algo][trip_size] = trip_data[algo].get(trip_size, []) + [avg_time]
                total_avg_times[algo].append(avg_time)

    for algo, sizes in trip_data.items():
        plt.plot(list(sizes.keys()), [sum(times)/len(times) for times in sizes.values()], label=algo)

    plt.xlabel('Trip Size')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Trip Size')
    plt.legend()
    plt.grid(True)
    # plt.savefig('results_graph.png')   
     # Calculate and print the average of the average times
    for algo, avg_times in total_avg_times.items():
        avg_of_avg = sum(avg_times) / len(avg_times)
        print(f"Average of the average times for {algo}: {avg_of_avg}")
    plt.show()



if __name__ == "__main__":
    main()
