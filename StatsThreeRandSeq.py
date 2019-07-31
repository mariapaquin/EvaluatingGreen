import pandas as pd;
from scipy.stats.stats import pearsonr
from scipy import stats

# Read in data
withGreen1 = pd.read_csv("data/random/A/with-green.csv")
withoutGreen1 = pd.read_csv("data/random/A/without-green.csv")
invocations1 = pd.read_csv("data/random/A/invocations.csv")
cacheHits1 = pd.read_csv("data/random/A/cacheHits.csv")

withGreen2 = pd.read_csv("data/random/B/with-green.csv")
withoutGreen2 = pd.read_csv("data/random/B/without-green.csv")

withGreen3 = pd.read_csv("data/random/C/with-green.csv")
withoutGreen3 = pd.read_csv("data/random/C/without-green.csv")

withGreen1 = withGreen1.join(invocations1)
withGreen1 = withGreen1.join(cacheHits1)


df1 = pd.merge(withoutGreen1, withGreen1, on=['project', 'package', 'class', 'method'])

df1 = pd.merge(df1, withGreen2, on=['project', 'package', 'class', 'method'])
df1 = pd.merge(df1, withoutGreen2, on=['project', 'package', 'class', 'method'])

df1 = pd.merge(df1, withGreen3, on=['project', 'package', 'class', 'method'])
df1 = pd.merge(df1, withoutGreen3, on=['project', 'package', 'class', 'method'])

df1.rename(columns={'time':'timeA',
                    'time_green':'time_greenA',
                    'time_x':'timeB',
                    'time_green_x':'time_greenB',
                    'time_y':'timeC',
                    'time_green_y':'time_greenC'},
            inplace=True)

df1 = df1[df1['invocations'] > 5]

df1.reset_index(inplace=True)
df1 = df1.drop(['index'], axis=1)

df1['TsA'] = pd.to_numeric(df1['time_greenA'])/pd.to_numeric(df1['timeA'])
df1['TsB'] = pd.to_numeric(df1['time_greenB'])/pd.to_numeric(df1['timeB'])
df1['TsC'] = pd.to_numeric(df1['time_greenC'])/pd.to_numeric(df1['timeC'])

df1['Rs'] = pd.to_numeric(df1['cacheHits'])/pd.to_numeric(df1['invocations'])

print('A - pearson coefficient and p value:', pearsonr(df1['TsA'], df1['Rs']))
print('B - pearson coefficient and p value:', pearsonr(df1['TsB'], df1['Rs']))
print('C - pearson coefficient and p value:', pearsonr(df1['TsC'], df1['Rs']), '\n')

# ALL
# A - pearson coefficient and p value: (0.01056944847215674, 0.8975128413271659)
# B - pearson coefficient and p value: (0.038940363996649754, 0.634992975236394)
# C - pearson coefficient and p value: (0.003586494483039891, 0.9651391607275552)

# CONSTRAINT HEAVY
# A - pearson coefficient and p value: (-0.328148800941102, 0.07666617563110442)
# B - pearson coefficient and p value: (-0.49531309098000104, 0.0053852135390309724)
# C - pearson coefficient and p value: (-0.3145848644001468, 0.09043061461007369)

print('A, B -', stats.ttest_ind(df1['TsA'], df1['TsB']))
print('A, C -', stats.ttest_ind(df1['TsA'], df1['TsC']))
print('B, C -', stats.ttest_ind(df1['TsB'], df1['TsC']))