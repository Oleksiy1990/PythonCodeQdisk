import numpy as np 
import scipy as sp 
import pandas as pd 

dset1 = pd.read_excel("waterflow.xlsx") #produces a Dataframe

print(dset1.iloc[3:8,1].values)

inner_top_avgs = np.divide(dset1.iloc[3:8,1].values,dset1.iloc[3:8,0].values)
#print(inner_top_avgs)
inner_top_flow = np.mean(inner_top_avgs)
inner_top_dev = np.std(inner_top_avgs)

print("Inner top avg ",inner_top_flow,"inner top dev ",inner_top_dev)

mid_top_avgs = np.divide(dset1.iloc[3:8,4].values,dset1.iloc[3:8,3].values)
#print(inner_top_avgs)
mid_top_flow = np.mean(mid_top_avgs)
mid_top_dev = np.std(mid_top_avgs)

print("Middle top avg ",mid_top_flow,"middle top dev ",mid_top_dev)

outer_top_avgs = np.divide(dset1.iloc[3:8,7].values,dset1.iloc[3:8,6].values)
#print(inner_top_avgs)
outer_top_flow = np.mean(outer_top_avgs)
outer_top_dev = np.std(outer_top_avgs)

print("Outer top avg ",outer_top_flow,"outer top dev ",outer_top_dev)

inner_btm_avgs = np.divide(dset1.iloc[14:19,1].values,dset1.iloc[14:19,0].values)
#print(inner_top_avgs)
inner_btm_flow = np.mean(inner_btm_avgs)
inner_btm_dev = np.std(inner_btm_avgs)

print("Inner btm avg ",inner_btm_flow,"inner btm dev ",inner_btm_dev)

mid_btm_avgs = np.divide(dset1.iloc[14:19,4].values,dset1.iloc[14:19,3].values)
#print(inner_top_avgs)
mid_btm_flow = np.mean(mid_btm_avgs)
mid_btm_dev = np.std(mid_btm_avgs)

print("Mid btm avg ",mid_btm_flow,"Mid btm dev ",mid_btm_dev)


outer_btm_avgs = np.divide(dset1.iloc[14:19,7].values,dset1.iloc[14:19,6].values)
#print(inner_top_avgs)
outer_btm_flow = np.mean(outer_btm_avgs)
outer_btm_dev = np.std(outer_btm_avgs)

print("Out btm avg ",outer_btm_flow,"out btm dev ",outer_btm_dev)