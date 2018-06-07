PE02: Number of patients of specific gender in the dataset

Use this query to determine the number of women and men in an a databse. The gender concept code for women is 8532 and for men is 8507. There are also unknown gender (8551), other (8521) and ambiguous (8570).

Sample query:

SELECT COUNT(person_ID) AS num_persons_count

FROM Person

WHERE GENDER_CONCEPT_ID = 8532

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| Gender Concept ID | 8532 | Yes | Concept Identifier for 'female' |

Output:

| Field |  Description |
| --- | --- |
| num_persons_count | Number of patients in the dataset of specific gender |

Sample output record:

|  Field |  Value |
| --- | --- |
| num_persons_count | 2859298 |



PE03: Number of patients grouped by gender

This query is similar to PE02, but it lists all available genders (male, female, unknown, ambiguous, other) across all person records. The input to the query is a value (or a comma-separated list of values) of a gender_concept_id. If the input is omitted, all possible values for gender_concept_id are summarized.

Sample query:

SELECT person.GENDER_CONCEPT_ID, concept.CONCEPT_NAME AS gender_name, COUNT(person.person_ID) AS num_persons_count

FROM person

INNER JOIN concept ON person.GENDER_CONCEPT_ID = concept.CONCEPT_ID

GROUP BY person.GENDER_CONCEPT_ID, concept.CONCEPT_NAME;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Gender_concept_ID |  Gender concept ID as defined in CDM vocabulary |
| Gender_Name | Gender name as defined in CDM vocabulary |
| Num_Persons_count | Count of patients with specific gender ID |

Sample output record:

|  Field |  Value |
| --- | --- |
| Gender_concept_ID | 8507 |
| Gender_Name | Male |
| Num_Persons_count | 1607473 |



PE06: Number of patients grouped by year of birth

Counts the year of birth (year_of_birth) across all person records. All existing values for year of birth are summarized.

Sample query:

SELECT year_of_birth, COUNT(person_id) AS Num_Persons_count

FROM person

GROUP BY year_of_birth

ORDER BY year_of_birth;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  year_of_birth |  Year of birth of the patient |
|  Num_Persons_count |  Number of patients in the dataset of specific year of birth |

Sample output record:

| Field |  Value |
| --- | --- |
|  year_of_birth |  1950 |
|  Num_Persons_count |  389019 |



PE07: Number of patients grouped by residence state location

This query is used to count the locations (location_id) across all person records. All possible values for location are summarized.

Sample query:

SELECT NVL( state, 'XX' )

AS state_abbr, count(\*) as Num_Persons_count

FROM person

LEFT OUTER JOIN location

USING( location_id )

GROUP BY NVL( state, 'XX' )

ORDER BY 1;

Input:

None

Output:

| Field |  Description |
| --- | --- |
| State | State of residence |
| Num_Persons_count | Number of patients in the dataset residing in specific state |

Sample output record:

| Field |  Value |
| --- | --- |
| State | MA |
| Num_Persons_count | 1196292 |



PE08: Number of patients grouped by zip code of residence

Counts the patients' zip of their residence location across all person records. All possible values for zip are summarized. Zip code contains only the first 3 digits in most databases.

Sample query:

SELECT state, NVL( zip, '9999999' ) AS zip, count(\*) Num_Persons_count

FROM person

LEFT OUTER JOIN location

USING( location_id )

GROUP BY state, NVL( zip, '9999999' )

ORDER BY 1, 2;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| State | State of residence |
| Zip | 3 digit zip code of residence |
| Num_Persons_count | Number of patients in the dataset residing in a specific zip code |

Sample output record:

| Field |  Value |
| --- | --- |
| State | MA |
| Zip | 019 |
| Num_Persons_count | 477825 |



PE09: Number of patients by gender, stratified by year of birth

Count the genders (gender_concept_id) across all person records, arrange into groups by year of birth. All possible values for gender concepts stratified by year of birth are summarized.

Sample query:

SELECT gender_concept_id, c.concept_name AS gender_name, year_of_birth, COUNT(p.person_id) AS num_persons

FROM person p

INNER JOIN concept c ON p.gender_concept_id = c.concept_id

GROUP BY gender_concept_id, c.concept_name, year_of_birth

