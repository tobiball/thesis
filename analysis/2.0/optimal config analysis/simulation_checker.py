import pandas as pd
import random
import numpy as np
import markov_ah_ttest as mat
import json
import math
from random import randrange
from multiprocessing import Process
from numba import jit
import statistics
import copy
from pathlib import Path

mut_gain_array = [0.25, 0.15, 0.25, 0.6, 0.1, 0.6, 0.75, 0.15]

strong_result = 3300 * 5
breaker_cost = 3600 * 5
simulation_depth = 5000
ga_length = 8
processors = 10
name = "all_strategies"
random_array = True
min_value = 0.1
revisions = 100


def prob_simulation(probability_pair):
    clearing = 1
    t_wealth = 0
    data = []
    id = 0
    while id < simulation_depth:
        if clearing < 5:
            prob_pair = random.choices(probability_pair, k=1)
        pG, pT = prob_pair[0][0], prob_pair[0][1]
        # decision = pG > pT * ran.normal(loc=1, scale=0.3) #choice
        mu, sigma = 1, 0.1  # mean and standard deviation
        s = np.random.normal(mu, sigma)
        decision = pG * s > pT * t_wealth  # BUILD AN ERROR
        outcome = "pass"
        if decision:
            result = random.uniform(0, 1)  # result
            outcome = "neutral"
            if result < pG:
                t_wealth += 1
                outcome = "gain"
            elif result < pG + pT:
                t_wealth = 0
                outcome = "loss"
        id += 1
        data.append({"id": id, "pG": pG, "pT": pT, "dec": int(decision), "outcome": outcome, "wealth": float(t_wealth),
                     "tri": float(clearing)})
        clearing += 1
        if clearing == 5 or outcome == "loss":
            clearing = 1
            t_wealth = 0  #

    df = pd.DataFrame(data)
    return (df)

#
# def write_json(old_cost,gain_array,strat_costs,name,process_nr,result_type):
#     data = {old_cost: [gain_array, strat_costs]}
#     base = Path(result_type + name)
#     jsonpath = base / (str(old_cost) + result_type + name + str(process_nr) + ".json")
#     base.mkdir(exist_ok=True)
#     jsonpath.write_text(json.dumps(data))

def engine(process_nr):
    while True:
        arr = mut_gain_array + mut_gain_array[::-1]
        array = np.array(arr).reshape(len(mut_gain_array), 2)
        costs = (mat.markov(prob_simulation(array), array))
        weight_wealth_strat = 1.5
        costs[3] = costs[3] * weight_wealth_strat
        [cost_n, cost_g, cost_t, cost_w] = costs
        sd_costs = round(statistics.stdev(costs))
        cost = sum(costs) + sd_costs

        print("PROCESS" + str(process_nr))
        print("")
        print("this_cost: " + str(cost) + "     naive:" + str(cost_n), "gain:" + str(cost_g),
              "loss:" + str(cost_t), "weighted_wealth:" + str(cost_w), "stddev:" + str(sd_costs))
        print("this_g_array: " + str(array[:, 0]))
        print("")
        print("////////////////////////////////////////////////////////////////////////")
        print("////////////////////////////////////////////////////////////////////////")


if __name__ == '__main__':
    jobs = []
    for process in range(processors):
        p = Process(target=engine, args=[process])
        jobs.append(p)
        p.start()
