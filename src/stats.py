import argparse
import csv
from datetime import datetime
import numpy as np
import pandas as pd
from dask import dataframe as dd
from dask.array import from_array as fa
from .utils import *

class Stats():
    def init_location(self, args):
        if args.filter_country is None:
            return (None, None, None)
        items = args.filter_country[0].lower().split(',')
        countries = set()
        regions = set()
        region_of_country = set()
        for item in items:
            if item[0] == "-":
                regions.add(item[1:])
            elif "-" not in item:
                countries.add(item)
            else:
                s = item.split('-')
                region_of_country.add((s[0],s[1]))
        return (countries, regions, region_of_country)
        
    def init_os(self, args):
        if args.filter_os is None:
            return list()
        items = args.filter_os[0].split(',')
        l = list()
        for item in items:
            os = None
            mini = None
            maxi = None
            vs = item.split('-')
            prev = None
            for v in vs:
                if v == "min":
                    prev = "min"
                elif v == "max":
                    prev = "max"
                elif prev == "min":
                    prev = None
                    mini = v
                elif prev == "max":
                    prev = None
                    maxi = v
                elif prev == None:
                    os = v
            l.append((os, mini, maxi))
        return l
        
    def init_names(self, args):
        l = list()
        if args.filter_by_name is None:
            return None
        #print("args.filter_by_name",args.filter_by_name[0])
        #print("args.filter_by_name.split(';')",args.filter_by_name[0].split(';'))
        for a in args.filter_by_name[0].split(';'):
            items = a.split(',')
            l.append((items[0],set(x.lower() for x in items[1:])))
        #print("\ncolumns and names")
        #print(l,'\n\n')
        return l
            
    def __init__(self, args, sep=',', blocksize=64000000):
        self.csvFilePath = args.input[0]
        if args.group_by is not None:
            self.group_by = args.group_by[0].split(',')
        else:
            args.group_by = None
        if args.start is not None:
            self.start_time = pd.to_datetime(args.start[0])
        else:
            self.start_time = None
        if args.end is not None:
            self.end_time = pd.to_datetime(args.end[0])
        else:
            self.end_time = None
        if args.blocksize is not None and args.sep is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=args.sep[0], 
                header=0, blocksize=args.blocksize[0], 
                dtype={'geo_city': 'object'}, 
                parse_dates=['timestamp_raw', 'table_date'])
        elif args.blocksize is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=sep, 
                    header=0, blocksize=args.blocksize[0], 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        elif args.sep is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=args.sep[0], 
                    header=0, blocksize=64000000, 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        else:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=sep, 
                    header=0, blocksize=64000000, 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        self.countries, self.regions, self.region_of_country = self.init_location(args)
        # self.os = self.init_os(args)
        self.filter_names = self.init_names(args)
        
    def filter_by_country_region(self):
        self.dfd.replace(np.nan, '', regex=True)
        self.dfd["new_col"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
        self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                    | self.dfd.geo_region.str.lower().isin(self.regions)
                    | self.dfd["new_col"].isin(self.region_of_country)]
        self.dfd = self.dfd.drop(['new_col'], axis=1)
        
    def filter_by_name(self):
        for colName, names in self.filter_names:
            self.dfd = self.dfd[self.dfd[colName].str.lower().isin(names)]
    
    def filter_by_range(self):
        if self.start_time:
            self.dfd = self.dfd[self.dfd["timestamp_raw"] >= self.start_time]
        elif self.end_time:
            self.dfd = self.dfd[self.dfd["timestamp_raw"] <= self.end_time]
#        if self.os:
#            oses = set()
#            for os in self.os:
#                oses.add(os[0])
#                print("HERE 2")
#                print("os[1]",os[1])
                # min
#                if os[1] is not None:
#                    print("HERE 3")
#                    print(float(filter(lambda x: x.isdigit(),self.dfd["device_os_version"].str)[0]))
#                    self.dfd = self.dfd[not (self.dfd["device_os"]==os[0] 
#                    & (float(filter(lambda x: x.isdigit(),self.dfd["device_os_version"].str)[0] 
#                    + '.' + filter(lambda x: x.isdigit(),self.dfd["device_os_version"].str)[1:]) 
#                    <= os[1]))]
                # max
#                if os[2] is not None:
#                    self.dfd = self.dfd[not (self.dfd["device_os"]==os[0] & self.dfd["device_os_version"] >= os[2])]
#            self.dfd = self.dfd[self.dfd["device_os"].isin(oses)]

    def filter(self):
        if self.filter_names is not None:
            self.filter_by_name()
        self.filter_by_range()
        self.dfd.compute()
        if self.countries is not None:
            self.filter_by_country_region()
        
    def aggregate(self):
        # group by field names
        # group by os and range. DO LATER
        # country
        # country and region
        # do the reader filters actually stay filtered?
        return self.dfd.groupby(self.group_by).size()
        #self.dfd[self.group_by].value_counts()
        #aggregate by date ranges?
        

        

