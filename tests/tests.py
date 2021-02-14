import unittest
from unittest.mock import patch, Mock, MagicMock
from random import randint
import json
import csv
import os
import configparser
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from src.utils import *

from interface import *

class TestJSON(unittest.TestCase):
    def test_json_output_size(self):
        jsonFilePath = ''
        for i in range(10):
            jsonFilePath += chr(randint(0, 255))
        jsonFilePath +=  ".json"
        f = open("test_samples.json",'r')
        cases = json.load(f)
        f.close()
        for csvFilePath in cases["csvs"]:
            csv_to_json(csvFilePath, jsonFilePath)
            f = open(jsonFilePath, 'r')
            json_rows = len(json.load(f))
            f.close()
            csv_rows = 0
            f = open(csvFilePath, 'r')
            for row in csv.DictReader(f):
                csv_rows += 1
            f.close()
            self.assertEqual(json_rows,csv_rows)
            os.remove(jsonFilePath)

            
class TestAnalysis(unittest.TestCase):

    def test_date_filter(self):
        args = parse_args(['@test_date_filter.txt'])
        stats = Stats(args)
        stats.filter()
        start_date = pd.Timestamp(year=2019, month=9, day=30, hour=20, 
                    minute=30, second=0, microsecond=0, tz='UTC')
        end_date = pd.Timestamp(year=2019, month=10, day=1, hour=21, 
                    minute=30, second=0, microsecond=0, tz='UTC')
        # check if the column is of timestamp type
        self.assertTrue(stats.dfd.timestamp_raw.dtype == "datetime64[ns, UTC]")
        for idx, row in stats.dfd.iterrows():
            self.assertTrue(row['timestamp_raw'] <= end_date and row['timestamp_raw'] >= start_date)  
        
    def test_name_filter(self):
        args = parse_args(['@test_name_filter.txt'])
        stats = Stats(args)
        stats.filter()
        stats.dfd.compute()
        oses = {'android','ios'}
        cat = {"tablet"}
        mod = {"ipad pro 12.9 2nd gen","sm-a105m"}
        android = False
        ios = False
        tablet = False
        ipad = False
        sm = False
        for idx, row in stats.dfd.iterrows():
            self.assertTrue(lower(row['device_os']) in oses 
            and lower(row["device_category"]) in cat 
            and lower(row["device_model_name"]) in mod,
            "Failed on row " + str(idx))
        stats.aggregate()
        
    def test_country_region_city_filter(self):
        args = parse_args(['@test_c_filter.txt'])
        stats = Stats(args)
        stats.filter()
        stats.dfd.compute()
        countries = {"cuba"}
        regions = {"crimea"}
        region_of_country = {("peru","piura")}
        c = False
        r = False
        cr = False
        for idx, row in stats.dfd.iterrows():
            country = lower(row['geo_country'])
            region = lower(row["geo_region"])
            self.assertTrue(country in countries or region in regions
                or (country,region) in region_of_country)
            if country in countries:
                c = True
            if region in regions:
                r = True
            if (country,region) in region_of_country:
                cr = True
        self.assertTrue(c and r and cr)

            

unittest.main()
