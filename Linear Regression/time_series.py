import pandas as pd
import sqlite3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import deque


def load_data(fname):
    """ Read the given database into two pandas dataframes. 
    
    Args: 
        fname (string): filename of sqlite3 database to read
        
    Returns:
        (pd.DataFrame, pd.DataFrame): a tuple of two dataframes, the first for the vehicle data and the 
                                      second for the prediction data. 
    """
    # create dataframe
    conn = sqlite3.connect(fname)
    vdf = pd.read_sql_query("SELECT * FROM vehicles", conn)
    pdf = pd.read_sql_query("SELECT * FROM predictions", conn)
    # drop empty rows and duplicates
    dropped_vdf = vdf.replace(to_replace="", value=np.nan).dropna(axis=0, thresh=4).drop_duplicates()
    dropped_pdf = pdf.replace("", np.nan).dropna(axis=0, thresh=4).drop_duplicates()
        # convert types
    dropped_vdf["tmstmp"] = pd.to_datetime(dropped_vdf["tmstmp"])
    convert_vdf_dict = {"vid":"int64", 
                        "lat":"float64", 
                        "lon":"float64", 
                        "hdg":"int64", 
                        "pid":"int64", 
                        "pdist":"int64", 
                        "spd":"int64", 
                        "tatripid":"int64"}
    dropped_pdf["tmstmp"] = pd.to_datetime(dropped_pdf["tmstmp"])
    dropped_pdf["prdtm"] = pd.to_datetime(dropped_pdf["prdtm"])
    convert_pdf_dict = {"stpid":"int64", 
                        "vid":"int64", 
                        "dstp":"int64",
                        "tatripid":"int64"}
    converted_vdf = dropped_vdf.astype(convert_vdf_dict)
    converted_pdf = dropped_pdf.astype(convert_pdf_dict)
    return (converted_vdf, converted_pdf)

def split_trips(df):
    """ Splits the dataframe of vehicle data into a list of dataframes for each individual trip. 
    
    Args: 
        df (pd.DataFrame): A dataframe containing vehicle data
        
    Returns: 
        (list): A list of dataframes, where each dataFrame contains vehicle data for a single trip
    """
    indexed_df = df.drop_duplicates().set_index('tmstmp', inplace=False)
    # important to group by vid and des otherwise there will be duplicates
    # on 61A and 61B
    groupbby = indexed_df.groupby(['vid', 'des'])
    keys = groupbby.groups.keys()
    trip_df_list = []
    for key in keys:
        vid_group = groupbby.get_group(key)
        pdist = vid_group['pdist']
        start_trip = vid_group.index[0:1].append(vid_group[pdist.diff(1) < -10000].index)
        end_trip = vid_group[pdist.diff(-1) > 10000].index.append(vid_group.index[-1:])
        for (start, end) in zip(start_trip, end_trip):
            trip_df = vid_group.loc[start:end]
            trip_df_list.append(trip_df)
    return trip_df_list

class SlidingAverage:
    def __init__(self,k):
        """ Initializes a sliding average calculator which keeps track of the average of the last k seen elements. 
        
        Args: 
            k (int): the number of elements to average (the half-width of the sliding average window)
        """
        self.k = k
        self.size = 2*k+1
        self.d = deque()
        self.sum = 0
        self.average = 0
        
    def update(self,x):
        """ Computes the sliding average after having seen element x 
        
        Args:
            x (float): the next element in the stream to view
            
        Returns: 
            (float): the new sliding average after having seen element x, if it can be calculated
        """
        if x == None:
            self.sum -= self.d.popleft()
            self.average = self.sum / len(self.d)
            return self.average
        elif len(self.d) < self.k:
            self.d.append(x)
            self.sum += x
            return None
        elif self.k <= len(self.d) < self.size:
            self.d.append(x)
            self.sum += x
            self.average = self.sum / len(self.d)
            return self.average
        elif self.size <= len(self.d):
            self.d.append(x)
            self.sum += x - self.d.popleft()
            self.average = self.sum / self.size
            return self.average
        
def compute_sliding_averages(s, k):
    """ Computes the sliding averages for a given Pandas series using the SlidingAverage class. 
    
    Args:
        s (pd.Series): a Pandas series for which the sliding average needs to be calculated
        k (int): the half-width of the sliding average window 
        
    Returns:
        (pd.Series): a Pandas series of the sliding averages
    
    """
    sa = SlidingAverage(k)
    out = np.array([])
    nan = np.array([None] * k)
    appended_s = np.append(s.values, nan)
    for e in appended_s:
        new_out = sa.update(e)
        if new_out != None:
            out = np.append(out, new_out)
    return pd.Series(out)

def plot_trip(trips, k):
    """ Plots the sliding average speed as a function of time 
    
    Args: 
        trip (list): list of trip DataFrames to plot
        k (int): the half-width of the sliding average window
    """
    ax_list = []
    for trip in trips:
        spd = compute_sliding_averages(trip.spd, k)
        time = trip.index.time
        fig, ax = plt.subplots()
        ax.plot(time, spd)
        ax.set_xlabel("time")
        ax.set_ylabel("speed")
        ax_list.append(ax)

def plot_avg_spd(df, t):
    """ Plot the average speed of all recorded buses within t minute intervals 
    Args: 
        df (pd.DataFrame): dataframe of bus data
        t (int): the granularity of each time period (in minutes) for which
        an average is speed is calculated
    """
    dropped_df = df.drop_duplicates().loc[:, ["tmstmp", "spd"]]
    time_index = np.array([dt - datetime.timedelta(minutes=((dt.hour * 60 + dt.minute) % t)) for dt in dropped_df.tmstmp])
    indexed_df = dropped_df.set_index(time_index, inplace=False)
    avg_spd = indexed_df.spd.groupby(by=indexed_df.index.time).mean()
    fig, ax = plt.subplots()
    ax.plot(avg_spd, ".")
    ax.set_xlabel("time")
    ax.set_ylabel("speed")
    return ax