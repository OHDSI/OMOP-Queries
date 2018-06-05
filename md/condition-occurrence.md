CO04:Count In what place of service where condition diagnoses.
------------------

Returns the distribution of the visit place of service where the condition was reported.

**Sample query:**

    SELECT concept\_name AS place\_of\_service\_name, place\_freq

    FROM (

    SELECT care\_site\_id, count(\*) AS place\_freq

    FROM (

    SELECT care\_site\_id

    FROM (

    SELECT visit\_occurrence\_id

    FROM condition\_occurrence

    WHERE condition\_concept\_id = 31967

    AND visit\_occurrence\_id

    IS NOT NULL) AS from\_cond

    LEFT JOIN (

    SELECT visit\_occurrence\_id, care\_site\_id

    FROM visit\_occurrence) AS from\_visit ON from\_cond.visit\_occurrence\_id=from\_visit.visit\_occurrence\_id )

    GROUP BY care\_site\_id

    ORDER BY place\_freq ) AS place\_id\_count

    LEFT JOIN (

    SELECT concept\_id, concept\_name

    FROM concept) AS place\_concept ON place\_id\_count.care\_site\_id=place\_concept.concept\_id

    ORDER BY place\_freq;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept ID for 'Nausea' |





**Output:**

| ** Field** | ** Description** |
| --- | --- |
| place\_of\_service\_name | The place of service where the condition was reported. |
| place\_freq | Frequency of the place of service. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| place\_of\_service\_name | Emergency Room |
| place\_freq | 35343 |

CO05: Breakout of condition by gender, age
---------------

Returns the distribution of condition breakouts per gender and age.

**Sample query:**

    SELECT
      concept\_name AS gender,
      age,
      gender\_age\_freq

    FROM (

      SELECT

        gender\_concept\_id,

        age,

        COUNT(1) gender\_age\_freq

      FROM (

        SELECT

          year\_of\_birth,
    
          month\_of\_birth,

          day\_of\_birth,

          gender\_concept\_id,

          condition\_start\_date,

          DATEDIFF(years, CONVERT(DateTime, year\_of\_birth||'-01-01'), condition\_start\_date) AS age

        FROM (

          SELECT

            person\_id,

            condition\_start\_date

          FROM condition\_occurrence

          WHERE

            condition\_concept\_id = 31967 AND

            person\_id IS NOT NULL

        ) AS from\_cond

        LEFT JOIN person as from\_person ON from\_cond.person\_id=from\_person.person\_id ) AS gender\_count

      GROUP BY

        gender\_concept\_id,

        age

      ORDER BY gender\_age\_freq

    ) AS gender\_id\_age\_count

    LEFT JOIN concept as concept\_list ON gender\_id\_age\_count.gender\_concept\_id=concept\_list.concept\_id

    ORDER BY gender\_age\_freq DESC;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept ID for 'Nausea' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| gender | A person's gender |
| age | A person's age in years |
| gender\_age\_freq | The frequency of a condition breakout for person gender at a certain age. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| gender | Female |
| age | 50 |
| gender\_age\_freq | 3136 |

CO06:What are a person's comorbidities.
-------------------

### Returns all coexisting conditions for a given person as defined in the condition\_era table.

**Sample query:**

    SELECT DISTINCT

      CASE WHEN concept\_name\_1>concept\_name\_2 THEN concept\_name\_1 ELSE concept\_name\_2 END as condition1,

      CASE WHEN concept\_name\_1>concept\_name\_2 THEN concept\_name\_2 ELSE concept\_name\_1 END AS condition2

    FROM (

      SELECT

        concept\_name\_1,

        concept\_name AS concept\_name\_2

      FROM (

        SELECT

          condition\_concept\_id\_2,

          concept\_name AS concept\_name\_1

        FROM (

          SELECT

            table1.condition\_concept\_id AS condition\_concept\_id\_1,

            table2.condition\_concept\_id AS condition\_concept\_id\_2

          FROM

            (SELECT \* FROM condition\_era WHERE person\_id = 136931019) AS table1,

            (SELECT \* FROM condition\_era WHERE person\_id = 136931019) AS table2

          WHERE

            table2.condition\_era\_start\_date <= table1.condition\_era\_end\_date AND

            (table2.condition\_era\_end\_date IS NULL OR table2.condition\_era\_end\_date >= table1.condition\_era\_start\_date) AND

            table1.condition\_concept\_id<>table2.condition\_concept\_id

        ) AS comorb

        LEFT JOIN concept AS concept\_list ON comorb.condition\_concept\_id\_1=concept\_list.concept\_id

      ) AS comorb2

      LEFT JOIN concept AS concept\_list ON comorb2.condition\_concept\_id\_2=concept\_list.concept\_id

    ) AS condition\_pairs;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| person\_id | 136931019 | Yes | Randomly picked person identifier |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Condition 1 | Name of one condition in the comorbidity. |
| Condition 2 | Name of the other condition in the comorbidity. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Condition 1 | Hyperlipidemia |
| Condition 2 | Abnormal breathing |

CO07: Frequency of hospitalized for a condition
-----------

Returns the distribution of number of times a person has been hospitalized where a certain condition was reported.

**Sample query:**

    SELECT

      number\_of\_hospitlizations,

      count(\*) AS persons\_freq

    FROM (

      SELECT

        person\_id,

        COUNT(\*) AS number\_of\_hospitlizations

      FROM (

        SELECT distinct

          condition\_era\_id,

          era.person\_id

        FROM (

          SELECT

            condition\_start\_date,

            condition\_end\_date,

            from\_cond.person\_id

          FROM (

            SELECT

              visit\_occurrence\_id,

              condition\_start\_date,

              condition\_end\_date,

              person\_id

            FROM condition\_occurrence

            WHERE

              condition\_concept\_id=31967 AND

              visit\_occurrence\_id IS NOT NULL

          ) AS FROM\_cond

          JOIN visit\_occurrence AS FROM\_visit

            ON FROM\_cond.visit\_occurrence\_id=FROM\_visit.visit\_occurrence\_id

          JOIN care\_site cs on from\_visit.care\_site\_id=cs.care\_site\_id

             where place\_of\_service\_concept\_id=8717

        ) AS occurr,

        (

          SELECT

            condition\_era\_id,

            person\_id,

            condition\_era\_start\_date,

            condition\_era\_end\_date

          FROM condition\_era

          WHERE condition\_concept\_id=31967

        ) AS era

        WHERE

          era.person\_id=occurr.person\_id AND

          era.condition\_era\_start\_date <= occurr.condition\_end\_date AND

          (era.condition\_era\_end\_date IS NULL OR era.condition\_era\_end\_date >= occurr.condition\_start\_date)

      )

      GROUP BY person\_id

      ORDER BY number\_of\_hospitlizations desc

    )

    GROUP BY number\_of\_hospitlizations

    ORDER BY persons\_freq desc

    ;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| number\_of\_hospitlizations | Number of times a person was reported to be hospitalized with a certain condition. |
| persons\_freq | Number of persons which were reported to have a certain number of hospilizations with a certain condition. |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| number\_of\_hospitlizations | 2 |
| persons\_freq | 177 |

CO08: Duration of hospitalization for a conditions
-----------

Returns the the average length in days of all hospitalizations where a certain condition was reported

**Sample query:**

    SELECT

      avg(hosp\_no\_days) AS average\_hosp\_duration\_count

    FROM (

      SELECT DISTINCT

        hosp\_no\_days,

        person\_id,

        from\_visit.visit\_occurrence\_id

      FROM (

        SELECT

          visit\_occurrence\_id, condition\_start\_date, condition\_end\_date, person\_id

        FROM condition\_occurrence

        WHERE

          condition\_concept\_id = 31967 AND

          visit\_occurrence\_id IS NOT NULL

      ) AS from\_cond

      JOIN (

        SELECT

          DATEDIFF(DAY, visit\_start\_date, visit\_end\_date) + 1 AS hosp\_no\_days,

          visit\_start\_date,

          visit\_occurrence\_id,

          place\_of\_service\_concept\_id

        FROM visit\_occurrence v

        JOIN care\_site c on v.care\_site\_id=c.care\_site\_id

        WHERE place\_of\_service\_concept\_id = 8717

      ) AS from\_visit

        ON from\_cond.visit\_occurrence\_id = from\_visit.visit\_occurrence\_id );



**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| average\_hosp\_duration\_count | Average length in days of all hospitalization where a certain condition was reported. +1 was added for partial days (e.g. 1.5 days were counted as 2 days). |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| average\_hosp\_duration\_count | 7 |

CO09: Is a condition seasonal, alergies for example
---------------

Returns the distribution of condition occurrence per season in the northern hemisphere, defined in the following way:

|  Spring |  March 21 - June 21 |
| --- | --- |
|  Summer |  June 22 - September 22 |
|  Fall |  September 23 - December 21 |
|  Winter |  December 22 - March 20 |

**Sample query:**

    SELECT season, COUNT(\*) as season\_freq

    FROM (

    SELECT CASE

    WHEN (daymonth>0320

    AND daymonth<=0621) THEN 'Spring' WHEN (daymonth>0621

    AND daymonth<=0922) THEN 'Summer' WHEN (daymonth>0922

    AND daymonth<=1221) THEN 'Fall' WHEN (daymonth>1221

    OR (daymonth>0000

    AND daymonth<=0520)) THEN 'Winter' ELSE 'Unknown' end AS season

    FROM (

    SELECT cast(substring(condition\_start\_date

    from 6 for 2)|| substring(condition\_start\_date

    from 9 for 2) as int) AS daymonth,condition\_start\_date

    FROM condition\_occurrence

    WHERE condition\_concept\_id = 31967 ) ) AS condition\_season

    GROUP BY season

    ORDER BY season\_freq;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |


