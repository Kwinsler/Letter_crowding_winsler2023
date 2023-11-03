# Analysis for Study 1 of "Fundamental changes in the spatial properties of visual perception after a lifetime of reading crowded letters"
# - Kurt Winsler

# packages
require(lme4)
require(lmerTest)
require(car)

require(dplyr)
require(tidyr)

require(ggplot2)
require(gridExtra)

# working directory
setwd("/Users/kwinsler/Documents/GitHub/Letter_crowding_study/Study1")

# load data
s1a_dat <- read.delim(file = 'a_letters_vs_invertedletters/CRD_INV_HOR_data.csv', sep = ',', header = T)
s1b_dat <- read.delim(file = 'b_letters_vs_gabors/CRD_GAB_HOR_data.csv', sep = ',', header = T)

# combine data
s1a_dat$Experiment <- 'INV'
s1b_dat$Experiment <- 'GAB'

alldat <- rbind(s1a_dat, s1b_dat)
alldat$Stair_short <- substr(alldat$Stair, 3, 9) # better label

## Bar plots

# aggregated data to plot
all_pdat <- alldat %>% 
  group_by(Experiment, Stair_short, Condition) %>%  
  summarise(mean = mean(Mean), 
            sd = sd(Mean),
            n = n(),  
            se = sd(Mean)/sqrt(n())) %>%
  mutate(Stair = case_when(
    Stair_short == "LPstair" ~ '-6',
    Stair_short == "LFstair" ~ '-4',
    Stair_short == "LNstair" ~ '-2',
    Stair_short == "RNstair" ~ '+2',
    Stair_short == "RFstair" ~ '+4',
    Stair_short == "RPstair"~ '+6'))

# plot
ylimits <- c(0,0.7)

all_pdat[all_pdat$Experiment == 'INV', ] %>% # filter data and pipe
  ggplot(aes(Stair, mean, fill = Condition)) + # x = stair (location), y = mean, fill = upright vs inverted
    geom_bar(stat="identity", position = 'dodge', aes(fill = Condition)) + # make bar plot
    scale_fill_manual("Condition", values = c("Inverted" = "#e85656", "Upright" = "#00c1d6")) + # manual color mapping
    scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) + # manually set order of x axis
    geom_errorbar(position = position_dodge(.9), aes(ymin = mean - se, ymax = mean + se), width=0.2) + # add error bars (se is a column in the data)
    labs(x = 'Target Eccentricity (degrees)',  # x label
         y = 'Crowding Threshold (proportion of eccentricity)', # y label
         title = 'Inverted versus upright letters', # title
         tag = 'a.') + # tag (the a.)
    scale_y_continuous(limits = ylimits,expand = expansion(mult = c(0, .1))) + # set y limits (ylimits is an object of 2 values) and make bars touch bottom axis
    theme_classic() + # blank background and no upper or right line 
    theme(plot.title = element_text(hjust = 0.5), # center title
          legend.position=c(.9,.9), # put condition legend into top right of plot
          plot.tag = element_text(face = "bold"), # bold the "a." tag
          text = element_text(size=25)) -> p1 # set font and assign to object

all_pdat[all_pdat$Experiment == 'GAB', ] %>%
  ggplot(aes(Stair, mean, fill = Condition)) +
  geom_bar(stat="identity", position = 'dodge', aes(fill = Condition)) +
  scale_fill_manual("Condition", values = c("Gabor" = "#f28149", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = mean - se, ymax = mean + se), width=0.2) + 
  labs(x = 'Target Eccentricity (degrees)', 
       y = 'Crowding Threshold (proportion of eccentricity)', 
       title = 'Gabors versus upright letters',
       tag = 'b.') +
  scale_y_continuous(limits = ylimits, expand = expansion(mult = c(0, .1))) +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        legend.position=c(.9,.9),
        text = element_text(size=25),
        plot.tag = element_text(face = "bold"),
        plot.margin = unit(c(0,0,0,1), "cm")) -> p2

grid.arrange(p1, p2, nrow = 1)
# exported at 1800 x 800

## Bar plots with data points overlayed

alldat %>% 
  mutate(Stair = case_when(
    Stair_short == "LPstair" ~ '-6',
    Stair_short == "LFstair" ~ '-4',
    Stair_short == "LNstair" ~ '-2',
    Stair_short == "RNstair" ~ '+2',
    Stair_short == "RFstair" ~ '+4',
    Stair_short == "RPstair"~ '+6')) -> alldat

ylimits <- c(0,1)
bar_alpha <- 0
point_alpha <- .5

