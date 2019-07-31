import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd;
from sklearn.linear_model import LinearRegression;

fig, ax = plt.subplots(1, 2)
# fig.tight_layout()
fig.set_figheight(4.5)
fig.set_figwidth(12)

fig2, ax2 = plt.subplots(1, 2)
# fig2.tight_layout()
fig2.set_figheight(4)
fig2.set_figwidth(8)

# Read in data
withGreen1 = pd.read_csv("data/random/A/with-green.csv")
withoutGreen1 = pd.read_csv("data/random/A/without-green.csv")
invocations1 = pd.read_csv("data/random/A/invocations.csv")
cacheHits1 = pd.read_csv("data/random/A/cacheHits.csv")

# Create data frame
withGreen1 = withGreen1.join(invocations1)
withGreen1 = withGreen1.join(cacheHits1)


df1 = pd.merge(withoutGreen1, withGreen1, on=['project', 'package', 'class', 'method'])
df1 = df1[df1['invocations']>0]

df1.reset_index(inplace=True)
df1 = df1.drop(['index'], axis=1)

print(df1.groupby('class')['method'].nunique().size)

# Calculate time ratio
df1['Ts'] = pd.to_numeric(df1['time_green'])/pd.to_numeric(df1['time'])
print('size of sequence 1 ', df1['Ts'] .size)

x = pd.DataFrame(np.arange(0.0, df1['Ts'].size, 1))

linear_regressor = LinearRegression()
linear_regressor.fit(x, df1['Ts'].values)
Y_pred = linear_regressor.predict(x)

ax[0].plot(df1.index, df1['Ts'], drawstyle="steps-pre", linewidth=0.75)
ax[0].set_ylabel('Ts')
ax[0].set_xlabel('Program #')
ax[0].set_ylim([0, 1.5])
# ax[0].plot(x, Y_pred, color='red')


df1['Rs'] = pd.to_numeric(df1['cacheHits'])/pd.to_numeric(df1['invocations'])

ax[1].plot(df1.index, df1['Rs'], drawstyle="steps-pre", linewidth=0.75)
ax[1].set_ylabel('Rs')
ax[1].set_xlabel('Program #')
# ax[1].title.set_text('S1')

ax2[0].boxplot(df1['Ts'])
ax2[0].set_ylabel('Ts')
ax2[0].set_ylim([0, 1.5])

ax2[1].boxplot(df1['Rs'])
ax2[1].set_ylabel('Rs')


plt.show()
fig.savefig('plots/random/all/TsRs.png')
fig2.savefig('plots/random/all/TsRsBoxplot.png')