**Output:**

| **Field** | ** Description** |
| --- | --- |
| season | Season as defined in the northern hemisphere. |
| season\_freq | Frequency of condition occurrence in the season. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| season | Summer |
| season\_freq | 62924 |

CO12: Distribution of condition end dates.
------------

This query is used to to provide summary statistics for condition occurrence end dates (condition\_occurrence\_end\_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

    with end\_rank as (

      SELECT

        condition\_end\_date-'0001-01-01' as num\_end\_date,

        condition\_end\_date,

        sum(1) over (partition by 1 order by condition\_end\_date asc rows between unbounded preceding and current row) as rownumasc

      FROM

        condition\_occurrence

    ),

    other\_stat as (

      SELECT

        count(condition\_end\_date) as condition\_end\_date\_count,

        min(condition\_end\_date) as condition\_end\_date\_min,

        max(condition\_end\_date) as condition\_end\_date\_max,

        to\_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition\_end\_date-'0001-01-01') as int) as condition\_end\_date\_average,

        stddev((condition\_end\_date-'0001-01-01')) as condition\_end\_date\_stddev

      FROM

        condition\_occurrence

      WHERE

        condition\_end\_date is not null

    )

    SELECT

      (SELECT count(condition\_end\_date) FROM condition\_occurrence WHERE condition\_end\_date is null) AS condition\_end\_date\_null\_count,

      \*

    FROM

      other\_stat,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_end\_date-'0001-01-01') as int) AS condition\_end\_date\_25percentile

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

          (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

      ) AS condition\_end\_date\_25percentile,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_end\_date-'0001-01-01') as int) as condition\_end\_date\_median

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

          (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

      ) AS condition\_end\_date\_median,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_end\_date-'0001-01-01') as int) as condition\_end\_date\_75percentile

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

          (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

      ) AS condition\_end\_date\_75percentile;

**Input:**

None



**Output:**

| **Field** | ** Description** |
| --- | --- |
| condition\_end\_date\_null\_count | Number of condition occurrences where end date is null |
| condition\_end\_date\_count | Number of condition occurrence end dates |
| condition\_end\_date\_min | The earliest end date of a condition occurrence |
| condition\_end\_date\_max | The latest end date of a condition occurrence |
| condition\_end\_date\_average | The average end date (spanning from the earliest to the latest date and counted by days) |
| condition\_end\_date\_stddev | The standard deviation of end dates, in number of days (spanning from the earliest to the latest date and counted by days) |
| condition\_end\_date\_25percentile |  An end date where 25 percent of the other end dates are earlier |
| condition\_end\_date\_median |  An end date where half of the other end dates are earlier and half are later |
| condition\_end\_date\_75percentile |  An end date where 75 percent of the other end dates are earlier |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| condition\_end\_date\_null\_count | 0 |
| condition\_end\_date\_count | 224523674 |
| condition\_end\_date\_min | 2003-01-01 |
| condition\_end\_date\_max | 011-12-15 |
| condition\_end\_date\_average | 2008-11-30 |
| condition\_end\_date\_stddev | 651.19 |
| condition\_end\_date\_25percentile | 2007-10-30 |
| condition\_end\_date\_median | 2009-05-07 |
| condition\_end\_date\_75percentile | 2010-05-04 |

CO13: Distribution of condition start dates
-----------

This query is used to to provide summary statistics for condition occurrence start dates (condition\_occurrence\_start\_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

    with end\_rank as (

      SELECT

        condition\_start\_date-'0001-01-01' as num\_start\_date,

        condition\_start\_date,

        sum(1) over (partition by 1 order by condition\_start\_date asc rows between unbounded preceding and current row) as rownumasc

      FROM

        condition\_occurrence

    ),

    other\_stat as (

      SELECT

        count(condition\_start\_date) as condition\_start\_date\_count,

        min(condition\_start\_date) as condition\_start\_date\_min,

        max(condition\_start\_date) as condition\_start\_date\_max,

        to\_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition\_start\_date-'0001-01-01') as int) as condition\_start\_date\_average,

        stddev((condition\_start\_date-'0001-01-01')) as condition\_start\_date\_stddev

      FROM

        condition\_occurrence

      WHERE

        condition\_start\_date is not null

    )

    SELECT

      (SELECT count(condition\_start\_date) FROM condition\_occurrence WHERE condition\_start\_date is null) AS condition\_start\_date\_null\_count,

      \*

    FROM

      other\_stat,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_start\_date-'0001-01-01') as int) AS condition\_start\_date\_25percentile

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

          (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

      ) AS condition\_start\_date\_25percentile,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_start\_date-'0001-01-01') as int) as condition\_start\_date\_median

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

          (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

      ) AS condition\_start\_date\_median,

      ( SELECT

          to\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\_start\_date-'0001-01-01') as int) as condition\_start\_date\_75percentile

        FROM

          (select \*,(select count(\*) from end\_rank) as rowno from end\_rank)

        WHERE

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

          (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

      ) AS condition\_start\_date\_75percentile;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| condition\_start\_date\_null\_count | Number of condition occurrences where start date is null |
| condition\_start\_date\_count | Number of condition occurrence start dates |
| condition\_start\_date\_min | The earliest start date of a condition occurrence |
| condition\_start\_date\_max | The latest start date of a condition occurrence |
| condition\_start\_date\_average | The average start date (spanning from the earliest to the latest date and counted by days) |
| condition\_start\_date\_stddev | The standard deviation of start dates, in number of days (spanning from the earliest to the latest date and counted by days) |
| condition\_start\_date\_25percentile | A start date where 25 percent of the other end dates are earlier |
| condition\_start\_date\_median | A start date where half of the other end dates are earlier and half are later |
| condition\_start\_date\_75percentile | A start date where 75 percent of the other end dates are earlier |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| condition\_end\_date\_null\_count | 0 |
| condition\_end\_date\_count | 224523674 |
| condition\_end\_date\_min | 2003-01-01 |
| condition\_end\_date\_max | 2011-11-08 |
| condition\_end\_date\_average | 2008-11-30 |
| condition\_end\_date\_stddev | 651.27 |
| condition\_end\_date\_25percentile | 2007-10-30 |
| condition\_end\_date\_median | 2009-05-06 |
| condition\_end\_date\_75percentile | 2010-05-03 |

CO14: Counts of condition types

This query is used to count the condition type concepts (condition\_type\_concept\_id, in the CDM V2 condition\_occurrence\_type) across all condition occurrence records. The input to the query is a value of a condition\_type\_concept\_id.

**Sample query:**

    SELECT condition\_type\_freq, condition\_type\_concept\_id, concept\_name

    FROM (

    SELECT condition\_type\_concept\_id, count(\*) as condition\_type\_freq

    FROM (

    SELECT \*

    from condition\_occurrence)

    WHERE condition\_concept\_id = 31967

    GROUP BY condition\_type\_concept\_id) AS condition\_type\_count

    LEFT JOIN (

    SELECT concept\_id, concept\_name

    FROM concept) AS type\_concept ON condition\_type\_count.condition\_type\_concept\_id=type\_concept.concept\_id

    ORDER BY condition\_type\_freq;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_type\_freq | Frequency of a specific condition\_type |
| condition\_type\_concept\_id | Unique ID for condition\_type |
| concept\_name |  Description of the condition's data source |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_type\_freq | 4735 |
| condition\_type\_concept\_id | 38000235 |
| concept\_name | Outpatient header - 6th position |

CO15: Distribution of number of distinct conditions persons have
----------

