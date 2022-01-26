import sys
import pandas as pd
import numpy as np

def get_percentil(serie, per):
	sort = serie.sort_values()
	lenght = len(serie)
	if lenght == 0:
		return np.nan
	
	Q = (lenght-1) * per/100
	f = np.floor(Q)
	c = np.ceil(Q)
	
	if f == Q:
		return sort.iloc[int(Q)]
	return sort.iloc[int(c)] * (Q - f) + sort.iloc[int(f)] * (c - Q)



def get_info(describe, serie, value):

	serie.dropna(inplace=True)
	try:
		max_, min_, sum_ = serie[0], serie[0], serie[0]
	except:
		max_, min_, sum_ = np.nan, np.nan, np.nan

	for index, row in serie.items():
		if row > max_:
				max_ = row
		if row < min_:
				min_ = row
		if index > 0:
				sum_ += row
	
	lenght = len(serie.dropna())
	if lenght == 0:
		mean = np.nan
	else:
		mean = sum_ / (lenght)
	if lenght <= 1:
		std = np.nan
	else:
		std = ((1 / (lenght - 1)) * sum((serie - mean)**2))**(1/2)

	describe.loc[('min'), value] = min_
	describe.loc[('max'), value] = max_
	describe.loc[('count'), value] = lenght
	describe.loc[('mean'), value] = mean
	describe.loc[('25%'), value] = get_percentil(serie,25)
	describe.loc[('50%'), value] = get_percentil(serie,50)
	describe.loc[('75%'), value] = get_percentil(serie,75)
	describe.loc[('std'), value] = std



def main():
	if len(sys.argv) == 2:
		data_name = sys.argv[1]
	elif len(sys.argv) < 2:
		print("No path file has been included")
	try:
		df = pd.read_csv(data_name)
	except:
		print("No file" + data_name)

	describe = pd.DataFrame({'':['count','mean','std','min','25%','50%','75%','max']})
	describe.set_index('', inplace=True)
	columns = df.columns


	for value in columns:
		if df[value].dtypes == float or df[value].dtypes == int:
			describe[value] = 0
			get_info(describe, df[value], value)
	print(describe)
	print(df.describe())

if	__name__ == '__main__':
	main()