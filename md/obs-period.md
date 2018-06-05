
**OP01:** Count number of people who have at least one observation period in the database that is longer than 365 days.

**Sample query:**

SELECT COUNT(DISTINCT person\_ID) AS NUM\_persons

FROM observation\_period

WHERE observation\_period\_END\_DATE - observation\_period\_START\_DATE >= 365;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Num\_Persons | Number of patients who have at least one observation period in the database that is longer than 365 days |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| Num\_Persons | 105119818 |
OP02 **:** Distribution of length of observation, in months, among first observation periods across the population

Count distribution of length of observation, in months, among first observation periods across the population.

**Sample query:**

SELECT        DATEDIFF(month, observation\_period\_start\_date, observation\_period\_end\_date) as num\_months,

                COUNT(distinct person\_id) AS num\_persons

FROM

        (

        SELECT        person\_ID,

                        observation\_period\_START\_DATE,

                        observation\_period\_END\_DATE,

                        rank() OVER (PARTITION BY person\_ID ORDER BY observation\_period\_START\_DATE ASC) AS OP\_NUMBER

        FROM

                observation\_period

        ) AS OP1

WHERE

        op\_number = 1

GROUP BY        DATEDIFF(month,observation\_period\_START\_DATE, observation\_period\_END\_DATE)

ORDER BY        DATEDIFF(month,observation\_period\_START\_DATE, observation\_period\_END\_DATE) ASC

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| num\_month | Number of month duration |
| num\_persons | Number of patients whose observation period with num\_month duration |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_months |  1 |
| num\_persons | 4132770 |
### OP03:Number of people continuously observed throughout a year.

Count number of people continuously observed throughout a specified year.

**Sample query:**

SELECT COUNT(DISTINCT person\_ID) AS NUM\_persons

FROM observation\_period

WHERE observation\_period\_start\_date <= '01-jan-2011'

AND observation\_period\_end\_date >= '31-dec-2011';

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| num\_persons |  Number of patients whose observation period within range of days |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_persons |  32611748 |
### OP04:Number of people who have gap in observation (two or more observations)

Count number of people who have two or more observations.

**Sample query:**

SELECT count( person\_id ) AS num\_persons

FROM -- more than one observatio period

( SELECT person\_id

FROM observation\_period GROUP BY person\_id

HAVING COUNT( person\_id ) > 1 );

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| num\_persons |  Number of patients who have two or more observations |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_persons |  18650793 |
### OP05: Average length of observation, in month.

Count average length of observation period in month.

**Sample query:**

SELECT avg(

datediff(month, observation\_period\_start\_date , observation\_period\_end\_date ) ) AS num\_months

FROM observation\_period;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| num\_months |  Average length of observation, in month |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_months |  30 |
### OP06: Average length of observation, in days.

### Count average number of observation days.

**Sample query:**

SELECT avg( observation\_period\_end\_date - observation\_period\_start\_date ) AS num\_days

FROM observation\_period;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| num\_days |  Average length of observation, in days |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_days |  966 |
### OP07:Distribution of age across all observation period records

Count distribution of age across all observation period records:  the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

WITH t AS (

SELECT DISTINCT

              person\_id, EXTRACT( YEAR FROM first\_observation\_date ) - year\_of\_birth AS age

         FROM -- person, first observation date

            ( SELECT person\_id

                   , min( observation\_period\_start\_date ) AS first\_observation\_date

                FROM observation\_period

               GROUP BY person\_id

            )

         JOIN person USING( person\_id )

        WHERE year\_of\_birth IS NOT NULL

) SELECT count(\*) AS num\_people

     , min( age ) AS min\_age

     , max( age ) AS max\_age

     , round( avg( age ), 2 ) AS avg\_age

     , round( stdDev( age ), 1 ) AS stdDev\_age

     , (SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY age ) over () FROM t) AS percentile\_25

     , (SELECT DISTINCT PERCENTILE\_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over () FROM t) AS median\_age

     , (SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY age ) over () FROM t) AS percentile\_75

        FROM t;

**Input:**

None



**Output:**

