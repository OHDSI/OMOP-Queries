Observation Period Queries
---

OP01: Count number of people who have at least one observation period in the database that is longer than 365 days.
---

Sample query:

```sql
    SELECT COUNT(DISTINCT person_ID) AS NUM_persons

    FROM observation_period

    WHERE observation_period_END_DATE - observation_period_START_DATE >= 365;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Num_Persons | Number of patients who have at least one observation period in the database that is longer than 365 days |

Sample output record:

|  Field |  Value |
| --- | --- |
| Num_Persons | 105119818 |


OP02 : Distribution of length of observation, in months, among first observation periods across the population
---

Count distribution of length of observation, in months, among first observation periods across the population.

Sample query:

```sql
    SELECT        DATEDIFF(month, observation_period_start_date, observation_period_end_date) as num_months,

                    COUNT(distinct person_id) AS num_persons

    FROM

            (

            SELECT        person_ID,

                            observation_period_START_DATE,

                            observation_period_END_DATE,

                            rank() OVER (PARTITION BY person_ID ORDER BY observation_period_START_DATE ASC) AS OP_NUMBER

            FROM

                    observation_period

            ) AS OP1

    WHERE

            op_number = 1

    GROUP BY        DATEDIFF(month,observation_period_START_DATE, observation_period_END_DATE)

    ORDER BY        DATEDIFF(month,observation_period_START_DATE, observation_period_END_DATE) ASC
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| num_month | Number of month duration |
| num_persons | Number of patients whose observation period with num_month duration |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_months |  1 |
| num_persons | 4132770 |



OP03:Number of people continuously observed throughout a year.
---

Count number of people continuously observed throughout a specified year.

Sample query:

```sql
    SELECT COUNT(DISTINCT person_ID) AS NUM_persons

    FROM observation_period

    WHERE observation_period_start_date <= '01-jan-2011'

    AND observation_period_end_date >= '31-dec-2011';
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| num_persons |  Number of patients whose observation period within range of days |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_persons |  32611748 |



OP04:Number of people who have gap in observation (two or more observations)
---

Count number of people who have two or more observations.

Sample query:

```sql
    SELECT count( person_id ) AS num_persons

    FROM -- more than one observatio period

    ( SELECT person_id

    FROM observation_period GROUP BY person_id

    HAVING COUNT( person_id ) > 1 );
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| num_persons |  Number of patients who have two or more observations |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_persons |  18650793 |



OP05: Average length of observation, in month.
---

Count average length of observation period in month.

Sample query:

```sql
    SELECT avg(

    datediff(month, observation_period_start_date , observation_period_end_date ) ) AS num_months

    FROM observation_period;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| num_months |  Average length of observation, in month |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_months |  30 |

OP06: Average length of observation, in days.
---

Count average number of observation days.

Sample query:

```sql
    SELECT avg( observation_period_end_date - observation_period_start_date ) AS num_days

    FROM observation_period;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| num_days |  Average length of observation, in days |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_days |  966 |

OP07:Distribution of age across all observation period records
---

Count distribution of age across all observation period records:  the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
    WITH t AS (

    SELECT DISTINCT

                  person_id, EXTRACT( YEAR FROM first_observation_date ) - year_of_birth AS age

             FROM -- person, first observation date

                ( SELECT person_id

                       , min( observation_period_start_date ) AS first_observation_date

                    FROM observation_period

                   GROUP BY person_id

                )

             JOIN person USING( person_id )

            WHERE year_of_birth IS NOT NULL

    ) SELECT count(\*) AS num_people

         , min( age ) AS min_age

         , max( age ) AS max_age

         , round( avg( age ), 2 ) AS avg_age

         , round( stdDev( age ), 1 ) AS stdDev_age

         , (SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY age ) over () FROM t) AS percentile_25

         , (SELECT DISTINCT PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over () FROM t) AS median_age

         , (SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY age ) over () FROM t) AS percentile_75

            FROM t;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| num_people | Number of people in a dataset |
