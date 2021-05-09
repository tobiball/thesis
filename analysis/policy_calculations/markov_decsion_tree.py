import pandas as pd
from tabulate import tabulate


days = {4:[0,1,2,3],3:[0,1,2],2:[0,1],1:[0]}

# days = {'day_3':[0,1,2],'day_2':[0,1],'day_1':[0]}
expected_future_states = [0,1,2,3,4]

gain_probabilities = [0.15,0.30,0.45,0.6]
loss_probabilities = [0.1,0.2,0.3,0.4]
results = {1:0,'indifferent':0,0:0}  #foraging action choices
expected_outcome_by_wealth_state = {}
nodes = []
df = pd.DataFrame()
df_index = 0

for day in days:
    for wealth_state in days[day]: #wealth_state is the  amount of mushroomes foraged up to this stage
        probability_states = 0
        expected_outcome_for_states = 0
        for Pg in gain_probabilities:
            for Pd in loss_probabilities:
                df_index += 1
                A0 = expected_future_states[wealth_state]
                AG = expected_future_states[wealth_state + 1]
                probability_states += 1
                expected_relative_return_on_foraging = Pg * AG - (Pg + Pd) * A0 #return on foraging, taking into account wealth_state
                if expected_relative_return_on_foraging > 0:
                    action = 1
                    returns = Pg * AG + (1 - Pg - Pd) * A0 - wealth_state
                    expected_outcome_for_states += returns
                elif expected_relative_return_on_foraging < 0:
                    action = 0
                    returns = A0 - wealth_state
                    expected_outcome_for_states += returns
                else:
                    action = 'indifferent'
                results[action] += 1
             #   nodes[(day, Pg, Pd, wealth_state)] = {(AG, A0,(Pg * AG) + (1 - Pg - Pd) * A0 - wealth_state, action)}
                nodes.append({'df_index':df_index,'day':day,"wealth_state":wealth_state,"probability_gain":Pg,"probability_threat":Pd,"choice":action})

        expected_outcome = expected_outcome_for_states / probability_states + wealth_state
        expected_future_states[wealth_state] = expected_outcome
        expected_outcome_by_wealth_state[wealth_state,day] = expected_outcome
df = pd.DataFrame(nodes).set_index(["df_index"])
# for node in nodes:
#     print(node,nodes[node])
# print(expected_outcome_by_wealth_state)
# print(results)
print(tabulate(df, headers='keys', tablefmt='psql'))

df.to_csv('optimal_policy.csv')

