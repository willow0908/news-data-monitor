-- 模拟每日新闻平台核心运营指标计算
-- 使用窗口函数计算7日移动平均和环比增长率
-- 模拟：以采集日 2015-01-08 为基准，用 timedelta 倒推 sim_date

SELECT
    DATE('2015-01-08') - INTERVAL timedelta DAY AS sim_date,
    SUM(shares)          AS total_shares,
    COUNT(*)             AS article_count,
    AVG(shares)          AS avg_shares,
    AVG(SUM(shares)) OVER (ORDER BY DATE('2015-01-08') - INTERVAL timedelta DAY
                           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7_shares
FROM online_news
GROUP BY sim_date
ORDER BY sim_date;
