-- Create the "work" table
CREATE TABLE IF NOT EXISTS work (
    bot VARCHAR(10),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    activity VARCHAR(100)
);

-- Load the data from the Excel file into the "work" table

-- Query to output continuous periods of work with aggregated activities
WITH cte AS (
    SELECT bot, start_time, end_time,
           lag(end_time) OVER (PARTITION BY bot ORDER BY start_time) AS prev_end_time,
           activity,
           lag(activity) OVER (PARTITION BY bot ORDER BY start_time) AS prev_activity
    FROM work
),
periods AS (
    SELECT bot, start_time, end_time,
           CASE
               WHEN prev_end_time IS NULL OR start_time > prev_end_time THEN TRUE
               ELSE FALSE
           END AS new_period
    FROM cte
),
aggregated_periods AS (
    SELECT bot, start_time, end_time,
           CASE
               WHEN new_period THEN activity
               ELSE prev_activity || ',' || activity
           END AS aggregated_activity
    FROM periods
    LEFT JOIN cte ON periods.bot = cte.bot AND periods.start_time = cte.start_time
)
SELECT bot, start_time, end_time,
       STRING_TO_ARRAY(aggregated_activity, ',') AS activities
FROM aggregated_periods
WHERE new_period OR end_time = (SELECT MAX(end_time) FROM work)
ORDER BY bot, start_time;
