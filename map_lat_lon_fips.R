library(sf)
library(tidyverse)
library(haven)

protest <- read_dta("/Users/bomikang/Downloads/protest_ori9.dta")

counties<-st_read("/Users/bomikang/Downloads/cb_2018_us_county_500k/cb_2018_us_county_500k.shp", quiet=T)
df <- read.csv("/Users/bomikang/Downloads/institutions_geo_all.csv")
df <- subset(df, country == "United States")
df<-df%>%
  filter(!is.na(latitude), !is.na(longitude)) %>%
  st_as_sf(coords = c("longitude", "latitude"), crs=st_crs(counties))

intersected <- st_intersects(df, counties)

df_final <- df %>%
  mutate(intersection = as.integer(intersected),
         fips = if_else(is.na(intersection), "",
                        counties$GEOID[intersection]))

protest$geoid <- as.character(protest$geoid)
df_final$fips <- as.character(df_final$fips)

merged_data <- merge(protest, df_final, by.x = "geoid", by.y = "fips", all = FALSE)
selected_columns <- merged_data %>%
  select(geoid, state_name, county_name, ori9, protest, id, name, city)
write.csv(selected_columns, "/Users/bomikang/Downloads/protest_county_institutions.csv", row.names = FALSE)
