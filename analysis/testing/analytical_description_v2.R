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

# model_fit_evaluation <- function(behavioural_data) {
#Load data to dataframe
df_behaviour_raw <- read.csv('all_apps_wide-2021-05-18.csv')

#Remove na participants
# df_behaviour_raw <- head(df_behaviour_raw,4)

#Equalise all trial times to compare all trials simultaniously reegardless of rounds
df_behaviour <- setNames(data.frame(matrix(ncol = 7, nrow = 0)), c("participant_id", "treatment", "player_choice", "probability_gain","probability_threat","payoff","clearing_nr"))
for (num in 1:16)   ###Derive forrest from trial_nr, required for payoff calculation
  {
    row_index <- (num-1) * 100
df_behaviour[(row_index + 1):(row_index+100),1:7] <- (df_behaviour_raw[
                      c(
                        "participant.id_in_session",
                        paste(c("foraging_simulation.", num, ".player.treatment"), collapse = ""),
                        paste(c("foraging_simulation.", num, ".player.foraging_choice"), collapse = ""),
                        paste(c("foraging_simulation.", num, ".player.probability_gain"), collapse = ""),
                        paste(c("foraging_simulation.", num, ".player.probability_threat"), collapse = ""),
                        paste(c("foraging_simulation.", num, ".player.payoff"), collapse = ""),
                        paste(c("foraging_simulation.", num, ".player.clearing_number"), collapse = "")
                      )
    ])
  df_behaviour[(row_index + 1):(row_index+100),"forrest_nr"] <- ((df_behaviour_raw[paste(c("foraging_simulation.", num, ".player.trial_in_game"), collapse = "")])+3)   %/% 4
}

#introduces a cumulative sum showing the payoff of a participant up to that point in the forrest
df_behaviour <- df_behaviour %>%
       group_by(forrest_nr,participant_id) %>%
       mutate(wealth_state = cumsum(payoff) - payoff)

#Get optimal policy decsion from python script
df_optimal_policy <- (read.csv('optimal_policy.csv'))

#Combine real with policy results in data_frame
df_combined <- dplyr::left_join(df_behaviour,df_optimal_policy)

# best_models_for_treatments <- list()
# i <- 1
#
# for (treatment in list('joy','control'))
# {
#   #Regress optimal policy on choices for treatments
#   model_optimal <- lm(df_combined$player_choice~df_combined$optimal_choice,subset = df_combined$treatment == treatment)
#
#   #Do the same for gain and threat heursitc
#   model_gain <- lm(df_combined$player_choice~df_combined$probability_gain,subset = df_combined$treatment == treatment)
#
#   model_threat <- lm(df_combined$player_choice~df_combined$probability_threat,subset = df_combined$treatment == treatment)
#
#   #Find one variable models with lowest BIC
#   best_model_one_nr <- (which.min(c(BIC(model_optimal), BIC(model_gain), BIC(model_threat))))
#
#   #find one or two variable model with best BIC
#   if (best_model_one_nr == 1){
#     best_model_one <- model_optimal
#     model_optimal_gain <- lm(df_combined$player_choice~df_combined$optimal_choice + df_combined$probability_gain,subset = df_combined$treatment == treatment)
#     model_optimal_threat <- lm(df_combined$player_choice~df_combined$optimal_choice + df_combined$probability_threat,subset = df_combined$treatment == treatment)
#     best_model_nr <- (which.min(c(BIC(best_model_one), BIC(model_optimal_gain), BIC(model_optimal_threat))))
#     best_model <- list(best_model_one, model_optimal_gain, model_optimal_threat)[[best_model_nr]]
#   }else if (best_model_one_nr == 2){
#     best_model_one <- model_gain
#     model_gain_optimal <- lm(df_combined$player_choice~df_combined$probability_gain + df_combined$optimal_choice,subset = df_combined$treatment == treatment)
#     best_model_nr <- (which.min(c(BIC(best_model_one), BIC(model_gain_optimal))))
#     best_model <- list(best_model_one, model_gain_optimal)[[best_model_nr]]
#   }else{
#     best_model_one <- model_threat
#     model_threat_optimal <- lm(df_combined$player_choice~df_combined$probability_threat + df_combined$optimal_choice,subset = df_combined$treatment == treatment)
#     best_model_nr <- (which.min(c(BIC(best_model_one), BIC(model_threat_optimal))))
#     best_model <- list(best_model_one,  model_threat-optimal)[[best_model_nr]]
#   }

  #Iteratively create list of best models for each treatments
#   best_models_for_treatments[[i]] <- best_model
#   i <- i + 1
# }

# print('--------Best Model Joy:----------')
# summary(best_models_for_treatments[[1]])
#
#
# print('--------Best Model Control:----------')
# summary(best_models_for_treatments[[2]])

#SHOWS THAT DIFFERENT MODELS ARE BEST SUITED TO EXPLAIN BEHAVIOUR IN DIFFERENT TREATMENTS
#WHAT QUANTITATIVE VARIABLE WOULD BE BEST TO BE COMPARED HERE???


#Multinomiale logistische regression

#Interaktion treatment numerischen wahrscheinlichkeiten

#Interaktion treatment dummy zu wahrscheinlichkeiten

df_sub <- subset(df_combined,
                 treatment == "control"
                #   | treatment == 'joy'
              )

print(summary(lm(
    player_choice ~
        treatment
        # probability_gain +
        # treatment:probability_gain +
        + probability_threat
        + treatment:probability_threat
          # + optimal_choice
          # + treatment:optimal_choice
    # subset = (treatment == 'control' | treatment == 'joy'),
    ,data = df_joy)))

