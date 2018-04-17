import random
import pandas as pd
import warnings
import time


warnings.filterwarnings("ignore")

get_dust = {'common': 5, 'rare': 20, 'epic': 100, 'legendary': 400,
            'goldencommon': 50, 'goldenrare': 100,
            'goldenepic': 400, 'goldenlegendary': 1600}

use_dust = {'common': 40, 'rare': 100, 'epic': 400, 'legendary': 1600}

class pack_num:

    def __init__(self, quantity:list, probability:list):

        self.quan_list = quantity
        self.prob_list = probability


    @staticmethod
    def open_pack(expansion:list,weights:list,lgd_had:list, empire=False, lgd_repeat=True):

        level = ['common', 'rare', 'epic', 'legendary', 'goldencommon', 'goldenrare', 'goldenepic', 'goldenlegendary']
        cardsget = []
        prob = weights

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




    def dust_for_pack(self, lgd_repeat=True, dust_cost=140):
        """

        :return:
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

    def dust_for_cards(self, empire = False, lgd_repeat = True, bonus = 40):

        quan = self.quan_list
        prob = self.prob_list
        owned = {}
        packopened = 0
        dusthave = 0
        dustneeded = 2 * quan[0] * list(use_dust.values())[0] + 2 * quan[1] * list(use_dust.values())[1] \
                     + 2 * quan[2] * list(use_dust.values())[2] + quan[3] * list(use_dust.values())[3]
        lgd_had=[]

        while dustneeded>dusthave:
            packopened+=1
            if (packopened/bonus > 1)&(packopened%bonus==0):
                cardsget=self.open_pack(quan, prob, lgd_had,lgd_repeat=lgd_repeat,empire=empire)
            else:
                cardsget = self.open_pack(quan, prob, lgd_had,lgd_repeat=lgd_repeat)
                # print(cardsget)
            dust_gain, owned, lgd_had,dust_needed_decrease=self.get_dust(cardsget, owned, lgd_had)
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
    # print(sum(frozen)*2-frozen[3])
    for i in range(10000):
        times = num.dust_for_cards(lgd_repeat=False)
        # times = num.dust_for_pack(lgd_repeat=False)
        print(times)
        total += times
            # outcome.append(times)


    print(total/10000)
    elapsed_time = time.process_time() - start
    print(elapsed_time)