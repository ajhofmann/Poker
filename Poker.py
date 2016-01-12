# Author: Adam Hofmann

# Five Draw Poker Game designed and developed in Python to gain experience in GUI.

import random
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
random.seed()

suits = ['C', 'D', 'H', 'S']
cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
deck = ['' for i in range(52)]
for i in range(4):
    for j in range(13):
        deck[i + j*4] = cards[j]+suits[i]

def shuffle():
    global deck
    for i in range(1000):
        num1 = random.randint(0,51)
        num2 = random.randint(0,51)
        temp = deck[num1]
        deck[num1] = deck[num2]
        deck[num2] = temp

shuffle()

# Retrieves all the numbers in a hand, sorted
def numsinhand(hand):
    return sorted(hand[0] + hand[2] + hand[4] + hand[6] + hand[8])

# ------------------------------------------
# Functions to determine if a hand has a certain sequence
# all functions require an input in the form of a string as
# NSNSNSNSNS Where N is the card number and S is the suit
# ------------------------------------------

# Determines what card wins by comparing high cards
def tiebreakhigh(hand1, hand2):
    nums1 = numsinhand(hand1)
    nums2 = numsinhand(hand2)
    for i in range(5):
        if highcard(nums1) != highcard(nums2):
            return highcard(nums1) < highcard(nums2)
        else:
            nums1.remove(cards[highcard(nums1)])
            nums2.remove(cards[highcard(nums2)])
    return 'tie'

# Determines if the hand has one pair
def isonepair(hand):
    nums = numsinhand(hand)
    return nums[0] == nums[1] or \
           nums[1] == nums[2] or \
           nums[2] == nums[3] or \
           nums[3] == nums[4]


# Determines if the hand has a two pair
def istwopair(hand):
    nums = numsinhand(hand)
    return nums[0] == nums[1] and nums[2] == nums[3] or\
           nums[0] == nums[1] and nums[3] == nums[4] or \
           nums[1] == nums[2] and nums[3] == nums[4]

# Determines if the hand has a three of a kind
def isthreeofakind(hand):
    nums = numsinhand(hand)
    return nums[0] == nums[2] or nums[1] == nums[3] or nums[2] == nums[4]

# Determines if the hand has a straight
def isstraight(hand):
    for i in range(9):
        count = 0
        for j in range(5):
            if cards[i+j] in hand:
                count += 1
            if count == 5:
                return True
    return False

# Determines if the hand has a flush
def isflush(hand):
    if hand[1] == hand[3] and hand[3] == hand[5] and hand[5] == hand[7] and hand[7] == hand[9]:
        return True
    return False

# Determines if the hand has a full house
def isfullhouse(hand):
    nums = numsinhand(hand)
    return nums[0] == nums[1] and nums[2] == nums[4] or\
           nums[0] == nums[2] and nums[3] == nums[4]

# Determines if the hand has a four of a kind
def isfourofakind(hand):
    nums = numsinhand(hand)
    return nums[0] == nums[3] or nums[1] == nums[4]

# Determines if the hand has a straight flush
def isstraightflush(hand):
    return (isflush(hand) and isstraight(hand))

# Determines if the hand has a royal flush
def isroyalflush(hand):
    if isflush(hand):
        count = 0
        for i in range(5):
            if cards[i] in hand:
                count += 1
        return count == 5
    return False

# ------------------------------------------
# end hand rankings
# ------------------------------------------

# functions that determine which hand wins
functs = [isroyalflush, isstraightflush, isfourofakind, isfullhouse, isflush, isstraight, isthreeofakind, istwopair, isonepair, tiebreakhigh]

# Determines the index of the highest card in the hand
def highcard(hand):
    for i in range(13):
        if cards[i] in hand:
            return i

# returns the pairs in a two pair hand and the other card
def twopairbreakdown(hand):
    hand = numsinhand(hand)
    if hand[0] == hand[1]:
        if hand[2] == hand[3]:
            if cards.index(hand[0]) < cards.index(hand[3]):
                return [hand[0], hand[3], hand[4]]
            else:
                return [hand[3], hand[0], hand[4]]
        if cards.index(hand[0]) < cards.index(hand[3]):
            return [hand[0], hand[3], hand[2]]
        else:
            return [hand[3], hand[0], hand[2]]
    if cards.index(hand[1]) < cards.index(hand[3]):
        return [hand[1], hand[3], hand[0]]
    else:
        return [hand[3], hand[1], hand[0]]

def onepairbreakdown(hand):
    nums = numsinhand(hand)
    for i in range(4):
        if nums[i] == nums[i+1]:
            return [nums[i]] + nums[:i] + nums[i+1:]



# takes two truth hands and a hand type and determines if the hands would
# tie win or lose based on that hand type
# T = Tie, True = P1 wins, False = P2 wins, N = no one wins yet
def nextAct(hand1, hand2, function):
    if function == tiebreakhigh:
        return tiebreakhigh(hand1, hand2)
    if function(hand1) and function(hand2):
        return 'T'
    if function(hand1):
        return True
    if function(hand2):
        return False
    return 'N'

