

def hash_function(input_str):
    current_value = 0
    
    # Loop through each character in the input string
    for char in input_str:
        # Convert the character to its ASCII value
        ascii_value = ord(char)
        # Add the ASCII value to the current value
        current_value += ascii_value
        # Multiply the current value bby 17
        current_value *= 17
        # Set the current value to the remainder of dividing itself by 256
        current_value %= 256

    return current_value

def main():
    with open("december_15/input.txt", "r") as f:
        components = f.readlines()[0].strip().split(",")

    """ Part 1 """
    sum_ = 0
    for component in components:
        sum_ += hash_function(component)

    print(f"Part 1: {sum_}")

    
if __name__ == "__main__":
    main()