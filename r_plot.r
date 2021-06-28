## This is the R script to generate Figure 3.

library(wesanderson)
library(readr)
library(ggplot2)
library(gridExtra)


final_plot <- read_csv("final_plot.csv")

p<-ggplot(data=final_plot,mapping =aes(x=field,y=`average number of times this phrase appeared in the journal`,fill=field))
p+geom_col()+facet_wrap(~`word`)+scale_fill_brewer(palette="Dark2")+ theme(
  axis.title.x=element_blank(),
  axis.text.x=element_blank(),
  text=element_text(size=14))


