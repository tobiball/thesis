# Title     : Main Analysis
# Objective : TODO
# Created by: tobi
# Created on: 18/06/2021

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
library(zoo, warn.conflicts = FALSE)
library(base, warn.conflicts = FALSE)
library(stats, warn.conflicts = FALSE)

library(dplyr, warn.conflicts = FALSE)
library(foreign, warn.conflicts = FALSE)
library(xtable, warn.conflicts = FALSE)
library(ggplot2, warn.conflicts = FALSE)
library(sandwich, warn.conflicts = FALSE)
library(lmtest, warn.conflicts = FALSE)
library(stargazer, warn.conflicts = FALSE)
library(miceadds, warn.conflicts = FALSE)
library(texreg, warn.conflicts = FALSE)

data_preperation <- function(behavioural_data) {
#Load data to dataframe
#df_behaviour_raw <- read.csv('all_apps_wide-2021-05-18.csv')
df_behaviour_raw <- read.csv(behavioural_data)
df_behaviour_raw <- subset(df_behaviour_raw,df_behaviour_raw$participant._current_page_name == "Fin")

subject_number <- nrow(df_behaviour_raw)
column_count <- 11

#Equalise all trial times to compare all trials simultaniously reegardless of rounds
df_behaviour <- setNames(data.frame(matrix(ncol = column_count, nrow = 0)), c("participant_id", "treatment","valence","arousal","dominance", "player_choice", "probability_gain","probability_threat","success","reaction_time","clearing_nr"))
for (num in 1:16)   ###Derive forest from trial_nr, required for payoff calculation
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
  df_behaviour[(row_index + 1):(row_index+subject_number),"forest_nr"] <- ((df_behaviour_raw[paste(c("foraging_app.", num, ".player.trial_in_game"), collapse = "")])+3)   %/% 4

    num_prev <- num - 1
    if (num_prev != 0){
    df_behaviour[(row_index + 1):(row_index+subject_number),"attack_prev"] <- df_behaviour_raw[paste(c("foraging_app.", num_prev, ".player.death"), collapse = "")]
    }
    else {
      df_behaviour[(row_index + 1):(row_index+subject_number),"attack_prev"] <- 0
    }
}


df_behaviour <- df_behaviour[complete.cases(df_behaviour), ]

df_behaviour$valence <- df_behaviour$valence - 50
df_behaviour$dominance <- df_behaviour$dominance - 50
df_behaviour$arousal <- df_behaviour$arousal / 2

#introduces a cumulative sum showing the payoff of a participant up to that point in the forest
df_behaviour <- df_behaviour %>%
       group_by(forest_nr,participant_id) %>%
       mutate(wealth_state = cumsum(success) - success)

#Get optimal policy decsion from python script
df_optimal_policy <- (read.csv('main/optimal_policy.csv'))
df_combined <- dplyr::left_join(df_behaviour,df_optimal_policy)

#Combine real with policy results in data_frame
# names(df_combined)[16] <- "rnpmds_"
df_combined$optimal_choice[df_combined$optimal_choice == 'indifferent'] <- 0.5
df_combined$probability_threat <- as.numeric(df_combined$probability_threat *1.5)
df_combined$optimal_choice <- as.numeric(df_combined$optimal_choice)

#df_m <- subset(df_behaviour_raw, fin_prolific.1.player.treatment == 'fear')


#print(mean(df_m$induction_check.1.player.arousal,na.rm=TRUE))
# N = matrix(0,3,16, byrow = T)
# n = 119
# states = c('joy','fear','control')

# for(i in 1:n){
#   for(j in 1:3){
#     p = sum(df_combined$participant_id==i & df_combined$treatment==states[j])
#     N[j, p] = N[1, p] + 1
#   }
# }
     return((df_combined))
#   return(list(df_combined,df_behaviour))
}

logit2prob <- function(logit){
  odds <- exp(logit)
  prob <- odds / (1 + odds)
  return(prob)
}
# preped_data <- data_preperation("exp_data_clean.csv")
# df_combined <- preped_data[[1]]
# df_behaviour<- preped_data[[2]]

# #---------------------------REGRESSIONS-------------------------------#
df_behaviour_raw <- read.csv("main/exp_data_clean.csv")
df_behaviour_raw <- subset(df_behaviour_raw,df_behaviour_raw$participant._current_page_name == "Fin")

induction_valence <- lm(
                       induction_check.1.player.valence ~ fin_prolific.1.player.treatment,data = df_behaviour_raw)
