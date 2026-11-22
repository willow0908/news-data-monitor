# 新闻热度异常监测项目

基于 Kaggle Online News Popularity 数据集，对新闻平台每日阅读量做聚合统计、异常检测与可视化分析。

## 项目结构

- `data/`：原始数据集
- `sql/daily_metrics.sql`：每日核心指标 SQL 查询（含7日移动平均、环比增长）
- `notebook/news_anomaly_analysis.py`：异常检测与可视化脚本
- `output/`：分析结果图表

## 分析方法

- 数据集无真实发布日期列，仅有 timedelta（发布至2015-01-08采集日的天数），本项目以采集日为基准倒推构造模拟日期维度，按模拟日聚合 shares / 发文数 / 篇均阅读量，用 3σ 识别异常波动日，并分析星期几、标题长度与传播量的关系，模拟新闻平台日常监控与运营周报流程。
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

Source: Fernandes, Vinagre & Cortez (2015), A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News, EPIA 2015.
