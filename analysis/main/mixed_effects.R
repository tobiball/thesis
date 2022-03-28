# Title     : TODO
# Objective : TODO
# Created by: tobi
# Created on: 07/07/2021

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
library(optimx)
library(minqa)
source("main.R")
#---------------------------REGRESSIONS-------------------------------#


df_combined <- data_preperation("../exp_data_clean.csv")

df_tobi <- subset(df_combined,df_combined$rnpmds_ != "indifferent")

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

affects_html <- htmlreg(l =list(base,valence_arousal,double,full),
        custom.model.names = c("(2)","(6)", "(7)","(8)" ),
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
        padding = 0,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1,
        caption = "Multi Dimensional Affect Models")  #Its clever to just use the html to write the descriptionr below the picture bro

#Vales"(6)", "(7)","(8)"    valence_arousal,double,full




fcount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'fear'))
jcount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'joy'))
ccount <-nrow(subset(df_combined, player_choice == rnpmds_ & treatment == 'control'))
fcount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'fear'))
jcount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'joy'))
ccount0 <-nrow(subset(df_combined, player_choice != rnpmds_ & treatment == 'control'))




#
# x = as.numeric(df_combined$player_choice == df_combined$rnpmds_)
# y = df_combined$arousal
# z = df_combined$valence
#
#
# scatter3D(x, y, z, pch = 18,  theta = 20, phi = 20,
#           main = "", xlab = "rnpmDS",
#           ylab ="Valence", zlab = "Arousal",
#           bty = 'g')
# mem1 <- glmer(
#     player_choice ~
#        probability_gain +
#        probability_threat +
#        rnpmds_ +
#        wealth_state +
#        clearing_nr +
#     + (1 | participant_id),
#     data = df_combined,
#   subset = (df_combined$rnpmds_ != "indifferent"),
#   family = binomial,
#  control = glmerControl(optimizer ='bobyqa',optCtrl=list(maxfun=2e5)),
#     nAGQ=0)

mem2 <- glmer(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
    + (1 | participant_id),
    data = df_combined,
  subset = (df_combined$rnpmds_ != "indifferent"),
  family = binomial,
 control = glmerControl(optimizer ='bobyqa',optCtrl=list(maxfun=2e5)),
    nAGQ=0,
)

mem4 <- glmer(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:probability_gain +
       valence:probability_threat +
       valence:rnpmds_ +
    + (1 | participant_id),
    data = df_combined,
  subset = (df_combined$rnpmds_ != "indifferent"),
  family = binomial,
 control = glmerControl(optimizer ='bobyqa',optCtrl=list(maxfun=2e5)),
    nAGQ=0,
)

mem6 <- glmer(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
       valence:arousal:probability_gain +
       valence:arousal:probability_threat +
       valence:arousal:rnpmds_ +
    + (1 | participant_id),
    data = df_combined,
  subset = (df_combined$rnpmds_ != "indifferent"),
  family = binomial,
 control = glmerControl(optimizer ="Nelder_Mead"),
    nAGQ=0,
)
mem8 <- glmer(
    player_choice ~
       probability_gain +
       probability_threat +
       rnpmds_ +
         valence:arousal:dominance:probability_threat+
         valence:arousal:dominance:probability_gain+
    valence:arousal:dominance:rnpmds_
    + (1 | participant_id),
    data = df_combined,
  subset = (df_combined$rnpmds_ != "indifferent"),
  family = binomial,
 control = glmerControl(optimizer ='optimx', optCtrl=list(method='L-BFGS-B')),
    nAGQ=0,
)



screenreg(l =list(mem2,mem4,mem6,mem8),
        custom.model.names = c("ME (2)","ME (4)","ME (6)","ME (8)"),
          custom.coef.names = c("(Intercept)",
                                "P(Success)", "P(Predator)", "rnpmDS",
                                "P(Success)XVal","P(Predator)XVal","rnpmDSXVal",
                                "P(Success)XValXAro","P(Predator)XValXAro","rnpmDSXValXAro",
                                "P(Success)XValXAroXDom","P(Predator)XValXAroXDom","rnpmDSXValXAroXDom"),
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
        # padding = 8,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1
          )
me_html <- texreg(l =list(mem2,mem4,mem6,mem8),
        custom.model.names = c("ME (2)","ME (4)","ME (6)","ME (8)"),
          custom.coef.names = c("(Intercept)",
                                "P(Success)", "P(Predator)", "rnpmDS",
                                "P(Success)XVal","P(Predator)XVal","rnpmDSXVal",
                                "P(Success)XValXAro","P(Predator)XValXAro","rnpmDSXValXAro",
                                "P(Success)XValXAroXDom","P(Predator)XValXAroXDom","rnpmDSXValXAroXDom"),
        digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
                  no.margin = TRUE,
        padding = 15,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1,margin = 0,
                   caption = "Mixed Effects Affect Models")


plotreg(mem6,   ci.level = 0.95,
        ci.inner = 0.5,
        custom.coef.map = list("probability_gain:valence:arousal" = "P(Success)XValXAro",
                               "probability_threat:valence:arousal" = "P(Predator)XValAro",
                               "rnpmds_1:valence:arousal" = "rnpmDSXValAro")) + theme(text = element_text(size = 20))

#
# length(fixef(mem))
# numcols <- grep("^c\\.",names(df_combined))

