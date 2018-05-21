rm(list = ls())
library(ggplot2)
library(ggmap)
library(ggrepel)
setwd("C:\\Users\\nwfxy\\Dropbox\\ProgrammingProjects\\mrt_breakdown\\DataViz\\DataViz")

station_c2 <- read.csv("station_count2.csv")
station_names <- read.csv("train-station-chinese-names.csv")


m <- get_map("Singapore",zoom = 11,scale = 1,color = "bw")

EW <- station_c2[grepl("EW",station_c2$station) ,]
EW$order <- as.numeric(gsub("[^0-9]","",EW$station))
EW <- EW[order(EW$order),]
EW$station_short <- substr(EW$mrt_station_english,1,5)

x <- qmap("Singapore",base_layer = ggplot(aes(x = lon, y = lat,label = mrt_station_english), data = EW),zoom = 11,scale = 1,color = "bw")
x + geom_point(aes(color = count), size = 5) + scale_color_gradientn(colors = c("green","grey45"),limits = c(1,60))  + geom_path(size = 1.5,mapping = aes(color = count)) +
  geom_text(aes(label= station_short, fontface = "italic"),size = 3.5,hjust = 0.5, vjust= -2) + 
  geom_text(aes(label= station, fontface = "bold"),size = 3.5,hjust = 0.5, vjust= -1) + geom_label(aes(label= count, fontface = "bold"),size = 3,hjust = 0.5, vjust= 1.5) 




CC <- station_c2[grepl("CC",station_c2$station) ,]
CC$order <- as.numeric(gsub("[^0-9]","",CC$station))
CC <- CC[order(CC$order),]
CC$station_short <- substr(CC$mrt_station_english,1,5)

x <- qmap("Singapore",base_layer = ggplot(aes(x = lon, y = lat,label = mrt_station_english), data = CC),zoom = 12,scale = 1,color = "bw")
x + geom_point(aes(color = count), size = 5) +  scale_color_gradientn(colors = c("darkorange","grey45"),limits = c(1,60))  + geom_path(size = 1.5,mapping = aes(color = count)) +
  geom_text(aes(label= station_short, fontface = "italic"),size = 3.5,hjust = 0.5, vjust= -2, color = "black") + 
  geom_text(aes(label= station, fontface = "bold"),size = 3.5,hjust = 0.5, vjust= -1) + geom_label(aes(label= count, fontface = "bold"),size = 3,hjust = 0.5, vjust= 1.5) 




NS <- station_c2[grepl("NS",station_c2$station) ,]
NS$order <- as.numeric(gsub("[^0-9]","",NS$station))
NS <- NS[order(NS$order),]
NS$station_short <- substr(NS$mrt_station_english,1,5)

x <- qmap("Singapore",base_layer = ggplot(aes(x = lon, y = lat,label = mrt_station_english), data = NS),zoom = 12,scale = 1,color = "bw")
x + geom_point(aes(color = count), size = 5)+ scale_color_gradientn(colors = c("red","grey45"),limits = c(1,120))  + geom_path(size = 1.5,mapping = aes(color = count)) +
  geom_text(aes(label= station_short, fontface = "italic"),size = 3.5,hjust = 0.5, vjust= -2, color = "black") + 
  geom_text(aes(label= station, fontface = "bold"),size = 3.5,hjust = 0.5, vjust= -1, color = "navyblue") + geom_label(aes(label= count, fontface = "bold"),size = 3,hjust = 0.5, vjust= 1.5) 



NE <- station_c2[grepl("NE",station_c2$station) ,]
NE$order <- as.numeric(gsub("[^0-9]","",NE$station))
NE <- NE[order(NE$order),]
NE$station_short <- substr(NE$mrt_station_english,1,5)

x <- qmap("Singapore",base_layer = ggplot(aes(x = lon, y = lat,label = mrt_station_english), data = NE),zoom = 11,scale = 1,color = "bw")
x + geom_point(aes(color = count), size = 5) + scale_color_gradientn(colors = c("purple","grey45"),limits = c(1,60)) + geom_path(size = 1.5,mapping = aes(color = count)) +
  geom_text(aes(label= station_short, fontface = "italic"),size = 3,hjust = 1.5, vjust= -2,color = "purple") + 
  geom_text(aes(label= station, fontface = "bold"),size = 3.5,hjust = 0.5, vjust= -1, color = "navyblue") + geom_label(aes(label= count, fontface = "bold"),size = 3,hjust = -0.5, vjust= 1.5) 


