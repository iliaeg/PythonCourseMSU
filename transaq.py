import pandas as pd
import math

def ceil_five(x):
    return 5 * math.ceil(x / 5)

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
	# data = pd.DataFrame({'time':_sorted.index, 'count':_sorted.values})
	# print(data.count())
	# print(data)
	# print("90% = ", data[int(math.ceil(0.9*data.count()))])