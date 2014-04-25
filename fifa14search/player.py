import urllib2
from google import search
from bs4 import BeautifulSoup

class Player(object):
    
    def __init__(self, assetId, name):
        self.assetId = assetId
        self.name = name
        
    def __str__(self):
        return "(%s) %s" % (self.assetId, self.name)
    
class SofifaSearch(object):
    
    @staticmethod
    def get_player_by_name(name):
        query = "site:sofifa.com inurl:14w %s" % name
        for url in search(query, stop=1):
            return SofifaSearch.extract_player_info(url)
        raise ValueError("Player not found!")
        
    @staticmethod
    def get_player_by_asset_id(asset_id):
        query = "site:sofifa.com inurl:14w ID %s" % str(asset_id)
        for url in search(query, stop=1):
            return SofifaSearch.extract_player_info(url)
        raise ValueError("Player not found!")
    
    @staticmethod
    def extract_player_info(sofifa_url):
        sofifa_content = urllib2.urlopen(sofifa_url).read()
        soup = BeautifulSoup(sofifa_content)
        name = soup.findAll('h1')[0].div.text.strip()
        assetId = soup.findAll('ul', class_='text-right')[0].li.text.split('\r\n')[1]
        return Player(assetId, name)