# Student_Absences.R
# By: Isabelle Yang
# Date created: 04/15
#
# Preliminaries ----------------------------------------------------------------
student <- read.csv('/Users/isabelleyang/Desktop/Econ Project/student-mat.csv')
library(dplyr)

# Save the Summary Statistics --------------------------------------------------
library(vtable)
st(student,
   vars = c('absences', 'Dalc', 'Walc', 'famsup'),
   labels = c('Absences', 'Weekday Alcohol Consumption', 'Weekend Alcohol Consumption',
               'Family Educational Support'),
   numformat = formatfunc(big.mark = ',', digits=4),
   file = '/Users/isabelleyang/Desktop/Econ Project/summary_table.html')

# Cleaning the Data ------------------------------------------------------------
student <- student %>%
  select(absences, Dalc, Walc, famsup, studytime) %>%
  mutate(famsup = if_else(famsup == 'yes', 1, 0))

# Running the regression -------------------------------------------------------
library(stargazer)
library(car)
library(lmtest)
# run our regression as we did before
lm <- lm(absences ~ Dalc + Walc + famsup + studytime, data=student)
lm_robust_vcov <- hccm(lm, type="hc0")
lm_robust_se <- sqrt(diag(lm_robust_vcov))