This query is used to provide summary statistics for the number of different distinct conditions (condition\_concept\_id) of all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

    with ranked as (

      SELECT

        num\_of\_conditions,

        row\_number() over (order by num\_of\_conditions asc) AS rownumasc

      FROM(

        select

          person\_id,

          count(distinct condition\_concept\_id) AS num\_of\_conditions

        FROM condition\_occurrence

        where person\_id!=0

        GROUP BY person\_id

      )

    ),

    other\_stat AS (

      SELECT

        count(num\_of\_conditions) as condition\_dist\_num\_count,

        min(num\_of\_conditions) as condition\_dist\_num\_min,

        max(num\_of\_conditions) as condition\_dist\_num\_max,

        avg(num\_of\_conditions) as condition\_dist\_num\_averege,

        stddev(num\_of\_conditions) as condition\_dist\_num\_stddev

      FROM (

        SELECT

          count(distinct condition\_concept\_id) AS num\_of\_conditions,

          person\_id

        FROM condition\_occurrence

        WHERE person\_id!=0

        GROUP BY person\_id

      )

    )

    SELECT

      (SELECT count(distinct person\_id) FROM condition\_occurrence WHERE person\_id!=0 and condition\_occurrence\_id is null) AS condition\_null\_count,

      \*

    FROM

      other\_stat,

      ( SELECT distinct

          num\_of\_conditions as condition\_dist\_num\_25percentile

        FROM

          (select \*,(select count(\*) from ranked) as rowno from ranked)

        WHERE

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

          (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

          (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

      ) AS condition\_end\_date\_25percentile,

      ( SELECT distinct

          num\_of\_conditions as condition\_dist\_num\_median

        FROM

          (select \*,(select count(\*) from ranked) as rowno from ranked)

        WHERE

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

          (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

          (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

      ) AS condition\_end\_date\_median,

      ( SELECT distinct

          num\_of\_conditions as condition\_dist\_num\_75percentile

        FROM

          (select \*,(select count(\*) from ranked) as rowno from ranked)

        WHERE

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

          (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

          (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

      ) AS condition\_end\_date\_75percentile;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_null\_count | Number of condition occurrences where condition\_occurrence\_id is null |
| condition\_count | Number of condition occurrences |
| condition\_dist\_num\_min | The lowest number of distinct condition occurrences |
| condition\_dist\_num\_max | The highest number of distinct condition occurrences |
| condition\_dist\_num\_averege | The avarege number of distinct condition occurrences |
| condition\_dist\_num\_stddev | The standard deviation of distinct condition occurence numbers |
| condition\_dist\_num\_25percentile | A distinct condition occurrence number where 25 percent of the other numbers are lower |
| condition\_dist\_num\_median | A distinct condition occurrence number where half of the other numbers are lower and half are higher |
| condition\_dist\_num\_75percentile | A distinct condition occurrence number where 75 percent of the other numbers are lower |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_null\_count | 0 |
| condition\_count | 4395019 |
| condition\_dist\_num\_min | 1 |
| condition\_dist\_num\_max | 327 |
| condition\_dist\_num\_averege | 17 |
| condition\_dist\_num\_stddev | 16.94 |
| condition\_dist\_num\_25percentile | 6 |
| condition\_dist\_num\_median | 12 |
| condition\_dist\_num\_75percentile | 23 |

CO16: Counts of number of distinct conditions persons have
----------

This query is used to count the number of different distinct conditions (condition\_concept\_id) of all persons. The input to the query is a value for a concept identifier.

**Sample query:**

    SELECT count(c.condition\_concept\_id) conditions\_count, c.person\_id

    FROM condition\_occurrence c

    WHERE condition\_concept\_id = 201820

    GROUP BY c.person\_id

    ORDER BY 1

    DESC;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 201820 | Yes | Condition concept identifier for 'Diabetes mellitus' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| conditions\_count | Number of conditions recorded for the person |
| person\_id | Person identifier |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| conditions\_count |  39 |
| person\_id |  20017834818 |

CO17: Distribution of condition occurrence records per person
-----------

This query is used to provide summary statistics for the number of condition occurrence records (condition\_occurrence\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

**Sample query:**

    with ranked as

      (

      SELECT num\_of\_conditions, sum(1) over (partition by 1

      ORDER BY num\_of\_conditions asc rows BETWEEN unbounded preceding AND current row) AS rownumasc

      FROM (

                                            SELECT count(\*) as num\_of\_conditions

                                            FROM condition\_occurrence

                                            WHERE person\_id!=0

                                            GROUP BY person\_id

                                    )

      ),

      other\_stat AS

      (

       SELECT count(num\_of\_conditions) AS condition\_num\_count,

                            min(num\_of\_conditions) AS condition\_num\_min,

          max(num\_of\_conditions) AS condition\_num\_max,

                            avg(num\_of\_conditions) AS condition\_num\_averege,

          stddev(num\_of\_conditions) as condition\_num\_stddev

       FROM (

                                       SELECT count(\*) AS num\_of\_conditions, person\_id

                                       FROM   condition\_occurrence

                                       WHERE person\_id!=0

                                       GROUP BY person\_id

                               )

      )

    SELECT

     (

            SELECT count(distinct person\_id)

            FROM condition\_occurrence

            WHERE person\_id!=0 AND condition\_occurrence\_id IS NULL

     ) AS condition\_null\_count,

     \* FROM other\_stat,

     (

      SELECT num\_of\_conditions AS condition\_num\_25percentile

      FROM (SELECT \*,(SELECT count(\*) FROM ranked) as rowno FROM ranked)

      WHERE (rownumasc=cast (rowno\*0.25 as int) AND mod(rowno\*25,100)=0) OR

         (rownumasc=cast (rowno\*0.25 as int) AND mod(rowno\*25,100)>0) OR

         (rownumasc=cast (rowno\*0.25 as int)+1 AND mod(rowno\*25,100)>0)

     ) AS condition\_num\_25percentile,

     (

      SELECT num\_of\_conditions AS condition\_num\_median

      FROM (SELECT \*,(SELECT count(\*) FROM ranked) AS rowno FROM ranked)

      WHERE (rownumasc=cast (rowno\*0.50 AS int) AND mod(rowno\*50,100)=0) OR

         (rownumasc=cast (rowno\*0.50 AS int) AND mod(rowno\*50,100)>0) OR

         (rownumasc=cast (rowno\*0.50 AS int)+1 AND mod(rowno\*50,100)>0)

     ) AS condition\_num\_median,

     (

      SELECT num\_of\_conditions AS condition\_num\_75percentile

      FROM (SELECT \*,(SELECT count(\*) FROM ranked) as rowno FROM ranked)

      WHERE (rownumasc=cast (rowno\*0.75 as int) AND mod(rowno\*75,100)=0) OR

         (rownumasc=cast (rowno\*0.75 as int) AND mod(rowno\*75,100)>0) OR

         (rownumasc=cast (rowno\*0.75 as int)+1 AND mod(rowno\*75,100)>0)

     ) AS condition\_num\_75percentile

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_null\_count | Number of persons with at least one null condition\_occurrence\_id |
| condition\_num\_count | Number of distinct persons with conditions |
| condition\_num\_min | The lowest number of condition occurences |
| condition\_num\_max | The highest number of condition occurences |
| condition\_num\_averege | The average number of condition occurences |
| condition\_num\_stddev | The standard deviation of condition occurence numbers |
| condition\_num\_25percentile | A condition occurence number where 25 percent of the other numbers are lower |
| condition\_num\_median | A condition occurence number where half of the other numbers are lower and half are higher |
| condition\_num\_75percentile | A condition occurence number where 75 percent of the other numbers are lower |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_null\_count | 4395019 |
| condition\_num\_count |   |
| condition\_num\_min | 1 |
| condition\_num\_max | 7144 |
| condition\_num\_averege | 51 |
| condition\_num\_stddev | 86.63 |
| condition\_num\_25percentile | 11 |
| condition\_num\_median | 26 |
| condition\_num\_75percentile | 58 |
**CO19**** :**Counts of condition occurrence records stratified by observation month

This query is used to count the condition occurrence records stratified by observation month.

**Sample query:**

SELECT extract(month

from condition\_start\_date) month\_number, count(\*) as number\_of\_conditions\_in\_month

FROM condition\_occurrence

GROUP BY extract(month

from condition\_start\_date)

ORDER BY 1;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| Month\_number | Month number |
| Number\_of\_conditions\_in\_month |  The number of the condition occurrences is a specified month. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Month\_number |  3 |
| Number\_of\_conditions\_in\_month |  20643257 |
**CO21:** Distribution of age, stratified by condition

This query is used to provide summary statistics for the age across all condition occurrence records stratified by condition (condition\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest condition occurrence. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id.

Oracle specific query.

**Sample query:**

SELECT concept\_name AS condition

     , condition\_concept\_id

     , count(\*) AS condition\_occurrences

     , min( age ) over () AS min\_age

     , max( age ) over () AS max\_age

     , round( avg( age ), 2 ) AS avg\_age

     , round( stdDev( age ) over (), 1 ) AS stdDev\_age

     , PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY age ) over ()

                                     AS percentile\_25

     , PERCENTILE\_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over ()

                                     AS median\_age

     , PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY age ) over ()

                                     AS percentile\_75

  FROM -- condition occurrences with age at time of condition

     ( SELECT condition\_concept\_id

            , EXTRACT( YEAR from condition\_start\_date ) AS age -- year\_of\_birth

         FROM condition\_occurrence

         JOIN person USING( person\_id )

        WHERE condition\_concept\_id

           IN -- all SNOMED codes for diabetes

            ( 192691, 193323, 194700, 195771, 200687, 201254,

         201530, 201531, 201820, 201826 , 318712, 373999,

         377821, 4008576, 4009780, 4024659, 4030061,

         4034960, 4034962, 4047906 , 40480000, 4048202,

         40482883, 40488810, 4058243, 4062685, 4062686,

         4062687, 4063042, 4063043 , 4079850, 4096041,

         4096042, 4096668, 4096670, 4096671, 4099214,

         4099215, 4099217, 4099334 , 4099651, 4099652,

         4099653, 4099741, 4102018, 4129378, 4129516,

         4129519, 4130162, 4130164 , 4130166, 4136889,

         4137214, 4140808, 4143529, 4143689, 4143857,

         4144583, 4145827, 4151281 , 4151282, 4152858,

         4155634, 4166381, 4178452, 4178790, 4192852,

         4193704, 4196141, 4198296 , 4200873, 4200875,

         4202383, 4212631, 4221344, 4222222, 4222410,

         4222547, 4222553, 4222687 , 4222834, 4223303,

         4223444, 4224254, 4224709, 4224723, 4225013,

         4225055, 4225656, 4226245 , 4227210, 4228102,

         4228112, 4230254, 4231917, 4235410, 4237068,

         4240589, 4245270, 4252384, 4263902, 4295011,

         4304377, 4312138, 4321756, 4322638, 4325113,

         4326434, 4327944, 435216 , 439770, 443012,

         443412, 443592

            )

     )

  JOIN concept ON concept\_id = condition\_concept\_id

GROUP BY concept\_name, condition\_concept\_id, age

ORDER BY condition\_occurrences DESC

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id list | 192691, 193323, 194700, 195771, 200687, 201254, 201530, 201531, 201820, 201826 , 318712, 373999, 377821, 4008576, 4009780, 4024659, 4030061, 4034960, 4034962, 4047906 , 40480000, 4048202, 40482883, 40488810, 4058243, 4062685, 4062686, 4062687, 4063042, 4063043 , 4079850, 4096041, 4096042, 4096668, 4096670, 4096671, 4099214, 4099215, 4099217, 4099334 , 4099651, 4099652, 4099653, 4099741, 4102018, 4129378, 4129516, 4129519, 4130162, 4130164 , 4130166, 4136889, 4137214, 4140808, 4143529, 4143689, 4143857, 4144583, 4145827, 4151281 , 4151282, 4152858, 4155634, 4166381, 4178452, 4178790, 4192852, 4193704, 4196141, 4198296 , 4200873, 4200875, 4202383, 4212631, 4221344, 4222222, 4222410, 4222547, 4222553, 4222687 , 4222834, 4223303, 4223444, 4224254, 4224709, 4224723, 4225013, 4225055, 4225656, 4226245 , 4227210, 4228102, 4228112, 4230254, 4231917, 4235410, 4237068, 4240589, 4245270, 4252384, 4263902, 4295011, 4304377, 4312138, 4321756, 4322638, 4325113, 4326434, 4327944, 435216 , 439770, 443012, 443412, 443592 | Yes | SNOMED condition concept identifiers for dia |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition | Name of the condition |
| condition\_concept\_id | Condition concept identifier |
| min\_age | Minimum age of the people with condition |
| max\_age | Maximum age of the people with condition |
| avg\_age | Average age of the people with condition |
| stdDev\_age | Standard deviation of the people  with condition |
| percentile\_25 | Age 25th percentile of the people with condition |
| median\_age | Median age  of the people with condition |
| percentile\_75 | Age 75th percentile of the people with condition |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition | Type 1 diabetes mellitus |
| condition\_concept\_id | 201826 |
| min\_age | 2006 |
| max\_age | 2017 |
| avg\_age | 2014 |
| stdDev\_age | 3.6 |
| percentile\_25 | 2009 |
| median\_age | 2013 |
| percentile\_75 | 2015 |
**CO22:** Counts of conditions, stratified by condition type

This query is used to count conditions across all condition occurrence records stratified by condition occurrence type

**Sample query:**

SELECT concept\_name AS condition\_occurrence\_type , condition\_type\_concept\_id , count(\*) AS occurrence\_type\_count

FROM condition\_occurrence

JOIN concept ON concept\_id = condition\_type\_concept\_id

GROUP BY concept\_name, condition\_type\_concept\_id;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_occurrence\_type | Name of the condition occurrence type |
| condition\_type\_concept\_id | Concept identifier for condition type |
| occurrence\_types\_count | Number of occurrence types |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_occurrence\_type |  EHR Chief Complaint |
| condition\_type\_concept\_id |  42894222 |
| occurrence\_types\_count |  65445068 |
**CO**** 23 ****:** Distribution of condition occurrence month/year, stratified by condition.

This query is used to summary statistics of the condition month/year start dates across all condition occurrence records, stratified by condition (condition\_concept\_id).  The input to the query is a value  of a condition\_concept\_id.

**Sample query:**

SELECT        condition\_concept\_id,

                concept\_name,

                condition\_month\_year,

                count(\*) AS count\_occur

FROM

        (

        SELECT        condition\_concept\_id,

                        concept\_name,

                        to\_char(date\_trunc('month',condition\_start\_date),'MM-YYYY') AS condition\_month\_year,

                        date\_trunc('month',condition\_start\_date) AS m1

                FROM        condition\_occurrence, concept

                WHERE        condition\_occurrence.condition\_concept\_id        = concept.concept\_id

                AND                condition\_concept\_id                                                = 192279

        ) AS        m1

GROUP BY        condition\_concept\_id,

                        concept\_name,

                        condition\_month\_year,

                        m1

ORDER BY        m1





**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 192279 | Yes | Condition concept identifier for 'Diabetic Nephropathy' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | Concept identifier for condition |
| condition\_name | Meaningful and descriptive name for the concept. |
| condition\_month\_year | The month/year when the instance of the condition is recorded. |
| occurrences\_count |  Number of condition occurrences |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |  192279 |
| condition\_name |  Diabetic nephropathy |
| condition\_month\_year |  05-2004 |
| occurrences\_count |  348 |
**CO24:** Counts of genders, stratified by condition

This query is used to count all genders (gender\_concept\_id), stratified by condition (condition\_concept\_id). All existing value combinations are summarized. Since some of the conditions have values only for one of the genders, in order not to present the concept id and name twice, a CASE clause is used.

**Sample query:**

SELECT  ( CASE WHEN (male\_id<> null)

            THEN (male\_id)

            ELSE (female\_id) END) as concept\_id,

        ( CASE WHEN (male\_concept\_name<> null)

                        THEN (male\_concept\_name)

                        ELSE (female\_concept\_name) END) AS name

                        , count\_male,

                        count\_female FROM (

SELECT    male\_list.condition\_concept\_id male\_id,

          male\_list.concept\_name male\_concept\_name,

                       male\_list.count\_male count\_male ,

                       female\_list.condition\_concept\_id female\_id,

                       female\_list.concept\_name female\_concept\_name,

                       female\_list.count\_female count\_female FROM (

SELECT    condition\_concept\_id,

          concept\_name,

          count(\*) AS count\_male

FROM      condition\_occurrence, concept

WHERE     condition\_occurrence.condition\_concept\_id=concept.concept\_id

          AND person\_id IN (SELECT person\_id

                           FROM   person

                           WHERE  gender\_concept\_id=8507)

GROUP BY  condition\_concept\_id, concept\_name) male\_list

FULL JOIN (

SELECT    condition\_concept\_id,

          concept\_name,

          count(\*) AS count\_female

FROM      condition\_occurrence, concept

WHERE     condition\_occurrence.condition\_concept\_id=concept.concept\_id and

          person\_id in

          (SELECT person\_id

FROM      person

WHERE     gender\_concept\_id =8532)

GROUP BY  condition\_concept\_id, concept\_name) as female\_list

          on male\_list.condition\_concept\_id=female\_list.condition\_concept\_id)

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| concept\_id | Condition concept identifier |
| name | Concept name |
| count\_male | Number of concepts for male patients |
| count\_female | Number of concepts for female patients |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| concept\_id |  26711 |
| name |  Chronic pharyngitis |
| count\_male |  6234 |
|  count\_female |  11598 |
**CO25:** Counts of condition records per person, stratified by condition.

Count number of condition per person stratified by condition.

**Sample query:**

SELECT condition\_concept\_id, num\_of\_occurrences, count(\*) num\_of\_patients

FROM (

SELECT condition\_concept\_id, person\_id, count(\*) num\_of\_occurrences

FROM condition\_occurrence co

WHERE co.condition\_concept\_id = 200219

GROUP BY person\_id, condition\_concept\_id)

GROUP BY condition\_concept\_id, num\_of\_occurrences;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 200219 | Yes | Condition concept identifier for 'Abdominal pain' |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | Condition concept identifier |
| num\_occurrences | Number of condition occurrences |
| num\_of\_patients | Number of patients with num\_occurrences |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |  200219 |
| num\_occurrences |  10 |
| num\_of\_patients |  3681 |
### CO04:Count In what place of service where condition diagnoses.

### Returns the distribution of the visit place of service where the condition was reported.

\*\*Sample query:\*\*

SELECT concept\\_name AS place\\_of\\_service\\_name, place\\_freq

FROM (

SELECT care\\_site\\_id, count(\\*) AS place\\_freq

FROM (

SELECT care\\_site\\_id

FROM (

SELECT visit\\_occurrence\\_id

FROM condition\\_occurrence

WHERE condition\\_concept\\_id = 31967

AND visit\\_occurrence\\_id

IS NOT NULL) AS from\\_cond

LEFT JOIN (

SELECT visit\\_occurrence\\_id, care\\_site\\_id

FROM visit\\_occurrence) AS from\\_visit ON from\\_cond.visit\\_occurrence\\_id=from\\_visit.visit\\_occurrence\\_id )

GROUP BY care\\_site\\_id

ORDER BY place\\_freq ) AS place\\_id\\_count

LEFT JOIN (

SELECT concept\\_id, concept\\_name

FROM concept) AS place\\_concept ON place\\_id\\_count.care\\_site\\_id=place\\_concept.concept\\_id

ORDER BY place\\_freq;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept ID for 'Nausea' |





\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| place\\_of\\_service\\_name | The place of service where the condition was reported. |

| place\\_freq | Frequency of the place of service. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| place\\_of\\_service\\_name | Emergency Room |

| place\\_freq | 35343 |

\*\*CO05\*\*\*\* :\*\*Breakout of condition by gender, age

Returns the distribution of condition breakouts per gender and age.

\*\*Sample query:\*\*

SELECT

  concept\\_name AS gender,

  age,

  gender\\_age\\_freq

FROM (

  SELECT

    gender\\_concept\\_id,

    age,

    COUNT(1) gender\\_age\\_freq

  FROM (

    SELECT

      year\\_of\\_birth,

      month\\_of\\_birth,

      day\\_of\\_birth,

      gender\\_concept\\_id,

      condition\\_start\\_date,

      DATEDIFF(years, CONVERT(DateTime, year\\_of\\_birth||'-01-01'), condition\\_start\\_date) AS age

    FROM (

      SELECT

        person\\_id,

        condition\\_start\\_date

      FROM condition\\_occurrence

      WHERE

        condition\\_concept\\_id = 31967 AND

        person\\_id IS NOT NULL

    ) AS from\\_cond

    LEFT JOIN person as from\\_person ON from\\_cond.person\\_id=from\\_person.person\\_id ) AS gender\\_count

  GROUP BY

    gender\\_concept\\_id,

    age

  ORDER BY gender\\_age\\_freq

) AS gender\\_id\\_age\\_count

LEFT JOIN concept as concept\\_list ON gender\\_id\\_age\\_count.gender\\_concept\\_id=concept\\_list.concept\\_id

ORDER BY gender\\_age\\_freq DESC;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept ID for 'Nausea' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| gender | A person's gender |

| age | A person's age in years |

| gender\\_age\\_freq | The frequency of a condition breakout for person gender at a certain age. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| gender | Female |

| age | 50 |

| gender\\_age\\_freq | 3136 |

### CO06:What are a person's comorbidities.

### Returns all coexisting conditions for a given person as defined in the condition\\_era table.

\*\*Sample query:\*\*

SELECT DISTINCT

  CASE WHEN concept\\_name\\_1>concept\\_name\\_2 THEN concept\\_name\\_1 ELSE concept\\_name\\_2 END as condition1,

  CASE WHEN concept\\_name\\_1>concept\\_name\\_2 THEN concept\\_name\\_2 ELSE concept\\_name\\_1 END AS condition2

FROM (

  SELECT

    concept\\_name\\_1,

    concept\\_name AS concept\\_name\\_2

  FROM (

    SELECT

      condition\\_concept\\_id\\_2,

      concept\\_name AS concept\\_name\\_1

    FROM (

      SELECT

        table1.condition\\_concept\\_id AS condition\\_concept\\_id\\_1,

        table2.condition\\_concept\\_id AS condition\\_concept\\_id\\_2

      FROM

        (SELECT \\* FROM condition\\_era WHERE person\\_id = 136931019) AS table1,

        (SELECT \\* FROM condition\\_era WHERE person\\_id = 136931019) AS table2

      WHERE

        table2.condition\\_era\\_start\\_date <= table1.condition\\_era\\_end\\_date AND

        (table2.condition\\_era\\_end\\_date IS NULL OR table2.condition\\_era\\_end\\_date >= table1.condition\\_era\\_start\\_date) AND

        table1.condition\\_concept\\_id<>table2.condition\\_concept\\_id

    ) AS comorb

    LEFT JOIN concept AS concept\\_list ON comorb.condition\\_concept\\_id\\_1=concept\\_list.concept\\_id

  ) AS comorb2

  LEFT JOIN concept AS concept\\_list ON comorb2.condition\\_concept\\_id\\_2=concept\\_list.concept\\_id

) AS condition\\_pairs;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| person\\_id | 136931019 | Yes | Randomly picked person identifier |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Condition 1 | Name of one condition in the comorbidity. |

| Condition 2 | Name of the other condition in the comorbidity. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Condition 1 | Hyperlipidemia |

| Condition 2 | Abnormal breathing |

\*\*CO07\*\*\*\* :\*\*Frequency of hospitalized for a condition

Returns the distribution of number of times a person has been hospitalized where a certain condition was reported.

\*\*Sample query:\*\*

SELECT

  number\\_of\\_hospitlizations,

  count(\\*) AS persons\\_freq

FROM (

  SELECT

    person\\_id,

    COUNT(\\*) AS number\\_of\\_hospitlizations

  FROM (

    SELECT distinct

      condition\\_era\\_id,

      era.person\\_id

    FROM (

      SELECT

        condition\\_start\\_date,

        condition\\_end\\_date,

        from\\_cond.person\\_id

      FROM (

        SELECT

          visit\\_occurrence\\_id,

          condition\\_start\\_date,

          condition\\_end\\_date,

          person\\_id

        FROM condition\\_occurrence

        WHERE

          condition\\_concept\\_id=31967 AND

          visit\\_occurrence\\_id IS NOT NULL

      ) AS FROM\\_cond

      JOIN visit\\_occurrence AS FROM\\_visit

        ON FROM\\_cond.visit\\_occurrence\\_id=FROM\\_visit.visit\\_occurrence\\_id

      JOIN care\\_site cs on from\\_visit.care\\_site\\_id=cs.care\\_site\\_id

         where place\\_of\\_service\\_concept\\_id=8717

    ) AS occurr,

    (

      SELECT

        condition\\_era\\_id,

        person\\_id,

        condition\\_era\\_start\\_date,

        condition\\_era\\_end\\_date

      FROM condition\\_era

      WHERE condition\\_concept\\_id=31967

    ) AS era

    WHERE

      era.person\\_id=occurr.person\\_id AND

      era.condition\\_era\\_start\\_date <= occurr.condition\\_end\\_date AND

      (era.condition\\_era\\_end\\_date IS NULL OR era.condition\\_era\\_end\\_date >= occurr.condition\\_start\\_date)

  )

  GROUP BY person\\_id

  ORDER BY number\\_of\\_hospitlizations desc

)

GROUP BY number\\_of\\_hospitlizations

ORDER BY persons\\_freq desc

;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| number\\_of\\_hospitlizations | Number of times a person was reported to be hospitalized with a certain condition. |

| persons\\_freq | Number of persons which were reported to have a certain number of hospilizations with a certain condition. |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| number\\_of\\_hospitlizations | 2 |

| persons\\_freq | 177 |

\*\*CO08\*\*\*\* :\*\*Duration of hospitalization for a conditions

Returns the the average length in days of all hospitalizations where a certain condition was reported

\*\*Sample query:\*\*

SELECT

  avg(hosp\\_no\\_days) AS average\\_hosp\\_duration\\_count

FROM (

  SELECT DISTINCT

    hosp\\_no\\_days,

    person\\_id,

    from\\_visit.visit\\_occurrence\\_id

  FROM (

    SELECT

      visit\\_occurrence\\_id, condition\\_start\\_date, condition\\_end\\_date, person\\_id

    FROM condition\\_occurrence

    WHERE

      condition\\_concept\\_id = 31967 AND

      visit\\_occurrence\\_id IS NOT NULL

  ) AS from\\_cond

  JOIN (

    SELECT

      DATEDIFF(DAY, visit\\_start\\_date, visit\\_end\\_date) + 1 AS hosp\\_no\\_days,

      visit\\_start\\_date,

      visit\\_occurrence\\_id,

      place\\_of\\_service\\_concept\\_id

    FROM visit\\_occurrence v

    JOIN care\\_site c on v.care\\_site\\_id=c.care\\_site\\_id

    WHERE place\\_of\\_service\\_concept\\_id = 8717

  ) AS from\\_visit

    ON from\\_cond.visit\\_occurrence\\_id = from\\_visit.visit\\_occurrence\\_id );



\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| average\\_hosp\\_duration\\_count | Average length in days of all hospitalization where a certain condition was reported. +1 was added for partial days (e.g. 1.5 days were counted as 2 days). |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| average\\_hosp\\_duration\\_count | 7 |

\*\*CO09\*\*\*\* :\*\*Is a condition seasonal, alergies for example

Returns the distribution of condition occurrence per season in the northern hemisphere, defined in the following way:

|  Spring |  March 21 - June 21 |

| --- | --- |

|  Summer |  June 22 - September 22 |

|  Fall |  September 23 - December 21 |

|  Winter |  December 22 - March 20 |

\*\*Sample query:\*\*

SELECT season, COUNT(\\*) as season\\_freq

FROM (

SELECT CASE

WHEN (daymonth>0320

AND daymonth<=0621) THEN 'Spring' WHEN (daymonth>0621

AND daymonth<=0922) THEN 'Summer' WHEN (daymonth>0922

AND daymonth<=1221) THEN 'Fall' WHEN (daymonth>1221

OR (daymonth>0000

AND daymonth<=0520)) THEN 'Winter' ELSE 'Unknown' end AS season

FROM (

SELECT cast(substring(condition\\_start\\_date

from 6 for 2)|| substring(condition\\_start\\_date

from 9 for 2) as int) AS daymonth,condition\\_start\\_date

FROM condition\\_occurrence

WHERE condition\\_concept\\_id = 31967 ) ) AS condition\\_season

GROUP BY season

ORDER BY season\\_freq;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |





\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| season | Season as defined in the northern hemisphere. |

| season\\_freq | Frequency of condition occurrence in the season. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| season | Summer |

| season\\_freq | 62924 |

\*\*CO12\*\* : Distribution of condition end dates.

This query is used to to provide summary statistics for condition occurrence end dates (condition\\_occurrence\\_end\\_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

with end\\_rank as (

  SELECT

    condition\\_end\\_date-'0001-01-01' as num\\_end\\_date,

    condition\\_end\\_date,

    sum(1) over (partition by 1 order by condition\\_end\\_date asc rows between unbounded preceding and current row) as rownumasc

  FROM

    condition\\_occurrence

),

other\\_stat as (

  SELECT

    count(condition\\_end\\_date) as condition\\_end\\_date\\_count,

    min(condition\\_end\\_date) as condition\\_end\\_date\\_min,

    max(condition\\_end\\_date) as condition\\_end\\_date\\_max,

    to\\_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition\\_end\\_date-'0001-01-01') as int) as condition\\_end\\_date\\_average,

    stddev((condition\\_end\\_date-'0001-01-01')) as condition\\_end\\_date\\_stddev

  FROM

    condition\\_occurrence

  WHERE

    condition\\_end\\_date is not null

)

SELECT

  (SELECT count(condition\\_end\\_date) FROM condition\\_occurrence WHERE condition\\_end\\_date is null) AS condition\\_end\\_date\\_null\\_count,

  \\*

FROM

  other\\_stat,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_end\\_date-'0001-01-01') as int) AS condition\\_end\\_date\\_25percentile

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)=0) or

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)>0) or

      (rownumasc=cast (rowno\\*0.25 as int)+1 and mod(rowno\\*25,100)>0)

  ) AS condition\\_end\\_date\\_25percentile,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_end\\_date-'0001-01-01') as int) as condition\\_end\\_date\\_median

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)=0) or

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)>0) or

      (rownumasc=cast (rowno\\*0.50 as int)+1 and mod(rowno\\*50,100)>0)

  ) AS condition\\_end\\_date\\_median,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_end\\_date-'0001-01-01') as int) as condition\\_end\\_date\\_75percentile

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)=0) or

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)>0) or

      (rownumasc=cast (rowno\\*0.75 as int)+1 and mod(rowno\\*75,100)>0)

  ) AS condition\\_end\\_date\\_75percentile;

