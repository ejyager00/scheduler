import datetime
import pandas as pd
import networkx as nx

def during(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime):
return not (start1>end2 or start2>end1)

def create_overlap_chart(shifts: pd.DataFrame):
    for i in range(shifts.shape[0]):
        overlapping_shifts = []
        for j in range(shifts.shape[0]):
            if i!=j:
                if during(shifts['start'][i],shifts['end'][i],shifts['start'][j],shifts['end'][j]):
                    overlapping_shifts.append(j)
        shifts['overlapping'][i]=tuple(overlapping_shifts)

def create_graph(shifts):
    shift_graph = nx.Graph()
    shift_graph.add_nodes_from(list(range(shifts.shape[0])))
    for i in range(shifts.shape[0]):
        for x in shifts['overlapping'][i]:
            shift_graph.add_edge(i, x)
    return shift_graph