ORDER BY concept_name, year_of_birth;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  gender_concept_id |  CDM vocabulary concept identifier |
|  gender_name |  Gender name as defined in CDM vocabulary |
|  year_of_birth |  Stratification by year of birth |
|  num_persons |  Number of patients in the dataset of specific gender / year of birth |

Sample output record:

|  Field |  Value |
| --- | --- |
|  gender_concept_id |  8507 |
|  gender_name |  MALE |
|  year_of_birth |  1950 |
|  num_persons |  169002 |



PE10 :Number of patients by day of the year stratified by day of birth

This query is used to count the day of birth (day_of_birth) across all person records. All possible values for day of birth are summarized. Not all databases maintain day of birth. This query is only available from CDM V4 and above.

Sample query:

SELECT day_of_birth, COUNT(person_ID) AS num_persons

FROM person

GROUP BY day_of_birth

ORDER BY day_of_birth;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Day_Of_Year | Day of the year 1 through 365 |
| Num_Rows | Number of records |

Sample output record:

| Field |  Value |
| --- | --- |
| Day_Of_Year | 001 |
| Num_Rows | 34462921 |



PE11: Number of patients by month stratified by day of birth

This query is used to count number of patients grouped by month of birth within all person records. All possible values for month of birth are summarized. Not all databases maintain month of birth. This query is only available from CDM V4 and above.

Sample query:

SELECT NVL(month_of_birth,1) AS month_of_year, count(\*) AS num_records

FROM person

GROUP BY month_of_birth

ORDER BY 1;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  month |  Month year 1 through 12 |
|  num_rows |  Number of records |

Sample output record:

| Field |  Value |
| --- | --- |
|  month |  1 |
|  num_rows |  34462921 |



PE12: Distribution of year of birth

This query is used to to provide summary statistics for the age across all patient records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum. No input is required for this query.

Sample query:

SELECT percentile_25

     , median

     , percentile_75

     , MIN( year_of_birth )    AS minimum

     , MAX( year_of_birth )    AS maximum

     , CAST(AVG( year_of_birth ) AS INTEGER)   AS mean

     , STDDEV( year_of_birth ) AS stddev

FROM

(SELECT MAX( CASE WHEN( percentile = 1 ) THEN year_of_birth END ) AS percentile_25

      , MAX( CASE WHEN( percentile = 2 ) THEN year_of_birth END ) AS median

      , MAX( CASE WHEN( percentile = 3 ) THEN year_of_birth END ) AS percentile_75

  FROM -- year of birth / percentile

     ( SELECT year_of_birth, births

            /\* The first sum is the sum of all the values from the first year of birth

               to the current year.  The second sum is the total of all the years of birth.

               The result is a cumulative percent of the total for each year.  You want to

               capture when the percentage goes from 24 to 25 as percentile_25, from 49 to 50

               as the median and from 74 to 75 as the percentile_75.  Multiplying by 4 then SA

               adding 1 just makes so that instead of looking at percentage, you get the whole

               number 1 if the percentage is less than 25, 2 when the percentage is between 25

               and 50, and so on.

             \*/

            , FLOOR( CAST( SUM( births ) OVER( ORDER BY year_of_birth ROWS UNBOUNDED PRECEDING ) AS DECIMAL )

                   / CAST( SUM( births ) OVER( ORDER BY year_of_birth ROWS BETWEEN UNBOUNDED PRECEDING

                                                                      AND UNBOUNDED FOLLOWING )  AS DECIMAL )

                   \* 4

                   ) + 1 percentile

        FROM -- Year with number of birthsQ

           ( SELECT year_of_birth, count(\*) AS births

               FROM person

              GROUP BY year_of_birth

           )

    )where percentile <= 3

) percentile_table, person

GROUP BY percentile_25, median, percentile_75

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  percentile_25 |  25th percentile of year of birth |
|  median |  Median patient year of birth |
|  percentile_75 |  75th percentile of year of birth |
|  minimum |  Minimum year of birth  |
|  maximum |  Maximum year of birth |
|  mean |  Mean patient year of birth |
|  stddev |  Standard deviation of year of birth |

Sample output record:

|  Field |  Value |
| --- | --- |
|  percentile_25 |  1954 |
|  median |  1965 |
|  percentile_75 |  1979 |
|  minimum |  1893  |
|  maximum |  2010  |
|  mean |  1968  |
|  stddev |  17.277  |