\*\*Input:\*\*

None



\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_end\\_date\\_null\\_count | Number of condition occurrences where end date is null |

| condition\\_end\\_date\\_count | Number of condition occurrence end dates |

| condition\\_end\\_date\\_min | The earliest end date of a condition occurrence |

| condition\\_end\\_date\\_max | The latest end date of a condition occurrence |

| condition\\_end\\_date\\_average | The average end date (spanning from the earliest to the latest date and counted by days) |

| condition\\_end\\_date\\_stddev | The standard deviation of end dates, in number of days (spanning from the earliest to the latest date and counted by days) |

| condition\\_end\\_date\\_25percentile |  An end date where 25 percent of the other end dates are earlier |

| condition\\_end\\_date\\_median |  An end date where half of the other end dates are earlier and half are later |

| condition\\_end\\_date\\_75percentile |  An end date where 75 percent of the other end dates are earlier |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| condition\\_end\\_date\\_null\\_count | 0 |

| condition\\_end\\_date\\_count | 224523674 |

| condition\\_end\\_date\\_min | 2003-01-01 |

| condition\\_end\\_date\\_max | 011-12-15 |

| condition\\_end\\_date\\_average | 2008-11-30 |

| condition\\_end\\_date\\_stddev | 651.19 |

| condition\\_end\\_date\\_25percentile | 2007-10-30 |

