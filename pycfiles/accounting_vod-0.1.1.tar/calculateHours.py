# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/accountingModules/calculateHours.py
# Compiled at: 2012-04-17 21:14:54
import sys, re, math, accountingModules.theGlobals as globalConf

def time_to_hours(time_str):
    try:
        hours, minutes, seconds = time_str.split(':')
    except ValueError:
        return -1

    return int(hours) + int(minutes) / 60.0 + int(seconds) / 3600.0


def calculate_node_hours(logLine):
    cores_per_node = int(globalConf.cores_per_node)
    mppnppn = int(globalConf.mppnppn)
    used_core_hours = 0
    nodes_used = 0
    used_walltime = 0
    try:
        match_walltime = re.search('resources_used.walltime=?([^ >]+)', logLine)
        used_walltime = match_walltime.group().split('=')[1]
        used_core_hours = 0
        used_walltime = time_to_hours(used_walltime)
        match_size = re.search('Resource_List.size=?([^ >]+)', logLine)
        if match_size:
            jobsize = match_size.group().split('=')[1]
            cores_used = float(jobsize) / float(cores_per_node)
            used_core_hours = float(used_walltime) * float(cores_used)
            nodes_used = int(jobsize)
        else:
            match_mppwidth = re.search('Resource_List.mppwidth=?([^ >]+)', logLine)
            match_mppnppn = re.search('Resource_List.mppnppn=?([^ >]+)', logLine)
            if match_mppnppn:
                mppnppn = int(match_mppnppn.group().split('=')[1])
            mppwidth = match_mppwidth.group().split('=')[1]
            nodes_used = math.ceil(float(mppwidth) / float(mppnppn))
            cores_used = nodes_used * cores_per_node
            used_core_hours = used_walltime * cores_used
            used_core_hours = round(used_core_hours)
    except:
        print logLine + '*** UNUSUAL ***'

    return (
     used_core_hours, nodes_used, used_walltime)