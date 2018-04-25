import random
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import copy


get_dust = {'common': 5, 'rare': 20, 'epic': 100, 'legendary': 400,
            'goldencommon': 50, 'goldenrare': 100,
            'goldenepic': 400, 'goldenlegendary': 1600}

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
        self.quan_list = quantity
        self.prob_list = probability


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
        level = ['common', 'rare', 'epic', 'legendary', 'goldencommon', 'goldenrare', 'goldenepic', 'goldenlegendary']
        cardsget = []
        prob = copy.copy(weights)

        if empire:
            for i in (0,1,4,5):
                prob[i] = 0

        cardlevel = random.choices(level, prob, k=5)

        for level in cardlevel:

            if level == 'common' or level == 'goldencommon':
                cardsget.append((level, random.randint(1, expansion[0])))

            elif level == 'rare' or level == 'goldenrare':
                cardsget.append((level, random.randint(1, expansion[1])))

            elif level == 'epic' or level == 'goldenepic':
                cardsget.append((level, random.randint(1, expansion[2])))

            elif level == 'legendary' or level == 'goldenlegendary':

                if lgd_repeat or (len(lgd_had) >= expansion[3]):
                    cardsget.append((level, random.randint(1, expansion[3])))
                else:
                    cardsget.append(
                            (level, random.choice(list(set(range(1, expansion[3] + 1)).difference(set(lgd_had))))))

        return cardsget


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
        dust_gain = 0
        dust_needed_decrease = 0


        for card in cardsget:
            if card[0] in ['common', 'rare', 'epic']:

                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease+= use_dust[card[0]]

                elif owned[card] == 1:
                    owned[card] = 2
                    dust_needed_decrease += use_dust[card[0]]

                else:
                    dust_gain += get_dust[card[0]]


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




    def dust_for_pack(self, lgd_repeat=True, dust_cost=125):
        """
        Simulate strategy II: use dust for a new pack
        :param lgd_repeat: If true, repeated legendary cards are allowed to show up.
        :param dust_cost: the cost of dust for every pack.
        :return: the number of pack that need to be purchased
        """
        quan = self.quan_list
        prob = self.prob_list
        owned = {}
        packopened = 0
        dusthave = 0
        lgd_had = []

        while (sum(owned.values()) < (sum(quan) * 2 - quan[3])):

            cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)
            packopened += 1

            dust_gain, owned, lgd_had, dust_need_decrease = self.get_dust(cardsget, owned, lgd_had)

            dusthave += dust_gain

            while ((dusthave >= dust_cost) & (sum(owned.values()) < (sum(quan) * 2 - quan[3]))):
                try:
                    cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)

                    dust_gain, owned, lgd_had, dust_need_decrease = self.get_dust(cardsget, owned, lgd_had)
                    dusthave += dust_gain - dust_cost

                except IndexError:
                    print(cardsget, lgd_had)

        return packopened

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
        owned = {}
        packopened = 0
        dusthave = 0
        dustneeded = 2 * quan[0] * list(use_dust.values())[0] + 2 * quan[1] * list(use_dust.values())[1] \
                     + 2 * quan[2] * list(use_dust.values())[2] + quan[3] * list(use_dust.values())[3]
        lgd_had=[]

        while dustneeded>dusthave:
            packopened+=1
            if (packopened/bonus > 1)&(packopened%bonus==0):
                cardsget=self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat, empire=empire)
            else:
                cardsget = self.open_pack(quan, prob, lgd_had, lgd_repeat=lgd_repeat)

            dust_gain, owned, lgd_had,dust_needed_decrease=self.get_dust(cardsget, owned, lgd_had)
            dustneeded-=dust_needed_decrease
            dusthave+=dust_gain
        return packopened