# a plot
ggplot(data = NULL, aes(fill = Condition)) + # data is null because 2 data objects used (for bar and points)
  geom_bar(data = all_pdat[all_pdat$Experiment == 'INV', ], # mean data
           aes(Stair, mean, fill = Condition, color = Condition),
           size = 1.5,
           alpha = bar_alpha,
           stat="identity", position = 'dodge') + # make bar plot
  scale_fill_manual("Condition", values = c("Inverted" = "#e85656", "Upright" = "#00c1d6")) + # manual color mapping
  scale_color_manual("Condition", values = c("Inverted" = "#e85656", "Upright" = "#00c1d6")) + # manual color mapping
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) + # manually set order of x axis
  # add points
  geom_point(data = alldat[alldat$Experiment == 'INV', ], # raw data
             aes(Stair, Mean, color = Condition, stroke = 0), alpha = point_alpha, 
             position=position_jitterdodge(jitter.width = 0.1, dodge.width= .9)) +
  # error bars (after points for layering)
  geom_errorbar(data = all_pdat[all_pdat$Experiment == 'INV', ],
                aes(Stair, mean, ymin = mean - se, ymax = mean + se),
                position = position_dodge(.9),
                width=0.2) + 
  # other aesthetics
  labs(x = 'Target Eccentricity (degrees)',  # x label
       y = 'Crowding Threshold (proportion of eccentricity)', # y label
       title = 'Inverted versus upright letters', # title
       tag = 'a.') + # tag (the a.)
  scale_y_continuous(limits = ylimits,expand = expansion(mult = c(0, .1))) + # set y limits (ylimits is an object of 2 values) and make bars touch bottom axis
  theme_classic() + # blank background and no upper or right line 
  theme(plot.title = element_text(hjust = 0.5), # center title
        legend.position=c(.9,.9), # put condition legend into top right of plot
        plot.tag = element_text(face = "bold"), # bold the "a." tag
        text = element_text(size=25)) -> p1 # set font and assign to object

# b plot
ggplot(data = NULL, aes(fill = Condition)) + # data is null because 2 data objects used (for bar and points)
  geom_bar(data = all_pdat[all_pdat$Experiment == 'GAB', ], # mean data
           aes(Stair, mean, fill = Condition, color = Condition),
           size = 1.5,
           alpha = bar_alpha,
           stat="identity", position = 'dodge') + # make bar plot
  scale_fill_manual("Condition", values = c("Gabor" = "#f28149", "Upright" = "#00c1d6")) + # manual color mapping
  scale_color_manual("Condition", values = c("Gabor" = "#f28149", "Upright" = "#00c1d6")) + # manual color mapping
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) + # manually set order of x axis
  # add points
  geom_point(data = alldat[alldat$Experiment == 'GAB', ], # raw data
             aes(Stair, Mean, color = Condition, stroke = 0), alpha = point_alpha, 
             position=position_jitterdodge(jitter.width = 0.1, dodge.width= .9)) +
  # error bars (after points for layering)
  geom_errorbar(data = all_pdat[all_pdat$Experiment == 'GAB', ],
                aes(Stair, mean, ymin = mean - se, ymax = mean + se),
                position = position_dodge(.9),
                width=0.2) + 
  # other aesthetics
  labs(x = 'Target Eccentricity (degrees)',  # x label
       y = 'Crowding Threshold (proportion of eccentricity)', # y label
       title = 'Gabor patches versus upright letters', # title
       tag = 'b.') + # tag (the a.)
  scale_y_continuous(limits = ylimits,expand = expansion(mult = c(0, .1))) + # set y limits (ylimits is an object of 2 values) and make bars touch bottom axis
  theme_classic() + # blank background and no upper or right line 
  theme(plot.title = element_text(hjust = 0.5), # center title
        legend.position=c(.9,.9), # put condition legend into top right of plot
        plot.tag = element_text(face = "bold"), # bold the "a." tag
        text = element_text(size=25)) -> p2 # set font and assign to object 

# exported at 1800 x 800
grid.arrange(p1, p2, nrow = 1)



### Other plots

## Violin plots
ylimits <- c(0,1)

