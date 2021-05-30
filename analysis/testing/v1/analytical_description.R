# Title     : Analytical Description
# Objective : Regress experimental subject data on computational models and compare model fits for different treatments
# Created by: tobi
# Created on: 08/05/2021

#________________________________-
#The purpose of this script is to predict decisions from a foraging experiment with different models
#The  experiment uses 3 models with one predictor
  #Game-optimal model: Optimal for the defined boundaries of the experiment.
  #Gain/Threat heursitic: Uses gain/threat probability to predict the behaviour.

#The game-optimal model has been algorithmically calculated in analysis/policy_calculations/markov_decsion_tree.py
#This script:
#1. Imports the behavioural data    DONE
#2. Cleans the data   DONE
#3. Imports the computational model   DONE
#4. Joins all data in data_frame    DONE
#5. Regresses behavioural data on the three models DONE
#6. Compares the predictive quality of the models DONE
#7. Investigate if a model combining optimal and one of the probability heursitics yields best result
#8. Compare best predictive models between treatments HOW?

library(dplyr)
library(foreign)
library(xtable)

model_fit_evaluation <- function(behavioural_data) {
  #Load data to dataframe
  df_behaviour_raw <- read.csv(behavioural_data)

  #Remove na participants
  df_behaviour_raw <- head(df_behaviour_raw,4)

  #Equalise all trial times to compare all trials simultaniously reegardless of rounds
  df_behaviour <- setNames(data.frame(matrix(ncol = 6, nrow = 0)), c("participant_id", "player_choice", "probability_gain","probability_threat","payoff","clearing_nr"))
  for (num in 1:8)   ###Derive forrest from trial_nr, required for payoff calculation
    {
      row_index <- (num-1) * 4
    df_behaviour[(row_index + 1):(row_index+4),1:6] <- (df_behaviour_raw[
                          c(
                            "participant.id_in_session",
                            paste(c("foraging_test.", num, ".player.foraging_choice"), collapse = ""),
                            paste(c("foraging_test.", num, ".player.probability_gain"), collapse = ""),
                            paste(c("foraging_test.", num, ".player.probability_threat"), collapse = ""),
                            paste(c("foraging_test.", num, ".player.payoff"), collapse = ""),
                            paste(c("foraging_test.", num, ".player.clearing_number"), collapse = "")
                          )
        ])
      df_behaviour[(row_index + 1):(row_index+4),"forrest_nr"] <- ((df_behaviour_raw[paste(c("foraging_test.", num, ".player.trial_in_game"), collapse = "")])+3)   %/% 4
    }

  #introduces a cumulative sum showing the payoff of a participant up to that point in the forrest
  df_behaviour <- df_behaviour %>%
         group_by(forrest_nr,participant_id) %>%
         mutate(wealth_state = cumsum(payoff) - payoff)

  #Get optimal policy decsion from python script
  df_optimal_policy <- (read.csv('../../beta_analysis/optimal_policy.csv'))

  #Combine real with policy results in data_frame
  df_combined <- dplyr::left_join(df_behaviour,df_optimal_policy)

  #Regress optimal policy on choices
  model_optimal <- lm(df_combined$player_choice~df_combined$choice)

  #Do the same for gain and threat heursitc
  model_gain <- lm(df_combined$player_choice~df_combined$probability_gain)
  model_threat <- lm(df_combined$player_choice~df_combined$probability_threat)

  #Retain models BIC's in data_frame
  bic_summary <- data.frame(Model = c("model_optimal", "model_gain", "model_threat"),
  BIC = c(BIC(model_optimal), BIC(model_gain), BIC(model_threat)), stringsAsFactors = FALSE)

  #Select best model
  #TODO

  #Test best model in combination with other models
  #TODO

  #Return all evaluated models in table
  return(bic_summary)

}

#Run model fit function to get BIC's table (and best models)
model_fit_evaluation("behavioural_data_control_group.csv")

#Compare models of different treatments with each other
#TODO -> run for loop over treatment data_frames and select method for comparison