| condition\\_end\\_date\\_median | 2009-05-07 |

| condition\\_end\\_date\\_75percentile | 2010-05-04 |

\*\*CO13:\*\* Distribution of condition start dates

This query is used to to provide summary statistics for condition occurrence start dates (condition\\_occurrence\\_start\\_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

with end\\_rank as (

  SELECT

    condition\\_start\\_date-'0001-01-01' as num\\_start\\_date,

    condition\\_start\\_date,

    sum(1) over (partition by 1 order by condition\\_start\\_date asc rows between unbounded preceding and current row) as rownumasc

  FROM

    condition\\_occurrence

),

other\\_stat as (

  SELECT

    count(condition\\_start\\_date) as condition\\_start\\_date\\_count,

    min(condition\\_start\\_date) as condition\\_start\\_date\\_min,

    max(condition\\_start\\_date) as condition\\_start\\_date\\_max,

    to\\_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition\\_start\\_date-'0001-01-01') as int) as condition\\_start\\_date\\_average,

    stddev((condition\\_start\\_date-'0001-01-01')) as condition\\_start\\_date\\_stddev

  FROM

    condition\\_occurrence

  WHERE

    condition\\_start\\_date is not null

)

SELECT

  (SELECT count(condition\\_start\\_date) FROM condition\\_occurrence WHERE condition\\_start\\_date is null) AS condition\\_start\\_date\\_null\\_count,

  \\*