| **Field** | ** Description** |
| --- | --- |
| num\_people | Number of people in a dataset |
| min\_age | Minimum age of person |
| max\_age | Maximum age of a person |
| avg\_age | Average age of people in the dataset |
| stdDev\_age | Standard deviation of person age |
|  percentile\_25 |  25th percentile of of the age group |
|  median\_age |  50th percentile of the age group |
|  percentile\_75 |  75th percentile of the age group |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
| num\_people | 151039265 |
| min\_age |  0 |
| max\_age |  85 |
| avg\_age |  31 |
| stdDev\_age |  19.4 |
| percentile\_25 |  16 |
| median\_age |  31 |
| percentile\_75 |  47 |
### OP08: Distribution of observation period records per person

Counts the number of observation period records (observation\_period\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

**Sample query:**

WITH obser\_person AS

(

        SELECT        person\_id,

                        count(\*) as observation\_periods

        FROM        observation\_period

                                JOIN        person USING( person\_id )

        GROUP BY        person\_id

)

SELECT        min( observation\_periods ) AS min\_periods ,

                max( observation\_periods ) AS max\_periods ,

                round( avg( observation\_periods ), 2 ) AS avg\_periods ,

                round( stdDev( observation\_periods ), 1 ) AS stdDev\_periods ,

                (SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY observation\_periods ) OVER() FROM obser\_person) AS percentile\_25 ,

                (SELECT DISTINCT PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY observation\_periods ) OVER() FROM obser\_person) AS median ,

                (SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY observation\_periods ) OVER() FROM obser\_person) AS percentile\_75

FROM

        obser\_person

**Input:**

None





**Output:**

| **Field** | ** Description** |
| --- | --- |
|  min\_periods |  Minimum number of periods  |
|  max\_periods |  Maximum number of periods |
|  avg\_periods |  Average number of periods |
|  stdDev\_periods |  Standard Deviation of periods |
|  percentile\_25 |  25th percentile of periods |
|  median |  Median of periods |
|  percentile\_75 |  75th percentile of periods |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  min\_periods |  1 |
|  max\_periods |  10 |
|  avg\_periods |  1.12 |
|  stdDev\_periods |  0.30 |
|  percentile\_25 |  1 |
|  median |  1 |
|  percentile\_75 |  1  |
### OP09:Observation period records per person

List all people (person\_id) who has specific number of observations. The input to the query is a value (or a comma-separated list of values) for a record count.

**Sample query:**

SELECT p.person\_id, count(1) observation\_period\_count

FROM observation\_period p

GROUP BY p.person\_id

having count(1) = 3;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| person\_id | Person identifier |
| observation\_period\_count | Number of periods |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| person\_id |  826002 |
| observation\_period\_count |  3 |
### OP10: Observation period records stratified by observation month

### Counts the observation period records stratified by observation month. All possible values are summarized.

**Sample query:**

SELECT

  month,

  sum( observations ) AS num\_observations

FROM (

  SELECT

    person\_id,

    start\_date,

    end\_date ,

    month ,

    min\_count,

    remainder ,

    start\_month,

    DECODE( SIGN(start\_month + remainder - 12), -1, start\_month + remainder, 12) end1 ,

    1,

    start\_month + remainder - 12 end2 ,

    min\_count + CASE

      WHEN MONTH >= start\_month AND MONTH <= DECODE( SIGN(start\_month + remainder - 12), -1, start\_month + remainder, 12) THEN 1

      WHEN MONTH >= 1 AND MONTH <= start\_month + remainder - 12 THEN 1

      ELSE 0

    END AS observations

  FROM (

    SELECT 1 AS month

    UNION SELECT 2

    UNION SELECT 3

    UNION SELECT 4

    UNION SELECT 5

    UNION SELECT 6

    UNION SELECT 7

    UNION SELECT 8

    UNION SELECT 9

    UNION SELECT 10

    UNION SELECT 11

    UNION SELECT 12  )

  CROSS JOIN (

    SELECT

      person\_id,

      start\_date,

      end\_date ,

      min\_count,

      start\_month,

      remainder

    FROM (

      SELECT

        person\_id,

        observation\_period\_start\_date start\_date ,

        observation\_period\_end\_date as end\_date ,

        round(months\_between( observation\_period\_end\_date, observation\_period\_start\_date ) ) AS months /\* number of complete years \*/ ,

        floor( round(months\_between( observation\_period\_end\_date, observation\_period\_start\_date ) ) / 12 ) AS min\_count ,

        extract( month from observation\_period\_start\_date ) start\_month ,

        mod( cast(round(months\_between( observation\_period\_end\_date, observation\_period\_start\_date ) ) AS integer), 12 ) AS remainder

      FROM

        observation\_period

    )

  )

) GROUP BY month order by month;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  month |  Month number 1-12 |
|  num\_observations |  Number of observation in a specific month |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  month |  1 |
|  num\_observations |  12266979 |
**OP11:** Distribution of observation period end dates

