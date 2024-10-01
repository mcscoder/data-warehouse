use weather_db
select
    *
from
    Date_Dim dd;

select
    *
from
    Location_Dim ld;

select
    *
from
    Weather_Fact wf;

-- Average temperature each month
SELECT
    year,
    month,
    AVG(Temperature_C) AS avg_temp
FROM
    Weather_Fact wf
    JOIN Date_Dim dd ON wf.date_id = dd.date_id
GROUP BY
    year,
    month
ORDER BY
    year,
    month;

-- Average precipitation 
SELECT
    ld.Location,
    AVG(Precipitation_mm) AS avg_precipitation
FROM
    Weather_Fact wf
    JOIN Location_Dim ld ON wf.location_id = ld.location_id
GROUP BY
    ld.Location
ORDER BY
    avg_precipitation DESC;

SELECT
    ld.Location,
    dd.`month`,
    AVG(wf.Wind_Speed_kmh)
FROM
    Weather_Fact wf
    JOIN Location_Dim ld ON wf.location_id = ld.location_id
    JOIN Date_Dim dd ON wf.date_id = dd.date_id
WHERE
    dd.`month` = 1
GROUP BY
    ld.Location,
    dd.`month`;

desc Date_Dim;