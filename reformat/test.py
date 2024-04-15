def get_reroute_boolean(proportion):
    total_elements = 1000
    percentage_to_pick = proportion
    num_elements_to_pick = int(total_elements * percentage_to_pick)

    # Step 2: Determine the interval
    num_intervals = num_elements_to_pick - 1
    interval = total_elements // num_intervals

    # Step 3: Pick elements at intervals and create the boolean array
    boolean_array = [False] * total_elements
    for i in range(0, total_elements, interval):
        boolean_array[i] = True

    # Ensure we have exactly num_elements_to_pick True values
    true_count = boolean_array.count(True)
    if true_count > num_elements_to_pick:
        for i in range(total_elements - 1, -1, -1):
            if boolean_array[i]:
                boolean_array[i] = False
                true_count -= 1
            if true_count == num_elements_to_pick:
                break

    # print(boolean_array)
    return boolean_array

array  = get_reroute_boolean(0.23)
print(array)
i = 0
for item in array:
    if item == True:
        i = i + 1

print(array[i])
print(i)