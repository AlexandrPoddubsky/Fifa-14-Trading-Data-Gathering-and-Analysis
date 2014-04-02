from fifa14search.player import Player, SofifaSearch
from core import TradeItemInfoAnalysis, TradeItemInfoAnalysisCollector
import pkg_resources 
import logging
import pandas


class IntegratedPlayerInfo(object):
    """main class in order to access player related infos"""
    
    player_file = pkg_resources.resource_filename('fut14gathering', 'players.txt')
    output_folder='player_stats'
    search_engine = SofifaSearch
    logger = logging.getLogger("IntegratedPlayerInfo")
    
    def __init__(self, assetId=None, player_name=None, output_folder=None):
        if assetId:
            self.player = IntegratedPlayerInfo.search_player_by_assetId(assetId)
        elif player_name:
            self.player = IntegratedPlayerInfo.search_player_by_name(player_name)
        else:
            raise ValueError("need to specify assetId or player name to determine the player")
        self.output_folder = output_folder if output_folder else IntegratedPlayerInfo.output_folder
        self.player_stat_file = "%s/%s" % (self.output_folder, self.player.assetId)
        self.financial_collector = TradeItemInfoAnalysisCollector()
        self.update_trade_item_info_data()
        
    def get_min_max_data_frame(self):
        final_series = self.financial_collector.get_min_max_bins_player()
        return pandas.DataFrame(final_series, index=self.financial_collector.get_time_series()) 

    def get_min_data_frame(self):
        final_series = self.financial_collector.get_min_bins_player()
        return pandas.DataFrame(final_series, index=self.financial_collector.get_time_series()) 
    
    def get_max_data_frame(self):
        final_series = self.financial_collector.get_max_bins_player()
        return pandas.DataFrame(final_series, index=self.financial_collector.get_time_series()) 

    def get_all_possible_keys(self):
        return self.financial_collector.get_all_player_types()
        
    def update_trade_item_info_data(self):
        try:
            with open(self.player_stat_file, 'r') as f:
                self.logger.debug("opening trading data: %s" % self.player_stat_file)
                financial = TradeItemInfoAnalysis(self.player, f.read().strip())
                self.financial_collector.add_financial_analysis(financial)
        except IOError:
            IntegratedPlayerInfo.logger.warn("no stats data found for %s" % str(self.player.assetId))
                
        
    @staticmethod
    def search_player_by_name(name, search_in_cache=True):
        if search_in_cache:
            player = IntegratedPlayerInfo._search_in_cache(name)
            if player:
                return player
        
        player = IntegratedPlayerInfo.search_engine.get_player_by_name(name)
        IntegratedPlayerInfo._add_to_cache(player)
        return player
    
    @staticmethod
    def search_player_by_assetId(asset_id, search_in_cache=True):
        if search_in_cache:
            player = IntegratedPlayerInfo._search_in_cache(asset_id)
            if player:
                IntegratedPlayerInfo.logger.debug("found in cache: %s" % asset_id)
                return player
        IntegratedPlayerInfo.logger.debug("looking up player info: %s" % asset_id)
        player = IntegratedPlayerInfo.search_engine.get_player_by_asset_id(asset_id)
        IntegratedPlayerInfo._add_to_cache(player)
        return player
    
    @staticmethod    
    def _search_in_cache(name):
        with open(IntegratedPlayerInfo.player_file, 'r+') as f:
            players = f.readlines()
            for cached_player_line in players:
                if name in cached_player_line:
                    player_name = ' '.join(cached_player_line.split(' ')[1:]).strip()
                    player_asset_id = cached_player_line.split(' ')[0]
                    return Player(player_asset_id, player_name)

    @staticmethod
    def _add_to_cache(player):
        with open(IntegratedPlayerInfo.player_file, 'a+') as f:
            player_line = "%s %s\n" % (player.assetId, player.name)
            f.write(player_line.encode('UTF-8'))
