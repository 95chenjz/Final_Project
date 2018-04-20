from HearthStone import pack_num
import numpy as np
import math
import matplotlib.pyplot as plt

def simulate(pack_num, lgd_repeat=False):
    outcome = []
    mean = []

    y_error = []
    for k in range(10, 110, 10):
        for i in range(k):
            times = pack_num.dust_for_pack(lgd_repeat=lgd_repeat)
            # print(times)
            outcome.append(times)
        mean.append(np.mean(outcome))
        variance = np.var(outcome)
        confidence_interval_low = 1.96 * np.mean(outcome) - math.sqrt(variance)
        confidence_interval_high = 1.96 * np.mean(outcome) + math.sqrt(variance)
        y_error.append(confidence_interval_high - confidence_interval_low)

    # print(outcome)
    print(mean)
    print(y_error)

    plt.figure()
    x = list(range(10, 110, 10))
    plt.errorbar(x, mean, yerr=y_error)
    plt.show()


