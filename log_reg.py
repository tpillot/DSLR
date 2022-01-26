import pandas as pd
pd.set_option('display.max_column',None)
pd.set_option('display.max_rows',None)
import numpy as np
import sys

class LogReg():

	"""docstring for LogReg"""
	def __init__(self, lr=0.2, epoch=10000):
		self.lr = lr
		self.epoch = epoch
	
	def model(self, X):
		return np.dot(self.W.T, X) + self.b

	def sigmoide(self, z):
		# print(np.shape(z))
		return 1 / (1 + np.exp(-z))
	
	def fit(self, x, Y):

		X = x.T
		n = np.shape(X)[0]
		m = np.shape(X)[1]

		self.W = np.zeros((n, 1))
		self.b = 0

		for i in range(0,self.epoch):
			# print(np.shape(self.W))
			Y_pred = self.sigmoide(self.model(X))
			dZ = Y_pred - Y.T
			dW = 1/m * np.dot(X, dZ.T)
			db = 1/m * np.sum(dZ)
			self.W = self.W - self.lr * dW
			self.b = self.b - self.lr * db


		
# 		# A = sigmoide(model(X, W, B))

	def predict(self, x):
		X = x.T
		Y_pred = self.sigmoide(self.model(X))
		return Y_pred.T


def main():
	if len(sys.argv) == 2:
		data_name = sys.argv[1]
	elif len(sys.argv) < 2:
		print("No path file has been included")
	try:
		df = pd.read_csv(data_name)
	except:
		print("No file" + data_name)


	df.drop(columns=['Care of Magical Creatures'], inplace=True)
	df = df.fillna(df.mean())
	X = df.drop(columns=['Hogwarts House','Index'])
	classes = df['Hogwarts House'].unique()
	df.rename(columns={'Hogwarts House': 'HogwartsHouse'}, inplace=True)
	X = X._get_numeric_data()
	for name in X.columns:
		X[name] = (X[name] - X[name].mean()) / X[name].std()

	for classe in classes:
		df[classe] = 0

	for i,row in df.iterrows():
		df.loc[(i), row.HogwartsHouse] = 1

	for classe in classes:
		lr = LogReg()
		lr.fit(X.to_numpy(), df[classe].to_numpy())
		X[classe] = lr.predict(X.to_numpy())

	columns_len = np.shape(X)[1]
	df2 = X.iloc[:, columns_len - 4 :columns_len]

	df['predict'] = df2.idxmax(axis="columns")
	print((df['predict'] == df['HogwartsHouse']).mean())

	

if	__name__ == '__main__':
	main()








