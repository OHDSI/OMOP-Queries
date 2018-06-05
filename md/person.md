**PE02:** Number of patients of specific gender in the dataset

Use this query to determine the number of women and men in an a databse. The gender concept code for women is 8532 and for men is 8507. There are also unknown gender (8551), other (8521) and ambiguous (8570).

**Sample query:**

SELECT COUNT(person\_ID) AS num\_persons\_count

FROM Person

WHERE GENDER\_CONCEPT\_ID = 8532

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| Gender Concept ID | 8532 | Yes | Concept Identifier for 'female' |

**Output:**

| **Field** | ** Description** |
| --- | --- |
| num\_persons\_count | Number of patients in the dataset of specific gender |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| num\_persons\_count | 2859298 |
**PE03:** Number of patients grouped by gender

This query is similar to PE02, but it lists all available genders (male, female, unknown, ambiguous, other) across all person records. The input to the query is a value (or a comma-separated list of values) of a gender\_concept\_id. If the input is omitted, all possible values for gender\_concept\_id are summarized.

**Sample query:**

SELECT person.GENDER\_CONCEPT\_ID, concept.CONCEPT\_NAME AS gender\_name, COUNT(person.person\_ID) AS num\_persons\_count

FROM person

INNER JOIN concept ON person.GENDER\_CONCEPT\_ID = concept.CONCEPT\_ID

GROUP BY person.GENDER\_CONCEPT\_ID, concept.CONCEPT\_NAME;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Gender\_concept\_ID |  Gender concept ID as defined in CDM vocabulary |
| Gender\_Name | Gender name as defined in CDM vocabulary |
| Num\_Persons\_count | Count of patients with specific gender ID |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| Gender\_concept\_ID | 8507 |
| Gender\_Name | Male |
| Num\_Persons\_count | 1607473 |
**PE06:** Number of patients grouped by year of birth

Counts the year of birth (year\_of\_birth) across all person records. All existing values for year of birth are summarized.

**Sample query:**

SELECT year\_of\_birth, COUNT(person\_id) AS Num\_Persons\_count

FROM person

GROUP BY year\_of\_birth

ORDER BY year\_of\_birth;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  year\_of\_birth |  Year of birth of the patient |
|  Num\_Persons\_count |  Number of patients in the dataset of specific year of birth |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  year\_of\_birth |  1950 |
|  Num\_Persons\_count |  389019 |
**PE07:** Number of patients grouped by residence state location

This query is used to count the locations (location\_id) across all person records. All possible values for location are summarized.

**Sample query:**

SELECT NVL( state, 'XX' )

AS state\_abbr, count(\*) as Num\_Persons\_count

FROM person

LEFT OUTER JOIN location

USING( location\_id )

GROUP BY NVL( state, 'XX' )

ORDER BY 1;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| State | State of residence |
| Num\_Persons\_count | Number of patients in the dataset residing in specific state |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
| State | MA |
| Num\_Persons\_count | 1196292 |
**PE08:** Number of patients grouped by zip code of residence

Counts the patients' zip of their residence location across all person records. All possible values for zip are summarized. Zip code contains only the first 3 digits in most databases.

**Sample query:**

SELECT state, NVL( zip, '9999999' ) AS zip, count(\*) Num\_Persons\_count

FROM person

LEFT OUTER JOIN location

USING( location\_id )

GROUP BY state, NVL( zip, '9999999' )

ORDER BY 1, 2;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| State | State of residence |
| Zip | 3 digit zip code of residence |
| Num\_Persons\_count | Number of patients in the dataset residing in a specific zip code |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
| State | MA |
| Zip | 019 |
| Num\_Persons\_count | 477825 |
**PE09:** Number of patients by gender, stratified by year of birth

Count the genders (gender\_concept\_id) across all person records, arrange into groups by year of birth. All possible values for gender concepts stratified by year of birth are summarized.

**Sample query:**

SELECT gender\_concept\_id, c.concept\_name AS gender\_name, year\_of\_birth, COUNT(p.person\_id) AS num\_persons

FROM person p

INNER JOIN concept c ON p.gender\_concept\_id = c.concept\_id

GROUP BY gender\_concept\_id, c.concept\_name, year\_of\_birth

