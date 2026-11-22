# 新闻热度异常监测项目

基于 Kaggle Online News Popularity 数据集，对新闻平台每日阅读量做聚合统计、异常检测与可视化分析。

## 项目结构

- `data/`：原始数据集
- `sql/daily_metrics.sql`：每日核心指标 SQL 查询（含7日移动平均、环比增长）
- `notebook/news_anomaly_analysis.py`：异常检测与可视化脚本
- `output/`：分析结果图表

## 分析方法

- 按天聚合阅读量、发文数、篇均阅读量
- 3σ 原则识别阅读量异常波动日期
- 发文量、发布时间、标题长度与阅读量的关系可视化

## 运行环境
bash
pip install -r requirements.txt

## 运行方式
bash
python notebook/news_anomaly_analysis.py
输出结果保存至 `output/dashboard.png`。

## 数据来源

Kaggle - Online News Popularity Dataset
