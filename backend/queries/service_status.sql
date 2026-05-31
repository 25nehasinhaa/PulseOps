-- Service health snapshot from recent Sentry activity.
SELECT
    'sentry' AS source,
    level AS severity,
    COUNT(*) AS error_count,
    MAX(last_seen) AS last_occurrence
FROM sentry.issues
WHERE last_seen >= NOW() - INTERVAL '1 hour'
GROUP BY level
ORDER BY error_count DESC;
