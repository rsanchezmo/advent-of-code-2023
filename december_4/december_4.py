import re

def main():
    with open('./december_4/input.txt', 'r') as f:
        cards = f.readlines()


    """ Part 1 """
    sum_points = 0
    for card in cards:
        card = card.split(':')[1]  # remove the initial card name

        winning_nums_str = card.split('|')[0]
        own_nums_str = card.split('|')[1].replace('\n', ' ')

        winning_nums = re.findall(r'\d+', winning_nums_str)

        counter = 0
        for winning_num in winning_nums:
            counter += own_nums_str.count(' ' + winning_num + ' ')

        points = 0
        if counter > 0:
            points = 2**(counter-1)

        sum_points += points

    print(f'Total points worth: {sum_points}')

    """ Part 2 """
    n_cards = len(cards)
    cards_counter = [1] * n_cards

    for i, card in enumerate(cards):
        card = card.split(':')[1]  # remove the initial card name

        winning_nums_str = card.split('|')[0]
        own_nums_str = card.split('|')[1].replace('\n', ' ')

        winning_nums = re.findall(r'\d+', winning_nums_str)

        counter = 0
        for winning_num in winning_nums:
            counter += own_nums_str.count(' ' + winning_num + ' ')

        for next_card in range(i+1, counter + i + 1):
            if next_card < n_cards:
                cards_counter[next_card] += cards_counter[i]
        
    print(f"Total cards: {sum(cards_counter)}")


         


if __name__ == '__main__':
        main()