FROM

  other\\_stat,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_start\\_date-'0001-01-01') as int) AS condition\\_start\\_date\\_25percentile

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)=0) or

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)>0) or

      (rownumasc=cast (rowno\\*0.25 as int)+1 and mod(rowno\\*25,100)>0)

  ) AS condition\\_start\\_date\\_25percentile,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_start\\_date-'0001-01-01') as int) as condition\\_start\\_date\\_median

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)=0) or

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)>0) or

      (rownumasc=cast (rowno\\*0.50 as int)+1 and mod(rowno\\*50,100)>0)

  ) AS condition\\_start\\_date\\_median,

  ( SELECT

      to\\_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition\\_start\\_date-'0001-01-01') as int) as condition\\_start\\_date\\_75percentile

    FROM

      (select \\*,(select count(\\*) from end\\_rank) as rowno from end\\_rank)

    WHERE

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)=0) or

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)>0) or

      (rownumasc=cast (rowno\\*0.75 as int)+1 and mod(rowno\\*75,100)>0)

  ) AS condition\\_start\\_date\\_75percentile;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_start\\_date\\_null\\_count | Number of condition occurrences where start date is null |

| condition\\_start\\_date\\_count | Number of condition occurrence start dates |

| condition\\_start\\_date\\_min | The earliest start date of a condition occurrence |

| condition\\_start\\_date\\_max | The latest start date of a condition occurrence |

| condition\\_start\\_date\\_average | The average start date (spanning from the earliest to the latest date and counted by days) |

| condition\\_start\\_date\\_stddev | The standard deviation of start dates, in number of days (spanning from the earliest to the latest date and counted by days) |

| condition\\_start\\_date\\_25percentile | A start date where 25 percent of the other end dates are earlier |

| condition\\_start\\_date\\_median | A start date where half of the other end dates are earlier and half are later |

| condition\\_start\\_date\\_75percentile | A start date where 75 percent of the other end dates are earlier |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| condition\\_end\\_date\\_null\\_count | 0 |

| condition\\_end\\_date\\_count | 224523674 |

| condition\\_end\\_date\\_min | 2003-01-01 |

| condition\\_end\\_date\\_max | 2011-11-08 |

| condition\\_end\\_date\\_average | 2008-11-30 |

| condition\\_end\\_date\\_stddev | 651.27 |

| condition\\_end\\_date\\_25percentile | 2007-10-30 |

| condition\\_end\\_date\\_median | 2009-05-06 |

| condition\\_end\\_date\\_75percentile | 2010-05-03 |

\*\*CO14:\*\* Counts of condition types

This query is used to count the condition type concepts (condition\\_type\\_concept\\_id, in the CDM V2 condition\\_occurrence\\_type) across all condition occurrence records. The input to the query is a value of a condition\\_type\\_concept\\_id.

\*\*Sample query:\*\*

SELECT condition\\_type\\_freq, condition\\_type\\_concept\\_id, concept\\_name

FROM (

SELECT condition\\_type\\_concept\\_id, count(\\*) as condition\\_type\\_freq

FROM (

SELECT \\*

from condition\\_occurrence)

WHERE condition\\_concept\\_id = 31967

GROUP BY condition\\_type\\_concept\\_id) AS condition\\_type\\_count

LEFT JOIN (

SELECT concept\\_id, concept\\_name

FROM concept) AS type\\_concept ON condition\\_type\\_count.condition\\_type\\_concept\\_id=type\\_concept.concept\\_id

ORDER BY condition\\_type\\_freq;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_type\\_freq | Frequency of a specific condition\\_type |

| condition\\_type\\_concept\\_id | Unique ID for condition\\_type |

| concept\\_name |  Description of the condition's data source |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_type\\_freq | 4735 |

| condition\\_type\\_concept\\_id | 38000235 |

| concept\\_name | Outpatient header - 6th position |

\*\*CO15:\*\* Distribution of number of distinct conditions persons have

This query is used to provide summary statistics for the number of different distinct conditions (condition\\_concept\\_id) of all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

with ranked as (

  SELECT

    num\\_of\\_conditions,

    row\\_number() over (order by num\\_of\\_conditions asc) AS rownumasc

  FROM(

    select

      person\\_id,

      count(distinct condition\\_concept\\_id) AS num\\_of\\_conditions

    FROM condition\\_occurrence

    where person\\_id!=0

    GROUP BY person\\_id

  )

),

other\\_stat AS (

  SELECT

    count(num\\_of\\_conditions) as condition\\_dist\\_num\\_count,

    min(num\\_of\\_conditions) as condition\\_dist\\_num\\_min,

    max(num\\_of\\_conditions) as condition\\_dist\\_num\\_max,

    avg(num\\_of\\_conditions) as condition\\_dist\\_num\\_averege,

    stddev(num\\_of\\_conditions) as condition\\_dist\\_num\\_stddev

  FROM (

    SELECT

      count(distinct condition\\_concept\\_id) AS num\\_of\\_conditions,

      person\\_id

    FROM condition\\_occurrence

    WHERE person\\_id!=0

    GROUP BY person\\_id

  )

)

SELECT

  (SELECT count(distinct person\\_id) FROM condition\\_occurrence WHERE person\\_id!=0 and condition\\_occurrence\\_id is null) AS condition\\_null\\_count,

  \\*

