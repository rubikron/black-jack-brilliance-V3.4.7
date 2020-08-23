import requests
import json
import pandas as pd
import random
def get_prediction(data={"dl1":"9","pl1":"10","pl2":"2","round_number":1}):
	url = 'https://k3hn7n41xi.execute-api.us-east-1.amazonaws.com/Predict/56ff48c3-e2a9-4f23-b741-10af77f4bc1c'
	r = requests.post(url, data=json.dumps(data))
	response = getattr(r,'_content').decode("utf-8")
	response_ai = json.loads(response)
	response_body = json.loads(response_ai['body'])
	predicted_label = response_body["predicted_label"]
	return str(predicted_label)
# shuffle should return shuffled list of deck()
# deal() should remove the first card of the list and return that same card
# deal_hand() should return first 2 cards in a list while removing them


# set up
possible_suits = ["hearts","spades","clubs","diamonds"]
possible_values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]

deck = []
show_deck = []
for suit in possible_suits:
	for value in possible_values:
		deck.append(f"{value} of {suit}")

for x in range(52):
	show_deck.append(deck[x])

def shuffle():
	return random.shuffle(show_deck)



def deal():
	x = show_deck[0]
	show_deck.remove(x)
	return x

def deal_hand():
	cards_to_deal = []
	for x in range(2):
		cards_to_deal.append(deal())
	return cards_to_deal

def hand_count(list1,ace=0):
	handcount = 0
	for x in list1:
		if "Ace" in x:
			handcount += ace
		elif (x[0:2]) != "Qu" and (x[0:2]) != "Ki" and (x[0:2]) != "Ja":
			handcount += int(x[0:2])
		else:
			handcount += 10
	return handcount

round_num = 1

# beggining of user interacting with blackjack game interface
pl_score = 0
dl_score = 0
while len(show_deck) > 25:
	if len(show_deck) < 52:
		for th in range(77):
			print('       *** NEW ROUND ***')
	pl = []
	dl = []
	shuffle()
	pl.extend(deal_hand())
	dl.extend(deal_hand())
	
	print(f'AI score: {pl_score}')
	print(f'Dealer score: {dl_score}')

	# print(dl)
	pl_count = hand_count(pl)
	dl_count = hand_count(dl)
	print('Round information:')
	print(f"AI's cards: {pl[0]}, {pl[1]}")
	print(f"Dealer's card: {dl[0]}")
	g = 0

	print(f"Current AI hand count: {pl_count}")
	pll1 = (pl[0].split())[0]
	pll2 = (pl[1].split())[0]
	if pll1 == 'Jack' or pll1 == 'Queen' or pll1 == 'King':
		pll1 = '10'
	elif 'Ace' == pll1:
		pll1 = 'A'
	else:
		pll1 = pll1

	if pll2 == 'Jack' or pll2 == 'Queen' or pll2 == 'King':
		pll2 = '10'
	elif 'Ace' == pll2:
		pll2 = 'A'
	else:
		pll2 = pll2


	dll = dl[0][0:2]
		
	x = get_prediction({'dl1': dll,'pl1': pll1,'pl2' : pll2,'round_number' : round_num})
		
	if x == 'hit':
		x = 'Yes'
	elif x == 'stay':
		x = 'No'
	print('\n')
	print('Does the AI want to draw a card:')
	print(f'{x}\n')	
	if x == "No":	
		pass
	else:
		d = deal()
		print(f'{d} has been dealed to AI.')
		pl.append(d)
		pl_count = hand_count(pl)
		print(f"current sum: {pl_count}")
		print('\n')

		n_pl1 = pl_count - 10
		if pl_count <= 21:
			if n_pl1 == 1 or n_pl1 == 11:
				n_pl1 == 'A'
			else:
				n_pl1 = str(n_pl1)
			n_pl2 = '10'
			h = get_prediction({'dl1': dll,'pl1': n_pl1,'pl2' : n_pl2,'round_number' : (round_num + 1)})
			print('Does the AI want to draw a card:')
			if h == 'hit':
				print('Yes')
				j = deal()
				print('\n')
				print(f'{j} has been dealed to AI.')
				pl.append(j)
				pl_count = hand_count(pl)
				print('\n')
				print(f"current sum: {pl_count}")
			else:
				print('No')
		else:
			print('Does the AI want to draw a card:')
			print('No')

	for x in range(len(pl)):
		if "Ace" in pl[x]:
			print("Does AI want ace to have the value 11 or 1: ")
			if pl_count + 11 > pl_count + 1 and pl_count + 11 < 22:
				s = 11
			else:
				s = 1
			print(s)
			pl_count += s
			print(f"current sum: {pl_count}")

		
	
	print("\nAI final card set:")		
			
	for e in range(len(pl)): 
		print(pl[e], end =", ")  
		
	# x = hand_count()
	print('\n')
	print(f"final sum: {pl_count}")
	
	import time
	f = input("Ready to continue?: ")
	while f != "yes":
		time.sleep(0.7)
	if pl_count > 21:
		print("Uh-oh... AI busted. Dealer Won.")
		dl_score += 1
	else: 

	#Dealer Section
		for x in range(77):
			print('       Dealer Turn       ')
		print("dealer section")
		print(f"{dl[0]},{dl[1]}\n")		
		
		if 'Ace' in dl[0] or 'Ace' in dl[1]:
			while dl_count <= 5:
				w = deal()
				dl.append(w)
				print(dl)
				print(f"appended {w}")
				dl_count = hand_count(dl)
				print(f"current sum: {dl_count}")
			
		else:
			while dl_count <= 16:
				w = deal()
				dl.append(w)
				print(f"appended {w}")
				print(dl)
				dl_count = hand_count(dl)
				print(f"current sum: {dl_count}")

				if hand_count(dl) + 11 > 16 and hand_count(dl) + 11 <= 21:
					break

		while True:
			o = input("\nDealer, do you want to draw a card?: ")
			if o == "no":
			
				break
			else:
				y = deal()
				print(y)
				dl.append(y)
				dl_count = hand_count(dl)
				print(f"current sum: {dl_count}")
		for u in dl:
			if "Ace" in u:
				t = input("Do you want yor ace to have the value 11 or 1: ")
				t = int(t)
				
				dl_count += t
				
		print('\n')
		if dl_count > 21:
			print('Player won. Dealer bust.')
			pl_score += 1
		elif pl_count > dl_count:
			print(f'Player hand: {pl}')
			print(f'Dealer hand: {dl}')
			print('\n')
			print('Player won because of a higher value.')
			pl_score += 1
		elif dl_count > pl_count:
			print(f'Player hand: {pl}')
			print(f'Dlayer hand: {dl}')
			print('\n')
			print('Dealer won because of a higher value.')
			dl_score += 1
			
		elif pl_count == dl_count:
			print('\n')
			print('It is a tie!')
	wer = input("Ready for the next round?: ")
	if len(show_deck) < 25:
		break
	else:
		while wer != "yes":
			time.sleep(0.7)
		round_num += 1
print('\n\n')
print('Hey There! Thanks for trying out BlackJack Brilliance AI!!')
print('If you want to try it again, press the up arrow key and then enter!')