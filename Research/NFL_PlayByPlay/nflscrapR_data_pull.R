library(nflscrapR)

po_season_play_by_play <- function(Season) {
    # Google R style format
    # Below the function put together the proper URLs for each playoff game in each 
    # season and runs the game_play_by_play function across the entire season
    game_ids <- extracting_gameids(Season, TRUE)
    pbp_data_unformatted <- lapply(game_ids, FUN = game_play_by_play)
    df_pbp_data <- dplyr::bind_rows(pbp_data_unformatted) %>% 
                   dplyr::mutate(Season = Season)
    # Output #
    df_pbp_data
}
save_all_seasons_pbp <- function(){
    for (season in c(2009,2010,2011,2012,2013,2014,2015,2016)){
        print(paste('Extracting Regular',season,'season'))
        rs <- season_play_by_play(season)
        write.csv(rs,paste('rs_pbp_',season,'.csv'))
        
        print(paste('Extracting Playoffs',season,'season'))
        po <- po_season_play_by_play(season)
        write.csv(po,paste('po_pbp_',season,'.csv'))
    }
}