FROM

  other\\_stat,

  ( SELECT distinct

      num\\_of\\_conditions as condition\\_dist\\_num\\_25percentile

    FROM

      (select \\*,(select count(\\*) from ranked) as rowno from ranked)

    WHERE

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)=0) or

      (rownumasc=cast (rowno\\*0.25 as int) and mod(rowno\\*25,100)>0) or

      (rownumasc=cast (rowno\\*0.25 as int)+1 and mod(rowno\\*25,100)>0)

  ) AS condition\\_end\\_date\\_25percentile,

  ( SELECT distinct

      num\\_of\\_conditions as condition\\_dist\\_num\\_median

    FROM

      (select \\*,(select count(\\*) from ranked) as rowno from ranked)

    WHERE

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)=0) or

      (rownumasc=cast (rowno\\*0.50 as int) and mod(rowno\\*50,100)>0) or

      (rownumasc=cast (rowno\\*0.50 as int)+1 and mod(rowno\\*50,100)>0)

  ) AS condition\\_end\\_date\\_median,

  ( SELECT distinct

      num\\_of\\_conditions as condition\\_dist\\_num\\_75percentile

    FROM

      (select \\*,(select count(\\*) from ranked) as rowno from ranked)

    WHERE

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)=0) or

      (rownumasc=cast (rowno\\*0.75 as int) and mod(rowno\\*75,100)>0) or

      (rownumasc=cast (rowno\\*0.75 as int)+1 and mod(rowno\\*75,100)>0)

  ) AS condition\\_end\\_date\\_75percentile;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_null\\_count | Number of condition occurrences where condition\\_occurrence\\_id is null |

| condition\\_count | Number of condition occurrences |

| condition\\_dist\\_num\\_min | The lowest number of distinct condition occurrences |

| condition\\_dist\\_num\\_max | The highest number of distinct condition occurrences |

| condition\\_dist\\_num\\_averege | The avarege number of distinct condition occurrences |

| condition\\_dist\\_num\\_stddev | The standard deviation of distinct condition occurence numbers |

| condition\\_dist\\_num\\_25percentile | A distinct condition occurrence number where 25 percent of the other numbers are lower |

| condition\\_dist\\_num\\_median | A distinct condition occurrence number where half of the other numbers are lower and half are higher |

| condition\\_dist\\_num\\_75percentile | A distinct condition occurrence number where 75 percent of the other numbers are lower |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_null\\_count | 0 |

| condition\\_count | 4395019 |

| condition\\_dist\\_num\\_min | 1 |

| condition\\_dist\\_num\\_max | 327 |

| condition\\_dist\\_num\\_averege | 17 |

| condition\\_dist\\_num\\_stddev | 16.94 |

| condition\\_dist\\_num\\_25percentile | 6 |

| condition\\_dist\\_num\\_median | 12 |

| condition\\_dist\\_num\\_75percentile | 23 |

\*\*CO16:\*\* Counts of number of distinct conditions persons have

This query is used to count the number of different distinct conditions (condition\\_concept\\_id) of all persons. The input to the query is a value for a concept identifier.

\*\*Sample query:\*\*

SELECT count(c.condition\\_concept\\_id) conditions\\_count, c.person\\_id

FROM condition\\_occurrence c

WHERE condition\\_concept\\_id = 201820

GROUP BY c.person\\_id

ORDER BY 1

DESC;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 201820 | Yes | Condition concept identifier for 'Diabetes mellitus' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| conditions\\_count | Number of conditions recorded for the person |

| person\\_id | Person identifier |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| conditions\\_count |  39 |

| person\\_id |  20017834818 |

\*\*CO17:\*\* Distribution of condition occurrence records per person

This query is used to provide summary statistics for the number of condition occurrence records (condition\\_occurrence\\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

\*\*Sample query:\*\*

with ranked as

  (

  SELECT num\\_of\\_conditions, sum(1) over (partition by 1

  ORDER BY num\\_of\\_conditions asc rows BETWEEN unbounded preceding AND current row) AS rownumasc

  FROM (

                                        SELECT count(\\*) as num\\_of\\_conditions

                                        FROM condition\\_occurrence

                                        WHERE person\\_id!=0

                                        GROUP BY person\\_id

                                )

  ),

  other\\_stat AS

  (

   SELECT count(num\\_of\\_conditions) AS condition\\_num\\_count,

                        min(num\\_of\\_conditions) AS condition\\_num\\_min,

      max(num\\_of\\_conditions) AS condition\\_num\\_max,

                        avg(num\\_of\\_conditions) AS condition\\_num\\_averege,

      stddev(num\\_of\\_conditions) as condition\\_num\\_stddev

   FROM (

                                   SELECT count(\\*) AS num\\_of\\_conditions, person\\_id

                                   FROM   condition\\_occurrence

                                   WHERE person\\_id!=0

                                   GROUP BY person\\_id

                           )

  )

SELECT

 (

        SELECT count(distinct person\\_id)

        FROM condition\\_occurrence

        WHERE person\\_id!=0 AND condition\\_occurrence\\_id IS NULL

 ) AS condition\\_null\\_count,

 \\* FROM other\\_stat,

 (

  SELECT num\\_of\\_conditions AS condition\\_num\\_25percentile

  FROM (SELECT \\*,(SELECT count(\\*) FROM ranked) as rowno FROM ranked)

  WHERE (rownumasc=cast (rowno\\*0.25 as int) AND mod(rowno\\*25,100)=0) OR

     (rownumasc=cast (rowno\\*0.25 as int) AND mod(rowno\\*25,100)>0) OR

     (rownumasc=cast (rowno\\*0.25 as int)+1 AND mod(rowno\\*25,100)>0)

 ) AS condition\\_num\\_25percentile,

 (

  SELECT num\\_of\\_conditions AS condition\\_num\\_median

  FROM (SELECT \\*,(SELECT count(\\*) FROM ranked) AS rowno FROM ranked)

  WHERE (rownumasc=cast (rowno\\*0.50 AS int) AND mod(rowno\\*50,100)=0) OR

     (rownumasc=cast (rowno\\*0.50 AS int) AND mod(rowno\\*50,100)>0) OR

     (rownumasc=cast (rowno\\*0.50 AS int)+1 AND mod(rowno\\*50,100)>0)

 ) AS condition\\_num\\_median,

 (

  SELECT num\\_of\\_conditions AS condition\\_num\\_75percentile

  FROM (SELECT \\*,(SELECT count(\\*) FROM ranked) as rowno FROM ranked)

  WHERE (rownumasc=cast (rowno\\*0.75 as int) AND mod(rowno\\*75,100)=0) OR

     (rownumasc=cast (rowno\\*0.75 as int) AND mod(rowno\\*75,100)>0) OR

     (rownumasc=cast (rowno\\*0.75 as int)+1 AND mod(rowno\\*75,100)>0)

 ) AS condition\\_num\\_75percentile

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_null\\_count | Number of persons with at least one null condition\\_occurrence\\_id |

| condition\\_num\\_count | Number of distinct persons with conditions |

| condition\\_num\\_min | The lowest number of condition occurences |

| condition\\_num\\_max | The highest number of condition occurences |

| condition\\_num\\_averege | The average number of condition occurences |

| condition\\_num\\_stddev | The standard deviation of condition occurence numbers |

| condition\\_num\\_25percentile | A condition occurence number where 25 percent of the other numbers are lower |

| condition\\_num\\_median | A condition occurence number where half of the other numbers are lower and half are higher |

| condition\\_num\\_75percentile | A condition occurence number where 75 percent of the other numbers are lower |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_null\\_count | 4395019 |

| condition\\_num\\_count |   |

| condition\\_num\\_min | 1 |

| condition\\_num\\_max | 7144 |

| condition\\_num\\_averege | 51 |

| condition\\_num\\_stddev | 86.63 |

| condition\\_num\\_25percentile | 11 |

| condition\\_num\\_median | 26 |

| condition\\_num\\_75percentile | 58 |

\*\*CO19\*\*\*\* :\*\*Counts of condition occurrence records stratified by observation month

This query is used to count the condition occurrence records stratified by observation month.

\*\*Sample query:\*\*

SELECT extract(month

from condition\\_start\\_date) month\\_number, count(\\*) as number\\_of\\_conditions\\_in\\_month

FROM condition\\_occurrence

GROUP BY extract(month

from condition\\_start\\_date)

ORDER BY 1;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| Month\\_number | Month number |

| Number\\_of\\_conditions\\_in\\_month |  The number of the condition occurrences is a specified month. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Month\\_number |  3 |

| Number\\_of\\_conditions\\_in\\_month |  20643257 |

\*\*CO21:\*\* Distribution of age, stratified by condition

This query is used to provide summary statistics for the age across all condition occurrence records stratified by condition (condition\\_concept\\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest condition occurrence. The input to the query is a value (or a comma-separated list of values) of a condition\\_concept\\_id.

Oracle specific query.

\*\*Sample query:\*\*

SELECT concept\\_name AS condition

     , condition\\_concept\\_id

     , count(\\*) AS condition\\_occurrences

     , min( age ) over () AS min\\_age

     , max( age ) over () AS max\\_age

     , round( avg( age ), 2 ) AS avg\\_age

     , round( stdDev( age ) over (), 1 ) AS stdDev\\_age

     , PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY age ) over ()

                                     AS percentile\\_25

     , PERCENTILE\\_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over ()

                                     AS median\\_age

     , PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY age ) over ()

                                     AS percentile\\_75

  FROM -- condition occurrences with age at time of condition

     ( SELECT condition\\_concept\\_id

            , EXTRACT( YEAR from condition\\_start\\_date ) AS age -- year\\_of\\_birth

         FROM condition\\_occurrence

         JOIN person USING( person\\_id )

        WHERE condition\\_concept\\_id

           IN -- all SNOMED codes for diabetes

            ( 192691, 193323, 194700, 195771, 200687, 201254,

         201530, 201531, 201820, 201826 , 318712, 373999,

         377821, 4008576, 4009780, 4024659, 4030061,

         4034960, 4034962, 4047906 , 40480000, 4048202,

         40482883, 40488810, 4058243, 4062685, 4062686,

         4062687, 4063042, 4063043 , 4079850, 4096041,

         4096042, 4096668, 4096670, 4096671, 4099214,

         4099215, 4099217, 4099334 , 4099651, 4099652,

         4099653, 4099741, 4102018, 4129378, 4129516,

         4129519, 4130162, 4130164 , 4130166, 4136889,

         4137214, 4140808, 4143529, 4143689, 4143857,

         4144583, 4145827, 4151281 , 4151282, 4152858,

         4155634, 4166381, 4178452, 4178790, 4192852,

         4193704, 4196141, 4198296 , 4200873, 4200875,

         4202383, 4212631, 4221344, 4222222, 4222410,

         4222547, 4222553, 4222687 , 4222834, 4223303,

         4223444, 4224254, 4224709, 4224723, 4225013,

         4225055, 4225656, 4226245 , 4227210, 4228102,

         4228112, 4230254, 4231917, 4235410, 4237068,

         4240589, 4245270, 4252384, 4263902, 4295011,

         4304377, 4312138, 4321756, 4322638, 4325113,

         4326434, 4327944, 435216 , 439770, 443012,

         443412, 443592

            )

     )

  JOIN concept ON concept\\_id = condition\\_concept\\_id