This query is used to to provide summary statistics for observation period end dates (observation\_period\_end\_date) across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

WITH op AS

( SELECT to\_number( to\_char( observation\_period\_end\_date, 'J' ), 9999999 )::INT AS end\_date

         FROM observation\_period)

SELECT to\_date( min( end\_date ), 'J' ) AS min\_end\_date

     , to\_date( max( end\_date ), 'J' ) AS max\_end\_date

     , to\_date( round( avg( end\_date ) ), 'J' ) AS avg\_end\_date

     , round( stdDev( end\_date ) ) AS stdDev\_end\_days

     , to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY end\_date ) OVER () FROM op), 'J' ) AS percentile\_25

     , to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.5)  WITHIN GROUP (ORDER BY end\_date ) OVER () FROM op), 'J' ) AS median

     , to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY end\_date ) OVER () FROM op), 'J' ) AS percentile\_75

  FROM op; /\* end\_date \*/

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| min\_end\_date |  Minimum value of observation period end date |
| max\_end\_date |  Maximum value of observation  period end date |
| avg\_end\_date |  Average value of observation period end date |
| stdDev\_end\_date |  Standard deviation of observation period end date |
| percentile\_25 |  25th percentile of observation period end date |
| median |  Median value of observation period end date |
| percentile\_75 |  75th percentile of observation period end date |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| min\_end\_date | 1/31/2003 |
| max\_end\_date |  6/30/2011 |
|  avg\_end\_date |  11/21/2009 |
|  stdDev\_end\_date |  614 |
|  percentile\_25 |  12/31/2008 |
|  median |  12/31/2009 |
|  percentile\_75 |  12/31/2010 |
**OP12:** Distribution of observation period length

This query is used to provide summary statistics for the observation period length across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. No input is required for this query.

**Sample query:**

SELECT

        min( period\_length ) OVER() AS min\_period,

        max( period\_length ) OVER() AS max\_period,

        round( avg( period\_length ) OVER(), 2 ) AS avg\_period,

        round( stdDev( period\_length ) OVER(), 1 ) AS stdDev\_period,

        PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY period\_length ) OVER() AS percentile\_25,

        PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY period\_length ) OVER() AS median,

        PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY period\_length ) OVER() AS percentile\_75

FROM /\* period\_length \*/

        (

                SELECT

                        observation\_period\_end\_date - observation\_period\_start\_date + 1 AS period\_length

                FROM

                        observation\_period

        )

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| min\_period | Minimum observation period duration in days |
| max\_period | Maximum observation period duration in days |
| avg\_period | Average observation period in days |
| stdDev\_period | Standard deviation of observation period days |
| percentile\_25 | 25th percentile of observation period days |
| median | Median value of of observation period |
| percentile\_75 | 25th percentile of observation period days  |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  min\_period |  1 |
|  max\_period |  2372 |
|  avg\_period |  655.91 |
|  stdDev\_period |  501 |
|  percentile\_25 |  365 |
|  median |  487 |
|  percentile\_75 |  731 |
**OP13:** Distribution of observation period start dates

This query is used to to provide summary statistics for observation period start dates (observation\_period\_start\_date) across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

WITH op AS

        ( SELECT to\_number( to\_char( observation\_period\_start\_date, 'J' ), 9999999)::INT AS start\_date FROM observation\_period )

