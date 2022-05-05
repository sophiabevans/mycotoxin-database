library(readxl)
library(tidyverse)

mycotoxin_df <- read_excel("~/BostonUniversity/BF768/homework/database_project/BiologicalRemovalOfMycotoxins.xlsx")

col_info <- mycotoxin_df[1,]

mycotoxin_df <- mycotoxin_df %>% 
  filter(!(Organism == "Taxonomic name"))

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

#Text input: source, link, organism name, mycotoxin, characterization assay, 
  #identified enzyme col, additional info, char context,
  #curator, contributor, notes
#dropdown: domain, enzymatic, enzyme identified, pathogenicity, respiration, location
#checkbox: environment- text box for other, removal mechanism
#calendar: curation and contribution dates

#Environment;
#("Human", "Soil", "Water", "Plants", "Animal", "Food", Other")

#removal mechanism in ("Biotransformation", "Absorption", "Adsorption", "Degradation", "Regulation", Unknown")
rem <-str_to_title(mycotoxin_df$`Removal mechanism`)
rem <- str_replace_all(string = rem, pattern = ".*Regulation.*", replacement = "Regulation")
rem <- str_replace_all(string = rem, pattern = "Adsorption,.*", replacement = "Adsorption")
rem <- str_replace_all(string = rem, pattern = "Biotransformation \\(.*", replacement = "Biotransformation")

#enzymatic
enz <- str_to_title(mycotoxin_df$`Enzymatic?`)
enz <- str_replace(string = enz, pattern = "Unk.*", replacement = "Unknown")

#intra/extra cellular
cell <- str_to_title(mycotoxin_df$`Intracellular or Extracellular?`)
cell <- str_replace(string = cell, pattern = "Un.*|Likely.*|Na", replacement = "Unknown")
cell <- str_replace(string = cell, pattern = "Extra.*", replacement = "Extracellular")
cell <- str_replace(string = cell, pattern = "Intra.*", replacement = "Intracellular")

mycotoxin_df <- mycotoxin_df %>%
  rename("Environment" = "Native environment") %>%
  mutate(Domain = dom, 
         `Pathogenicity` = paths, 
         `Respiration` = aran, 
         `Mycotoxin` = str_to_title(`Target mycotoxin`),
          Mycotoxin = str_squish(Mycotoxin),
         `Enzymatic?` = enz,
         `Location` = cell %>% replace_na("Unknown"),
         `Enzyme identified?`= str_to_title(`Enzyme identified?`),
         `Removal mechanism` = rem) %>%
  separate_rows(Mycotoxin, sep = "(/|, |And )+") %>%
  separate_rows(Organism, sep = "(/|, )+") %>% 
  mutate(Environment = str_to_title(Environment), 
         Environment = str_replace_all(Environment, ",", ";"),
         Environment = str_replace_all(Environment, " ", ""),
         Environment = str_split(Environment, ";"),
         Organism = str_trim(Organism, side = "both"),
         "N" = row_number()) %>%
  rowwise() %>%
  mutate(Environment = str_c(str_sort(Environment), collapse = ";"),
         Environment = substring(Environment, 2)) %>%
  dplyr::select(-c(`Intracellular or Extracellular?`, `Pathogen?`, `Target mycotoxin`, `Aerobic or Anaerobic?`))

write_tsv(mycotoxin_df, file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/mycotoxin_removal.tsv")

org <- mycotoxin_df %>%
  dplyr::select(N, Domain, Organism, Pathogenicity, Respiration, Environment) %>%
  group_by(Domain, Organism, Pathogenicity, Respiration, Environment) %>%
  mutate(OrgN = min(N)) %>%
  ungroup()
  #rename(OrgN = N)

lit <- mycotoxin_df %>%
  dplyr::select(N, `Characterization context`, `Characterization assay`, Source, Link, `Additional information`) %>%
  group_by(`Characterization context`, `Characterization assay`, Source, Link, `Additional information`) %>%
  mutate(LitN = min(N)) %>%
  ungroup() 
  #rename(litN = N)
  
cur_cont <- mycotoxin_df %>%
  dplyr::select(N, Contributor, `Contribution date`, `Curator(s)`, `Curation date`, `Curation notes`) %>%
  group_by(Contributor, `Contribution date`, `Curator(s)`, `Curation date`, `Curation notes`) %>%
  mutate(CurN = min(N)) %>%
  ungroup() 


mycotoxin <- mycotoxin_df %>%
  dplyr::select(N, `Mycotoxin`, `Removal mechanism`, `Enzymatic?`, Location)%>% 
  group_by(`Mycotoxin`, `Removal mechanism`, `Enzymatic?`, Location) %>%
  mutate(MycN = min(N)) %>%
  ungroup() 


m <- inner_join(org, mycotoxin, by = "N") %>%
  inner_join(lit, by = "N") %>%
  inner_join(cur_cont, by = "N")


myc_df_N <- m %>%
  dplyr::select(N, Domain, Organism, Pathogenicity, Respiration, Environment, 
         `Mycotoxin`, `Removal mechanism`, `Enzymatic?`, Location, 
         `Characterization context`, `Characterization assay`, Source, Link, `Additional information`, 
         Contributor, `Contribution date`, `Curator(s)`, `Curation date`, `Curation notes`, OrgN, MycN, LitN, CurN) %>%
  mutate(`Contribution date` = as.character(`Contribution date`), `Curation date` = as.character(`Curation date`)) %>%
  replace(is.na(.), "NULL")


write_tsv(myc_df_N, file = "~/BostonUniversity/BF768/homework/mycotoxin-database/data/mycotoxinN.tsv")
