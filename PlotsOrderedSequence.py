import matplotlib.pyplot as plt;
import pandas as pd;
from scipy.stats.stats import pearsonr

fig = plt.figure()
fig.set_figheight(4.5)
fig.set_figwidth(12)

# Read in data
withGreen1 = pd.read_csv("data/ordered/A/with-green.csv")
withoutGreen1 = pd.read_csv("data/ordered/A/without-green.csv")
invocations1 = pd.read_csv("data/ordered/A/invocations.csv")
cacheHits1 = pd.read_csv("data/ordered/A/cacheHits.csv")

# Create data frame
withGreen1 = withGreen1.join(invocations1)
withGreen1 = withGreen1.join(cacheHits1)

df1 = pd.merge(withoutGreen1, withGreen1, on=['project', 'package', 'class', 'method'])
df1 = df1[df1['invocations'] > 0]

df1.reset_index(inplace=True)
df1 = df1.drop(['index'], axis=1)

# Calculate time ratio
df1['Ts'] = pd.to_numeric(df1['time_green'])/pd.to_numeric(df1['time'])

print('number of methods: ', df1['Ts'] .size)
print('number of classes', df1.groupby('class')['method'].nunique().size)

# Plot
plt.plot(df1.index, df1['Ts'], drawstyle="steps-pre", linewidth=0.75)
plt.ylabel('Ts')
plt.xlabel('Program #')
plt.ylim([0, 1.2])

grouped = df1.groupby(['project'])
for name, group in grouped:
    plt.axvline(x=list(group.index)[0], color='c', linewidth=0.5)

fig2 = plt.figure()
fig2.set_figheight(4.5)
fig2.set_figwidth(12)

# Calculate reuse ratio
df1['Rs'] = pd.to_numeric(df1['cacheHits'])/pd.to_numeric(df1['invocations'])

# Plot
plt.plot(df1.index, df1['Rs'], drawstyle="steps-pre", linewidth=0.75)
plt.ylabel('Rs')
plt.xlabel('Program #')

grouped = df1.groupby(['project'])
for name, group in grouped:
    plt.axvline(x=list(group.index)[0], color='c', linewidth=0.5)


print('pearson coefficient and p value:', pearsonr(df1['Ts'], df1['Rs']))

plt.show()
fig.savefig('plots/ordered/all/Ts.png')
fig2.savefig('plots/ordered/all/Rs.png')