SELECT

        to\_date( min( start\_date ), 'J' ) AS min\_start\_date ,

        to\_date( max( start\_date ), 'J' ) AS max\_start\_date ,

        to\_date( round( avg( start\_date ) ), 'J' ) AS avg\_start\_date ,

        round( stdDev( start\_date ) ) AS stdDev\_days,

        to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY start\_date )  OVER() FROM op), 'J' ) AS percentile\_25 ,

        to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY start\_date )  OVER() FROM op), 'J' ) AS median ,

        to\_date( (SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY start\_date )  OVER() FROM op), 'J' ) AS percentile\_75

FROM

                op

;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  min\_start\_date |  Minimum start date value |
|  max\_start\_date |  Maximum start date value |
|  avg\_start\_date |  Average start date value |
|  stdDev\_days |  Standard Deviation of start date |
|  percentile\_25 |  25th percentile of start date |
|  median |  Median of start date |
|  percentile\_75 |  75th percentile of start date |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  min\_start\_date |  1/1/2003 |
|  max\_start\_date |  6/30/2011 |
|  avg\_start\_date |  2/5/2008 |
|  stdDev\_days |  741 |
|  percentile\_25 |  1/1/2006 |
|  median |  1/1/2009 |
|  percentile\_75 |  1/1/2010 |
**OP14**** :**Distribution of age, stratified by gender

### This query is used to provide summary statistics for the age across all observation records stratified by gender (gender\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest observation date. Age is summarized for all existing gender\_concept\_id values.

**Sample query:**

WITH t AS /\* person, gender, age \*/

     ( SELECT person\_id, NVL( concept\_name, 'MISSING' ) AS gender

            , extract( year FROM first\_observation\_date ) - year\_of\_birth AS age

         FROM -- person, first observation period date

            ( SELECT person\_id

                   , min( observation\_period\_start\_date ) AS first\_observation\_date

                FROM observation\_period

               GROUP BY person\_id

            )

         JOIN person USING( person\_id )

         LEFT OUTER JOIN concept ON concept\_id = gender\_concept\_id

        WHERE year\_of\_birth IS NOT NULL

     )

SELECT gender

     , count(\*) AS num\_people

     , min( age ) AS min\_age

     , max( age ) AS max\_age

     , round( avg( age ), 2 ) AS avg\_age

     , round( stdDev( age ), 1 ) AS stdDev\_age

     , (SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY age ) over ()

                                     AS percentile\_25 FROM t)

     , (SELECT DISTINCT PERCENTILE\_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over ()

                                     AS median FROM t)

     , (SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY age ) over ()

                                     AS percential\_75 FROM t)

  FROM t

GROUP BY gender

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  gender |  Gender concept name |
|  num\_people |  Number of people with specific gender |
|  min\_age |  Minimum age across observation of people with specific gender |
|  max\_age |  Maximum age across observation of people with specific gender |
|  avg\_age |  Average age across observation of people with specific gender |
|  stdDev\_age |  Standard deviation of age across observation within specific gender |
|  percentile\_25 |  25th percentile age across observation within specific gender |
|  median |  Median age across observation within specific gender |
|  percentile\_75 |  75th percentile age across observation within specific gender |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
|  gender |  MALE |
|  num\_people |  1607472 |
|  min\_age |  0 |
|  max\_age |  103 |
|  avg\_age |  40.78 |
|  stdDev\_age |  18.60 |
|  percentile\_25 |  29 |
|  median |  45 |
|  percentile\_75 |  55 |
**OP15:** Counts of age, stratified by gender

### This query is used to count the age across all observation records stratified by gender (gender\_concept\_id). The age value is defined by the earliest observation date. Age is summarized for all existing gender\_concept\_id values.

**Sample query:**

SELECT        age,

                gender,

                count(\*) AS num\_people

FROM

        (

        SELECT        person\_id,

                        NVL( concept\_name, 'MISSING' ) AS gender,

                        extract( YEAR FROM first\_observation\_date ) - year\_of\_birth AS age

        FROM

                (

                SELECT        person\_id,

                                min( observation\_period\_start\_date ) AS first\_observation\_date

                FROM

                        observation\_period

                GROUP BY person\_id

                )

                        JOIN

                                person USING( person\_id )

                        LEFT OUTER JOIN

                                concept

                                        ON        concept\_id = gender\_concept\_id

        WHERE

                extract( YEAR FROM first\_observation\_date ) - year\_of\_birth >= 0

        )

