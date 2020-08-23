import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Make a deck
def make_decks(num_decks, card_types):
    new_deck = []
    for i in range(num_decks):
        for j in range(4):
            new_deck.extend(card_types)
    random.shuffle(new_deck)
    return new_deck

# This function lists out all permutations of ace values in the
# array sum_array.
# For example, if you have 2 aces, there are 4 permutations:
#     [[1,1], [1,11], [11,1], [11,11]]
# These permutations lead to 3 unique sums: [2, 12, 22]
# Of these 3, only 2 are <=21 so they are returned: [2, 12]
def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # This loop gets the permutations
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i]=1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i]=11
    # Only return values that are valid (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1)\
                     if s<=21]))# Convert num_aces, an int to a list of lists
# For example if num_aces=2, the output should be [[1,11],[1,11]]
# I require this format for the get_ace_values function
def ace_values(num_aces):
    temp_list = []
    for i in range(num_aces):
        temp_list.append([1,11])
    return get_ace_values(temp_list)

# Total up value of hand
def total_up(hand):
    aces = 0
    total = 0
    
    for card in hand:
        if card != 'A':
            total += card
        else:
            aces += 1
    
    # Call function ace_values to produce list of possible values
    # for aces in hand
    ace_value_list = ace_values(aces)
    final_totals = [i+total for i in ace_value_list if i+total<=21]
    
    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)

stacks = 100002

players = 1
num_decks = 1

blah_list = []
blah_list2 = []

card_types = ['A',2,3,4,5,6,7,8,9,10,10,10,10]
round_num = 0
dealer_hand_val = 1
# df = pd.DataFrame(columns=["dl1","dl2","dl3","dl4","pl1","pl2","player results","round number"])
for stack in range(stacks):
    blackjack = set(['A',10])
    dealer_cards = make_decks(num_decks, card_types)
    while len(dealer_cards) > 20:
        
        curr_player_results = np.zeros((1,players), dtype=int)
        
        dealer_hand = []
        player_hands = [[] for player in range(players)]        # Deal FIRST card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Deal SECOND card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Deal THIRD card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Dealer checks for 21
        if set(dealer_hand) == blackjack:
            for player in range(players):
                if set(player_hands[player]) != blackjack:
                    curr_player_results[0,player] = -1
                else:
                    curr_player_results[0,player] = 0
        else:
            for player in range(players):
                # Players check for 21
                if set(player_hands[player]) == blackjack:
                    curr_player_results[0,player] = 1
                else:
                    # Hit randomly, check for busts
                    while (random.random() >= 0.5) and \
                    (total_up(player_hands[player]) <= 11):
                        player_hands.append(player)
                        (dealer_cards.pop(0))
                        if total_up(player_hands[player]) > 21:
                            curr_player_results[0,player] = -1
                            break

        # Dealer hits based on the rules
        while total_up(dealer_hand) < 17:
            dealer_hand.append(dealer_cards.pop(0))
        # Compare dealer hand to players hand 
        # but first check if dealer busted
        if total_up(dealer_hand) > 21:
            for player in range(players):
                if curr_player_results[0,player] != -1:
                    curr_player_results[0,player] = 1

        else:
            for player in range(players):
                if total_up(player_hands[player]) > \
                total_up(dealer_hand):
                    if total_up(player_hands[player]) <= 21:
                        curr_player_results[0,player] = 1
                elif total_up(player_hands[player]) == \
                total_up(dealer_hand):
                    curr_player_results[0,player] = 0
                else:
                    curr_player_results[0,player] = -1
        

        round_num += 1
        if len(dealer_cards) < 20:
            round_num = 1
            
		
         
        while len(dealer_hand) < 4:
            dealer_hand.append(0)


        player_results = []
        player_results.append(list(curr_player_results[0]))
        
        round_num = int(round_num)
        


        #making a dataframe
        
        # print ("DH:", dealer_hand)
        # print ("PH:", player_hands)
        # print ("PR:", player_results)
        # print ("RN:", round_num)

        blah_list.append([dealer_hand[0], 
                            # dealer_hand[1], 
                            # dealer_hand[2], 
                            # dealer_hand[3],
                            player_hands[0][0],
                            player_hands[0][1],
                            # player_results[0][0],
                            round_num])
        blah_list2.append([dealer_hand[0], 
                            dealer_hand[1], 
                            # dealer_hand[2], 
                            # dealer_hand[3],
                            player_hands[0][0],
                            player_hands[0][1],
                            player_hands[0][2],
                            player_results[0][0],
                            round_num])
        


dfpl2 = pd.DataFrame(blah_list, columns=["dl1", "pl1", "pl2", "round_number"])
dfpl2.to_csv('black_jack_setpl2.csv', index=False)
print ("dfpl2 has all the info")


dfpl3 = pd.DataFrame(blah_list2, columns=["dl1",'dl2', "pl1", "pl2","pl3", "player_result", "round_number"])
dfpl3.to_csv('black_jack_setpl3.csv', index=False)
print ("dfpl3 has all the info")
hits = 0
stays = 0
