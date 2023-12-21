import re

def main():
    with open('./december_2/input.txt', 'r') as f:
        games = f.readlines()

    red_cubes = 12
    green_cubes = 13
    blue_cubes = 14

    valid_games = 0
    for i, game in enumerate(games):
        reds = (re.findall(r' (\d+) red', game))
        reds = list(map(int, reds))
        max_reds = max(reds)

        blues = (re.findall(r' (\d+) blue', game))
        blues = list(map(int, blues))
        max_blues = max(blues)

        greens = (re.findall(r' (\d+) green', game))
        greens = list(map(int, greens))
        max_greens = max(greens)

        if (max_reds <= red_cubes) and (max_greens <= green_cubes) and (max_blues <= blue_cubes):
            valid_games += (i + 1)

    print(f"Valid games sum: {valid_games}")

    valid_games = 0
    for i, game in enumerate(games):
        reds = (re.findall(r' (\d+) red', game))
        reds = list(map(int, reds))
        max_reds = max(reds) if reds else 1

        blues = (re.findall(r' (\d+) blue', game))
        blues = list(map(int, blues))
        max_blues = max(blues) if blues else 1

        greens = (re.findall(r' (\d+) green', game))
        greens = list(map(int, greens))
        max_greens = max(greens) if greens else 1

        prod = max_greens * max_blues * max_reds

        valid_games += prod

    print(f"Valid games sum: {valid_games}")





if __name__ == "__main__":
    main()