ORDER BY concept\_name, year\_of\_birth;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  gender\_concept\_id |  CDM vocabulary concept identifier |
|  gender\_name |  Gender name as defined in CDM vocabulary |
|  year\_of\_birth |  Stratification by year of birth |
|  num\_persons |  Number of patients in the dataset of specific gender / year of birth |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  gender\_concept\_id |  8507 |
|  gender\_name |  MALE |
|  year\_of\_birth |  1950 |
|  num\_persons |  169002 |
**PE10**** :**Number of patients by day of the year stratified by day of birth

This query is used to count the day of birth (day\_of\_birth) across all person records. All possible values for day of birth are summarized. Not all databases maintain day of birth. This query is only available from CDM V4 and above.

**Sample query:**

SELECT day\_of\_birth, COUNT(person\_ID) AS num\_persons

FROM person

GROUP BY day\_of\_birth

ORDER BY day\_of\_birth;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Day\_Of\_Year | Day of the year 1 through 365 |
| Num\_Rows | Number of records |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
| Day\_Of\_Year | 001 |
| Num\_Rows | 34462921 |
**PE11:** Number of patients by month stratified by day of birth

This query is used to count number of patients grouped by month of birth within all person records. All possible values for month of birth are summarized. Not all databases maintain month of birth. This query is only available from CDM V4 and above.

**Sample query:**

SELECT NVL(month\_of\_birth,1) AS month\_of\_year, count(\*) AS num\_records

FROM person

GROUP BY month\_of\_birth

ORDER BY 1;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  month |  Month year 1 through 12 |
|  num\_rows |  Number of records |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  month |  1 |
|  num\_rows |  34462921 |
**PE12:** Distribution of year of birth

This query is used to to provide summary statistics for the age across all patient records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum. No input is required for this query.

**Sample query:**

SELECT percentile\_25

     , median

     , percentile\_75

     , MIN( year\_of\_birth )    AS minimum

     , MAX( year\_of\_birth )    AS maximum

     , CAST(AVG( year\_of\_birth ) AS INTEGER)   AS mean

     , STDDEV( year\_of\_birth ) AS stddev

FROM

(SELECT MAX( CASE WHEN( percentile = 1 ) THEN year\_of\_birth END ) AS percentile\_25

      , MAX( CASE WHEN( percentile = 2 ) THEN year\_of\_birth END ) AS median

      , MAX( CASE WHEN( percentile = 3 ) THEN year\_of\_birth END ) AS percentile\_75

  FROM -- year of birth / percentile

     ( SELECT year\_of\_birth, births

            /\* The first sum is the sum of all the values from the first year of birth

               to the current year.  The second sum is the total of all the years of birth.

               The result is a cumulative percent of the total for each year.  You want to

               capture when the percentage goes from 24 to 25 as percentile\_25, from 49 to 50

               as the median and from 74 to 75 as the percentile\_75.  Multiplying by 4 then SA

               adding 1 just makes so that instead of looking at percentage, you get the whole

               number 1 if the percentage is less than 25, 2 when the percentage is between 25

               and 50, and so on.

             \*/

            , FLOOR( CAST( SUM( births ) OVER( ORDER BY year\_of\_birth ROWS UNBOUNDED PRECEDING ) AS DECIMAL )

                   / CAST( SUM( births ) OVER( ORDER BY year\_of\_birth ROWS BETWEEN UNBOUNDED PRECEDING

                                                                      AND UNBOUNDED FOLLOWING )  AS DECIMAL )

                   \* 4

                   ) + 1 percentile

        FROM -- Year with number of birthsQ

           ( SELECT year\_of\_birth, count(\*) AS births

               FROM person

              GROUP BY year\_of\_birth

           )

    )where percentile <= 3

) percentile\_table, person

GROUP BY percentile\_25, median, percentile\_75

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  percentile\_25 |  25th percentile of year of birth |
|  median |  Median patient year of birth |
|  percentile\_75 |  75th percentile of year of birth |
|  minimum |  Minimum year of birth  |
|  maximum |  Maximum year of birth |
|  mean |  Mean patient year of birth |
|  stddev |  Standard deviation of year of birth |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  percentile\_25 |  1954 |
|  median |  1965 |
|  percentile\_75 |  1979 |
|  minimum |  1893  |
|  maximum |  2010  |
|  mean |  1968  |
|  stddev |  17.277  |
\*\*PE02:\*\* Number of patients of specific gender in the dataset

Use this query to determine the number of women and men in an a databse. The gender concept code for women is 8532 and for men is 8507. There are also unknown gender (8551), other (8521) and ambiguous (8570).

\*\*Sample query:\*\*

