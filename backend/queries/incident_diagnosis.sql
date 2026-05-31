-- Core Coral query: finds root cause by joining deployments, errors, and comms.
SELECT
    g.title AS pr_title,
    g.merged_at AS pr_merged_at,
    g.user_login AS pr_author,
    s.message AS sentry_error,
    s.first_seen AS sentry_first_seen,
    s.times_seen AS sentry_count,
    sl.text AS slack_message,
    sl.channel AS slack_channel,
    ROUND((EXTRACT(EPOCH FROM (s.first_seen - g.merged_at)) / 60)::numeric, 1)
        AS time_to_incident_minutes
FROM github.pull_requests g
JOIN sentry.issues s
    ON s.first_seen >= g.merged_at
    AND s.first_seen <= g.merged_at + INTERVAL '24 hours'
JOIN slack.messages sl
    ON sl.timestamp >= g.merged_at
    AND sl.channel = '#incidents'
WHERE s.level IN ('fatal', 'error')
    AND g.merged_at >= NOW() - INTERVAL '24 hours'
ORDER BY s.first_seen DESC
LIMIT 20;
