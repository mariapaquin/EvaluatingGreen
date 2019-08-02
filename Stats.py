import pandas as pd;
from scipy.stats.stats import pearsonr
from scipy import stats
import numpy as np

green1 = pd.read_csv("data/random/A/with-green.csv")
noGreen1 = pd.read_csv("data/random/A/without-green.csv")
invocations = pd.read_csv("data/random/A/invocations.csv")
cacheHits = pd.read_csv("data/random/A/cacheHits.csv")
green1 = green1.join(invocations)
green1 = green1.join(cacheHits)
df1 = pd.merge(noGreen1, green1, on=['project', 'package', 'class', 'method'])

green2 = pd.read_csv("data/random/B/with-green.csv")
noGreen2 = pd.read_csv("data/random/B/without-green.csv")
invocations = pd.read_csv("data/random/B/invocations.csv")
cacheHits = pd.read_csv("data/random/B/cacheHits.csv")
green2 = green2.join(invocations)
green2 = green2.join(cacheHits)
df2 = pd.merge(noGreen2, green2, on=['project', 'package', 'class', 'method'])

green3 = pd.read_csv("data/random/C/with-green.csv")
noGreen3 = pd.read_csv("data/random/C/without-green.csv")
invocations = pd.read_csv("data/random/C/invocations.csv")
cacheHits = pd.read_csv("data/random/C/cacheHits.csv")
green3 = green3.join(invocations)
green3 = green3.join(cacheHits)
df3 = pd.merge(noGreen3, green3, on=['project', 'package', 'class', 'method'])

greenOrdered = pd.read_csv("data/ordered/A/with-green.csv")
noGreenOrdered = pd.read_csv("data/ordered/A/without-green.csv")
invocations = pd.read_csv("data/ordered/A/invocations.csv")
cacheHits = pd.read_csv("data/ordered/A/cacheHits.csv")
greenOrdered = greenOrdered.join(invocations)
greenOrdered = greenOrdered.join(cacheHits)
df4 = pd.merge(noGreenOrdered, greenOrdered, on=['project', 'package', 'class', 'method'])

df1 = df1[df1['invocations'] > 0]
df2 = df2[df2['invocations'] > 0]
df3 = df3[df3['invocations'] > 0]
df4 = df4[df4['invocations'] > 0]

# df1.reset_index(inplace=True)
# df1 = df1.drop(['index'], axis=1)

df1['Rs'] = pd.to_numeric(df1['cacheHits'])/pd.to_numeric(df1['invocations'])
df2['Rs'] = pd.to_numeric(df2['cacheHits'])/pd.to_numeric(df2['invocations'])
df3['Rs'] = pd.to_numeric(df3['cacheHits'])/pd.to_numeric(df3['invocations'])
df4['Rs'] = pd.to_numeric(df4['cacheHits'])/pd.to_numeric(df4['invocations'])

df1['Ts'] = pd.to_numeric(df1['time_green'])/pd.to_numeric(df1['time'])
df2['Ts'] = pd.to_numeric(df2['time_green'])/pd.to_numeric(df2['time'])
df3['Ts'] = pd.to_numeric(df3['time_green'])/pd.to_numeric(df3['time'])
df4['Ts'] = pd.to_numeric(df4['time_green'])/pd.to_numeric(df4['time'])


print('A - pearson coefficient and p value:', pearsonr(df1['Ts'], df1['Rs']))
print('B - pearson coefficient and p value:', pearsonr(df2['Ts'], df2['Rs']))
print('C - pearson coefficient and p value:', pearsonr(df3['Ts'], df3['Rs']))
print('D - pearson coefficient and p value:', pearsonr(df4['Ts'], df4['Rs']), '\n')

# ALL
# A - pearson coefficient and p value: (0.01056944847215674, 0.8975128413271659)
# B - pearson coefficient and p value: (0.038940363996649754, 0.634992975236394)
# C - pearson coefficient and p value: (0.003586494483039891, 0.9651391607275552)
#
# CONSTRAINT HEAVY
# A - pearson coefficient and p value: (-0.328148800941102, 0.07666617563110442)
# B - pearson coefficient and p value: (-0.49531309098000104, 0.0053852135390309724)
# C - pearson coefficient and p value: (-0.3145848644001468, 0.09043061461007369)

print('median time ratio')
print(np.median(df1['Ts']))
print(np.median(df2['Ts']))
print(np.median(df3['Ts']))
print(np.median(df4['Ts']), '\n')

print('median reuse ratio')
print(np.median(df1['Rs']))
print(np.median(df2['Rs']))
print(np.median(df3['Rs']))
print(np.median(df4['Rs']), '\n')

print('time ratio')
print('A, B -', stats.ttest_ind(df1['Ts'], df2['Ts']))
print('A, C -', stats.ttest_ind(df1['Ts'], df3['Ts']))
print('A, D -', stats.ttest_ind(df1['Ts'], df4['Ts']))
print('B, C -', stats.ttest_ind(df2['Ts'], df3['Ts']))
print('B, D -', stats.ttest_ind(df2['Ts'], df4['Ts']))
print('C, D -', stats.ttest_ind(df3['Ts'], df4['Ts']), '\n')

print('reuse ratio')
print('A, B -', stats.ttest_ind(df1['Rs'], df2['Rs']))
print('A, C -', stats.ttest_ind(df1['Rs'], df3['Rs']))
print('A, D -', stats.ttest_ind(df1['Rs'], df4['Rs']))
print('B, C -', stats.ttest_ind(df2['Rs'], df3['Rs']))
print('B, D -', stats.ttest_ind(df2['Rs'], df4['Rs']))
print('C, D -', stats.ttest_ind(df3['Rs'], df4['Rs']))