SELECT COUNT(person\\_ID) AS num\\_persons\\_count

FROM Person

WHERE GENDER\\_CONCEPT\\_ID = 8532

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| Gender Concept ID | 8532 | Yes | Concept Identifier for 'female' |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| num\\_persons\\_count | Number of patients in the dataset of specific gender |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| num\\_persons\\_count | 2859298 |

\*\*PE03:\*\* Number of patients grouped by gender

This query is similar to PE02, but it lists all available genders (male, female, unknown, ambiguous, other) across all person records. The input to the query is a value (or a comma-separated list of values) of a gender\\_concept\\_id. If the input is omitted, all possible values for gender\\_concept\\_id are summarized.

\*\*Sample query:\*\*

SELECT person.GENDER\\_CONCEPT\\_ID, concept.CONCEPT\\_NAME AS gender\\_name, COUNT(person.person\\_ID) AS num\\_persons\\_count

FROM person

INNER JOIN concept ON person.GENDER\\_CONCEPT\\_ID = concept.CONCEPT\\_ID

GROUP BY person.GENDER\\_CONCEPT\\_ID, concept.CONCEPT\\_NAME;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Gender\\_concept\\_ID |  Gender concept ID as defined in CDM vocabulary |

| Gender\\_Name | Gender name as defined in CDM vocabulary |

| Num\\_Persons\\_count | Count of patients with specific gender ID |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| Gender\\_concept\\_ID | 8507 |

| Gender\\_Name | Male |

| Num\\_Persons\\_count | 1607473 |

\*\*PE06:\*\* Number of patients grouped by year of birth

Counts the year of birth (year\\_of\\_birth) across all person records. All existing values for year of birth are summarized.

\*\*Sample query:\*\*

SELECT year\\_of\\_birth, COUNT(person\\_id) AS Num\\_Persons\\_count

FROM person

GROUP BY year\\_of\\_birth

ORDER BY year\\_of\\_birth;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  year\\_of\\_birth |  Year of birth of the patient |

|  Num\\_Persons\\_count |  Number of patients in the dataset of specific year of birth |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  year\\_of\\_birth |  1950 |

|  Num\\_Persons\\_count |  389019 |

\*\*PE07:\*\* Number of patients grouped by residence state location

This query is used to count the locations (location\\_id) across all person records. All possible values for location are summarized.

\*\*Sample query:\*\*

SELECT NVL( state, 'XX' )

AS state\\_abbr, count(\\*) as Num\\_Persons\\_count

FROM person

LEFT OUTER JOIN location

USING( location\\_id )

GROUP BY NVL( state, 'XX' )

ORDER BY 1;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| State | State of residence |

| Num\\_Persons\\_count | Number of patients in the dataset residing in specific state |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

| State | MA |

| Num\\_Persons\\_count | 1196292 |

\*\*PE08:\*\* Number of patients grouped by zip code of residence

Counts the patients' zip of their residence location across all person records. All possible values for zip are summarized. Zip code contains only the first 3 digits in most databases.

\*\*Sample query:\*\*

SELECT state, NVL( zip, '9999999' ) AS zip, count(\\*) Num\\_Persons\\_count

FROM person

LEFT OUTER JOIN location

USING( location\\_id )

GROUP BY state, NVL( zip, '9999999' )

ORDER BY 1, 2;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| State | State of residence |

| Zip | 3 digit zip code of residence |

| Num\\_Persons\\_count | Number of patients in the dataset residing in a specific zip code |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

| State | MA |

| Zip | 019 |

| Num\\_Persons\\_count | 477825 |

\*\*PE09:\*\* Number of patients by gender, stratified by year of birth

Count the genders (gender\\_concept\\_id) across all person records, arrange into groups by year of birth. All possible values for gender concepts stratified by year of birth are summarized.

\*\*Sample query:\*\*

SELECT gender\\_concept\\_id, c.concept\\_name AS gender\\_name, year\\_of\\_birth, COUNT(p.person\\_id) AS num\\_persons

FROM person p

INNER JOIN concept c ON p.gender\\_concept\\_id = c.concept\\_id

GROUP BY gender\\_concept\\_id, c.concept\\_name, year\\_of\\_birth

ORDER BY concept\\_name, year\\_of\\_birth;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  gender\\_concept\\_id |  CDM vocabulary concept identifier |

|  gender\\_name |  Gender name as defined in CDM vocabulary |

|  year\\_of\\_birth |  Stratification by year of birth |