| min_age | Minimum age of person |
| max_age | Maximum age of a person |
| avg_age | Average age of people in the dataset |
| stdDev_age | Standard deviation of person age |
|  percentile_25 |  25th percentile of of the age group |
|  median_age |  50th percentile of the age group |
|  percentile_75 |  75th percentile of the age group |

Sample output record:

| Field |  Value |
| --- | --- |
| num_people | 151039265 |
| min_age |  0 |
| max_age |  85 |
| avg_age |  31 |
| stdDev_age |  19.4 |
| percentile_25 |  16 |
| median_age |  31 |
| percentile_75 |  47 |

OP08: Distribution of observation period records per person
---

Counts the number of observation period records (observation_period_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

Sample query:

```sql
    WITH obser_person AS

    (

            SELECT        person_id,

                            count(\*) as observation_periods

            FROM        observation_period

                                    JOIN        person USING( person_id )

            GROUP BY        person_id

    )

    SELECT        min( observation_periods ) AS min_periods ,

                    max( observation_periods ) AS max_periods ,

                    round( avg( observation_periods ), 2 ) AS avg_periods ,

                    round( stdDev( observation_periods ), 1 ) AS stdDev_periods ,

                    (SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY observation_periods ) OVER() FROM obser_person) AS percentile_25 ,

                    (SELECT DISTINCT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY observation_periods ) OVER() FROM obser_person) AS median ,

                    (SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY observation_periods ) OVER() FROM obser_person) AS percentile_75

    FROM

            obser_person
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  min_periods |  Minimum number of periods  |
|  max_periods |  Maximum number of periods |
|  avg_periods |  Average number of periods |
|  stdDev_periods |  Standard Deviation of periods |
|  percentile_25 |  25th percentile of periods |
|  median |  Median of periods |
|  percentile_75 |  75th percentile of periods |

Sample output record:

| Field |  Value |
| --- | --- |
|  min_periods |  1 |
|  max_periods |  10 |
|  avg_periods |  1.12 |
|  stdDev_periods |  0.30 |
|  percentile_25 |  1 |
|  median |  1 |
|  percentile_75 |  1  |


OP09:Observation period records per person
---

List all people (person_id) who has specific number of observations. The input to the query is a value (or a comma-separated list of values) for a record count.

Sample query:

```sql
    SELECT p.person_id, count(1) observation_period_count

    FROM observation_period p

    GROUP BY p.person_id

    having count(1) = 3;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| person_id | Person identifier |
| observation_period_count | Number of periods |

Sample output record:

|  Field |  Value |
| --- | --- |
| person_id |  826002 |
| observation_period_count |  3 |


OP10: Observation period records stratified by observation month
---

Counts the observation period records stratified by observation month. All possible values are summarized.

Sample query:

```sql
    SELECT

      month,

      sum( observations ) AS num_observations

    FROM (

      SELECT

        person_id,

        start_date,

        end_date ,

        month ,

        min_count,

        remainder ,

        start_month,

        DECODE( SIGN(start_month + remainder - 12), -1, start_month + remainder, 12) end1 ,

        1,

        start_month + remainder - 12 end2 ,

        min_count + CASE

          WHEN MONTH >= start_month AND MONTH <= DECODE( SIGN(start_month + remainder - 12), -1, start_month + remainder, 12) THEN 1

          WHEN MONTH >= 1 AND MONTH <= start_month + remainder - 12 THEN 1

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

          person_id,

          start_date,

          end_date ,

          min_count,

          start_month,

          remainder

        FROM (

          SELECT

            person_id,

            observation_period_start_date start_date ,

            observation_period_end_date as end_date ,

            round(months_between( observation_period_end_date, observation_period_start_date ) ) AS months /\* number of complete years \*/ ,

            floor( round(months_between( observation_period_end_date, observation_period_start_date ) ) / 12 ) AS min_count ,

            extract( month from observation_period_start_date ) start_month ,

            mod( cast(round(months_between( observation_period_end_date, observation_period_start_date ) ) AS integer), 12 ) AS remainder

          FROM

            observation_period

        )

      )

    ) GROUP BY month order by month;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  month |  Month number 1-12 |
|  num_observations |  Number of observation in a specific month |

Sample output record:

| Field |  Value |
| --- | --- |
|  month |  1 |
|  num_observations |  12266979 |



OP11: Distribution of observation period end dates
---

This query is used to to provide summary statistics for observation period end dates (observation_period_end_date) across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
    WITH op AS

    ( SELECT to_number( to_char( observation_period_end_date, 'J' ), 9999999 )::INT AS end_date

             FROM observation_period)

    SELECT to_date( min( end_date ), 'J' ) AS min_end_date

         , to_date( max( end_date ), 'J' ) AS max_end_date

         , to_date( round( avg( end_date ) ), 'J' ) AS avg_end_date

         , round( stdDev( end_date ) ) AS stdDev_end_days

         , to_date( (SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY end_date ) OVER () FROM op), 'J' ) AS percentile_25

         , to_date( (SELECT DISTINCT PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY end_date ) OVER () FROM op), 'J' ) AS median

         , to_date( (SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY end_date ) OVER () FROM op), 'J' ) AS percentile_75

      FROM op; /\* end_date \*/
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| min_end_date |  Minimum value of observation period end date |
| max_end_date |  Maximum value of observation  period end date |
| avg_end_date |  Average value of observation period end date |
| stdDev_end_date |  Standard deviation of observation period end date |
| percentile_25 |  25th percentile of observation period end date |
| median |  Median value of observation period end date |
| percentile_75 |  75th percentile of observation period end date |

Sample output record:

|  Field |  Description |
| --- | --- |
| min_end_date | 1/31/2003 |
| max_end_date |  6/30/2011 |
|  avg_end_date |  11/21/2009 |
|  stdDev_end_date |  614 |
|  percentile_25 |  12/31/2008 |
|  median |  12/31/2009 |
|  percentile_75 |  12/31/2010 |



OP12: Distribution of observation period length
---

This query is used to provide summary statistics for the observation period length across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. No input is required for this query.

Sample query:

```sql
    SELECT

            min( period_length ) OVER() AS min_period,

            max( period_length ) OVER() AS max_period,

            round( avg( period_length ) OVER(), 2 ) AS avg_period,

            round( stdDev( period_length ) OVER(), 1 ) AS stdDev_period,

            PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY period_length ) OVER() AS percentile_25,

            PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY period_length ) OVER() AS median,

            PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY period_length ) OVER() AS percentile_75

    FROM /\* period_length \*/

            (

                    SELECT

                            observation_period_end_date - observation_period_start_date + 1 AS period_length

                    FROM

                            observation_period

            )
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| min_period | Minimum observation period duration in days |
| max_period | Maximum observation period duration in days |
| avg_period | Average observation period in days |
| stdDev_period | Standard deviation of observation period days |
| percentile_25 | 25th percentile of observation period days |
| median | Median value of of observation period |
| percentile_75 | 25th percentile of observation period days  |

