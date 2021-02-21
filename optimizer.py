"""
Takes a list of shifts and possible employees and forms a schedule.

This assumes there is alrady a dataframe of shifts with tuples of possible
employees to fill the shift. If calling from the command line, include an
argument that is the location of a csv file containing a dataframe, and an
argument that is the name of the csv file to save the schedule to.

Methods:
during(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime) -> bool
create_overlap_chart(shifts: pd.DataFrame) -> pandas.DataFrame
create_graph(shifts: pd.DataFrame) -> networkx.Graph
deterministic_choices(shifts: pd.DataFrame, shift_graph: nx.Graph) -> pandas.DataFrame
def create_schedule(shifts: pd.DataFrame) -> pandas.DataFrame
main(args: list) -> pandas.DataFrame
"""
import sys
import datetime
import pandas as pd
import networkx as nx

def during(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime):
    """Gets and prints the spreadsheet's header columns

    Args:
        start1 (datetime.datetime): The start time of the first shift
        end1 (datetime.datetime): The end time of the first shift
        start2 (datetime.datetime): The start time of the other shift
        end2 (datetime.datetime): The end time of the other shift

    Returns:
        bool: true if the shifts overlap, false if they don't
    """
    #check if one shift starts after the other one ends, they don't overlap
    #otherwise, they do
    return not (start1>end2 or start2>end1)

def create_overlap_chart(shifts: pd.DataFrame):
    for i in range(shifts.shape[0]):
        overlapping_shifts = []
        for j in range(shifts.shape[0]):
            if i!=j:
                if during(shifts['start'][i],shifts['end'][i],shifts['start'][j],shifts['end'][j]):
                    overlapping_shifts.append(j)
        shifts['overlapping'][i]=tuple(overlapping_shifts)
    return shifts

def create_graph(shifts: pd.DataFrame):
    shift_graph = nx.Graph()
    shift_graph.add_nodes_from(list(range(shifts.shape[0])))
    for i in range(shifts.shape[0]):
        for x in shifts['overlapping'][i]:
            shift_graph.add_edge(i, x)
    return shift_graph

def deterministic_choices(shifts: pd.DataFrame, shift_graph: nx.Graph):
    #THIS FUNCTION IS NOT FINISHED
    change_made = True
    while change_made:
        change_made = False
        for i, row in shifts.iterrows():
            if row['Employee']==0 and len(row['PotentialEmployees'])==0:
                raise ValueError('There are no employees available for the shift from {} to {} on {}.'.format(row['Start'].time(),row['End'].time(),row['Start'].date()))
            elif row['Employee']==0:
                if len(row['PotentialEmployees'])==1:
                    row['Employee']=row['PotentialEmployees'][0]

def create_schedule(shifts: pd.DataFrame):
    create_overlap_chart(shifts)
    shift_graph = create_graph(shifts)
    deterministic_choices(shifts, shift_graph)
    return shifts

def main(args: list):
    try:
        shifts = pd.read_csv(args[0])
    except:
        print("Your file could not be opended")
    schedule = create_schedule(shifts)
    schedule.to_csv(args[1])
    return schedule

if __name__=='__main__':
    main(sys.argv[1:])
