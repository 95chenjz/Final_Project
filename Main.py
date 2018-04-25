from HearthStone import pack_num
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from Simulation import simulate
import warnings

warnings.filterwarnings("ignore")


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
