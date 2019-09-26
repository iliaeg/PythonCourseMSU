import pandas as pd
import numpy as np
import math

def ceil_five(x):
    return 5 * math.ceil(int(x) / 5)

cv = pd.read_csv(
    "data/mtesrl_20150626_MD0000600002_stats.txt",
    sep = '\t',
    skiprows = 2,
    header = 0,
    usecols = ['EVENT', 'AVGTSMR'],
    engine = 'python',
    skipfooter = 2
)

# print(cv)

cv_pivot = cv.pivot(columns='EVENT', values='AVGTSMR')
# print(cv_pivot)

for event_name in cv_pivot:
    event_time_sorted = cv_pivot[event_name].sort_values().reset_index(drop=True)
    event_count = event_time_sorted.count()
    #counts = event_time_sorted.value_counts().sort_index()
    #data = pd.DataFrame({'time':counts.index, 'count':counts.values})
    # print(data)
    # print(event_name)
    # print(data['time'].min())

    # _sorted = counts.sort_index()
    print(event_name)
    print(f"min = {event_time_sorted[0]}")
    # ind = pd.Series(_sorted.index)
    print(f"50 % = {event_time_sorted[math.ceil(0.5*event_count)]}")
    print(f"90 % = {event_time_sorted[math.ceil(0.9*event_count)]}")
    print(f"99 % = {event_time_sorted[math.ceil(0.99*event_count)]}")
    print(f"99.9 % = {event_time_sorted[math.ceil(0.999*event_count)]}")
    # print(event_time_sorted)

    event_time_ceil = event_time_sorted.apply(ceil_five)

    event_time_count = event_time_ceil.value_counts().sort_index()

    print(event_time_count)

    weight = event_time_count.values / event_count * 100

    processed_data = pd.DataFrame({
        'ExecTime': event_time_count.index,
        'TransNo': event_time_count.values,
        'Weight,%':
            list(
                map(
                    lambda x: round(x, 2),
                    event_time_count.values / event_count * 100
                ))
        })

    print(processed_data)

    print(type(weight))

    # event_time_count.index.where(event_time_count.index < 200, )

    # processed_data[]

    # print(np.array(list(map(lambda x: round(x, 2), weight))))
    

    # for index, time in enumerate(event_time_sorted):
    #     event_time_sorted[index] = 0
    # for time in event_time_sorted:
    #     time = ceil_five(time)

    # data = pd.DataFrame({'time':_sorted.index, 'count':_sorted.values})
    # print(data.count())
    # print(data)
    # print("90% = ", data[int(math.ceil(0.9*data.count()))])