GROUP BY concept\\_name, condition\\_concept\\_id, age

ORDER BY condition\\_occurrences DESC

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id list | 192691, 193323, 194700, 195771, 200687, 201254, 201530, 201531, 201820, 201826 , 318712, 373999, 377821, 4008576, 4009780, 4024659, 4030061, 4034960, 4034962, 4047906 , 40480000, 4048202, 40482883, 40488810, 4058243, 4062685, 4062686, 4062687, 4063042, 4063043 , 4079850, 4096041, 4096042, 4096668, 4096670, 4096671, 4099214, 4099215, 4099217, 4099334 , 4099651, 4099652, 4099653, 4099741, 4102018, 4129378, 4129516, 4129519, 4130162, 4130164 , 4130166, 4136889, 4137214, 4140808, 4143529, 4143689, 4143857, 4144583, 4145827, 4151281 , 4151282, 4152858, 4155634, 4166381, 4178452, 4178790, 4192852, 4193704, 4196141, 4198296 , 4200873, 4200875, 4202383, 4212631, 4221344, 4222222, 4222410, 4222547, 4222553, 4222687 , 4222834, 4223303, 4223444, 4224254, 4224709, 4224723, 4225013, 4225055, 4225656, 4226245 , 4227210, 4228102, 4228112, 4230254, 4231917, 4235410, 4237068, 4240589, 4245270, 4252384, 4263902, 4295011, 4304377, 4312138, 4321756, 4322638, 4325113, 4326434, 4327944, 435216 , 439770, 443012, 443412, 443592 | Yes | SNOMED condition concept identifiers for dia |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition | Name of the condition |

| condition\\_concept\\_id | Condition concept identifier |

| min\\_age | Minimum age of the people with condition |

| max\\_age | Maximum age of the people with condition |

| avg\\_age | Average age of the people with condition |

| stdDev\\_age | Standard deviation of the people  with condition |

| percentile\\_25 | Age 25th percentile of the people with condition |

| median\\_age | Median age  of the people with condition |

| percentile\\_75 | Age 75th percentile of the people with condition |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition | Type 1 diabetes mellitus |

| condition\\_concept\\_id | 201826 |

| min\\_age | 2006 |

| max\\_age | 2017 |

| avg\\_age | 2014 |

| stdDev\\_age | 3.6 |

| percentile\\_25 | 2009 |

| median\\_age | 2013 |

| percentile\\_75 | 2015 |

\*\*CO22:\*\* Counts of conditions, stratified by condition type

This query is used to count conditions across all condition occurrence records stratified by condition occurrence type

\*\*Sample query:\*\*

SELECT concept\\_name AS condition\\_occurrence\\_type , condition\\_type\\_concept\\_id , count(\\*) AS occurrence\\_type\\_count

FROM condition\\_occurrence

JOIN concept ON concept\\_id = condition\\_type\\_concept\\_id

GROUP BY concept\\_name, condition\\_type\\_concept\\_id;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_occurrence\\_type | Name of the condition occurrence type |

| condition\\_type\\_concept\\_id | Concept identifier for condition type |

| occurrence\\_types\\_count | Number of occurrence types |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_occurrence\\_type |  EHR Chief Complaint |

| condition\\_type\\_concept\\_id |  42894222 |

| occurrence\\_types\\_count |  65445068 |

\*\*CO\*\*\*\* 23 \*\*\*\*:\*\* Distribution of condition occurrence month/year, stratified by condition.

This query is used to summary statistics of the condition month/year start dates across all condition occurrence records, stratified by condition (condition\\_concept\\_id).  The input to the query is a value  of a condition\\_concept\\_id.

\*\*Sample query:\*\*

SELECT        condition\\_concept\\_id,

                concept\\_name,

                condition\\_month\\_year,

                count(\\*) AS count\\_occur

FROM

        (

        SELECT        condition\\_concept\\_id,

                        concept\\_name,

                        to\\_char(date\\_trunc('month',condition\\_start\\_date),'MM-YYYY') AS condition\\_month\\_year,

                        date\\_trunc('month',condition\\_start\\_date) AS m1

                FROM        condition\\_occurrence, concept

                WHERE        condition\\_occurrence.condition\\_concept\\_id        = concept.concept\\_id

                AND                condition\\_concept\\_id                                                = 192279

        ) AS        m1

GROUP BY        condition\\_concept\\_id,

                        concept\\_name,

                        condition\\_month\\_year,

                        m1

ORDER BY        m1





\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 192279 | Yes | Condition concept identifier for 'Diabetic Nephropathy' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_concept\\_id | Concept identifier for condition |

| condition\\_name | Meaningful and descriptive name for the concept. |

| condition\\_month\\_year | The month/year when the instance of the condition is recorded. |

| occurrences\\_count |  Number of condition occurrences |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_concept\\_id |  192279 |

| condition\\_name |  Diabetic nephropathy |

| condition\\_month\\_year |  05-2004 |

| occurrences\\_count |  348 |

\*\*CO24:\*\* Counts of genders, stratified by condition

This query is used to count all genders (gender\\_concept\\_id), stratified by condition (condition\\_concept\\_id). All existing value combinations are summarized. Since some of the conditions have values only for one of the genders, in order not to present the concept id and name twice, a CASE clause is used.

\*\*Sample query:\*\*

SELECT  ( CASE WHEN (male\\_id<> null)

            THEN (male\\_id)

            ELSE (female\\_id) END) as concept\\_id,

        ( CASE WHEN (male\\_concept\\_name<> null)

                        THEN (male\\_concept\\_name)

                        ELSE (female\\_concept\\_name) END) AS name

                        , count\\_male,

                        count\\_female FROM (

SELECT    male\\_list.condition\\_concept\\_id male\\_id,

          male\\_list.concept\\_name male\\_concept\\_name,

                       male\\_list.count\\_male count\\_male ,

                       female\\_list.condition\\_concept\\_id female\\_id,

                       female\\_list.concept\\_name female\\_concept\\_name,

                       female\\_list.count\\_female count\\_female FROM (

SELECT    condition\\_concept\\_id,

          concept\\_name,

          count(\\*) AS count\\_male

FROM      condition\\_occurrence, concept

WHERE     condition\\_occurrence.condition\\_concept\\_id=concept.concept\\_id

          AND person\\_id IN (SELECT person\\_id

                           FROM   person

                           WHERE  gender\\_concept\\_id=8507)

GROUP BY  condition\\_concept\\_id, concept\\_name) male\\_list

FULL JOIN (

SELECT    condition\\_concept\\_id,

          concept\\_name,

          count(\\*) AS count\\_female

FROM      condition\\_occurrence, concept

WHERE     condition\\_occurrence.condition\\_concept\\_id=concept.concept\\_id and

          person\\_id in

          (SELECT person\\_id

FROM      person

WHERE     gender\\_concept\\_id =8532)

GROUP BY  condition\\_concept\\_id, concept\\_name) as female\\_list

          on male\\_list.condition\\_concept\\_id=female\\_list.condition\\_concept\\_id)

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_id | Condition concept identifier |

| name | Concept name |

| count\\_male | Number of concepts for male patients |

| count\\_female | Number of concepts for female patients |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_id |  26711 |

| name |  Chronic pharyngitis |

| count\\_male |  6234 |

|  count\\_female |  11598 |

\*\*CO25:\*\* Counts of condition records per person, stratified by condition.

Count number of condition per person stratified by condition.

\*\*Sample query:\*\*

SELECT condition\\_concept\\_id, num\\_of\\_occurrences, count(\\*) num\\_of\\_patients

FROM (

SELECT condition\\_concept\\_id, person\\_id, count(\\*) num\\_of\\_occurrences

FROM condition\\_occurrence co

WHERE co.condition\\_concept\\_id = 200219

GROUP BY person\\_id, condition\\_concept\\_id)

GROUP BY condition\\_concept\\_id, num\\_of\\_occurrences;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 200219 | Yes | Condition concept identifier for 'Abdominal pain' |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_concept\\_id | Condition concept identifier |

| num\\_occurrences | Number of condition occurrences |

| num\\_of\\_patients | Number of patients with num\\_occurrences |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_concept\\_id |  200219 |

| num\\_occurrences |  10 |

| num\\_of\\_patients |  3681 |
