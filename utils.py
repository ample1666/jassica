import argparse
from datetime import datetime
from math import sqrt, asin, sin, cos, radians
# from pyspark.sql.functions import udf
# from pyspark.sql.types import StringType, ArrayType, IntegerType, FloatType


parser = argparse.ArgumentParser(description='XXXXX')
parser.add_argument('--low', type=int, default=30)
parser.add_argument('--high', type=int, default=60)
parser.add_argument('--needDays', type=int, default=1)
args = parser.parse_args()


def compute_how_long(t1,t2):
    try:
        t1 = datetime.strptime(t1.split('.')[0], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime(t2.split('.')[0], '%Y-%m-%d %H:%M:%S')
        return abs(t1.timestamp() - t2.timestamp()) / 60    # 单位：分钟
    except:
        return 0.

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1000     # 单位：米

import numpy as np
def get_Quartile(l, percent=50):
    '''percent=25, 第一四分位数;
       percent=50, 中位数; 
       percent=75, 第三四分位数;
    '''
    return float(np.percentile(l, percent))


from urllib.request import urlopen
from xml.etree.ElementTree import parse
import json

def request(start_lng, start_lat, end_lng, end_lat, key='9699765937f11eb0dcbe85e2590258ff'):
    url = "https://restapi.amap.com/v3/direction/driving?origin=%s,%s&destination=%s,%s&extensions=all&output=xml&key=%s" % (start_lng, start_lat, end_lng, end_lat, key)
    f = urlopen(url)
    doc = parse(f)
#     for item in doc.iterfind('route/paths/path'):
    distance = int(doc.findtext('route/paths/path/distance'))   # 单位：米
    duration = int(doc.findtext('route/paths/path/duration'))   # 单位：秒
    return distance, duration
