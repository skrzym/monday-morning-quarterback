library(nflscrapR)

for (season in c(2009,2010,2011,2012,2013,2014,2015,2016)){
    
    print(paste('Extracting Regular',season,'season'))
    rs <- season_play_by_play(season)
    write.csv(rs,paste('rs_pbp_',season,'.csv'))
    #rs <- extracting_gameids(season,FALSE)
    #count = 0
    #for (game in rs){
    #    print(paste('Game ', count, ' of ', length(rs)))
    #    write.csv(game_play_by_play(game),paste('rs_pbp_',season,'.csv'))
    #    count <- count + 1
    #}
    
    print(paste('Extracting Playoffs',season,'season'))
    po <- extracting_gameids(season,TRUE)
    count = 0
    for (game in po){
        print(paste('Game ', count, ' of ', length(rs)))
        write.csv(game_play_by_play(game),paste('po_pbp_',season,'.csv'))
        count <- count + 1
    }
}