Sample output record:

|  Field |  Value |
| --- | --- |
|  min_period |  1 |
|  max_period |  2372 |
|  avg_period |  655.91 |
|  stdDev_period |  501 |
|  percentile_25 |  365 |
|  median |  487 |
|  percentile_75 |  731 |

OP13: Distribution of observation period start dates
---

This query is used to to provide summary statistics for observation period start dates (observation_period_start_date) across all observation period records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
    WITH op AS

            ( SELECT to_number( to_char( observation_period_start_date, 'J' ), 9999999)::INT AS start_date FROM observation_period )

    SELECT

            to_date( min( start_date ), 'J' ) AS min_start_date ,

            to_date( max( start_date ), 'J' ) AS max_start_date ,

            to_date( round( avg( start_date ) ), 'J' ) AS avg_start_date ,

            round( stdDev( start_date ) ) AS stdDev_days,

            to_date( (SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY start_date )  OVER() FROM op), 'J' ) AS percentile_25 ,

            to_date( (SELECT DISTINCT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY start_date )  OVER() FROM op), 'J' ) AS median ,

            to_date( (SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY start_date )  OVER() FROM op), 'J' ) AS percentile_75

    FROM

                    op

    ;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  min_start_date |  Minimum start date value |
|  max_start_date |  Maximum start date value |
|  avg_start_date |  Average start date value |
|  stdDev_days |  Standard Deviation of start date |
|  percentile_25 |  25th percentile of start date |
|  median |  Median of start date |
|  percentile_75 |  75th percentile of start date |

