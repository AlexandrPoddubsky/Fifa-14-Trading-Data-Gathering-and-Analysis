Fifa-14-Trading-Data-Gathering-and-Analysis
============================================
Analysis
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


