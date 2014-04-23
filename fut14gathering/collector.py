import logging
import fut14
from fifa14search.player import SofifaSearch
from fut14analysis.core import TradeItemInfo, TradeItemInfoAnalysis
import time
import itertools



class TradeInfoEngine(object):
    
    def __init__(self, username, password, secret_answer, platform, debug=False):
        self.fut = fut14.Core(username, password, secret_answer, platform=platform, debug=debug)
        self.search_engine = SofifaSearch
        self.logger = logging.getLogger("TradeInfoEngine")
        
    def get_current_player_trades(self, player, max_pages=100, page_size=5, start_with_page=0):
        results = []
        cur_time = time.time()
        for i in range(start_with_page, max_pages):
            try:
                result_page = self.fut.searchAuctions('player', assetId=player.assetId, start=i*page_size, page_size=page_size)
                self.logger.debug("search for player %s got %i results" % (player.assetId, len(result_page)))
                if result_page:
                    results.append([TradeItemInfo(result, cur_time) for result in result_page])
                else:
                    break
            except:
                break
        infos = itertools.chain(*results)
        finance = TradeItemInfoAnalysis(player)
        finance.add_trade_item_infos(infos)
        return finance
    
class DataCollector(object):
    """collects trade info data"""
    
    def __init__(self, output_folder='player_stats'):
        self.output_folder = output_folder
        self.logger = logging.getLogger('DataCollector')
        
        
    def gather_data(self, player, trader_engine):
        """gets actual """
        player_file = "%s/%s" % (self.output_folder, player.assetId)
        self.logger.debug('retrieving info about %s' % player.assetId)
        finance_analysis = trader_engine.get_current_player_trades(player, max_pages=4, page_size=50)
        self.logger.debug('storing info about %s' % player.assetId)
        with open(player_file, 'a+') as f:
            all_data = '\n%s' % (finance_analysis.create_compact_data())
            f.write(all_data)
        self.logger.debug('completed storing info about %s' % player.assetId)
        return finance_analysis