def tiebreak(hand1, hand2, type):
    if type == isroyalflush:
        return 'tie'
    if type == isstraightflush or type == isstraight or type == isflush:
        return tiebreakhigh(hand1, hand2)
    if type == isfourofakind or type == isfullhouse or type == isthreeofakind:
        return highcard(numsinhand(hand1)[2]) < highcard(numsinhand(hand2)[2])
    if type == istwopair:
        hand1 = twopairbreakdown(hand1)
        hand2 = twopairbreakdown(hand2)
        for i in range(3):
            if cards.index(hand1[i]) != cards.index(hand2[i]):
                return cards.index(hand1[i]) < cards.index(hand2[i])
        return 'tie'
    if type == isonepair:
        nums1 = onepairbreakdown(hand1)
        nums2 = onepairbreakdown(hand2)
        if cards.index(nums1[0]) != cards.index(nums2[0]):
            return cards.index(nums1[0]) < cards.index(nums2[0])
        else:
            return tiebreakhigh(hand1, hand2)

# ---------------------------------------
# End functions that determine what hand wins
# ---------------------------------------



root = Tk()
root.geometry("480x330")

# Initialize action bottom bar

actionBar = Frame(root, relief=RAISED)
actionBar.pack(side=BOTTOM, fill=X)


# Initialize Draw selection area

selectBar = Frame(root)
selectBar.pack(side=BOTTOM, fill = X)

# Initialize Hand Area

handArea = tk.Frame(root)
handArea.pack(side=BOTTOM, fill=X)
handArea.config(background='black', height=150)

# Initialize playing area

playArea = tk.Frame(root)
playArea.pack(side=TOP, fill = BOTH, expand=1)
playArea.config(background='green')

# Open all of the card images into an array
deckImages = [PIL.ImageTk.PhotoImage(PIL.Image.open('card-gifs/' + deck[i] + '.gif')) for i in range(52)]
back = PIL.ImageTk.PhotoImage(PIL.Image.open('card-gifs/ZB.gif'))

# Create the players and the CPU's initial hand

cardnum = 0
curHand = ''
cpuHand = ''
hand = ['' for i in range(5)]
oppHand = ['' for i in range(5)]
for i in range(5):
    hand[i] = Label(handArea, image=deckImages[cardnum])
    hand[i].pack(side=LEFT, padx = 5, pady = 5)
    oppHand[i] = Label(playArea, image=back)
    oppHand[i].pack(side=LEFT, padx = 5)
    curHand += deck[i]
    cpuHand += deck[51-i]
    cardnum += 1

# Initializes discard buttons

discard = [IntVar() for i in range(5)]
discardButs = ['' for i in range(5)]
for i in range(5):
    discardButs[i] = tk.Checkbutton(selectBar, variable = discard[i])
    discardButs[i].pack(side = LEFT, padx = 35)

# Draw new cards for the player

def drawCards():
    global cardnum
    global discard
    global curHand
    global cpuHand
    for i in range(5):
        if discard[i].get():
            hand[i].configure(image=deckImages[cardnum])
            curHand = curHand[0:i*2] + deck[cardnum] + curHand[i*2+2:]
            cardnum += 1
    drawBut.configure(state = DISABLED)
    resultBut.configure(state = ACTIVE)
    message = ''
    for j in range(10):
        act = nextAct(curHand, cpuHand, functs[j])
        if act == True:
            message = 'You Won! Click to play again'
            break
        elif not act:
            message = 'You lost. Click to play again'
            break
        elif act == 'T':
            if tiebreak(curHand, cpuHand, functs[j]) != 'tie':
                if tiebreak(curHand, cpuHand, functs[j]):
                    message = 'You Won! Click to play again'
                break
            else:
                message = 'Tie! Click to play again'
    resultBut.configure(text = message)
    for i in range(5):
        oppHand[i].configure(image = deckImages[51-i])
    print(curHand, cpuHand)

# Restart the game

def restart():
    shuffle()
    global cardnum
    global cpuHand
    global curHand
    global deckImages
    global hand
    global oppHand
    global discard
    deckImages = [PIL.ImageTk.PhotoImage(PIL.Image.open('card-gifs/' + deck[i] + '.gif')) for i in range(52)]
    cardnum = 0
    cpuHand = ''
    curHand = ''
    for i in range(5):
        discard[i].set(0)
        hand[i].configure(image=deckImages[cardnum])
        oppHand[i].configure(image=back)
        curHand += deck[i]
        cpuHand += deck[51-i]
        cardnum += 1
    resultBut.configure(state = DISABLED, text = "Game in Progress")
    drawBut.configure(state = ACTIVE)

# Create actions on bottom bar

drawBut = tk.Button(actionBar, text = "Discard Selected Cards and Draw New Ones", command = lambda: drawCards())
drawBut.pack(side=LEFT, padx=5, pady=5)

quitBut = tk.Button(actionBar, text = "Exit", command = root.quit)
quitBut.pack(side=RIGHT, padx=5, pady=5)

resultBut = tk.Button(actionBar, text = "Game in Progress", command = lambda: restart(), state = DISABLED)
resultBut.pack(side = LEFT, padx = 5)

root.mainloop()