alldat[alldat$Experiment == 'INV', ] %>%
  ggplot(aes(Stair_short, Mean, fill = Condition)) +
  geom_violin(aes(fill = Condition), draw_quantiles = c(0.5)) +
  ylim(ylimits) +
  scale_fill_manual("Condition", values = c("Inverted" = "#cc0000", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c('LPstair', 'LFstair', 'LNstair','RNstair', 'RFstair','RPstair')) +
  labs(x = 'Location', y = 'Critical Spacing', 
       subtitle = 'Horizontal flankers',title = 'Inverted vs Normal letters') +
  theme(text = element_text(size=15)) -> p1

alldat[alldat$Experiment == 'GAB', ] %>%
  ggplot(aes(Stair_short, Mean, fill = Condition)) +
  geom_violin(aes(fill = Condition), draw_quantiles = c(0.5)) +
  ylim(ylimits) +
  scale_fill_manual("Condition", values = c("Gabor" = "#cc0000", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c('LPstair', 'LFstair', 'LNstair','RNstair', 'RFstair','RPstair')) +
  labs(x = 'Location', y = 'Critical Spacing', 
       subtitle = 'Horizontal flankers',title = 'Gabors vs Normal letters') +
  theme(text = element_text(size=15)) -> p2
  
grid.arrange(p1, p2, nrow = 1)

## dot/rain plots
ylimits <- c(0,1)
alpha <- .5

alldat[alldat$Experiment == 'INV', ] %>%
  ggplot(aes(Stair_short, Mean, color = Condition)) +
  geom_point(aes(color = Condition), alpha = alpha, 
             position=position_jitterdodge(jitter.width = 0.2)) +
  ylim(ylimits) +
  scale_color_manual("Condition", values = c("Inverted" = "#cc0000", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c('LPstair', 'LFstair', 'LNstair','RNstair', 'RFstair','RPstair')) +
  labs(x = 'Location', y = 'Critical Spacing', 
       subtitle = 'Horizontal flankers',title = 'Inverted vs Normal letters') +
  theme_bw() +
  theme(text = element_text(size=15)) -> p1

alldat[alldat$Experiment == 'GAB', ] %>%
  ggplot(aes(Stair_short, Mean, fill = Condition)) +
  geom_point(aes(color = Condition), alpha = alpha, 
             position=position_jitterdodge(jitter.width = 0.2)) +  
  ylim(ylimits) +
  scale_color_manual("Condition", values = c("Gabor" = "#cc0000", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c('LPstair', 'LFstair', 'LNstair','RNstair', 'RFstair','RPstair')) +
  labs(x = 'Location', y = 'Critical Spacing', 
       subtitle = 'Horizontal flankers',title = 'Gabors vs Normal letters') +
  theme_bw() +
  theme(text = element_text(size=15)) -> p2

grid.arrange(p1, p2, nrow = 1)

#### Analysis ####

## Study 1a - inverted vs upright letters

# main model
fit.s1a <- lmer(Mean ~ CondEff * HemifieldEff * EccentricityEff 
            + (1 | SUBJECT)
            + (0 + CondEff | SUBJECT)
            + (0 + HemifieldEff | SUBJECT)
            + (0 + EccentricityEff | SUBJECT)
            , data = s1a_dat)

summary(fit.s1a)
anova(fit.s1a, type = 3)

# upright only follow up
fit.s1a.upr <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                + (1 | SUBJECT)
                + (0 + HemifieldEff | SUBJECT)
                + (0 + EccentricityEff | SUBJECT)
                , data = s1a_dat[s1a_dat$Condition == "Upright", ] )

summary(fit.s1a.upr)
anova(fit.s1a.upr, type = 3)

# inverted only follow up
fit.s1a.inv <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1a_dat[s1a_dat$Condition == "Inverted", ] )

summary(fit.s1a.inv)
anova(fit.s1a.inv, type = 3)

## Study 1b - gabors vs upright letters

# main model
fit.s1b <- lmer(Mean ~ CondEff * HemifieldEff * EccentricityEff 
            + (1 | SUBJECT)
            + (0 + CondEff | SUBJECT)
            + (0 + HemifieldEff | SUBJECT)
            + (0 + EccentricityEff | SUBJECT)
            , data = s1b_dat)

summary(fit.s1b)
anova(fit.s1b, type = 3)

# upright only follow up
fit.s1b.upr <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1b_dat[s1b_dat$Condition == "Upright", ] )

summary(fit.s1b.upr)
anova(fit.s1b.upr, type = 3)

# gabor only follow up
fit.s1b.gab <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1b_dat[s1b_dat$Condition == "Gabor", ] )

summary(fit.s1b.gab)
anova(fit.s1b.gab, type = 3)

#### Cross-study analysis ####

## combine data
# inverted data
s1a_dat %>%
  filter(Condition == "Inverted") %>%
  mutate(SUBJECT = paste0(SUBJECT,'_2'),# new subject id because different subjects in both exps
         CondEff = -0.5) -> INV_dat  # set inv condition to -0.5 effect code (gabors are already 0.5)

# combine with gabor data
INV_dat %>%
  rbind(filter(s1b_dat, Condition == "Gabor")) -> combined_dat
  
# model
fit.inv_gab <- lmer(Mean ~ CondEff * HemifieldEff * EccentricityEff 
            + (1 | SUBJECT)
            + (0 + HemifieldEff | SUBJECT)
            + (0 + EccentricityEff | SUBJECT)
            , data = combined_dat)

summary(fit.inv_gab)
anova(fit.inv_gab, type = 3)


