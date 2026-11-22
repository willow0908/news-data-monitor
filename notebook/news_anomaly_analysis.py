import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 1. 读取数据 ==========
df = pd.read_csv('../data/OnlineNewsPopularity.csv')
df.columns = df.columns.str.strip()  # 去掉列名前后空格
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# ========== 2. 按天聚合 ==========
daily = df.groupby('date').agg(
    total_shares=('shares', 'sum'),
    article_count=('shares', 'count'),
    avg_shares=('shares', 'mean')
).reset_index()

# ========== 3. 3σ异常检测 ==========
mean_shares = daily['total_shares'].mean()
std_shares = daily['total_shares'].std()
daily['is_anomaly'] = daily['total_shares'].apply(
    lambda x: '异常' if abs(x - mean_shares) > 3 * std_shares else '正常'
)
anomaly_days = daily[daily['is_anomaly'] == '异常']

print(f"检测到 {len(anomaly_days)} 个异常日期:")
print(anomaly_days[['date', 'total_shares']].to_string(index=False))

# ========== 4. 可视化 ==========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].plot(daily['date'], daily['total_shares'], label='每日阅读量')
axes[0,0].scatter(anomaly_days['date'], anomaly_days['total_shares'],
                  color='red', s=100, label='异常点')
axes[0,0].set_title('新闻平台每日阅读量监控')
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].legend()

axes[0,1].scatter(daily['article_count'], daily['total_shares'])
axes[0,1].set_xlabel('每日发文数')
axes[0,1].set_ylabel('总阅读量')
axes[0,1].set_title('发文量 vs 阅读量')

df['weekday'] = df['weekday_is_monday'].apply(lambda x: '周一' if x == 1 else '其他')
weekday_avg = df.groupby('weekday')['shares'].mean()
axes[1,0].bar(weekday_avg.index, weekday_avg.values)
axes[1,0].set_title('星期几发布对阅读量的影响')

axes[1,1].scatter(df['n_tokens_title'], df['shares'], alpha=0.3, s=5)
axes[1,1].set_xlabel('标题长度（词数）')
axes[1,1].set_ylabel('分享量')
axes[1,1].set_title('标题长度 vs 阅读量')

plt.tight_layout()
plt.savefig('../output/dashboard.png', dpi=150)
print("✅ 仪表盘已保存至 output/dashboard.png")
