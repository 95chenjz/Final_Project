from HearthStone import pack_num
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from Simulation import simulate

if __name__ == '__main__':
    start = time.process_time()
    total = 0
    outcome = []

    frozen = [49,36,27,23]
    weight = [0.7016, 0.2174, 0.0395, 0.0084, 0.0147, 0.0147, 0.0026,0.0011]

    num = pack_num(frozen, weight)
    # print(sum(frozen)*2-frozen[3])

    # simulate(num)
    #
    for i in range(50):
        times = num.dust_for_cards(lgd_repeat=False, empire=True)
        # times = num.dust_for_pack(lgd_repeat=False)
        print(times)
        total += times
        outcome.append(times)


    print(total/50)
    # elapsed_time = time.process_time() - start
    # print(elapsed_time)


    # ax = sns.distplot(outcome)
    # mu = np.mean(outcome)
    # sigma = math.sqrt(np.var(outcome))
    #
    # clrs = [sns.xkcd_rgb['pale red'],
    #         sns.xkcd_rgb['dusty purple'],
    #         sns.xkcd_rgb['pale red']]
    #
    #
    #
    # ax.vlines([mu - sigma, mu, mu + sigma], 0.0, [0.35, 0.55, 0.35], linestyle='-.',
    #           colors= clrs, alpha=0.5)
    #
    # ax.set(title='Distribution of the Number of Packs in the First Strategy',
    #        xlabel='Packs', ylabel='Probability')
    #
    # sns.despine(offset=5, trim=True)
    # plt.show()