
def find_next_value(sequence):
    differences = []
    for i in range(1, len(sequence)):
        differences.append(sequence[i] - sequence[i - 1])

    if all(difference == 0 for difference in differences):
        return sequence[-1] + differences[-1]
    
    return find_next_value(differences) + sequence[-1]

def find_prev_value(sequence):
    differences = []
    for i in range(1, len(sequence)):
        differences.append(sequence[i] - sequence[i - 1])

    if all(difference == 0 for difference in differences):
        return sequence[0] - differences[0]
    
    return sequence[0] - find_prev_value(differences)

def main():
    with open('./december_9/input.txt', 'r') as f:
        lines = f.readlines()


    """ Part 1 """
    values = []
    for line in lines:
        sequence = list(map(int, line.strip().split(' ')))
        next_value = find_next_value(sequence)
        values.append(next_value)

    print(f"Sum of extrapolated values: {sum(values)}")

    """ Part 2 """
    values = []
    for line in lines:
        sequence = list(map(int, line.strip().split(' ')))
        prev_value = find_prev_value(sequence)
        values.append(prev_value)

    print(f"Sum of extrapolated values: {sum(values)}")

if __name__ == '__main__':
    main()