induction_arousal <- lm(
                       induction_check.1.player.arousal ~ fin_prolific.1.player.treatment,data = df_behaviour_raw)
induction_dominance <- lm(
                       induction_check.1.player.dominance ~ fin_prolific.1.player.treatment,data = df_behaviour_raw)

df_combined <- data_preperation("main/exp_data_clean.csv")

# test <- (glm.cluster(
#     player_choice ~
#        probability_threat
#        # probability_threat +
#        # optimal_choice +
#        # wealth_state +
#        # clearing_nr
#        # + attack_prev
#     #x     valence + arousal + dominance +
#
#        # + valence:probability_gain +
#        # valence:probability_threat +
#        # valence:optimal_choice +
#        # arousal:probability_gain +
#        # arousal:probability_threat +
#        # arousal:optimal_choice +
#        # dominance:probability_gain +
#        # dominance:probability_threat +
#        # dominance:optimal_choice
#
#        # + valence:arousal:probability_gain +
#        # valence:arousal:probability_threat +
#        # valence:arousal:optimal_choice +
#        # dominance:valence:probability_gain +
#        # valence:dominance:probability_threat +
#        # valence:dominance:optimal_choice +
#        # arousal:dominance:probability_gain +
#        # arousal:dominance:probability_threat +
#        # arousal:dominance:optimal_choice +
#        #
#        # valence:arousal:dominance:probability_gain +
#        # valence:arousal:dominance:probability_threat +
#        # valence:arousal:dominance:optimal_choice +
#
#        # treatment:probability_gain +
#        # treatment:probability_threat +
#        # treatment:optimal_choice +
#
#        # wealth_state:clearing_nr +
#        # reaction_time +
#        # forest_nr
#
#     ,subset = (df_combined$optimal_choice != "indifferent" & df_combined$treatment == "control")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
#
# base <- (glm.cluster(
#     player_choice ~
#        probability_gain +
#        probability_threat +
#        optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
#
# treatment <- (glm.cluster(
#     player_choice ~
#        probability_gain +
#        probability_threat +
#        optimal_choice +
#        treatment:probability_gain +
#        treatment:probability_threat +
#        treatment:optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
#
single <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       optimal_choice +
       wealth_state +
       clearing_nr +
       valence:probability_gain +
       valence:probability_threat +
       valence:optimal_choice
       # arousal:probability_gain +
       # arousal:probability_threat +
       # arousal:optimal_choice +
       # dominance:probability_gain +
       # dominance:probability_threat +
       # dominance:optimal_choice
    ,subset = (df_combined$optimal_choice != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

# double <- (glm.cluster(
#     player_choice ~
#        probability_gain +
#        probability_threat +
#        optimal_choice +
#        wealth_state +
#        clearing_nr +
#        valence:arousal:probability_gain +
#        valence:arousal:probability_threat +
#        valence:arousal:optimal_choice
#        # dominance:valence:probability_gain +
#        # valence:dominance:probability_threat +
#        # valence:dominance:optimal_choice +
#        # arousal:dominance:probability_gain +
#        # arousal:dominance:probability_threat +
#        # arousal:dominance:optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
# #
# full <- (glm.cluster(
#     player_choice ~
#        probability_gain +
#        probability_threat +
#        optimal_choice +
#        wealth_state +
#        clearing_nr +
#        valence:probability_gain +
#        valence:probability_threat +
#        valence:optimal_choice +
#        arousal:probability_gain +
#        arousal:probability_threat +
#        arousal:optimal_choice +
#        dominance:probability_gain +
#        dominance:probability_threat +
#        dominance:optimal_choice +
#        valence:arousal:probability_gain +
#        valence:arousal:probability_threat +
#        valence:arousal:optimal_choice +
#        dominance:valence:probability_gain +
#        valence:dominance:probability_threat +
#        valence:dominance:optimal_choice +
#        arousal:dominance:probability_gain +
#        arousal:dominance:probability_threat +
#        arousal:dominance:optimal_choice +
#          valence:arousal:dominance:probability_threat+
#          valence:arousal:dominance:probability_gain+
#     valence:arousal:dominance:optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
# #Display Options
#
#summary(single)
# screenreg(l =list(double),digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),padding =10,outer.rules = 1)
# #screenreg(l =list(base,treatment,single,double,full),digits = 4,stars = c(0.001, 0.01, 0.05, 0.1))
# # htmlreg(l =list(test,base,treatment),
# #         custom.model.names = c("(1)","(2)","(3)"),
# #         digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
# #         padding = 8,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1)
# #plotreg(template)
# html <- texreg(l =list(induction_valence,induction_arousal,induction_dominance),
#         custom.model.names = c("(Valence)","(Arousal)","(Dominance)"),
#         digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
#         padding = 30,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1,
#         caption = "Base DS and Treatment",)
# #ggplot(df_combined, aes(as.numeric(probability_gain)/as.numeric(probability_threat),reaction_time)) + geom_point()
# #stargazer(screenreg(template), type = "html", out = "main_analyisis.html")
#
# #df_combined$player_choice == df_combined$optimal_choice
# #plot(df_behaviour_raw$induction_check.1.player.valence,df_behaviour_raw$induction_check.1.player.arousal)
df_behaviour_raw[df_behaviour_raw == "fear"] <- 'Negative'
df_behaviour_raw[df_behaviour_raw == "joy"] <- 'Positive'
df_behaviour_raw[df_behaviour_raw == "control"] <- 'Neutral'
df_behaviour_raw[df_behaviour_raw == "fin_prolific.1.player.treatment"] <- 'treatment'
# qplot(df_behaviour_raw$induction_check.1.player.valence,geom = "histogram")

# qplot(df_behaviour_raw$fin_prolific.1.player.treatment, induction_check.1.player.valence,
#       data = df_behaviour_raw,
#       geom=c("boxplot", "jitter"),
#       fill = fin_prolific.1.player.treatment,
# #      title = 'blobl'
# ) + ggtitle("") +
#   stat_summary(fun=mean, geom="point", shape=20, size=14, color="yellow", fill="yellow") +
#   xlab("Induction") + ylab("Valence") + guides(fill=guide_legend(title="Induction"))  + theme(text = element_text(size = 20))


#qplot(induction_check.1.player.valence,induction_check.1.player.arousal, data = df_behaviour_raw)


# joy <- subset(df_combined$player_choice,df_combined$treatment == "joy")
# fear <- subset(df_combined$player_choice,df_combined$treatment == "fear")
# control <- subset(df_combined$player_choice,df_combined$treatment == "control")
# joy_results <- joy$player_choice == joy$rnpmds_
# joy_results <- joy$player_choice == joy$rnpmds_



glmc <- (glm.cluster(
    player_choice ~
       optimal_choice
    ,subset = (df_combined$optimal_choice != "indifferent" & df_combined$treatment == "control")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

glmf <- (glm.cluster(
    player_choice ~
       optimal_choice
    ,subset = (df_combined$optimal_choice != "indifferent" & df_combined$treatment == "fear")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

glmj <- (glm.cluster(
    player_choice ~
       optimal_choice
    ,subset = (df_combined$optimal_choice != "indifferent" & df_combined$treatment == "joy")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

# screenreg(extract(
#   lm1,
#   include.aic = FALSE,
#   include.bic = FALSE,
#   include.loglik = TRUE,
#   include.deviance = FALSE,
# ))
#
# screenreg(extract(
#   lmf,
#   include.aic = FALSE,
#   include.bic = FALSE,
#   include.loglik = TRUE,
#   include.deviance = FALSE,
# ))
#
# screenreg(extract(
#   lmj,
#   include.aic = FALSE,
#   include.bic = FALSE,
#   include.loglik = TRUE,
#   include.deviance = FALSE,
# ))

# logit2prob(coef(glmj))



# glm_base <- (glm.cluster(
#     player_choice ~
#        optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent" )
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
#
# glm_negative_induction <- (glm.cluster(
#     player_choice ~
#        optimal_choice
#     ,subset = (df_combined$optimal_choice != "indifferent" & df_combined$treatment == "fear")
#     ,cluster = "participant_id"
#     ,data = df_combined
#     ,family = "binomial"))
#
logit2prob <- function(logit){
  odds <- exp(logit)
  prob <- odds / (1 + odds)
  return(prob)
}
#
# model_prob <- function(glm){
#   intercept <- coef(glm)[1]
#   b <- coef(glm)[2]
#   logits <- intercept + b
#   prob <- logit2prob(logits)
#
#   return(prob)
# }

# model_prob(glm_base)
# model_prob(glm_negative_induction)



library(plyr)
# Break up d by state, then fit the specified model to each piece and
# return a list
models <- dlply(df_combined, "participant_id", function(df)
  lm(player_choice ~ optimal_choice, data = df))

# Apply coef to each model and return a data frame
ldply(models, coef)

# Print the summary of each model
# l_ply(models, summary, .print = TRUE)