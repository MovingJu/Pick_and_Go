import pandas as pd
import re

class Filter:

    @staticmethod
    def tour_filter(local_data):
        table = pd.read_csv("./data/tour_exclude.csv")
        filtered_data={'totalCount':0, 'items':[]}

        for target in local_data['items']: # type: ignore
            do_continue = False
            for elem in table["exceptions"]:
                pattern = rf"^{elem}"
                if re.match(pattern, target):
                   do_continue = True
                   continue
            if do_continue:
                continue
            filtered_data["items"].append(target)
        filtered_data['totalCount']=len(filtered_data['items'])

        return filtered_data
    
    @staticmethod
    def food_filter(local_data):
        table = pd.read_csv("./data/food_include.csv")
        filtered_data={'totalCount':0, 'items':[]}

        for target in local_data['items']: # type: ignore
            do_continue = False
            for elem in table["exceptions"]:
                pattern = rf"^{elem}"
                if not re.match(pattern, target):
                   do_continue = True
                   continue
            if do_continue:
                continue
            filtered_data["items"].append(target)
        filtered_data['totalCount']=len(filtered_data['items'])

        return filtered_data