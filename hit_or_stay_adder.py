import pandas as pd
import random
# shuffle should return shuffled list of deck()
# deal() should remove the first card of the list and return that same card
# deal_hand() should return first 2 cards in a list while removing them


# set up
possible_suits = ["hearts","spades","clubs","diamonds"]
possible_values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
def new_deck():
	lis = []
	show_deck = []
	for suit in possible_suits:
		for value in possible_values:
			lis.append(f"{value} of {suit}")
	return lis

deck = new_deck()




def deal():
	
	x = deck[0]
	deck.remove(x)
	return x



def hand_count(list1,ace=0):
	handcount = 0
	for m in list1:
		if 'A' == m or 'Ace' in m:
			# print(f'{m} is an Ace!')
			ind = list1.index(m)
			# print(ind)
			list1[ind] = str(11)
			# print(list1)
	for p in list1:
		handcount += int(p[0:2])
	return handcount
	


black_setpl2 = pd.read_csv("black_jack_setpl2.csv")
black_setpl3 = pd.read_csv("black_jack_setpl3.csv")


def some_func():
	for j in pl_hand:
			if 'Ace' in j:
				if hand_count(pl_hand,11) > 21:
					return 1
				elif hand_count(pl_hand,1) > 21:
					pl_hand.remove(j)
					return 0
				else:
					return 11	


colmn_vals = []
print(deck)
for index_num in range(0,len(black_setpl2)):
	if len(deck) < 7:
		deck = new_deck()
	card = deal()
	card2 = deal()
	pl_hand = []
	dl_hand = []
	dl_hand.extend([black_setpl3.loc[index_num,'dl1'],black_setpl3.loc[index_num,'dl2']])
	pl_hand.extend([black_setpl2.loc[index_num,'pl1'],black_setpl2.loc[index_num,'pl2']])
	pl_hand.append(card)
	ace = some_func()	
	ace2 = some_func()
	
	for h in pl_hand:
		if 'Queen' in h or 'Jack' in h or 'King' in h:
			inde = pl_hand.index(h)
			pl_hand[inde] = '10'

	pl_sum = hand_count(pl_hand,ace)
	dl_sum = hand_count(dl_hand,ace2)
	if pl_sum > 21:
		colmn_vals.append('stay')
	elif dl_sum < pl_sum and pl_sum > 21:
		colmn_vals.append('hit')
	else:
		colmn_vals.append('hit')



black_setpl2["Action"] = colmn_vals
black_setpl2.to_csv('black_jack_setpl2.csv', index=False)
hits = 0
stays = 0
for x in range(len(black_setpl2)):
	if black_setpl2.loc[x,'Action'] == 'hit':
		hits += 1
	else:
		stays += 1

print(hits)
print(stays)