Sample output record:

|  Field |  Value |
| --- | --- |
|  min_start_date |  1/1/2003 |
|  max_start_date |  6/30/2011 |
|  avg_start_date |  2/5/2008 |
|  stdDev_days |  741 |
|  percentile_25 |  1/1/2006 |
|  median |  1/1/2009 |
|  percentile_75 |  1/1/2010 |

OP14 :Distribution of age, stratified by gender
---

This query is used to provide summary statistics for the age across all observation records stratified by gender (gender_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest observation date. Age is summarized for all existing gender_concept_id values.

Sample query:

```sql
    WITH t AS /\* person, gender, age \*/

         ( SELECT person_id, NVL( concept_name, 'MISSING' ) AS gender

                , extract( year FROM first_observation_date ) - year_of_birth AS age

             FROM -- person, first observation period date

                ( SELECT person_id

                       , min( observation_period_start_date ) AS first_observation_date

                    FROM observation_period

                   GROUP BY person_id

                )

             JOIN person USING( person_id )

             LEFT OUTER JOIN concept ON concept_id = gender_concept_id

            WHERE year_of_birth IS NOT NULL

         )

    SELECT gender

         , count(\*) AS num_people

         , min( age ) AS min_age

         , max( age ) AS max_age

         , round( avg( age ), 2 ) AS avg_age

         , round( stdDev( age ), 1 ) AS stdDev_age

         , (SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY age ) over ()

                                         AS percentile_25 FROM t)

         , (SELECT DISTINCT PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over ()

                                         AS median FROM t)

         , (SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY age ) over ()

                                         AS percential_75 FROM t)

      FROM t

    GROUP BY gender
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  gender |  Gender concept name |
|  num_people |  Number of people with specific gender |
|  min_age |  Minimum age across observation of people with specific gender |
|  max_age |  Maximum age across observation of people with specific gender |
|  avg_age |  Average age across observation of people with specific gender |
|  stdDev_age |  Standard deviation of age across observation within specific gender |
|  percentile_25 |  25th percentile age across observation within specific gender |
|  median |  Median age across observation within specific gender |
|  percentile_75 |  75th percentile age across observation within specific gender |

Sample output record:

|  Field |  Description |
| --- | --- |
|  gender |  MALE |
|  num_people |  1607472 |
|  min_age |  0 |
|  max_age |  103 |
|  avg_age |  40.78 |
|  stdDev_age |  18.60 |
|  percentile_25 |  29 |
|  median |  45 |
|  percentile_75 |  55 |



OP15: Counts of age, stratified by gender
---

This query is used to count the age across all observation records stratified by gender (gender_concept_id). The age value is defined by the earliest observation date. Age is summarized for all existing gender_concept_id values.

Sample query:

```sql
    SELECT        age,

                    gender,

                    count(\*) AS num_people

    FROM

            (

            SELECT        person_id,

                            NVL( concept_name, 'MISSING' ) AS gender,

                            extract( YEAR FROM first_observation_date ) - year_of_birth AS age

            FROM

                    (

                    SELECT        person_id,

                                    min( observation_period_start_date ) AS first_observation_date

                    FROM

                            observation_period

                    GROUP BY person_id

                    )

                            JOIN

                                    person USING( person_id )

                            LEFT OUTER JOIN

                                    concept

                                            ON        concept_id = gender_concept_id

            WHERE

                    extract( YEAR FROM first_observation_date ) - year_of_birth >= 0

            )

    GROUP BY        age,

                            gender

    ORDER BY        age,

                            gender
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| age | Age across within observation |
| gender | Gender concept name stratification |
| num_people | Number of person within group |

Sample output record:

| Field |  Description |
| --- | --- |
| age |  1 |
| gender |  MALE |
| num_people |  22501 |



OP16: Count of genders, stratified by year and age group
---

This query is used to count the genders (gender_concept_id) across all observation period records stratified by year and age group. The age groups are calculated as 10 year age bands from the age of a person at the observation period start date. All possible value combinations are summarized.

Sample query:

```sql
    SELECT

      observation_year,

      age_group,

      gender,

      count(\*) AS num_people

    FROM (

      SELECT DISTINCT

        person_id ,

        EXTRACT( YEAR from observation_period_start_date ) AS observation_year

      FROM observation_period

    )

    JOIN (

      SELECT

        person_id,

        gender ,

        CAST(FLOOR( age / 10 ) \* 10 AS VARCHAR)||' to '||CAST(( FLOOR( age / 10 ) \* 10 ) + 9 AS VARCHAR) AS age_group

      FROM (

        SELECT

          person_id,

          NVL( concept_name, 'MISSING' ) AS gender,

          year_of_birth ,

          extract( YEAR FROM first_observation_date ) - year_of_birth AS age

        FROM (

          SELECT

            person_id,

            gender_concept_id,

            year_of_birth ,

            min( observation_period_start_date ) AS first_observation_date

          FROM

            observation_period

          JOIN person USING( person_id )

          GROUP BY

            person_id,

            gender_concept_id,

            year_of_birth

        )

        LEFT OUTER JOIN concept ON concept_id = gender_concept_id

        WHERE year_of_birth IS NOT NULL

      )

      WHERE age >= 0

    ) USING( person_id )

    GROUP BY

      observation_year,

      age_group,

      gender

    ORDER BY

      observation_year,

      age_group,

      gender;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| observation_year | Year of observation |
| age_group | Group of person by age |
| gender | Gender concept name |
| num_people | Number of people within year of observation, age group and gender |



Sample output record:

|  Field |  Description |
| --- | --- |
| observation_year |  2003 |
| age_group |  10 to 19 |
| gender |  MALE |
| num_people |  12060 |



OP17: Counts of observation period records stratified by observation end date month.
---

This query is used to count the observation period records stratified by observation month and person end. person end is an indicator whether a person has completed the last observation period in a given observation month. All possible values are summarized.

Sample query:

```sql
    SELECT EXTRACT( month

    FROM observation_period_end_date ) observation_month , count(\*) AS num_observations

    FROM observation_period

    GROUP BY observation_month

    ORDER BY 1;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| observation_month | Month of observation |
| num_observations | Number of observation within end of observation period month |

Sample output record:

|  Field |  Description |
| --- | --- |
| observation_month |  1 |
| num_observations |  62183 |



OP18 :Counts of observation period records stratified by start of observation month
---

This query is used to count the observation period records stratified by observation month and person end. person end is an indicator whether a person has initiated the first observation period in a given observation month. All possible values are summarized.

Sample query:

```sql
    SELECT EXTRACT( month

    FROM observation_period_start_date ) observation_month , count(\*) AS num_observations

    FROM observation_period

    GROUP BY observation_month

    ORDER BY 1;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| observation_month | Month of start of observation period |
| num_observations | Number of observations within specific month of observation |

Sample output record:

|  Field |  Description |
| --- | --- |
| observation_month |  1 |
| num_observations |  3987706 |



OP19 :Distribution of observation period length, stratified by age.
---

This query is used to provide summary statistics for the observation period length across all observation period records stratified by age: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. The age value is defined at the time of the observation date. All existing age values are summarized.

Sample query:

```sql
    SELECT

      age,

      count(\*) AS observation_periods_cnt ,

      min( period_length ) AS min_period ,

      max( period_length ) AS max_period ,

      round( avg( period_length ), 2 ) AS avg_period ,

      round( stdDev( period_length ), 1 ) AS stdDev_period ,

      percentile_25,

      median,

      percentile_75

    FROM (

      SELECT

        person_id,

        age,

        period_length,

        PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY period_length ) over(partition by age) AS percentile_25 ,

        PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY period_length ) over(partition by age) AS median ,

        PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY period_length ) over(partition by age) AS percentile_75

      FROM /\* person, age \*/ (

        SELECT

          person_id ,

          extract( YEAR FROM first_observation_date ) - year_of_birth AS age

        FROM (

          SELECT

            person_id ,

            min( observation_period_start_date ) AS first_observation_date

          FROM observation_period

          GROUP BY person_id

        )

        JOIN person USING( person_id )

        WHERE year_of_birth IS NOT NULL

      )

      JOIN  (

        SELECT

          person_id ,

          observation_period_end_date - observation_period_start_date + 1 AS period_length

        FROM observation_period

      ) USING( person_id )

    )

    GROUP BY

      age,

      percentile_25 ,

      median ,

      percentile_75;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| age | Stratification age |