GROUP BY        age,

                        gender

ORDER BY        age,

                        gender

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| age | Age across within observation |
| gender | Gender concept name stratification |
| num\_people | Number of person within group |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| age |  1 |
| gender |  MALE |
| num\_people |  22501 |
**OP16:** Count of genders, stratified by year and age group

This query is used to count the genders (gender\_concept\_id) across all observation period records stratified by year and age group. The age groups are calculated as 10 year age bands from the age of a person at the observation period start date. All possible value combinations are summarized.

**Sample query:**

SELECT

  observation\_year,

  age\_group,

  gender,

  count(\*) AS num\_people

FROM (

  SELECT DISTINCT

    person\_id ,

    EXTRACT( YEAR from observation\_period\_start\_date ) AS observation\_year

  FROM observation\_period

)

JOIN (

  SELECT

    person\_id,

    gender ,

    CAST(FLOOR( age / 10 ) \* 10 AS VARCHAR)||' to '||CAST(( FLOOR( age / 10 ) \* 10 ) + 9 AS VARCHAR) AS age\_group

  FROM (

    SELECT

      person\_id,

      NVL( concept\_name, 'MISSING' ) AS gender,

      year\_of\_birth ,

      extract( YEAR FROM first\_observation\_date ) - year\_of\_birth AS age

    FROM (

      SELECT

        person\_id,

        gender\_concept\_id,

        year\_of\_birth ,

        min( observation\_period\_start\_date ) AS first\_observation\_date

      FROM

        observation\_period

      JOIN person USING( person\_id )

      GROUP BY

        person\_id,

        gender\_concept\_id,

        year\_of\_birth

    )

    LEFT OUTER JOIN concept ON concept\_id = gender\_concept\_id

    WHERE year\_of\_birth IS NOT NULL

  )

  WHERE age >= 0

) USING( person\_id )

GROUP BY

  observation\_year,

  age\_group,

  gender

ORDER BY

  observation\_year,

  age\_group,

  gender;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| observation\_year | Year of observation |
| age\_group | Group of person by age |
| gender | Gender concept name |
| num\_people | Number of people within year of observation, age group and gender |



**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| observation\_year |  2003 |
| age\_group |  10 to 19 |
| gender |  MALE |
| num\_people |  12060 |
**OP17:** Counts of observation period records stratified by observation end date month.

This query is used to count the observation period records stratified by observation month and person end. person end is an indicator whether a person has completed the last observation period in a given observation month. All possible values are summarized.

**Sample query:**

SELECT EXTRACT( month

FROM observation\_period\_end\_date ) observation\_month , count(\*) AS num\_observations

FROM observation\_period

GROUP BY observation\_month

ORDER BY 1;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| observation\_month | Month of observation |
| num\_observations | Number of observation within end of observation period month |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| observation\_month |  1 |
| num\_observations |  62183 |
**OP18**** :**Counts of observation period records stratified by start of observation month

This query is used to count the observation period records stratified by observation month and person end. person end is an indicator whether a person has initiated the first observation period in a given observation month. All possible values are summarized.

**Sample query:**

SELECT EXTRACT( month

FROM observation\_period\_start\_date ) observation\_month , count(\*) AS num\_observations

FROM observation\_period

GROUP BY observation\_month

ORDER BY 1;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| observation\_month | Month of start of observation period |
| num\_observations | Number of observations within specific month of observation |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| observation\_month |  1 |
| num\_observations |  3987706 |
**OP19**** :**Distribution of observation period length, stratified by age.

This query is used to provide summary statistics for the observation period length across all observation period records stratified by age: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. The age value is defined at the time of the observation date. All existing age values are summarized.

**Sample query:**

SELECT

  age,

  count(\*) AS observation\_periods\_cnt ,

  min( period\_length ) AS min\_period ,

  max( period\_length ) AS max\_period ,

  round( avg( period\_length ), 2 ) AS avg\_period ,

  round( stdDev( period\_length ), 1 ) AS stdDev\_period ,

  percentile\_25,

  median,

  percentile\_75

