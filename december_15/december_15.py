

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

    """ Part 2 """
    hashmap = {}
    for component in components:
        if '=' in component:
            box, focal_lenght = component.split("=")
            box_id = hash_function(box)
            id = box + ' ' + focal_lenght

            print(f"= {id} {box_id}")

            box_components = hashmap.get(box_id, [])

            found = False
            for i, lens in enumerate(box_components):
                if box == lens.split(" ")[0]:
                    box_components[i] = id
                    hashmap[box_id] = box_components
                    found = True
                    break
            if not found:
                box_components.append(id)
                hashmap[box_id] = box_components

        if '-' in component:
            box = component.split("-")[0]
            box_id = hash_function(box)

            print(f"- {box} {box_id}")

            box_components = hashmap.get(box_id, [])

            for lens in box_components:
                if box == lens.split(" ")[0]:
                    box_components.remove(lens)
                    hashmap[box_id] = box_components
                    break

    from pprint import pprint
    pprint(hashmap)


    focusing_power = 0
    for box_id, box_components in hashmap.items():
        for i, lens in enumerate(box_components):
            focal_lenght = int(lens.split(" ")[-1])
            focusing_power += (box_id + 1) * (i + 1) * focal_lenght

    print(f"Part 2: {focusing_power}")


    
if __name__ == "__main__":
    main()