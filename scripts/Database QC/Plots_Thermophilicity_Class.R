# import packages
library("dplyr")
library("ggplot2")

# in working directory
data <- read.csv("Total.tsv" ,header=TRUE, sep = "\t", colClasses=c(
  "ncbiTaxID"="character", "Temp"="numeric"))

# change types
data$Temp = as.numeric(data$Temp)
data$Source = as.factor(data$Source)
data$Phylum <- as.factor(data$Phylum)
# replace Lyubetsky et al., 2020 with its abbreviation Lyu2020
levels(data$Source) <- c("aciDB", "BacDive", "CCUG", "CECT", "Lyu2020", 
                         "MediaDB", "NCTC", "NIES", "TEMPURA", "ThermoBase")

# average tehe temperature
agg_tbl <- data %>% group_by(Source, ncbiTaxID) %>% 
  summarise(Temp=mean(Temp))

# annotate with the thermophilicity class
data3 <- agg_tbl %>% mutate(Status = case_when( (Temp < 15) ~ "Psychrophile", 
                                             (Temp >= 15 & Temp <= 45) ~ "Mesophile", 
                                             (Temp > 45 & Temp <= 80) ~ "Thermophile", 
                                             (Temp > 80) ~ "Hyperthermophile" ))                                
data3$Status[is.na(data3$Status)] <- "other";
data3$Status <- as.factor(data3$Status)

# plot the thermophilicity class distribution within each database
plotTC <- ggplot(data3, aes(x = factor(Status, levels = c("Psychrophile", "Mesophile", "Thermophile", "Hyperthermophile")))) +
  geom_bar(aes(fill=factor(Source)), position= "fill") + ylab("Fraction") +
  xlab("Thermophilicity class") + theme_classic() +  scale_fill_brewer(name="", palette = "Paired") +
  theme(axis.text=element_text(size=12, color = "black"),axis.title=element_text(size=14), 
                           legend.title=element_text(size=14), legend.text=element_text(size=12)) + 
  theme(legend.position="bottom") + coord_flip()

plotTC

# plot the database distribution for each thermophilicity class
plotSourceTC <- ggplot(data3, aes(x = factor(Source))) +
  geom_bar(aes(fill=factor(Status, levels = c("Psychrophile", "Mesophile", "Thermophile", "Hyperthermophile"))), position= "fill") + ylab("Fraction") +
  xlab("Database") + theme_classic() +  scale_fill_manual("Class", 
        values = c("Psychrophile" = "#ABD1F3","Mesophile" = "#0F52BA", "Thermophile"= "#F88379", 
                   "Hyperthermophile" = "#E34234")) +
  theme(axis.text=element_text(size=12, color = "black"),axis.title=element_text(size=14), 
        legend.title=element_text(size=14), legend.text=element_text(size=12)) + 
  theme(legend.position="bottom") + coord_flip()

plotSourceTC
