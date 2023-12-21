import re

def get_number(line: str) -> int:
    digits = re.findall(r'\d', line)
    digits = [digits[0], digits[-1]] if len(digits) > 1 else digits[0] * 2
    number = int(''.join(digits))
    return number


def main():
    with open('./december_1/calibration.txt') as f:
        example_input = f.readlines() 

    # PART 1
    print("Part 1")
    sum_num = 0
    for line in example_input:
        number = get_number(line)
        sum_num += number

    print(f"The sum of all calibration numbers is: {sum_num}")

    print("Part 2")
    sum_num = 0
    word_to_num = {
        'one': 'o1e', 'two': 't2o', 'three': 'th3e', 'four': '4', 'five': '5e',
        'six': '6', 'seven': 's7n', 'eight': 'e8t', 'nine': '9e'
    }

    for line in example_input:
        for word, num in word_to_num.items():
            line = line.replace(word, num)
        number = get_number(line)
        sum_num += number
    print(f"The sum of all calibration numbers is: {sum_num}")

if __name__ == '__main__':
    main()