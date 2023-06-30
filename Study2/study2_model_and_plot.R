##### SET UP, LOAD DATA ####

# packages
require(dplyr)
require(tidyr)

require(lme4)
require(lmerTest)
require(car)

require(ggplot2)
require(gridExtra)
require(effects)

# working directory
setwd("~/Box Sync/CRD_data/CRD_INDIV/CRD2")
setwd("C:/Users/kwinsler/Box/CRD_data/CRD_INDIV/CRD2")

dat <- read.csv('CRD_INDIV_data.csv')

# comment out if you wish to include native readers of latin scrips that are not english
dat %>% filter(Native_English_reader == 'Y') -> dat

#### Initial plots ####
pdat <- dat %>% 
  group_by(Stair) %>%  
  summarise(mean = mean(Mean), 
            sd = sd(Mean),
            n = n(),  
            se = sd(Mean)/sqrt(n()))

ggplot(pdat, aes(Stair, mean)) +
  geom_bar(stat="identity", fill = "#00c1d6") +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = mean - se, ymax = mean + se), width=0.2) + 
  labs(x = 'Location', y = 'Proportion of eccentricity', title = "Critical spacing per location") +
  theme_bw() +
  theme(text = element_text(size=20))

# kde plot
ggplot(dat, aes(x=Mean, color=Stair, fill = Stair)) +
  geom_density(alpha = .3) + #position = 'stack', 
  theme(text = element_text(size=20)) + 
  labs(x = 'Critical Spacing (%)', y = 'Density', title = 'Kernel density per location') +
  scale_color_manual(values=c("#e85009", "#e87909","#cc0000",  "#3546e6", "#387bd9", "#6728d4")) +
  scale_fill_manual(values=c("#e85009", "#e87909","#cc0000",  "#3546e6", "#387bd9", "#6728d4"))

# density plots for subject variables
dat %>%
  group_by(SUBJECT) %>%
  summarize(ART = min(ART),
            Spelling = min(Spelling),
            VisWM = min(VisWM)) %>%
  select(-SUBJECT) %>% 
  gather() %>% 
  ggplot(aes(value)) +
  facet_wrap(~ key, scales = "free") +
  geom_density() 

#### ANALYSIS ####

## Scale individual difference data, effect code

# make sure numeric
dat$ART <- as.numeric(dat$ART)
dat$VisWM <- as.numeric(dat$VisWM)
dat$Spelling <- as.numeric(dat$Spelling)

dat %>%
  mutate(
    
    VWM_z = scale(VisWM),
    ART_z = scale(ART),
    Spelling_z = scale(Spelling),
    
    # Effect coded
    EccentricityEff = case_when(
      Eccentricity == 'Near' ~ -.5,
      Eccentricity == 'Far' ~ 0,
      Eccentricity == 'Peripheral' ~ .5),
    
    HemifieldEff = case_when(
      Hemifield == 'Left' ~ -.5,
      Hemifield == 'Right' ~ .5)
    
  ) -> dat

# Model
fit <- lmer(Mean ~ HemifieldEff * EccentricityEff * Spelling_z
            + HemifieldEff * EccentricityEff * VWM_z 
            + HemifieldEff * EccentricityEff * ART_z
            + (1 + EccentricityEff + HemifieldEff | SUBJECT)
            , data = dat)
summary(fit)
Anova(fit, type = 3)

# Model
fit.spe <- lmer(Mean ~ HemifieldEff * EccentricityEff * Spelling_z
            + (1 + EccentricityEff + HemifieldEff | SUBJECT)
            , data = dat)

summary(fit.spe)
Anova(fit.spe, type = 3)

# Model
fit.vwm <- lmer(Mean ~ HemifieldEff * EccentricityEff * VWM_z 
            + (1 + EccentricityEff + HemifieldEff | SUBJECT)
            , data = dat)
summary(fit.vwm)
Anova(fit.vwm, type = 3)

# Model
fit.art <- lmer(Mean ~ HemifieldEff * EccentricityEff * ART_z
            + (1 + EccentricityEff + HemifieldEff | SUBJECT)
            , data = dat)
summary(fit.art)
Anova(fit.art, type = 3)

#### Model plots ####

## Main effect plots
av_subThresh <- dat %>%
  group_by(SUBJECT) %>%
  summarize(Mean_threshold = mean(Mean),
            VWM = min(VWM_z),
            SPE = min(Spelling_z),
            ART = min(ART_z))

# SPELL
SPE_cor <- ggplot(av_subThresh, aes(SPE, Mean_threshold)) +
  geom_point() +
  geom_smooth(method=lm, color = "#6976FF") +
  labs(x = 'Spelling (z)', y = 'Average critical distance', title = 'Spelling') +
  theme_bw() +
  theme(text = element_text(size=20))

# ART
ART_cor <- ggplot(av_subThresh, aes(ART, Mean_threshold)) +
  geom_point() +
  geom_smooth(method=lm, color = "#9B74FF") +
  labs(x = 'Author recognition (z)', y = 'Average critical distance', title = 'Author recognition') +
  theme_bw() +
  theme(text = element_text(size=20))

# VWM
VWM_cor <- ggplot(av_subThresh, aes(VWM, Mean_threshold)) +
  geom_point() +
  geom_smooth(method=lm, color = "#BA6EFF" ) +
  labs(x = 'Visual working memory (z)', y = 'Average critical distance', title = 'Visual working memory') +
  theme_bw() +
  theme(text = element_text(size=20))

