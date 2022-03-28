# Title     : Main Analysis
# Objective : TODO
# Created by: tobi
# Created on: 18/06/2021

#________________________________-
library(dplyr)
library(foreign)
library(xtable)
library(ggplot2)
library(sandwich)
library(lmtest)
library(stargazer)
library(miceadds)
library(texreg)
library(webshot)
source("main.R")
#---------------------------REGRESSIONS-------------------------------#


df_combined <- data_preperation("../exp_data_clean.csv")

test <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       wealth_state +
       clearing_nr
       + attack_prev

    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

base <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

treatment <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       treatment:probability_gain +
       treatment:probability_threat +
       treatment:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

single <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       wealth_state +
       clearing_nr +
       valence:probability_gain +
       valence:probability_threat +
       valence:rnpmds_
       # arousal:probability_gain +
       # arousal:probability_threat +
       # arousal:rnpmds_ +
       # dominance:probability_gain +
       # dominance:probability_threat +
       # dominance:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))


#Display Options

#summary(template)
#screenreg(l =list(test,base,treatment),digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),padding =10,outer.rules = 1)
treatment_html <- texreg(l =list(test,base,treatment),
        custom.model.names = c("(1)","(2)","(3)"),
                          custom.coef.names = c("(Intercept)",
                                "P(Success)", "P(Predator)", "rnpmDS",
                                                "Wealth State", "Clearing Nr.", "Attack Prev.",
                                "P(Success)XNegative Induction","P(Success)XPostive Induction",
                          "P(Predator)XNegative Induction","P(Predator)XPostive Induction",
                            "rnpmDSXNegative Induction","rnpmDSXPositive Induction")
                              ,
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
        padding = 30,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1,
        caption = "Base DS and Treatment")
#plotreg(template)
#h
# tmlreg(template)
ggplot(df_combined, aes(as.numeric(probability_gain)/as.numeric(probability_threat),reaction_time)) + geom_point()
#stargazer(screenreg(template), type = "html", out = "main_analyisis.html")

#df_combined$player_choice == df_combined$rnpmds_


