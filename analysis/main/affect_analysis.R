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
library(plot3D)
library(lme4)
source("main.R")
#---------------------------REGRESSIONS-------------------------------#


df_combined <- data_preperation("../exp_data_clean.csv")

base_controls <- (glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
         wealth_state +
         clearing_nr +
         attack_prev
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

valence <- glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:probability_gain +
       valence:probability_threat +
       valence:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial")

single <- glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:probability_gain +
       valence:probability_threat +
       valence:rnpmds_ +
       arousal:probability_gain +
       arousal:probability_threat +
       arousal:rnpmds_ +
       dominance:probability_gain +
       dominance:probability_threat +
       dominance:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial")

valence_arousal <- glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:arousal:probability_gain +
       valence:arousal:probability_threat +
       valence:arousal:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial")

double <- glm.cluster(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:arousal:probability_gain +
       valence:arousal:probability_threat +
       valence:arousal:rnpmds_ +
       dominance:valence:probability_gain +
       valence:dominance:probability_threat +
       valence:dominance:rnpmds_ +
       arousal:dominance:probability_gain +
       arousal:dominance:probability_threat +
       arousal:dominance:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial")

full <- (glm.cluster(
    player_choice ~
      probability_gain +
       probability_threat +
       rnpmds_ +
      valence:arousal:dominance:probability_threat+
        valence:arousal:dominance:probability_gain+
    valence:arousal:dominance:rnpmds_
    ,subset = (df_combined$rnpmds_ != "indifferent")
    ,cluster = "participant_id"
    ,data = df_combined
    ,family = "binomial"))

#Display Options

#summary(template)
# screenreg(l =list(base,valence,single,valence_arousal,double,full),
#         custom.model.names = c("(2)","(4)","(5)","(6)", "(7)","(8)"),
#         digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
#         # padding = 8,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1
#           )
# plotreg(valence,   ci.level = 0.9,
#         ci.inner = 0.5,
#         custom.coef.map = list("probability_gain:valence" = "P(Success)XVal",
#                                "probability_threat:valence" = "P(Predator)XVal",
#                                "rnpmds_1:valence" = "rnpmDSXVal")) + theme(text = element_text(size = 20))
affects_html <- texreg(l =list(base,valence,single),
        custom.model.names = c("(2)","(4)", "(5)" ),
                       custom.coef.names = c("(Intercept)",
                                "P(Success)", "P(Predator)", "rnpmDS",
                                "P(Success)XVal","P(Predator)XVal","rnpmDSXVal",
                                "P(Success)XAro","P(Predator)XAro","rnpmDSXAro",
                                "P(Success)XDom","P(Predator)XDom","rnpmDSXDom"),
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
        padding = 0,outer.rules = 1, inner.rules = 0.3, symbol = "`",bold = 0.1,
        caption = "One Dimensional Affect Models")  #Its clever to just use the html to write the descriptionr below the picture bro

multi_affects_html <- texreg(l =list(base,valence_arousal,double,full),
        custom.model.names = c("(2)","(6)", "(7)","(8)" ),
                                       custom.coef.names = c("(Intercept)",
                                "P(Success)", "P(Predator)", "rnpmDS",
                                "P(Success)XValXAro","P(Predator)XValXAro","rnpmDSXValXAro",
                                                             "P(Success)XValXDom","P(Predator)XValXDom","rnpmDSXValXDom",
                                                             "P(Success)XAroXDom","P(Predator)XAroXDom","rnpmDSXAroXDom",
                                "P(Success)XValXAroXDom","P(Predator)XValXAroXDom","rnpmDSXValXAroXDom"),
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
        padding = 0,outer.rules = 1, inner.rules = 0.3, symbol = "'",bold = 0.1,
                               no.margin = TRUE,

        caption = "Multi Dimensional Affect Models")  #Its clever to just use the html to write the descriptionr below the picture bro

#Vales"(6)", "(7)","(8)"    valence_arousal,double,full



#htmlreg(template)
#ggplot(df_combined, aes(as.numeric(probability_gain)/as.numeric(probability_threat),reaction_time)) + geom_point()
#stargazer(screenreg(template), type = "html", out = "main_analyisis.html")

#df_combined$player_choice == df_combined$rnpmds_
# qplot(treatment, arousal,
#       data = df_combined
#       # data = subset(df_combined,player_choice == 1)
#       ,geom = "boxplot"
# )

# qplot(treatment, arousal, data = df_combined,
#       geom=c("boxplot", "jitter"), fill = treatment)
# ggplot( df_combined, aes(x=probability_gain, y=player_choice)) +
#   geom_point() +
#   geom_smooth(method = "glm",
#     method.args = list(family = "binomial"),
#     se = FALSE)
#
# ggplot(df_combined) +(aes(x=probability_gain, y=player_choice))

fcount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'fear'))
jcount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'joy'))
ccount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'control'))
fcount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'fear'))
jcount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'joy'))
ccount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'control'))



