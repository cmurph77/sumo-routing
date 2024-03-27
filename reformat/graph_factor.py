import re
import matplotlib.pyplot as plt

def parse_line(line):
    match = re.match(r'so_simple--\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] , Network: .* Trip Size: \d+, Average Time: (\d+\.\d+), Increase factor: (\d+\.\d+)', line)
    if match:
        avg_time = float(match.group(1))
        increase_factor = float(match.group(2))
        return avg_time, increase_factor
    else:
        return None, None

def main():
    increase_factors = []
    avg_times = []

    with open('factor_data.txt', 'r') as file:
        for line in file:
            avg_time, increase_factor = parse_line(line)
            if avg_time is not None and increase_factor is not None:
                increase_factors.append(increase_factor)
                avg_times.append(avg_time)

    plt.plot(increase_factors, avg_times, marker='o', linestyle='-')
    plt.xlabel('Increase Factor')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Increase Factor (so_simple)')
    plt.grid(True)
    # plt.savefig('so_simple_results_graph.png')
    plt.show()

if __name__ == "__main__":
    main()
