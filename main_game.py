import csv
import random


def get_town_list(filepath):
    towns = []
    with open(filepath, mode='r') as file:
        csvfile = csv.reader(file)
        for entry in csvfile:
            towns.append(entry)
    return towns


def get_player_list():
    players = []

    print('\n' + '- + -' * 22)

    player_count = int(input('How many people are playing: '))
    for i in range(player_count):
        name = f'P{i+1}'
        pos = 0
        balance = 500
        properties = []
        players.append([name, pos, balance, properties])

    print('\n' + '- + -' * 22)

    return players


def set_board(towns):
    board = []
    go = ['GO', 0, 0]
    chance = ['CHANCE', 0, 0]

    board.append(go)
    for i in range(4):
        board.append(towns[i])
    board.append(chance)
    for i in range(4, 8):
        board.append(towns[i])
    board.append(chance)
    for i in range(8, 12):
        board.append(towns[i])
    board.append(chance)
    for i in range(12, 16):
        board.append(towns[i])

    return board


def display_board(board, players):
    player_pos = []
    for i in range(20):
        player_pos.append([])

    for i in range(len(player_pos)):
        for j in range(len(players)):
            if i == int(players[j][1]):
                player_pos[i].append(players[j][0])

    print('\n' + '- + -' * 22 + '\n')
    for i in range(6):
        print(f'{board[i][0]:^20}', end='')
    print()

    for i in range(6):
        print(f'{str(player_pos[i]):^20}', end='')
    print('\n\n')

    for i in range(4):
        print(f'{board[19-i][0]:^20}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{board[6+i][0]:^20}')
        print(f'{str(player_pos[19-i]):^20}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{str(player_pos[6+i]):^20}')
        print('\n')

    for i in range(6):
        print(f'{board[15-i][0]:^20}', end='')
    print()

    for i in range(6):
        print(f'{str(player_pos[15-i]):^20}', end='')

    print('\n\n' + '- + -' * 22 + '\n')


def even_new_position(current, dice_num):
    new = current + dice_num
    if new > 19:
        new = new - 20
    return new


def odd_new_position(current, dice_num):
    new = current - dice_num
    if new < 0:
        new = 20 + new
    return new


#   Initialising board and players
towns_csv = 'C:/Users/mevin/Documents/monopoly/towns.csv'
town_list = get_town_list(towns_csv)

board_list = set_board(town_list)
player_list = get_player_list()


#   Initial Board display
print('\nGAME STARTS')
display_board(board_list, player_list)

#   Game Loop start
rounds = 1
losers_list = []
player_count = len(player_list)
while player_count > 1:
    print('Round:', rounds)

    turns = 0
    while turns < len(player_list):
        current_player = str(player_list[turns][0])
        current_position = int(player_list[turns][1])
        current_balance = int(player_list[turns][2])
        current_properties = player_list[turns][3]

        print('player:', current_player, '\tbalance:', current_balance)
        print('properties:', current_properties, '\n')

        dice = random.randint(1, 6)
        print(f'Dice rolled on {dice}.', end='\t')

        if (turns+1) % 2 == 0:
            new_position = even_new_position(current_position, dice)
            print(current_player, 'moves clockwise and lands on', end=' ')
        else:
            new_position = odd_new_position(current_position, dice)
            print(current_player, 'moves anticlockwise and lands on', end=' ')

        current_town = str(board_list[new_position][0])
        print(current_town, end=' ')

        if current_town == 'GO':
            print('which cannot be bought.')

        elif current_town == 'CHANCE':
            chance_num = random.randint(0,3)
            if chance_num == 0:
                print('\nBank pays you dividend of Rs10.')
                current_balance += 10
            elif chance_num == 1:
                print('\nSpeeding fine Rs15')
                current_balance -= 15
            elif chance_num == 2:
                print('\nYour building loan matures. Collect Rs30')
                current_balance += 30
            else:
                print('\nDoctor’s fee. Pay Rs20')
                current_balance -= 20
        else:
            current_town_price = int(board_list[new_position][1])
            current_town_rent = int(board_list[new_position][2])
            print('\tprice:', current_town_price, '\trent:', current_town_rent)

            owner = 'none'
            for i in range(len(player_list)):
                # check if property is owned
                if any(current_town in town for town in player_list[i][3]):
                    owner = player_list[i][0]
                    owner_index = i

                    if owner == current_player:
                        print(current_player, 'already owns', current_town)

                    else:
                        # Rent deduction
                        current_balance -= current_town_rent

                        # Rent added to owner's balance
                        player_list[owner_index][2] += current_town_rent
                        print(owner, 'owns', current_town, end='.  ')
                        print(current_player, 'has paid Rs', current_town_rent, 'in rent to', owner)

            if owner == 'none':
                print('Nobody owns', current_town, end='.  ')

                if current_balance >= current_town_price:
                    current_balance -= current_town_price
                    player_list[turns][3].append(current_town)
                    print(current_player, 'has purchased', current_town, 'for Rs', current_town_price)

                else:
                    print(current_player, 'does not have enough funds to purchase', current_town)

        player_list[turns][2] = current_balance
        if current_balance < 0:
            print(current_player, 'does not have enough funds to continue playing.')
            losers_list.append(player_list[turns])
            player_list.remove(player_list[turns])
            turns -= 1
        else:
            player_list[turns][1] = new_position

        display_board(board_list, player_list)
        turns += 1

    player_count = len(player_list)
    rounds += 1

winner_name = player_list[0][0]
winner_bal = player_list[0][2]
winner_prop = player_list[0][3]

print(winner_name, 'has won the game on round', rounds, '!!!\n')
print('##### GAME SUMMARY #####')
print(winner_name, 'is the winner with final balance of Rs', winner_bal, '\nand acquired', winner_prop)

print('\n##### Losing players stats #####')
for i in range(len(losers_list)):
    name = losers_list[i][0]
    properties = losers_list[i][3]
    print(name, 'owned', properties)