# combined
grid.arrange(SPE_cor, ART_cor, VWM_cor, nrow = 1)



## Effect plots

summary(fit)
y_efflimits <- c(-0.075,0.025)

## VWM
# get effects
vwmEffects <- Effect(c('HemifieldEff', 'EccentricityEff', 'VWM_z'), 
                     xlevels=list(HemifieldEff = c(-0.5,0.5),
                                  EccentricityEff = c(-0.5,0,0.5),
                                  VWM_z = c(-.5,.5)), 
                     fit)

vwmEffects <- as.data.frame(vwmEffects)

vwmEffects %>%
  group_by(EccentricityEff, HemifieldEff) %>%
  summarise(slope = fit[VWM_z == 0.5] - fit[VWM_z == -0.5],
            se = mean(se[VWM_z == 0.5],se[VWM_z == -0.5])) %>%
  mutate(Stair = case_when(
    EccentricityEff == 0.5 & HemifieldEff == -0.5 ~ "-6",
    EccentricityEff == 0 & HemifieldEff == -0.5 ~ "-4",
    EccentricityEff == -0.5 & HemifieldEff == -0.5 ~ "-2",
    EccentricityEff == -0.5 & HemifieldEff == 0.5 ~ "+2",
    EccentricityEff == 0 & HemifieldEff == 0.5 ~ "+4",
    EccentricityEff == 0.5 & HemifieldEff == 0.5 ~ "+6")) -> vwmEffects

# plot
vwm_effplot <- ggplot(vwmEffects, aes(Stair, slope)) +
  geom_bar(stat="identity", fill = "#BA6EFF") +
  ylim(y_efflimits) +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = slope - se, ymax = slope + se), width=0.2) + 
  labs(x = 'Location', y = 'Predicted spacing change') +
  theme_bw() +
  theme(text = element_text(size=20))

## Spelling
# get effects
speEffects <- Effect(c('HemifieldEff', 'EccentricityEff', 'Spelling_z'), 
                     xlevels=list(HemifieldEff = c(-0.5,0.5),
                                  EccentricityEff = c(-0.5,0,0.5),
                                  Spelling_z = c(-.5,.5)), 
                     fit)

speEffects <- as.data.frame(speEffects)

speEffects %>%
  group_by(EccentricityEff, HemifieldEff) %>%
  summarise(slope = fit[Spelling_z == 0.5] - fit[Spelling_z == -0.5],
            se = mean(se[Spelling_z == 0.5],se[Spelling_z == -0.5])) %>%
  mutate(Stair = case_when(
    EccentricityEff == 0.5 & HemifieldEff == -0.5 ~ "-6",
    EccentricityEff == 0 & HemifieldEff == -0.5 ~ "-4",
    EccentricityEff == -0.5 & HemifieldEff == -0.5 ~ "-2",
    EccentricityEff == -0.5 & HemifieldEff == 0.5 ~ "+2",
    EccentricityEff == 0 & HemifieldEff == 0.5 ~ "+4",
    EccentricityEff == 0.5 & HemifieldEff == 0.5 ~ "+6")) -> speEffects

spe_effplot <- ggplot(speEffects, aes(Stair, slope)) +
  geom_bar(stat="identity", fill = "#6976FF") +
  ylim(y_efflimits) +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = slope - se, ymax = slope + se), width=0.2) + 
  labs(x = 'Location', y = 'Predicted spacing change') +
  theme_bw() +
  theme(text = element_text(size=20))

## ART
# get effects
ARTEffects <- Effect(c('HemifieldEff', 'EccentricityEff', 'ART_z'), 
                     xlevels=list(HemifieldEff = c(-0.5,0.5),
                                  EccentricityEff = c(-0.5,0,0.5),
                                  ART_z = c(-.5,.5)), 
                     fit)

ARTEffects <- as.data.frame(ARTEffects)

ARTEffects %>%
  group_by(EccentricityEff, HemifieldEff) %>%
  summarise(slope = fit[ART_z == 0.5] - fit[ART_z == -0.5],
            se = mean(se[ART_z == 0.5],se[ART_z == -0.5])) %>%
  mutate(Stair = case_when(
    EccentricityEff == 0.5 & HemifieldEff == -0.5 ~ "-6",
    EccentricityEff == 0 & HemifieldEff == -0.5 ~ "-4",
    EccentricityEff == -0.5 & HemifieldEff == -0.5 ~ "-2",
    EccentricityEff == -0.5 & HemifieldEff == 0.5 ~ "+2",
    EccentricityEff == 0 & HemifieldEff == 0.5 ~ "+4",
    EccentricityEff == 0.5 & HemifieldEff == 0.5 ~ "+6"))-> ARTEffects

# plot
art_effplot <- ggplot(ARTEffects, aes(Stair, slope)) +
  geom_bar(stat="identity", fill = "#9B74FF") +
  ylim(y_efflimits) +
  scale_x_discrete(limits=c("-6","-4","-2","+2","+4","+6")) +
  geom_errorbar(position = position_dodge(.9), aes(ymin = slope - se, ymax = slope + se), width=0.2) + 
  labs(x = 'Location', y = 'Predicted spacing change') +
  theme_bw() +
  theme(text = element_text(size=20))


## all combined
grid.arrange(SPE_cor, ART_cor, VWM_cor,
             spe_effplot, art_effplot, vwm_effplot,
             nrow = 2)