FROM (

  SELECT

    person\_id,

    age,

    period\_length,

    PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY period\_length ) over(partition by age) AS percentile\_25 ,

    PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY period\_length ) over(partition by age) AS median ,

    PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY period\_length ) over(partition by age) AS percentile\_75

  FROM /\* person, age \*/ (

    SELECT

      person\_id ,

      extract( YEAR FROM first\_observation\_date ) - year\_of\_birth AS age

    FROM (

      SELECT

        person\_id ,

        min( observation\_period\_start\_date ) AS first\_observation\_date

      FROM observation\_period

      GROUP BY person\_id

    )

    JOIN person USING( person\_id )

    WHERE year\_of\_birth IS NOT NULL

  )

  JOIN  (

    SELECT

      person\_id ,

      observation\_period\_end\_date - observation\_period\_start\_date + 1 AS period\_length

    FROM observation\_period

  ) USING( person\_id )

)

GROUP BY

  age,

  percentile\_25 ,

  median ,

  percentile\_75;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| age | Stratification age |
| observation\_period\_cnt | Number of observation periods |
| min\_period | Minimum number of observation periods grouped by age |
| max\_period | Maximum number of observation periods grouped by age |
| avg\_period | Average number of observation periods grouped by age |
| stdDev\_period | Standard deviation of observation periods grouped by age |
| percentile\_25 | 25th percentile of observation periods stratified by age |
| median | Median of observation periods stratified by age |
| percentile\_75   | 75th percentile of observation periods stratified by age |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| age |  1 |
| observation\_period\_cnt |  49990 |
| min\_period |  1 |
| max\_period |  2372 |
| avg\_period |  571.28 |
| stdDev\_period |  40.60 |
| percentile\_25 |  365 |
| median |  366 |
| percentile\_75   |  730 |
**OP20:** Distribution of observation period length, stratified by gender.

This query is used to provide summary statistics for the observation period length across all observation period records stratified by gender (gender\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. All existing gender\_concept\_id values are summarized.

**Sample query:**

SELECT

  gender,

  count(\*) AS observation\_periods\_cnt ,

  min( period\_length ) AS min\_period ,

  max( period\_length ) AS max\_period ,

  round( avg( period\_length ), 2 ) AS avg\_period ,

  round( stdDev( period\_length ), 1 ) AS stdDev\_period ,

  percentile\_25,

  median,

  percentile\_75

FROM (

  SELECT

    person\_id,

    gender,

    period\_length,

    PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY period\_length ) over(partition by gender) AS percentile\_25 ,

    PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY period\_length ) over(partition by gender) AS median ,

    PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY period\_length ) over(partition by gender) AS percentile\_75

  FROM /\* person, age \*/ (

    SELECT

      person\_id ,

      concept\_name as gender

    FROM (

      SELECT

        person\_id ,

        min( observation\_period\_start\_date ) AS first\_observation\_date

      FROM observation\_period

      GROUP BY person\_id

    )

    JOIN person USING( person\_id )

    JOIN concept ON concept\_id = gender\_concept\_id

    WHERE year\_of\_birth IS NOT NULL

  )

  JOIN  (

    SELECT

      person\_id ,

      observation\_period\_end\_date - observation\_period\_start\_date + 1 AS period\_length

    FROM observation\_period

  ) USING( person\_id )

)

GROUP BY

  gender,

  percentile\_25 ,

  median ,

  percentile\_75;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| gender | Gender concept name |
| observations\_period\_cnt | Number of observation periods for specific gender |
| min\_period | Minimum duration of observation period in days |
| max\_period | Maximum duration of observation period in days |
| avg\_period | Average duration of observation in days |
| stdDev\_period | Standard deviation of observation |
| percentile\_25 | 25th percentile of observation periods in days |
| median | Median of observation periods in days |
| percentile\_75 | 75th percentile of observation periods in days |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| gender |  MALE |
| observations\_period\_cnt |  1812743 |
| min\_period |  1 |
| max\_period |  2372 |
| avg\_period |  653.77 |
| stdDev\_period |  502.40 |
| percentile\_25 |  365 |
| median |  457 |
| percentile\_75 |  731 |
