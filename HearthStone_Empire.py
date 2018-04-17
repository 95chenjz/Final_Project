import random
import pandas as pd
import warnings
import time
import copy

warnings.filterwarnings("ignore")

dustgetc = 5
dustgetr = 20
dustgete = 100
dustgetl = 400
dustgetgc = 50
dustgetgr = 100
dustgetge = 400
dustgetgl = 1600
dustusec = 40
dustuser = 100
dustusee = 400
dustusel = 1600

class pack_num:

    def __init__(self, quantity:list, probability:list):

        self.quan_list = quantity
        self.prob_list = probability


    @staticmethod
    def open_pack_legendaryrepeat(expansion:list,weights:list):

        level = ['common', 'rare', 'epic', 'legendary', 'goldencommon', 'goldenrare', 'goldenepic', 'goldenlegendary']
        cardsget = []
        cardlevel = random.choices(level, weights, k=5)

        for level in cardlevel:
            if level == 'common' or level == 'goldencommon':
                cardsget.append((level, random.randint(1, expansion[0])))
            elif level == 'rare' or level == 'goldenrare':
                cardsget.append((level, random.randint(1, expansion[1])))
            elif level == 'epic' or level == 'goldenepic':
                cardsget.append((level, random.randint(1, expansion[2])))
            elif level == 'legendary' or level == 'goldenlegendary':
                cardsget.append((level, random.randint(1, expansion[3])))
        return cardsget

    @staticmethod
    def open_empire_pack(expansion:list,weights:list):
        level = ['epic', 'legendary', 'goldenepic', 'goldenlegendary']
        cardsget = []
        cardlevel = random.choices(level, weights, k=5)
        for level in cardlevel:
            if level == 'epic' or level == 'goldenepic':
                cardsget.append((level, random.randint(1, expansion[2])))
            elif level == 'legendary' or level == 'goldenlegendary':
                cardsget.append((level, random.randint(1, expansion[3])))
        return cardsget

    @staticmethod
    def get_dust(cardsget: list, owned: dict, lgd_had: list):

        dust_gain = 0
        dust_needed_decrease=0
        for card in cardsget:

            if card[0] == 'goldencommon':
                dust_gain += dustgetgc

            elif card[0] == 'goldenrare':
                dust_gain += dustgetgr

            elif card[0] == 'goldenepic':
                dust_gain += dustgetge

            elif card[0] == 'goldenlegendary':
                dust_gain += dustgetgl

            elif card[0] == 'common':
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease+= dustusec

                elif owned[card] == 1:
                    owned[card] = 2
                    dust_needed_decrease += dustusec
                else:
                    dust_gain += dustgetc

            elif card[0] == 'rare':
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease += dustuser
                elif owned[card] == 1:
                    owned[card] = 2
                    dust_needed_decrease += dustuser
                else:
                    dust_gain += dustgetr

            elif card[0] == 'epic':
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease += dustusee
                elif owned[card] == 1:
                    owned[card] = 2
                    dust_needed_decrease += dustusee
                else:
                    dust_gain += dustgete

            elif card[0] == 'legendary':
                if card not in owned.keys():
                    owned[card] = 1
                    dust_needed_decrease += dustusel
                    lgd_had.append(card[1])

                else:
                    dust_gain += dustgetl

        return dust_needed_decrease,dust_gain, owned, lgd_had

    def empire_packs_for_all_cards(self,bonus:int):

        quan = copy.copy(self.quan_list)
        prob = copy.copy(self.prob_list)
        bonusprob=[prob[i] for i in (2,3,6,7)]
        owned = {}
        packopened = 0
        dusthave = 0
        dustneeded = 2 * quan[0] * dustusec + 2 * quan[1] * dustuser + 2 * quan[2] * dustusee + quan[3] * dustusel
        lgd_had=[]
        while dustneeded>dusthave:
            packopened+=1
            if packopened%bonus!=0:
                cardsget=self.open_pack_legendaryrepeat(quan, prob)
            else:
                cardsget = self.open_empire_pack(quan, bonusprob)
                print(cardsget)
            dust_needed_decrease, dust_gain, owned, lgd_had=self.get_dust(cardsget, owned, lgd_had)
            dustneeded-=dust_needed_decrease
            dusthave+=dust_gain
        return packopened



if __name__ == '__main__':
    start = time.process_time()
    total = 0
    outcome = []

    frozen = [49,36,27,23]
    weight = [0.7016, 0.2174, 0.0395, 0.0084, 0.0147, 0.0147, 0.0026,0.0011]

    num = pack_num(frozen, weight)

    for i in range(10000):
            # times = num.packs_for_all_cards()
        times = num.empire_packs_for_all_cards(90)
        print(times)
        total += times
            # outcome.append(times)


    print(total/10000)
    elapsed_time = time.process_time() - start
    print(elapsed_time)
