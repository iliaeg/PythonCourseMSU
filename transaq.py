import pandas as pd
import numpy as np
import math
import sys
import json
from os import path

from utils import ceil_five, trunc2, percent_stat, eprint


def main(argv):
    '''
    Usage: python transaq.py config.json [-d]

    Args:
        config: path to json configuration file
        flag -d: print debug info
    '''

    try:

        if (len(argv) < 2):
            eprint("Usage: python transaq.py config.json [-d]")
            return 1

        if "-h" in argv or "--help" in argv:
            print("Usage: python transaq.py config.json [-d]")
            return 0

        config_file = path.abspath(argv[1])

        if "-d" in argv:
            debug = True
        else:
            debug = False

        if not path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found")
        # read config
        with open(config_file, "r") as read_file:
            config = json.load(read_file)

        data_file = path.abspath(config['dataFileName'])
        if not path.exists(data_file):
            raise FileNotFoundError(f"Data file {data_file} not found")

        cv = pd.read_csv(
            config['dataFileName'],
            sep = '\t',
            skiprows = 2,
            header = 0,
            usecols = ['EVENT', 'AVGTSMR'],
            engine = 'python',
            skipfooter = 2
        )

        if cv.empty:
            raise Exception("No data in table present")

        # here NaN values can appear, so int type may be changed to float
        cv_pivot = cv.pivot(columns='EVENT', values='AVGTSMR')

        # print(cv_pivot)

        for event_name in cv_pivot:
            event_time_sorted = cv_pivot[event_name].sort_values()
            # drop NaN values
            event_time_sorted = event_time_sorted.dropna()
            # convert values back to int
            event_time_sorted = event_time_sorted.astype(int)
            event_time_sorted = event_time_sorted.reset_index(drop=True)
            event_count = event_time_sorted.count()

            # Statistics
            time_min = event_time_sorted[0]
            time_50 = percent_stat(event_time_sorted, event_count, 0.5)
            time_90 = percent_stat(event_time_sorted, event_count, 0.9)
            time_99 = percent_stat(event_time_sorted, event_count, 0.99)
            time_999 = percent_stat(event_time_sorted, event_count, 0.999)

            stat = {
                'EVENTNAME': event_name,
                'min': int(time_min),
                '50%': int(time_50),
                '90%': int(time_90),
                '99%': int(time_99),
                '99,9%': int(time_999)
            }

            # write statistics to file
            with open(event_name + config['statisticsFileName'], 'w') as outfile:
                json.dump(stat, outfile, indent=4)

            if debug:
                print(
                    "###==================================================###\n" + 
                    f"###================={event_name:^16}=================###\n" +
                    "###==================================================###\n"
                    )

                print(f"min = {time_min}")
                print(f"50 % = {time_50}")
                print(f"90 % = {time_90}")
                print(f"99 % = {time_99}")
                print(f"99.9 % = {time_999}\n")

            event_time_ceil = event_time_sorted.apply(ceil_five)
            event_time_count = event_time_ceil.value_counts().sort_index()

            event_time_weight = np.array(event_time_count.values / event_count * 100)

            event_time_percent = np.empty(([event_time_weight.size]), dtype=float)
            event_time_percent[0] = event_time_weight[0]
            for i, value in enumerate(event_time_weight[1:], start=1):
                event_time_percent[i] = event_time_percent[i - 1] + value

            processed_data = pd.DataFrame({
                'ExecTime': event_time_count.index,
                'TransNo': event_time_count.values,
                'Weight,%': trunc2(event_time_weight),
                'Percent,%': trunc2(event_time_percent)
                })

            processed_data.to_html(
                buf = event_name + config['tableFileName'],
                col_space = 100,
                index = False,
                justify = 'center'
                )

            if debug:
                print(processed_data)

    except FileNotFoundError as ex:
        eprint("FileNotFoundError exception caught: \n", ex)
        return 1
    except Exception as ex:
        eprint("An exception caught: ", ex)
        return 1

    return 0

if __name__ == "__main__":
    main(sys.argv[:])