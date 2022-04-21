library(tidyverse)
library(readxl)

mycotoxin_df <- read_excel("~/BostonUniversity/BF768/homework/database_project/BiologicalRemovalOfMycotoxins.xlsx")

col_info <- mycotoxin_df[1,]

mycotoxin_df <- mycotoxin_df %>% 
  filter(!is.na(`#`)) %>%
  select(-`#`)

#make domains consistent
dom <- str_replace_all(str_to_title(mycotoxin_df$Domain), pattern = "Eukary.*", replacement = "Eukarya")

#pathogen categories: Pathogenic, Non-Pathogenic, Opportunistic 
paths <- str_to_title(mycotoxin_df$`Pathogen?`)
paths <- str_replace_all(string = paths, pattern = ".*Opport.*", replacement = "Opportunistic")
paths <- str_replace_all(string = paths, pattern = ".*Non.Path.*", replacement = "Non-Pathogenic")
paths <- str_replace_all(string = paths, pattern = ".* Path.*|Path.*", replacement = "Pathogenic")

#aerobic or anaerobic: make consistent (all values either "Aerobic", "Anaerobic", or "Facultative")
aran <- str_to_title(mycotoxin_df$`Aerobic or Anaerobic?`)
aran<- str_replace_all(string = aran, pattern = ".*Facult.*", replacement = "Facultative")
aran<- str_replace_all(string = aran, pattern = ".*Anaer.*", replacement = "Anaerobic")
aran<- str_replace_all(string = aran, pattern = ".*Aer.*", replacement = "Aerobic")

#native environment: lots of info in this one so add column with all values in 
#("Human", "Soil", "Water", "Plants", "Other")

#removal mechanism in ("Biotransformation", "Absorption", "Adsorption", "Degradation", "Regulation", Unknown")

#enzymatic
enz <- str_to_title(mycotoxin_df$`Enzymatic?`)
enz <- str_replace(string = enz, pattern = "Unk.*", replacement = "Unknown")

#intra/extra cellular
cell <- str_to_title(mycotoxin_df$`Intracellular or Extracellular?`)
cell <- str_replace(string = cell, pattern = "Un.*|Likely.*|Na", replacement = "Unknown")
cell <- str_replace(string = cell, pattern = "Extra.*", replacement = "Extracellular")
cell <- str_replace(string = cell, pattern = "Intra.*", replacement = "Intracellular")

mycotoxin_df <- mycotoxin_df %>%
  mutate(Domain = dom, 
         `Pathogenicity` = paths, 
         `Respiration` = aran, 
         `Mycotoxin` = str_to_title(`Target mycotoxin`),
         `Enzymatic?` = enz,
         `Location` = cell %>% replace_na("Unknown"),
         `Enzyme identified?`= str_to_title(`Enzyme identified?`)) %>%
  separate_rows(Mycotoxin, sep = "(/|,|And)+") %>%
  separate_rows(Organism, sep = "(/|,)+") %>%
  select(-c(`Intracellular or Extracellular?`, `Pathogen?`, `Target mycotoxin`, `Aerobic or Anaerobic?`)) %>%
  rename("Environment" = "Native environment")
  

write_tsv(mycotoxin_df, file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/mycotoxin_removal.tsv")

org <- mycotoxin_df %>%
  select(Organism, Domain, Pathogenicity, Respiration, Environment)
write_tsv(distinct(org), file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/organism.tsv")

lit <- mycotoxin_df %>%
  select(`Characterization context`, `Characterization assay`, Source, Link, `Additional information`)
write_tsv(distinct(lit), file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/literature.tsv")
  
cur_cont <- mycotoxin_df %>%
  select(Contributor, `Contribution date`, `Curator(s)`, `Curation date`, `Curation notes`)
write_tsv(distinct(cur_cont), file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/curation.tsv")

mycotoxin <- mycotoxin_df %>%
  select(`Mycotoxin`, `Removal mechanism`, `Enzymatic?`, Location)
write_tsv(distinct(mycotoxin), file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/mycotoxin.tsv")


