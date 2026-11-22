import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. 读取
path = '/kaggle/input/datasets/thehapyone/uci-online-news-popularity-data-set/OnlineNewsPopularity.csv'
df = pd.read_csv(path)
df.columns = df.columns.str.strip()  

# 2. 用 timedelta 构造模拟日期（timedelta=发布到2015-01-08采集日的天数）
base_date = pd.Timestamp('2015-01-08')
df['sim_date'] = base_date - pd.to_timedelta(df['timedelta'], unit='D')
df['date_bucket'] = df['sim_date'].dt.strftime('%Y-%m-%d')  # 按真实倒推日聚合

# 3. 按天聚合（模拟“每日运营指标”）
daily = df.groupby('date_bucket').agg(
    total_shares=('shares', 'sum'),
    article_count=('shares', 'count'),
    avg_shares=('shares', 'mean')
).reset_index().sort_values('date_bucket')

# 4. 3σ异常检测
mu, sigma = daily['total_shares'].mean(), daily['total_shares'].std()
daily['is_anomaly'] = (daily['total_shares'] - mu).abs() > 3 * sigma
anom = daily[daily['is_anomaly']]

print(f"模拟日期桶数: {len(daily)}, 异常桶数: {len(anom)}")
print(anom[['date_bucket','total_shares','article_count']].to_string(index=False))

# 5. 可视化
fig, ax = plt.subplots(2, 2, figsize=(14, 10))

ax[0,0].plot(daily['date_bucket'], daily['total_shares'], lw=1, label='daily shares')
ax[0,0].scatter(anom['date_bucket'], anom['total_shares'], c='red', s=60, label='3σ anomaly')
ax[0,0].set_title('Simulated Daily Share Monitoring (by timedelta)')
ax[0,0].tick_params(axis='x', rotation=90, labelsize=6)
ax[0,0].legend()

ax[0,1].scatter(daily['article_count'], daily['total_shares'], s=8)
ax[0,1].set_xlabel('articles/day'); ax[0,1].set_ylabel('total shares')
ax[0,1].set_title('Volume vs Shares')

wd = [c for c in df.columns if c.startswith('weekday_is_')]
names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
avgs = [df[df[c]==1]['shares'].mean() for c in wd]
ax[1,0].bar(names, avgs)
ax[1,0].set_title('Avg Shares by Weekday')

ax[1,1].scatter(df['n_tokens_title'], df['shares'], alpha=0.2, s=4)
ax[1,1].set_xlabel('title length'); ax[1,1].set_ylabel('shares')
ax[1,1].set_title('Title Length vs Shares')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=150)
print('saved dashboard.png')
plt.show()
