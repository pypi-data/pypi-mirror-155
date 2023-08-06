#multi_corr helps to identify multicollinearity in a simple and straight manner.

Input
1. DataFrame with target feature in case of regression
2. Threshold for correlation

Output
1. Dataframe with correlation of two features
2. Dataframe with features which correlate with each other

Insight
1. Identify multicollinearity by looking at the target column (Regression) 
2. Discard features which are not relevant