| observation_period_cnt | Number of observation periods |
| min_period | Minimum number of observation periods grouped by age |
| max_period | Maximum number of observation periods grouped by age |
| avg_period | Average number of observation periods grouped by age |
| stdDev_period | Standard deviation of observation periods grouped by age |
| percentile_25 | 25th percentile of observation periods stratified by age |
| median | Median of observation periods stratified by age |
| percentile_75   | 75th percentile of observation periods stratified by age |

Sample output record:

|  Field |  Description |
| --- | --- |
| age |  1 |
| observation_period_cnt |  49990 |
| min_period |  1 |
| max_period |  2372 |
| avg_period |  571.28 |
| stdDev_period |  40.60 |
| percentile_25 |  365 |
| median |  366 |
| percentile_75   |  730 |



OP20: Distribution of observation period length, stratified by gender.
---

This query is used to provide summary statistics for the observation period length across all observation period records stratified by gender (gender_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an is defined as the difference between the start date and the end date. All existing gender_concept_id values are summarized.

Sample query:

```sql
    SELECT

      gender,

      count(\*) AS observation_periods_cnt ,

      min( period_length ) AS min_period ,

      max( period_length ) AS max_period ,

      round( avg( period_length ), 2 ) AS avg_period ,

      round( stdDev( period_length ), 1 ) AS stdDev_period ,

      percentile_25,

      median,

      percentile_75

    FROM (

      SELECT

        person_id,

        gender,

        period_length,

        PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY period_length ) over(partition by gender) AS percentile_25 ,

        PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY period_length ) over(partition by gender) AS median ,

        PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY period_length ) over(partition by gender) AS percentile_75

      FROM /\* person, age \*/ (

        SELECT

          person_id ,

          concept_name as gender

        FROM (

          SELECT

            person_id ,

            min( observation_period_start_date ) AS first_observation_date

          FROM observation_period

          GROUP BY person_id

        )

        JOIN person USING( person_id )

        JOIN concept ON concept_id = gender_concept_id

        WHERE year_of_birth IS NOT NULL

      )

      JOIN  (

        SELECT

          person_id ,

          observation_period_end_date - observation_period_start_date + 1 AS period_length

        FROM observation_period

      ) USING( person_id )

    )

    GROUP BY

      gender,

      percentile_25 ,

      median ,

      percentile_75;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| gender | Gender concept name |
| observations_period_cnt | Number of observation periods for specific gender |
| min_period | Minimum duration of observation period in days |
| max_period | Maximum duration of observation period in days |
| avg_period | Average duration of observation in days |
| stdDev_period | Standard deviation of observation |
| percentile_25 | 25th percentile of observation periods in days |
| median | Median of observation periods in days |
| percentile_75 | 75th percentile of observation periods in days |

Sample output record:

|  Field |  Description |
| --- | --- |
| gender |  MALE |
| observations_period_cnt |  1812743 |
| min_period |  1 |
| max_period |  2372 |
| avg_period |  653.77 |
| stdDev_period |  502.40 |
| percentile_25 |  365 |
| median |  457 |
| percentile_75 |  731 |



