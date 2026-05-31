-- Sprint delivery health from GitHub pull requests.
SELECT
    g.title AS pr_title,
    g.state AS pr_state,
    g.user_login AS author,
    g.created_at,
    g.merged_at,
    COUNT(g.id) OVER() AS total_prs,
    SUM(CASE WHEN g.state = 'open' THEN 1 ELSE 0 END) OVER() AS open_prs
FROM github.pull_requests g
WHERE g.created_at >= NOW() - INTERVAL '7 days'
ORDER BY g.created_at DESC
LIMIT 50;
