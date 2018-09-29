# python3_Apriori
Classical association rule minning algorithm

Three main args:
- support
- confidence
- lift

# Usage
Default value:
- minSupport 0.01
- minConfidence 0.7
- minLift 1.0

    python apriori.py -f ***.csv -s 0.2 -c 0.8 -l 1.2

# Data Formation
- .csv file
- item code (column names)
- binary value

# Requirements
- python 3.6.5
- pandas
- collections
- itertools

# References
https://blog.csdn.net/baimafujinji/article/details/53456931

https://github.com/asaini/Apriori/blob/master/apriori.py

https://www.cnblogs.com/nxld/p/6380417.html

