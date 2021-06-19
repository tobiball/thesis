# Title     : TODO
# Objective : TODO
# Created by: tobi
# Created on: 18/06/2021



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
#df_behaviour_raw <- read.csv('all_apps_wide-2021-05-18.csv')
df_behaviour_raw <- read.csv("exp_data_clean.csv")
df_behaviour_raw <- subset(df_behaviour_raw,df_behaviour_raw$participant._current_page_name == "Fin")
subject_number <- nrow(df_behaviour_raw)
column_count <- 11

#Equalise all trial times to compare all trials simultaniously reegardless of rounds
df_behaviour <- setNames(data.frame(matrix(ncol = column_count, nrow = 0)), c("participant_id", "treatment","valence","arousal","dominance", "player_choice", "probability_gain","probability_threat","success","reaction_time","clearing_nr"))
for (num in 1:16)   ###Derive forrest from trial_nr, required for payoff calculation
  {
    row_index <- (num-1) * subject_number
df_behaviour[(row_index + 1):(row_index+subject_number),1:column_count] <- (df_behaviour_raw[
                      c(
                        "participant.id_in_session",
                        "fin_prolific.1.player.treatment",
                        "induction_check.1.player.valence",
                        "induction_check.1.player.arousal",
                         "induction_check.1.player.dominance",
                        paste(c("foraging_app.", num, ".player.foraging_choice"), collapse = ""),
                        paste(c("foraging_app.", num, ".player.probability_gain"), collapse = ""),
                        paste(c("foraging_app.", num, ".player.probability_threat"), collapse = ""),
                        paste(c("foraging_app.", num, ".player.success"), collapse = ""),
                        paste(c("foraging_app.", num, ".player.dRT"), collapse = ""),
                        paste(c("foraging_app.", num, ".player.clearing_number"), collapse = "")

                      )
    ])
  df_behaviour[(row_index + 1):(row_index+subject_number),"forrest_nr"] <- ((df_behaviour_raw[paste(c("foraging_app.", num, ".player.trial_in_game"), collapse = "")])+3)   %/% 4
}
df_behaviour <- df_behaviour[complete.cases(df_behaviour), ]

df_behaviour$valence <- df_behaviour$valence - 50
df_behaviour$dominance <- df_behaviour$dominance - 50
df_behaviour$arousal <- df_behaviour$arousal / 2

#introduces a cumulative sum showing the payoff of a participant up to that point in the forrest
df_behaviour <- df_behaviour %>%
       group_by(forrest_nr,participant_id) %>%
       mutate(wealth_state = cumsum(success) - success)

#Get optimal policy decsion from python script
df_optimal_policy <- (read.csv('optimal_policy.csv'))

#Combine real with policy results in data_frame
df_combined <- dplyr::left_join(df_behaviour,df_optimal_policy)


# df_sub <- subset(df_combined,
#                  treatment == "control"
#                 #   | treatment == 'joy'
#               )

print(summary(lm(
    player_choice ~
       # valence:probability_gain +
       # valence:probability_threat +
       # valence:optimal_choice +
       # arousal:probability_gain +
       # arousal:probability_threat +
       # arousal:optimal_choice +
       # dominance:probability_gain +
       # dominance:probability_threat +
       # dominance:optimal_choice +


       # treatment:probability_gain +
       # treatment:probability_threat +
       # treatment:optimal_choice +


       valence:arousal:probability_gain +
       valence:arousal:probability_threat +
       valence:arousal:optimal_choice +
       valence:dominance:probability_gain +
       valence:dominance:probability_threat +
       valence:dominance:optimal_choice +
       arousal:dominance:probability_gain +
       arousal:dominance:probability_threat +
       arousal:dominance:optimal_choice +

       valence:arousal:dominance:probability_gain +
       valence:arousal:dominance:probability_threat +
       valence:arousal:dominance:optimal_choice +


       probability_gain +
       probability_threat +
       optimal_choice +
       wealth_state


    , subset = (optimal_choice != "indifferent"
    #& treatment == 'joy' | treatment == 'threat'
     ),
    ,data = df_combined)))