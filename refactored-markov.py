import pandas as pd

#defined a fuction to complete the markov model translation piece. Cuts down on clutt and repetitive typing
def markovtranslation(df,times):
	df = df.dot(df**times)
	print(df)


df = pd.DataFrame({'rainy': [.4, .7],
	'sunny' : [.6, .3]},
	index = ["rainy", "sunny"])

df2 = pd.DataFrame({'Bear':[.15,.8,.05],
	'Bull':[.9, .075, .025],
	'Stag':[.25,.25,.5]},
	index = ["Bear", "Bull", "Stag"])


#not a huge change but enough in a short script to clean things up
print(df.dot(df**1))
print(df2.dot(df2**200))

#important for if I would need to import something like this into a larger program. 
print(markovtranslation(df,1))
print(markovtranslation(df2,200))

