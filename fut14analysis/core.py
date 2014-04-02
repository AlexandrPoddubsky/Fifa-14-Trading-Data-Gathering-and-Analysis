import itertools
from collections import defaultdict
import collections
import logging
import datetime

        
class TradeItemInfo(object):
    """crucial information about a trade item is stored here"""
    
    def __init__(self, result=None, cur_time=None):
        
        if result:
            self.result = result
            self.buy_now = result['buyNowPrice']
            self.trade_id = result['tradeId']
            self.starting_bid = result['startingBid']
            self.current_bid = result['currentBid']
            self.rating = result['rating']
            self.position = result['position']
            self.offers = result['offers']
            self.formation = result['formation']
            self.discard_value = result['discardValue']
            self.owners = result['owners']
            self.last_price = result['lastSalePrice']
            self.asset_id = result['assetId']
            self.item_id = result['id']
        self.info_time = cur_time

    def __eq__(self, other):
        if isinstance(other, TradeItemInfo):
            return other.trade_id == self.trade_id
        else:
            return False
        
    def __hash__(self):
        return int(self.trade_id)
        
    def __str__(self):
        return "R %s BUY %s BID %s POS %s OWN %s (%s) TRADE %s" % (self.rating, self.buy_now, self.starting_bid, self.position, self.owners, self.last_price, self.trade_id)  
        
    def __repr__(self):
        return str(self)
    
    
class TradeItemInfoAnalysis(object):
    """analysis based on multiple TradeItemInfos is done here"""
    
    def __init__(self, player, unstructured_data=None):
        self.infos = defaultdict(set)
        self.player = player
        self.logger = logging.getLogger("TradeItemInfoAnalysis")
        if unstructured_data:
            self._parse_compact_data(unstructured_data)
            
    def add_trade_item_info(self, info):
        key = "%s/%s/%s" % (info.rating, info.position, info.formation)
        self.infos[key].add(info)
        
    def add_trade_item_infos(self, infos):
        for info in infos:
            self.add_trade_item_info(info)
            
    def get_bins(self, fun):
        """applies the user defined TradeItemInfo selction function on a set of TradeItemInfos based on player's rating, position and formation"""
        lowest_bins = {}
        for key in self.infos:
            buy_nows = [int(v.buy_now) for v in self.infos[key] if int(v.buy_now) > 0]
            if buy_nows:
                lowest_bins[key] = fun(buy_nows)
        
        return lowest_bins

    def get_lowest_bins(self):
        """gets lowest buy now prices based on player's rating, position and formation"""
        return self.get_bins(min)
    
    def get_highest_bins(self):
        """gets highest buy now prices based on player's rating, position and formation"""
        return self.get_bins(max)
    
    def get_highest_bin(self):
        """gets highest buy now price """
        return max(self.get_highest_bins().values())
    
    def get_lowest_bin(self):
        """gets lowest buy now price """
        return min(self.get_lowest_bins().values())
    
    def create_compact_data(self):
        strings = []
        for info_values in self.infos.values():
            for info in info_values:
                strings.append('%i %s %s %s %s %s %s %s %s' % (info.info_time, info.rating, info.buy_now, info.starting_bid, info.position, info.formation, info.owners, info.last_price, info.trade_id))
        return '\n'.join(strings)
    
    def _parse_compact_data(self, unstructured_data):
        for line in unstructured_data.strip().split('\n'):
            info = TradeItemInfo()
            if line:
                try:
                    info.info_time, info.rating, info.buy_now, info.starting_bid, info.position, info.formation, info.owners, info.last_price, info.trade_id = line.split(' ')
                    info.info_time = int(info.info_time)
                    self.add_trade_item_info(info)
                except ValueError:
                    self.logger.error("could not parse line: %s" % line)

    def __str__(self):
        strings = []
        for k in self.infos:
            strings.append('\n%s'% k)
            for v in self.infos[k]:
                strings.append('\t%s' % str(v))
        return '\n'.join(strings)
        
class TradeItemInfoAnalysisCollector(object):
    """collects multiple TradeItemInfoAnalysis regarding the TradeItemInfo collection time
    the objective is to build a series of TradeItemInfoAnalysis
    """
    
    @staticmethod
    def max_bin_filter(financial_analysis): 
        return financial_analysis.get_highest_bin()
        
    @staticmethod
    def min_bin_filter(financial_analysis):
        return financial_analysis.get_lowest_bin()
    
    @staticmethod
    def min_bins_filter(financial_analysis):
        return financial_analysis.get_lowest_bins()
    
    def __init__(self):
        self.slots = {}
        
    def build_series(self, fun, interesting_keys):
        series = list(self.get_series(fun))
        final_series = collections.defaultdict(list)
        for d in series:
            for k in interesting_keys:
                if k in d:
                    final_series[k].append(d[k])
                else:
                    final_series[k].append(0)
        return final_series
    
    def get_all_player_types(self):
        series = list(self.get_series(TradeItemInfoAnalysisCollector.min_bins_filter))
        all_keys = set()
        for d in series:
            all_keys |= set(d.keys())
        return all_keys
    
    def add_financial_analysis(self, financial_analysis):
        info_data = financial_analysis.infos.values()
        infos = itertools.chain(*info_data)
        for info in infos:
            if info.info_time not in self.slots:
                self.slots[info.info_time] = TradeItemInfoAnalysis(financial_analysis.player)
            self.slots[info.info_time].add_trade_item_info(info)

    def get_time_series(self):
        return [datetime.datetime.fromtimestamp(int(timestamp)) for timestamp in sorted(self.slots.keys())]
    
    def get_min_max_bins_player(self):
        return {'min' : self.get_min_bins_player(), 'max': self.get_max_bins_player()}

    def get_min_bins_player(self):
        return list(self.get_series(TradeItemInfoAnalysisCollector.min_bin_filter))
    
    def get_max_bins_player(self):
        return list(self.get_series(TradeItemInfoAnalysisCollector.max_bin_filter))

    def get_series(self, fun):
        for time_info_sec in self.slots.keys():
            if time_info_sec in self.slots:
                yield fun(self.slots[time_info_sec])
            else:
                yield None
