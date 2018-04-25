import random
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import copy

# remove the warnings in the output caused by different versions
warnings.filterwarnings("ignore")

# dust values got by disenchanting cards
get_dust = {'common': 5, 'rare': 20, 'epic': 100, 'legendary': 400,
            'goldencommon': 50, 'goldenrare': 100,
            'goldenepic': 400, 'goldenlegendary': 1600}

# dust values needed to craft cards
use_dust = {'common': 40, 'rare': 100, 'epic': 400, 'legendary': 1600}

class pack_num:
    """
    This class includes the methods of the process of collecting a full set of hearthstone expansion.
    It is simulated by a complete Monte Carlo process. Three strategy could be selected with
    different methods or parameters.
    """

    def __init__(self, quantity:list, probability:list):
        """
        Set default card list the probability of every card class
        :param quantity: a list of the number of each card in a expansion
        :param probability: a list of probability of every card class
        """
        # the maximum numbers of each card type that a player can have
        self.quan_list = quantity
        # the probabilities of opening each card type
        self.prob_list = probability

    # the cards got when opening a pack
    @staticmethod
    def open_pack(expansion:list,weights:list,lgd_had:list, empire=False, lgd_repeat=True):
        """
        Simulate the process of open a new pack of 5 cards.
        :param expansion: a list of expansion cards
        :param weights: a list of probabilities
        :param lgd_had: already-owned legend cards
        :param empire: if true, switch to strategy III
        :param lgd_repeat: If true, repeated legend cards will not appear until all legend card are collected
        :return: a list of 5 new cards (class, NO.).
        """

        # eight card types in Hearthstone
        level = ['common', 'rare', 'epic', 'legendary', 'goldencommon', 'goldenrare', 'goldenepic', 'goldenlegendary']
        # the list of cards got
        cardsget = []
        # the probabilities of opening each card type
        prob = copy.copy(weights)

        # if it is a bonus pack, you will only get epic and legendary cards
        if empire:
            # change the probabilities of opening common, rare, goldencommon and goldenrare into zero
            for i in (0,1,4,5):
                prob[i] = 0

        # random select five card types in all types according to the probabilities
        cardlevel = random.choices(level, prob, k=5)

        for level in cardlevel:

            # add a common card to the list of cards already got
            if level == 'common' or level == 'goldencommon':
                cardsget.append((level, random.randint(1, expansion[0])))

            # add a rare card to the list of cards already got
            elif level == 'rare' or level == 'goldenrare':
                cardsget.append((level, random.randint(1, expansion[1])))

            # add a epic card to the list of cards already got
            elif level == 'epic' or level == 'goldenepic':
                cardsget.append((level, random.randint(1, expansion[2])))

            # add a legendary card to the list of cards already got
            elif level == 'legendary' or level == 'goldenlegendary':

                # lgd_repeat == false means that every time you open a Legendary in a card pack,
                # it will be a Legendary card from the same set that you don’t already own.

                # lgd_repeat == true
                if lgd_repeat or (len(lgd_had) >= expansion[3]):
                    cardsget.append((level, random.randint(1, expansion[3])))
                # lgd_repeat == false
                else:
                    cardsget.append(
                            (level, random.choice(list(set(range(1, expansion[3] + 1)).difference(set(lgd_had))))))

        return cardsget

    # automatically disenchant the repeated cards into dust
    @staticmethod
    def get_dust(cardsget: list, owned: dict, lgd_had: list):
        """
        Get dust from repeated cards.
        :param cardsget: a list of 5 new cards
        :param owned: a dict of cards we have already had.
        :param lgd_had: a list of owned legend cards
        :return: dust_gain - total dust get from the pack,
                    owned - a dict of cards we have already had
                    lgd_had - a list of owned legend cards
                    dust_needed_decrease - deduction from total dust we need
        """

        # dust you already got
        dust_gain = 0
        # the decreased value of needed dust
        dust_needed_decrease = 0

        # if the cards got in this pack have exceeded the maximum number of
        # corresponding card type that a player can have
        for card in cardsget:
            if card[0] in ['common', 'rare', 'epic']:
                # you did not have this card, add a new one
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease+= use_dust[card[0]]
                # you had only one this card, add a new one
                elif owned[card] == 1:
                    owned[card] = 2
                    dust_needed_decrease += use_dust[card[0]]
                # you already had two this cards, disenchant this new card
                else:
                    dust_gain += get_dust[card[0]]

            # every time you open a Legendary in a card pack, it will be a Legendary card
            # from the same set that you don’t already own.
            elif card[0] == 'legendary':
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease += use_dust[card[0]]
                    lgd_had.append(card[1])

                else:
                    dust_gain += get_dust[card[0]]

            else:
                dust_gain = get_dust[card[0]]

        return dust_gain, owned, lgd_had, dust_needed_decrease


    # exchange dust for a pack
    def dust_for_pack(self, lgd_repeat=True, dust_cost=125):
        """
        Simulate strategy II: use dust for a new pack
        :param lgd_repeat: If true, repeated legendary cards are allowed to show up.
        :param dust_cost: the cost of dust for every pack.
        :return: the number of pack that need to be purchased
        """
        quan = self.quan_list
        prob = self.prob_list
        # cards you already had
        owned = {}
        # the number of packs you have opened
        packopened = 0
        # the value of dust you have
        dusthave = 0
        # the list of legendary cards you already have
        lgd_had = []

        # while the value of dust you have is smaller than the value of dust you need to craft all the cards
        while (sum(owned.values()) < (sum(quan) * 2 - quan[3])):

            # open a pack
            cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)
            packopened += 1

            # disenchant repeated cards
            dust_gain, owned, lgd_had, dust_need_decrease = self.get_dust(cardsget, owned, lgd_had)

            # add the dust you got from the last step to the dust you already have
            dusthave += dust_gain

            while ((dusthave >= dust_cost) & (sum(owned.values()) < (sum(quan) * 2 - quan[3]))):
                try:
                    cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)

                    dust_gain, owned, lgd_had, dust_need_decrease = self.get_dust(cardsget, owned, lgd_had)
                    dusthave += dust_gain - dust_cost

                except IndexError:
                    print(cardsget, lgd_had)

        return packopened

    # exchange dust for crafting a card
    def dust_for_cards(self, empire = False, lgd_repeat = True, bonus = 115):
        """
        Simulate strategy I & III: use dust for specific cards
        :param empire: If true, Strategy III
        :param lgd_repeat: If true, repeated legendary cards are allowed to show up.
        :param bonus:
        :return: the number of pack that need to be purchased
        """

        quan = copy.copy(self.quan_list)
        prob = copy.copy(self.prob_list)

        # cards you already had
        owned = {}

        # number of packs you have opened
        packopened = 0

        # value of dust you have
        dusthave = 0

        # the value of dust you need to craft all the cards
        dustneeded = 2 * quan[0] * list(use_dust.values())[0] + 2 * quan[1] * list(use_dust.values())[1] \
                     + 2 * quan[2] * list(use_dust.values())[2] + quan[3] * list(use_dust.values())[3]

        # legendary cards you already had
        lgd_had=[]

        # while the value of dust you have is smaller than the value of dust you need to craft all the cards
        while dustneeded>dusthave:
            # open a new pack
            packopened+=1
            # open a bonus pack
            if (packopened/bonus > 1)&(packopened%bonus==0):
                cardsget=self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat, empire=empire)
            # open a normal pack
            else:
                cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)
                # print(cardsget)
            # disenchant repeated cards
            dust_gain, owned, lgd_had,dust_needed_decrease=self.get_dust(cardsget, owned, lgd_had)
            # cut the dust you got from the last step to the dust you need
            dustneeded-=dust_needed_decrease
            # add the dust you got from the last step to the dust you already have
            dusthave+=dust_gain
        return packopened
