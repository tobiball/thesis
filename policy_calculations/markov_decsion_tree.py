

days = {'day_4':[0,1,2,3],'day_3':[0,1,2],'day_2':[0,1],'day_1':[0]}

# days = {'day_3':[0,1,2],'day_2':[0,1],'day_1':[0]}
expected_future_states = [0,1,2,3,4]

gain_probabilities = [0.15,0.30,0.45,0.6]
loss_probabilities = [0.1,0.2,0.3,0.4]
results = {'forage':0,'indifferent':0,'wait':0}
expected_outcome_by_wealth_state = {}
nodes = {}

for day in days:
    for wealth_state in days[day]: #wealth_state is the  amount of mushroomes foraged up to this stage
        probability_states = 0
        expected_outcome_for_states = 0
        for Pg in gain_probabilities:
            for Pd in loss_probabilities:
                A0 = expected_future_states[wealth_state]
                AG = expected_future_states[wealth_state + 1]
                probability_states += 1
                expected_relative_return_on_foraging = Pg * AG - (Pg + Pd) * A0 #return on foraging, taking into account wealth_state
                if expected_relative_return_on_foraging > 0:
                    action = 'forage'
                    returns = Pg * AG + (1 - Pg - Pd) * A0 - wealth_state
                    expected_outcome_for_states += returns
                elif expected_relative_return_on_foraging < 0:
                    action = 'wait'
                    returns = A0 - wealth_state
                    expected_outcome_for_states += returns
                else:
                    action = 'indifferent'
                results[action] += 1
                nodes[(day, Pg, Pd, wealth_state)] = {(AG, A0,(Pg * AG) + (1 - Pg - Pd) * A0 - wealth_state, action)}
        expected_outcome = expected_outcome_for_states / probability_states + wealth_state
        expected_future_states[wealth_state] = expected_outcome
        expected_outcome_by_wealth_state[wealth_state,day] = expected_outcome

for node in nodes:
    print(node,nodes[node])
print(expected_outcome_by_wealth_state)
print(results)