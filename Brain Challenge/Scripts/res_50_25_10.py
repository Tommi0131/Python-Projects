import numpy as np
import pylab as plt
import pandas as pd
import seaborn as sns
from os.path import join as pj
from joblib import dump, load
from os.path import join as pj
from sklearn.metrics import r2_score

#%%
data_dir='/home/STUDENTI/alessandr.dagostino2/Python-Projects/Brain Challenge/Data'
results_dir='/home/STUDENTI/alessandr.dagostino2/Python-Projects/Brain Challenge/Results'
scripts_dir='/home/STUDENTI/alessandr.dagostino2/Python-Projects/Brain Challenge/Scripts'

data_train=pd.read_csv(pj(data_dir, 'Training_Set_YESregressBYeTIVifCorr_LogScaled_combat_SVA.txt'),
                        header=0, sep='\t')
feats = data_train.loc[:,'lh_bankssts_area' :'rh.Whole_hippocampus'].values
y = data_train['age_floor'].values
X = feats #n_features = 954 n_samples = 2364

#%%
sorted_scores = pd.read_csv(pj(scripts_dir,   'Sorted_scores.csv'))
features_top50 = list(sorted_scores.loc[sorted_scores['top50_scores']>0].iloc[:,0])
features_top25 = list(sorted_scores.loc[sorted_scores['top25_scores']>0].iloc[:,0])
features_top10 = list(sorted_scores.loc[sorted_scores['top10_scores']>0].iloc[:,0])

X_50 = data_train.loc[:,features_top50]
X_25 = data_train.loc[:,features_top25]
X_10 = data_train.loc[:,features_top10]

#%% Loading results reviously computed from .csv

y_df = pd.read_csv(pj(scripts_dir,   'y_df_50_25_10.csv'), sep='\t')

#Set the Dataframe in tidy format
melt_y_df = pd.melt(y_df,
                    id_vars=['y_test'],
                    value_vars=['y_pred_50', 'y_pred_25', 'y_pred_10'],
                    var_name='run',
                    value_name = 'y_pred')

#Computing R^2 scores
r2 = []
r2.append(r2_score(y_df['y_pred_50'],y_df['y_test']))
r2.append(r2_score(y_df['y_pred_25'],y_df['y_test']))
r2.append(r2_score(y_df['y_pred_10'],y_df['y_test']))

#%% Drawing plots
lp = sns.lmplot(data=melt_y_df,
                x='y_test',
                y='y_pred',
                hue='run',
                col='run',
                robust=True,
                legend=True,\
                scatter_kws = dict(alpha = 0.5))
fig = lp.fig
for n,ax in enumerate(fig.axes):
    ax.set_title("run = {}  $R^2=${:.4f}".format(y_df.columns[-len(fig.axes)+n], r2[n] ))
fig.savefig(pj(scripts_dir, 'three_graphs.png'))
#%%

#Print the best estimators:
filename="grid_SVR_50.joblib"
svr_50 = load(pj(scripts_dir,  filename))
print(svr_50.best_params_)

filename="grid_SVR_25.joblib"
svr_25 = load(pj(scripts_dir,  filename))
print(svr_25.best_params_)

filename="grid_SVR_10.joblib"
svr_10 = load(pj(scripts_dir,  filename))
print(svr_10.best_params_)
