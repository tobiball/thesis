library(DirichletReg)

lake <- ArcticLake
head(ArcticLake)
AL <- DR_data(ArcticLake[,1:3])
plot(AL)
summary(AL)