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

simulation_extent = 50
strong_result = 350 * simulation_extent
breaker_cost1 = 370 * simulation_extent
breaker_cost2 = 360 * simulation_extent

simulation_depth = 100 * simulation_extent
ga_length = 8
processors = 14
name = "all_strategies_norm"
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


def write_json(old_cost, gain_array, strat_costs, sd_costs, name, process_nr, result_type):
    for c in range(len(strat_costs)):
        strat_costs[c] = normaliser(strat_costs[c])
    old_cost = normaliser(old_cost)
    data = {old_cost: [{"prob_set ":gain_array, "naive/gain/loss/wealth ":strat_costs,"sd ":sd_costs}]}
    base = Path(result_type + name)
    jsonpath = base / (str(old_cost) + result_type + name + str(process_nr) + ".json")
    base.mkdir(exist_ok=True)
    jsonpath.write_text(json.dumps(data))


def normaliser(result):
    norm_result = round(result / simulation_extent,2)
    return norm_result


def engine(process_nr):
    while True:
        gain_array = [0] * ga_length
        # gain_array = [0.3,0.25,0.25,0.2,0.4,0.35,0.35,0.3]
        broken_garry = random_array
        # array building loop
        while broken_garry:
            for pos in range(ga_length):
                gain_array[pos] = round(random.choice(np.arange(min_value, 1 - min_value, 0.05)), 2)
            # check array adhers to rules
            garry = np.array(gain_array).reshape(int(ga_length / 2), 2)
            broken_garry = False
            for arrs in garry:
                if sum(arrs) > 1 or arrs[0] == arrs[1]:  # no eq
                    broken_garry = True
                    break
        rev_count = 0
        old_cost = simulation_depth * 8
        simulate = True

        # optimisation logic
        mut_gain_array = []
        while simulate:
            rand_position = randrange(len(gain_array))
            increm = random.choice([-0.05, 0.05, -0.1, 0.1, -0.15, 0.15, -0.2, 0.2, -0.25, 0.25])
            mut_gain_array = copy.copy(gain_array)
            mut_gain_array[rand_position] += increm
            mut_gain_array[rand_position] = round(mut_gain_array[rand_position], 2)
            arr = mut_gain_array + mut_gain_array[::-1]  # mirror gain array on itself
            array = np.array(arr).reshape(len(mut_gain_array), 2)
            changed_pair = array[math.floor(rand_position / 2)]

            if not (not (min_value <= mut_gain_array[rand_position] <= 1 - min_value) or not (
                    sum(changed_pair) <= 1) or not (
                    round(changed_pair[0], 2) != round(changed_pair[1], 2))):  # no new equal pairs
                costs = (mat.markov(prob_simulation(array), array))
                weight_wealth_strat = 1.5
                costs[3] = costs[3] * weight_wealth_strat
                [cost_n, cost_g, cost_t, cost_w] = costs
                sd_costs = round(statistics.stdev(costs))
                cost = sum(costs) + sd_costs
                # cost = cost_w

                if cost < old_cost:
                    # gain_array = mut_gain_array
                    old_cost = cost
                    strat_costs = [cost_n, cost_g, cost_t, cost_w]
                    rev_count = 0
                    result_type = "simulation_log_"
                    write_json(old_cost, gain_array, strat_costs,sd_costs, name, process_nr, result_type)

                else:
                    rev_count += 1
                    if rev_count == revisions or \
                            rev_count == round(revisions / 4) and old_cost > breaker_cost1 or \
                            rev_count == round(revisions / 2) and old_cost > breaker_cost2:

                        if old_cost < strong_result:
                            result_type = "optimised_setup_"
                            write_json(old_cost, gain_array, strat_costs,sd_costs, name, process_nr, result_type)
                            rev_count = 0
                        simulate = False

                print("PROCESS {} \nthis cost: {}      naive: {} gain: {} loss: {} weighted_wealth: {} stdev: {} "
                      "\nthis_g_array: {} \n\ntop_cost: {}\ntop_g_array: {}\nreversed: {}".format(
                        process_nr,
                        normaliser(cost),
                        normaliser(cost_n),
                        normaliser(cost_g),
                        normaliser(cost_t),
                        normaliser(cost_w),
                        normaliser(sd_costs),
                        array[:, 0],
                        normaliser(old_cost),
                        gain_array,
                        rev_count
                ))
                print("/"*50)
                print("/"*50)


if __name__ == '__main__':
    jobs = []
    for process in range(processors):
        p = Process(target=engine, args=[process])
        jobs.append(p)
        p.start()