Induction <- c('Negatve','Negatve','Positive','Positive','Neutral','Neutral')
Choice <- c('rnpmDS','non-rnpmDS','rnpmDS','non-rnpmDS','rnpmDS','non-rnpmDS')
Choice_Count <- c(fcount,fcount0,jcount,jcount0,ccount,ccount0)
tvals <- data.frame(Induction,Choice,Choice_Count)

ggplot(tvals, aes(Induction, Choice_Count, fill = Choice)) +
  geom_bar(stat="identity", position = "dodge") +
  scale_fill_brewer(palette = "Set1") + theme(text = element_text(size = 20)) + labs(y= "Choice Count")

#
# # p<-ggplot(data=tvals, aes(x=treatments, y=values)) +
# #   geom_bar(stat="identity")
# # p
# #######################################################################
#
# plotreg(valence,   ci.level = 0.9,
#         custom.coef.map = list("probability_gain:valence" = "Probability Gain X Valence",
#                                "probability_threat:valence" = "Probability Threat X Valence",
#                                "rnpmds_1:valence" = "rnpmDS X Valence")) + theme(text = element_text(size = 20))

# df_combined <- df_combined %>%
#        group_by(participant_id) %>%
#        mutate(fuck_new_variable = cumsum(player_choice == rnpmds_)) %>%
#         summarise(participant_id,fuck_new_variable)


x = as.numeric(df_combined$player_choice == df_combined$rnpmds_)
y = df_combined$arousal
z = df_combined$valence
#
#
scatter3D(x, y, z, pch = 18,  theta = 20, phi = 20,
          main = "", xlab = "rnpmDS",
          ylab ="Valence", zlab = "Arousal",
          bty = 'g')

# mem <- glmer(
#     player_choice ~
#        # log(probability_gain) +
#        # log(probability_threat) +
#        # rnpmds_ +
#        # wealth_state +
#        # clearing_nr +
#        # valence:probability_gain +
#        # valence:probability_threat +
#        # valence:rnpmds_ +
#        # arousal:probability_gain +
#        # arousal:probability_threat +
#        # arousal:rnpmds_ +
#        # dominance:probability_gain +
#        # dominance:probability_threat +
#        # dominance:rnpmds_ +
#        valence:arousal:probability_gain +
#        valence:arousal:probability_threat +
#        valence:arousal:rnpmds_ +
#        valence:dominance:probability_gain +
#        valence:dominance:probability_threat +
#        valence:dominance:rnpmds_ +
#        arousal:dominance:probability_gain +
#        arousal:dominance:probability_threat +
#        arousal:dominance:rnpmds_ +
#        #   valence:arousal:dominance:probability_threat+
#     #      valence:arousal:dominance:probability_gain+
#     # valence:arousal:dominance:rnpmds_
#     + (1 | participant_id),
#     data = df_combined,
#   subset = (df_combined$rnpmds_ != "indifferent"),
#   family = binomial,
#   control = glmerControl(optimizer="bobyqa",
#  optCtrl=list(maxfun=2e6)
#                          ),
#     nAGQ = 1)
#
# # screenreg(mem)
#
# screenreg(mem,
#         custom.model.names = "1",
#         digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
#         # padding = 8,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1
#           )
#
# # summary(mem)
#
# length(fixef(mem))
# numcols <- grep("^c\\.",names(df_combined))

