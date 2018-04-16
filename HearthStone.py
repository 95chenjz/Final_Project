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
    def open_pack(expansion:list,weights:list,lgd_had:list):

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

                cardsget.append(
                    (level, random.choice(list(set(range(1, expansion[3] + 1)).difference(set(lgd_had))))))

        return cardsget



    def packs_for_all_cards(self):

        quan = self.quan_list
        prob = self.prob_list
        owned = {}
        packopened = 0
        dustneeded = 2 * quan[0] * dustusec + 2 * quan[1] * dustuser + 2 * quan[2] * dustusee + quan[3] * dustusel
        dusthave = 0
        lgd_had = []

        while dustneeded > dusthave:

            cardsget = self.open_pack(quan, prob, lgd_had)

            packopened += 1

            for card in cardsget:

                if card[0] == 'goldencommon':
                    dusthave += dustgetgc

                elif card[0] == 'goldenrare':
                    dusthave += dustgetgr

                elif card[0] == 'goldenepic':
                    dusthave += dustgetge

                elif card[0] == 'goldenlegendary':
                    dusthave += dustgetgl

                elif card[0] == 'common':
                    if card not in owned.keys():
                        owned[card] = 1
                        dustneeded -= dustusec
                    elif owned[card] == 1:

                        owned[card] = 2
                        dustneeded -= dustusec
                    else:
                        dusthave += dustgetc

                elif card[0] == 'rare':
                    if card not in owned.keys():
                        owned[card] = 1
                        dustneeded -= dustuser
                    elif owned[card] == 1:
                        owned[card] = 2
                        dustneeded -= dustuser
                    else:
                        dusthave += dustgetr

                elif card[0] == 'epic':
                    if card not in owned.keys():
                        owned[card] = 1
                        dustneeded -= dustusee
                    elif owned[card] == 1:
                        owned[card] = 2
                        dustneeded -= dustusee
                    else:
                        dusthave += dustgete

                elif card[0] == 'legendary':
                    if card not in owned.keys():
                        owned[card] = 1
                        dustneeded -= dustusel
                        lgd_had.append(card[1])
                    else:
                        dusthave += dustgetl

        return packopened


    @staticmethod
    def get_dust(cardsget: list, owned: dict, lgd_had: list):

        dust_gain = 0

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
                    # dustneeded -= dustusec

                elif owned[card] == 1:
                    owned[card] = 2
                    # dustneeded -= dustusec
                else:
                    dust_gain += dustgetc

            elif card[0] == 'rare':
                if card not in owned.keys():
                    owned[card] = 1
                    # dustneeded -= dustuser
                elif owned[card] == 1:
                    owned[card] = 2
                    # dustneeded -= dustuser
                else:
                    dust_gain += dustgetr

            elif card[0] == 'epic':
                if card not in owned.keys():
                    owned[card] = 1
                    # dustneeded -= dustusee
                elif owned[card] == 1:
                    owned[card] = 2
                    # dustneeded -= dustusee
                else:
                    dust_gain += dustgete

            elif card[0] == 'legendary':
                if card not in owned.keys():
                    owned[card] = 1
                    # dustneeded -= dustusel
                    lgd_had.append(card[1])

                else:
                    dust_gain += dustgetl

        return dust_gain, owned, lgd_had




    def dust_for_pack(self):
        """

        :return:
        """
        quan = copy.copy(self.quan_list)
        prob = copy.copy(self.prob_list)
        owned = {}
        packopened = 0
        # dustneeded = 2 * quan[0] * dustusec + 2 * quan[1] * dustuser + 2 * quan[2] * dustusee + quan[3] * dustusel
        dusthave = 0
        lgd_had = []

        while (sum(owned.values()) < 247):
            # print(sum(owned.values()))

            if (len(lgd_had) == quan[3]):
                prob[3] = prob[7] = 0

            cardsget = self.open_pack(quan, prob, lgd_had)
            packopened += 1


            dust_gain, owned, lgd_had = self.get_dust(cardsget, owned, lgd_had)

            dusthave += dust_gain

            while ((dusthave >= 100) & (sum(owned.values()) < 247)):
                try:
                    if (len(lgd_had) == quan[3]):
                        prob[3] = prob[7] = 0

                    cardsget = self.open_pack(quan, prob, lgd_had)
                    # print(owned)
                    dust_gain, owned, lgd_had = self.get_dust(cardsget, owned, lgd_had)
                    dusthave += dust_gain - 100


                except IndexError:
                    print(cardsget, lgd_had)


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
        times = num.dust_for_pack()
        # print(times)
        total += times
            # outcome.append(times)


    print(total/10000)
    elapsed_time = time.process_time() - start
    print(elapsed_time)