|  num\\_persons |  Number of patients in the dataset of specific gender / year of birth |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  gender\\_concept\\_id |  8507 |

|  gender\\_name |  MALE |

|  year\\_of\\_birth |  1950 |

|  num\\_persons |  169002 |

\*\*PE10\*\*\*\* :\*\*Number of patients by day of the year stratified by day of birth

This query is used to count the day of birth (day\\_of\\_birth) across all person records. All possible values for day of birth are summarized. Not all databases maintain day of birth. This query is only available from CDM V4 and above.

\*\*Sample query:\*\*

SELECT day\\_of\\_birth, COUNT(person\\_ID) AS num\\_persons

FROM person

GROUP BY day\\_of\\_birth

ORDER BY day\\_of\\_birth;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Day\\_Of\\_Year | Day of the year 1 through 365 |

| Num\\_Rows | Number of records |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

| Day\\_Of\\_Year | 001 |

| Num\\_Rows | 34462921 |

\*\*PE11:\*\* Number of patients by month stratified by day of birth

This query is used to count number of patients grouped by month of birth within all person records. All possible values for month of birth are summarized. Not all databases maintain month of birth. This query is only available from CDM V4 and above.

\*\*Sample query:\*\*

SELECT NVL(month\\_of\\_birth,1) AS month\\_of\\_year, count(\\*) AS num\\_records

FROM person

GROUP BY month\\_of\\_birth

ORDER BY 1;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  month |  Month year 1 through 12 |

|  num\\_rows |  Number of records |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  month |  1 |

|  num\\_rows |  34462921 |

\*\*PE12:\*\* Distribution of year of birth

This query is used to to provide summary statistics for the age across all patient records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum. No input is required for this query.

\*\*Sample query:\*\*

SELECT percentile\\_25

     , median

     , percentile\\_75

     , MIN( year\\_of\\_birth )    AS minimum

     , MAX( year\\_of\\_birth )    AS maximum

     , CAST(AVG( year\\_of\\_birth ) AS INTEGER)   AS mean

     , STDDEV( year\\_of\\_birth ) AS stddev

FROM

(SELECT MAX( CASE WHEN( percentile = 1 ) THEN year\\_of\\_birth END ) AS percentile\\_25

      , MAX( CASE WHEN( percentile = 2 ) THEN year\\_of\\_birth END ) AS median

      , MAX( CASE WHEN( percentile = 3 ) THEN year\\_of\\_birth END ) AS percentile\\_75

  FROM -- year of birth / percentile

     ( SELECT year\\_of\\_birth, births

            /\\* The first sum is the sum of all the values from the first year of birth

               to the current year.  The second sum is the total of all the years of birth.

               The result is a cumulative percent of the total for each year.  You want to

               capture when the percentage goes from 24 to 25 as percentile\\_25, from 49 to 50

               as the median and from 74 to 75 as the percentile\\_75.  Multiplying by 4 then SA

               adding 1 just makes so that instead of looking at percentage, you get the whole

               number 1 if the percentage is less than 25, 2 when the percentage is between 25

               and 50, and so on.

             \\*/

            , FLOOR( CAST( SUM( births ) OVER( ORDER BY year\\_of\\_birth ROWS UNBOUNDED PRECEDING ) AS DECIMAL )

                   / CAST( SUM( births ) OVER( ORDER BY year\\_of\\_birth ROWS BETWEEN UNBOUNDED PRECEDING

                                                                      AND UNBOUNDED FOLLOWING )  AS DECIMAL )

                   \\* 4

                   ) + 1 percentile

        FROM -- Year with number of birthsQ

           ( SELECT year\\_of\\_birth, count(\\*) AS births

               FROM person

              GROUP BY year\\_of\\_birth

           )

    )where percentile <= 3

) percentile\\_table, person

GROUP BY percentile\\_25, median, percentile\\_75

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  percentile\\_25 |  25th percentile of year of birth |

|  median |  Median patient year of birth |

|  percentile\\_75 |  75th percentile of year of birth |

|  minimum |  Minimum year of birth  |

|  maximum |  Maximum year of birth |

|  mean |  Mean patient year of birth |

|  stddev |  Standard deviation of year of birth |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  percentile\\_25 |  1954 |

|  median |  1965 |

|  percentile\\_75 |  1979 |

|  minimum |  1893  |

|  maximum |  2010  |

|  mean |  1968  |

|  stddev |  17.277  |
