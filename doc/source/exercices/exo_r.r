nom_solution <- "freq"

fonctionsAtt<-c("table","return")

freq<-function(v,x){return(table(x)[v])}

tests<-list(
    list("2","c(1,2,1,3,4,1,2)",reponse=freq(2,c(1,2,1,3,4,1,2)))
    ,list("'a'","c('a','b','a','d','a')",reponse=freq('a',c('a','b','a','d','a')))
)

