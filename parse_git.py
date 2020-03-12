from dateutil.parser import parse
import re
import datetime


def get_min_max_amount_of_commits(
    commit_log: str = commits, year: int = None
) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
        
    with open(commits) as commit:
        commit = commit.readlines()
        data = [i.strip("\n").split("|") for i in commit]
        date = [
            parse(i[0], fuzzy=True).strftime("%Y-%m-%d %H:%M:%S") for i in data
            ]
        changes = [i[1] for i in data]
        change_count = []
        for i in changes:
            temp = re.findall(r"\d+", i)
            change = list(map(int, temp))
            change_count.append(sum(change[1:]))
        commit_dict = dict(zip(date, change_count))
        key_list = []
        for key in commit_dict.keys():
            if key[0:7] not in key_list:
                key_list.append(key[0:7])
        commit_totals ={}
        for item in key_list:
            val = sum([
                commit_dict.get(i) 
                for i in commit_dict.keys()
                if item in i
            ])
            commit_totals[item] = val
    
    if year == None:
        least_active_month = min(commit_totals, key=commit_totals.get)
        most_active_month = max(commit_totals, key=commit_totals.get)
        return(least_active_month,most_active_month)
    else:
        year_dict = {
            k:v for (k,v) in commit_totals.items() if str(year) in k
            }
        least_active_month = min(year_dict, key = year_dict.get)
        most_active_month = max(year_dict, key = year_dict.get)
        return(least_active_month,most_active_month)
