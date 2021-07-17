# Title     : TODO
# Objective : TODO
# Created by: tobi
# Created on: 05/07/2021

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


df_combined <- data_preperation("exp_data_clean.csv")
df_combined$rnmpds_chosen <- as.factor(df_combined$rnpmds_ == df_combined$player_choice)

# reaction_time_reg <- glm.cluster(
#     reaction_time ~
#      probability_threat:valence +
#          probability_gain:valence +
#        rnmpds_chosen:valence     +
#        probability_threat:arousal +
#          probability_gain:arousal +
#        rnmpds_chosen:arousal +
#        probability_threat:dominance +
#          probability_gain:dominance +
#        rnmpds_chosen:dominance
#     ,cluster = "participant_id"
#     ,data = df_combined)
rtmem1 <- lmer(
    reaction_time ~
     probability_threat:valence +
         probability_gain:valence +
       rnmpds_chosen:valence     +
       probability_threat:arousal +
         probability_gain:arousal +
       rnmpds_chosen:arousal +
       probability_threat:dominance +
         probability_gain:dominance +
       rnmpds_chosen:dominance
    + (1 | participant_id),
    data = df_combined,)
df_combined <- df_combined[df_combined$reaction_time < 5000,]

# reaction_time_html <- htmlreg(reaction_time_reg,
#        # custom.model.names = c(""),
#         digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),
#         padding = 30,outer.rules = 1, inner.rules = 0.3, symbol = "~",bold = 0.1,
#         caption = "CAP")

scatter3D( df_combined$probability_threat,df_combined$arousal, df_combined$reaction_time, pch = 18,  theta = 20, phi = 20,
          main = "", xlab = "P(Predator)",
          zlab ="Reaction Time", ylab = "Arousal",
          bty = 'g')
scatter3D(df_combined$probability_threat,df_combined$arousal, df_combined$reaction_time, theta = -50, phi = 50 , bty = "g", type = "b",
           ticktype = "detailed", pch = 20,
           cex = c(0.5, 1, 1.5))
# summary(reaction_time_reg)

x<-df_combined$probability_gain
y<-df_combined$arousal
z<-df_combined$reaction_time

fit <- lm(z ~ x + y)
# predict values on regular xy grid
grid.lines = 26
x.pred <- seq(min(x), max(x), length.out = grid.lines)
y.pred <- seq(min(y), max(y), length.out = grid.lines)
xy <- expand.grid( x = x.pred, y = y.pred)
z.pred <- matrix(predict(fit, newdata = xy),
                 nrow = grid.lines, ncol = grid.lines)
# fitted points for droplines to surface
fitpoints <- predict(fit)
# scatter plot with regression plane
scatter3D(x, y, z, pch = 20, cex = 1,
    theta = 30, phi = 3, ticktype = "detailed", bty = 'g',
    xlab = "P(Success)", ylab = "Arousal", zlab = "Reaction Time (ms)",
    surf = list(x = x.pred, y = y.pred, z = z.pred,
    facets = 1), main = "P(Success) X Arousal")

#
# rtmem2 <- lmer(
#     reaction_time ~
#          probability_gain:valence
#     + (1 | participant_id),
#     data = df_combined,)
#
# rtmem3 <- lmer(
#     reaction_time ~
#        rnmpds_chosen:valence
#     + (1 | participant_id),
#     data = df_combined,)
#
# rtmem4 <- lmer(
#     reaction_time ~
#        probability_threat:arousal
#     + (1 | participant_id),
#     data = df_combined,)
#
# rtmem5 <- lmer(
#     reaction_time ~
#          probability_gain:arousal
#
#     + (1 | participant_id),
#     data = df_combined,)
# rtmem6 <- lmer(
#     reaction_time ~
#        rnmpds_chosen:arousal
#     + (1 | participant_id),
#     data = df_combined,)
# rtmem7 <- lmer(
#     reaction_time ~
#        probability_threat:dominance
#     + (1 | participant_id),
#     data = df_combined,)
# rtmem8 <- lmer(
#     reaction_time ~
#          probability_gain:dominance
#     + (1 | participant_id),
#     data = df_combined,)
# rtmem9 <- lmer(
#     reaction_time ~
#        rnmpds_chosen:dominance
#     + (1 | participant_id),
#     data = df_combined,)


screenreg(l =list(rtmem1),digits = 4,stars = c(0.001, 0.01, 0.05, 0.1),padding =10,outer.rules = 1)



# lst2 <- c(BIC(rtmem1),BIC(rtmem2),BIC(rtmem3),BIC(rtmem4),BIC(rtmem5),BIC(rtmem6),BIC(rtmem7),BIC(rtmem8),BIC(rtmem9))
# names <- c(1,2,3,4,5,6,7,8,9)
# df <- data.frame(names,lst2)
# barplot(df$lst2)