# Analysis for Study 1 of ""

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

# load cleaned data
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

all_pdat[all_pdat$Experiment == 'INV', ] %>%
  ggplot(aes(Stair, mean, fill = Condition)) +
    geom_bar(stat="identity", position = 'dodge', aes(fill = Condition)) +
    ylim(ylimits) +
    scale_fill_manual("Condition", values = c("Inverted" = "#cc0000", "Upright" = "#00c1d6")) +
    scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
    geom_errorbar(position = position_dodge(.9), aes(ymin = mean - se, ymax = mean + se), width=0.2) + 
    labs(x = 'Location', y = 'Proportion of eccentricity', 
         title = 'Inverted vs Normal letters') +
    theme_bw() +
    theme(text = element_text(size=20)) -> p1

all_pdat[all_pdat$Experiment == 'GAB', ] %>%
  ggplot(aes(Stair, mean, fill = Condition)) +
  geom_bar(stat="identity", position = 'dodge', aes(fill = Condition)) +
  ylim(ylimits) +
  scale_fill_manual("Condition", values = c("Gabor" = "#cc0000", "Upright" = "#00c1d6")) +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = mean - se, ymax = mean + se), width=0.2) + 
  labs(x = 'Location', y = 'Proportion of eccentricity', 
       title = 'Gabors vs Normal letters') +
  theme_bw() +
  theme(text = element_text(size=20)) -> p2

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
Anova(fit.s1a, type = 3)

# upright only follow up
fit.s1a.upr <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                + (1 | SUBJECT)
                + (0 + HemifieldEff | SUBJECT)
                + (0 + EccentricityEff | SUBJECT)
                , data = s1a_dat[s1a_dat$Condition == "Upright", ] )

summary(fit.s1a.upr)
Anova(fit.s1a.upr, type = 3)

# inverted only follow up
fit.s1a.inv <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1a_dat[s1a_dat$Condition == "Inverted", ] )

summary(fit.s1a.inv)
Anova(fit.s1a.inv, type = 3)

## Study 1b - gabors vs upright letters

# main model
fit.s1b <- lmer(Mean ~ Condition * HemifieldEff * EccentricityEff 
            + (1 | SUBJECT)
            + (0 + CondEff | SUBJECT)
            + (0 + HemifieldEff | SUBJECT)
            + (0 + EccentricityEff | SUBJECT)
            , data = s1b_dat)

summary(fit.s1b)
Anova(fit.s1b, type = 3)

# upright only follow up
fit.s1b.upr <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1b_dat[s1b_dat$Condition == "Upright", ] )

summary(fit.s1b.upr)
Anova(fit.s1b.upr, type = 3)

# gabor only follow up
fit.s1b.gab <- lmer(Mean ~ HemifieldEff * EccentricityEff 
                    + (1 | SUBJECT)
                    + (0 + HemifieldEff | SUBJECT)
                    + (0 + EccentricityEff | SUBJECT)
                    , data = s1b_dat[s1b_dat$Condition == "Gabor", ] )

summary(fit.s1b.gab)
Anova(fit.s1b.gab, type = 3)

#### Cross-study analysis ####

## combine data
# inverted data
s1a_dat %>%
  filter(Condition == "Inverted") %>%
  mutate(SUBJECT = paste0(SUBJECT,'_2')) -> INV_dat # new subject id because different subjects in both exps

# combine with gabor data
INV_dat %>%
  rbind(filter(s1b_dat, Condition == "Gabor")) -> combined_dat
  
# model
fit.inv_gab <- lmer(Mean ~ Condition * HemifieldEff * EccentricityEff 
            + (1 | SUBJECT)
            + (0 + HemifieldEff | SUBJECT)
            + (0 + EccentricityEff | SUBJECT)
            , data = combined_dat)

summary(fit.inv_gab)
Anova(fit.inv_gab, type = 3)


