#########################################################################################################################################
#load and transform overall stats.
overalltrade <- read_delim("Documents/GitHub/uiuc-projects/498dataviz/data/overalltrade.tsv", "\t", escape_double = FALSE, trim_ws = TRUE)
str(overalltrade)

#fix some of the column names.
overalltrade$TradeUsd = overalltrade$`Trade Usd`
overalltrade$Country = overalltrade$`Country Or Area`
overalltrade$WeightKg = overalltrade$`Weight Kg`

# subset and take columns of interest
trade_stats = overalltrade[, c(6,2,5,7)]
trade_stats = trade_stats[order(TradeUsd),]

# add a new column for trade in billions.
trade_stats$TradeInBillions =  as.numeric(format(round(trade_stats$TradeUsd / 1e9, 0), trim = TRUE))

# add a new column to convert weight to Tonnes. 1 tonne = 1000 KG.
trade_stats$WeightInMegaTonnes =  as.numeric(format(round(trade_stats$WeightKg / 1e6, 0), trim = TRUE))

trade_stats
# print min and max - to be used for y-xis domain
c(min(trade_stats$TradeInBillions), max(trade_stats$TradeInBillions))

dir = getwd()
filePath = file.path(dir, "trade_stats.csv")
filePath
write_csv(trade_stats, filePath , na = "NA", append = FALSE)

#test by reading the file back.
head(read_csv(filePath))
########################################################################################################################################
