# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:22:35 2022

@author: sarathbabu.karunanit
"""

import pandas as pd
def multicorr(df,threshold=0.5):
    """To identify multicollinearity in variables.
    
    Parameters:
    df - Dataframe for which Multicollinearity is to be calculated
    
    threshold - absolute value to filter positive and negative correlation 
    value identifying multicollinearity.
    
    Default threshold of 0.5 is provided.
    
    Returns:
    1. df_two - Dataframe containing pair of features having correlation
    value above the specified threshold.
    
    2. df_multi - Derived from df_two dataframe which contains all the features
     which correlate with other features above the specified threshold.
    
    """
    if len(df)>0:
        __df_corr=df.corr()
        __df_corr=__df_corr.stack().reset_index()
        __df_corr.columns=['x','y','corr']
        __df_corr['abs_corr']=abs(__df_corr['corr'])
        __df_corr=__df_corr.loc[(__df_corr['abs_corr']>=threshold)&(__df_corr['x']!=__df_corr['y'])]
        __df_corr=__df_corr.sort_values(by=['abs_corr'],ascending=False)
        
        cols=sorted(df.columns.values)
    
        __final=pd.DataFrame()
        for i in range(len(cols)):
            corr_cols=[]
            corr_cols.append(cols[i])
    
            j=__df_corr.loc[__df_corr.x==cols[i]].y.values
            if len(j)>0:
                j=sorted(j)[0]
                corr_cols.append(j)
    
            rem_cols=sorted(list(set(cols)-set(corr_cols)))
    
            for j in rem_cols:
                counts=0
                for k in corr_cols:
                    counts=counts+(__df_corr.loc[(__df_corr.x==k)&(__df_corr.y==j)].shape[0])
                if counts==len(corr_cols):
                    corr_cols.append(j)
            __final=pd.concat([__final,pd.DataFrame(corr_cols)],axis=1)
            __final.columns=__final.iloc[0].values
            
        del __df_corr['abs_corr']
        __df_corr=__df_corr.sort_values(by=['x'])
        __df_corr=__df_corr.reset_index(drop=True)
        
        __final=__final.iloc[1:]
        
        
        return __df_corr,__final
    else:
        return 'Empty Dataframe'
