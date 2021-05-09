# Title     : Analytical Description
# Objective : Regress experimental subject data on computational models and compare models
# Created by: tobi
# Created on: 08/05/2021

#________________________________-
#The purpose of this script is to predict decsions from a foraging experiment with different models
#The  experiment uses 3 models
  #Game-optimal model: Optimal for the defined boundaries of the experiment.
  #Gain/Threat heursitic: Uses gain/threat probability to predict the behaviour.

#The game-optimal model has been algorythmically calculated in analysis/policy_calculations/markov_decsion_tree.py
#This script:
#1. Imports the behavioural data    DONE
#2. Cleans the data   DONE
#3. Imports the computational model   DONE
#4. Joins all data in data_frame    JOIN IS INCOMPLETE
#5. Regresses behavioural data on the three models
#6. Compares the predictive quality of the models

library(dplyr)

#########--PURPOSE--########
#This analysis


#Load data to dataframe
tt <- read.csv("all_apps_wide-2021-05-07.csv")

#Remove na participants
tt <- head(tt,4)

#Equalise all trial times to compare all trials simultaniously
df <- setNames(data.frame(matrix(ncol = 6, nrow = 0)), c("participant_id", "player_choice", "probability_threat","probability_gain","payoff","clearing_nr"))
for (num in 1:8)   ###Derive forrest from trial_nr, required for payoff calculation
  {
    row_index <- (num-1) * 4
  df[(row_index + 1):(row_index+4),1:6] <- (tt[
                        c(
                          "participant.id_in_session",
                          paste(c("foraging_test.", num, ".player.foraging_choice"), collapse = ""),
                          paste(c("foraging_test.", num, ".player.probability_gain"), collapse = ""),
                          paste(c("foraging_test.", num, ".player.probability_threat"), collapse = ""),
                          paste(c("foraging_test.", num, ".player.payoff"), collapse = ""),
                          paste(c("foraging_test.", num, ".player.clearing_number"), collapse = "")
                        )
      ])
    df[(row_index + 1):(row_index+4),"forrest_nr"] <- ((tt[paste(c("foraging_test.", num, ".player.trial_in_game"), collapse = "")])+3)   %/% 4 ## convert real round number back to forrest, THIS HAS TO SOMEHOW BE AN ENTIRE COLUMN OPERATION

  }

#introduces a cumulative sum showing the payoff of a participant up to that point in the forrest
df <- df %>%
       group_by(forrest_nr,participant_id) %>%
       mutate(wealth_state = cumsum(payoff) - payoff)

#Get optimal policy decsion from python script
optimal_policy = (read.csv('optimal_policy.csv'))

#Combine real with policy results in dataframe
df_combined <- left_join(x = df, y = optimal_policy, by = c("probability_gain" , "probability_threat", "wealth_state","clearing_nr"), all.x=TRUE)

#Regress optimal policy on choices
optimal_model <- lm(df~df_combined)


#Do the same for threat and gain heursitc

