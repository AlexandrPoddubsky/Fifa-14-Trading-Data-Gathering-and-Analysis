Fifa-14-Trading-Data-Gathering-and-Analysis
============================================

##Gathering Data
```
from fut14analysis.facade import *
from fut14gathering.collector import *
```
First a login to the WebApp is required and a player needs to be defined.

```
engine = TradeInfoEngine(username, password, secret_answer, platform='ps3')
player = IntegratedPlayerInfo(player_name='khedira').player
```

Now the current trading data for the player can be retrieved:

```
collector = DataCollector()
print collector.gather_data(player, engine)
```

```
84/CDM/f433
	R 84 BUY 1500 BID 1400 POS CDM OWN 2 (1200) TRADE 141961290134

84/CDM/f451
	R 84 BUY 1500 BID 1400 POS CDM OWN 3 (1200) TRADE 141961311057
	R 84 BUY 0 BID 2100 POS CDM OWN 3 (2100) TRADE 141958474367

84/CDM/f3412
	R 84 BUY 1400 BID 1300 POS CDM OWN 7 (1100) TRADE 141961242118
	R 84 BUY 1600 BID 1500 POS CDM OWN 9 (1200) TRADE 141961239815
```


##Analysis
```
from fut14analysis.facade import *
```

Load a player (Sami Khedira) and get the data frame representing a time series of minimum buy prices. 

```
khedira = IntegratedPlayerInfo(player_name='khedira', output_folder='/Users/mateusz/Desktop/trader_data/player_stats')
ts = khedira.get_min_data_frame()
ts = ts.resample('30min', fill_method='ffill')
```

Using pandas the data can be examined such as:

```
ts.mean(), ts.median(), ts.std()
```




    (0    1129.551505
    dtype: float64,
     0    1200
    dtype: float64,
     0    147.539026
    dtype: float64)



Plotting is also very simple

```
ts.plot()
```
![Image](https://raw.githubusercontent.com/mateuszk87/Fifa-14-Trading-Data-Gathering-and-Analysis/master/img/stats_example.png?raw=true)


