-- 模拟每日新闻平台核心运营指标计算
-- 使用窗口函数计算7日移动平均和环比增长率

SELECT 
    date,
    total_shares AS 当日总阅读量,
    article_count AS 当日发文数,
    avg_shares AS 篇均阅读量,
    -- 7日移动平均
    AVG(total_shares) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS 七日移动平均,
    -- 环比增长率
    ROUND((total_shares - LAG(total_shares) OVER (ORDER BY date)) / 
          LAG(total_shares) OVER (ORDER BY date) * 100, 2) AS 环比增长率_百分比
FROM daily_news_metrics
ORDER BY date DESC;
