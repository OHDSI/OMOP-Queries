Condition Occurrence Queries
---

CO04: Count In what place of service where condition diagnoses.
---

Returns the distribution of the visit place of service where the condition was reported.

Sample query:

```sql
	SELECT concept_name AS place_of_service_name, place_freq

	FROM (

	SELECT care_site_id, count(\*) AS place_freq

	FROM (

	SELECT care_site_id

	FROM (

	SELECT visit_occurrence_id

	FROM condition_occurrence

	WHERE condition_concept_id = 31967

	AND visit_occurrence_id

	IS NOT NULL) AS from_cond

	LEFT JOIN (

	SELECT visit_occurrence_id, care_site_id

	FROM visit_occurrence) AS from_visit ON from_cond.visit_occurrence_id=from_visit.visit_occurrence_id )

	GROUP BY care_site_id

	ORDER BY place_freq ) AS place_id_count

	LEFT JOIN (

	SELECT concept_id, concept_name

	FROM concept) AS place_concept ON place_id_count.care_site_id=place_concept.concept_id

	ORDER BY place_freq;
```

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept ID for 'Nausea' |





Output:

|  Field |  Description |
| --- | --- |
| place_of_service_name | The place of service where the condition was reported. |
| place_freq | Frequency of the place of service. |

Sample output record:

|  Field |  Description |
| --- | --- |
| place_of_service_name | Emergency Room |
| place_freq | 35343 |


CO05 :Breakout of condition by gender, age
---

Returns the distribution of condition breakouts per gender and age.

Sample query:

```sql
	SELECT

	  concept_name AS gender,

	  age,

	  gender_age_freq

	FROM (

	  SELECT

	    gender_concept_id,

	    age,

	    COUNT(1) gender_age_freq

	  FROM (

	    SELECT

	      year_of_birth,

	      month_of_birth,

	      day_of_birth,

    	  gender_concept_id,

	      condition_start_date,

	      DATEDIFF(years, CONVERT(DateTime, year_of_birth||'-01-01'), condition_start_date) AS age

	    FROM (

	      SELECT

	        person_id,

	        condition_start_date

	      FROM condition_occurrence

	      WHERE

	        condition_concept_id = 31967 AND

	        person_id IS NOT NULL

	    ) AS from_cond

	    LEFT JOIN person as from_person ON from_cond.person_id=from_person.person_id ) AS gender_count

	  GROUP BY

	    gender_concept_id,

	    age

	  ORDER BY gender_age_freq

	) AS gender_id_age_count

	LEFT JOIN concept as concept_list ON gender_id_age_count.gender_concept_id=concept_list.concept_id

	ORDER BY gender_age_freq DESC;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept ID for 'Nausea' |

Output:

|  Field |  Description |
| --- | --- |
| gender | A person's gender |
| age | A person's age in years |
| gender_age_freq | The frequency of a condition breakout for person gender at a certain age. |

Sample output record:

|  Field |  Description |
| --- | --- |
| gender | Female |
| age | 50 |
| gender_age_freq | 3136 |


CO06:What are a person's comorbidities.
---

Returns all coexisting conditions for a given person as defined in the condition_era table.

Sample query:

```sql
	SELECT DISTINCT

	  CASE WHEN concept_name_1>concept_name_2 THEN concept_name_1 ELSE concept_name_2 END as condition1,

	  CASE WHEN concept_name_1>concept_name_2 THEN concept_name_2 ELSE concept_name_1 END AS condition2

	FROM (

	  SELECT

	    concept_name_1,

	    concept_name AS concept_name_2

	  FROM (

	    SELECT

	      condition_concept_id_2,

	      concept_name AS concept_name_1

	    FROM (

	      SELECT

	        table1.condition_concept_id AS condition_concept_id_1,

	        table2.condition_concept_id AS condition_concept_id_2

	      FROM

	        (SELECT \* FROM condition_era WHERE person_id = 136931019) AS table1,

	        (SELECT \* FROM condition_era WHERE person_id = 136931019) AS table2

	      WHERE

	        table2.condition_era_start_date <= table1.condition_era_end_date AND

	        (table2.condition_era_end_date IS NULL OR table2.condition_era_end_date >= table1.condition_era_start_date) AND

	        table1.condition_concept_id<>table2.condition_concept_id

	    ) AS comorb

	    LEFT JOIN concept AS concept_list ON comorb.condition_concept_id_1=concept_list.concept_id

	  ) AS comorb2

	  LEFT JOIN concept AS concept_list ON comorb2.condition_concept_id_2=concept_list.concept_id

	) AS condition_pairs;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| person_id | 136931019 | Yes | Randomly picked person identifier |

Output:

|  Field |  Description |
| --- | --- |
| Condition 1 | Name of one condition in the comorbidity. |
| Condition 2 | Name of the other condition in the comorbidity. |

Sample output record:

|  Field |  Description |
| --- | --- |
| Condition 1 | Hyperlipidemia |
| Condition 2 | Abnormal breathing |


CO07 :Frequency of hospitalized for a condition
---

Returns the distribution of number of times a person has been hospitalized where a certain condition was reported.

Sample query:

```sql
	SELECT

	  number_of_hospitlizations,

	  count(\*) AS persons_freq

	FROM (

	  SELECT

	    person_id,

	    COUNT(\*) AS number_of_hospitlizations

	  FROM (

	    SELECT distinct

	      condition_era_id,

	      era.person_id

	    FROM (

	      SELECT

	        condition_start_date,

	        condition_end_date,

	        from_cond.person_id

	      FROM (

	        SELECT

	          visit_occurrence_id,

	          condition_start_date,

	          condition_end_date,

	          person_id

	        FROM condition_occurrence

	        WHERE

	          condition_concept_id=31967 AND

	          visit_occurrence_id IS NOT NULL

	      ) AS FROM_cond

	      JOIN visit_occurrence AS FROM_visit

	        ON FROM_cond.visit_occurrence_id=FROM_visit.visit_occurrence_id

	      JOIN care_site cs on from_visit.care_site_id=cs.care_site_id

	         where place_of_service_concept_id=8717

	    ) AS occurr,

	    (

	      SELECT

	        condition_era_id,

	        person_id,

	        condition_era_start_date,

	        condition_era_end_date

	      FROM condition_era

	      WHERE condition_concept_id=31967

	    ) AS era

	    WHERE

	      era.person_id=occurr.person_id AND

	      era.condition_era_start_date <= occurr.condition_end_date AND

	      (era.condition_era_end_date IS NULL OR era.condition_era_end_date >= occurr.condition_start_date)

	  )

	  GROUP BY person_id

	  ORDER BY number_of_hospitlizations desc

	)

	GROUP BY number_of_hospitlizations

	ORDER BY persons_freq desc

	;
```

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

Output:

|  Field |  Description |
| --- | --- |
| number_of_hospitlizations | Number of times a person was reported to be hospitalized with a certain condition. |
| persons_freq | Number of persons which were reported to have a certain number of hospilizations with a certain condition. |

Sample output record:

| Field |  Description |
| --- | --- |
| number_of_hospitlizations | 2 |
| persons_freq | 177 |


CO08 :Duration of hospitalization for a conditions
---

Returns the the average length in days of all hospitalizations where a certain condition was reported

Sample query:

```sql
	SELECT

	  avg(hosp_no_days) AS average_hosp_duration_count

	FROM (

	  SELECT DISTINCT

	    hosp_no_days,

	    person_id,

	    from_visit.visit_occurrence_id

	  FROM (

	    SELECT

	      visit_occurrence_id, condition_start_date, condition_end_date, person_id

	    FROM condition_occurrence

	    WHERE

	      condition_concept_id = 31967 AND

	      visit_occurrence_id IS NOT NULL

	  ) AS from_cond

	  JOIN (

	    SELECT

	      DATEDIFF(DAY, visit_start_date, visit_end_date) + 1 AS hosp_no_days,

	      visit_start_date,

	      visit_occurrence_id,

	      place_of_service_concept_id

	    FROM visit_occurrence v

	    JOIN care_site c on v.care_site_id=c.care_site_id

	    WHERE place_of_service_concept_id = 8717

	  ) AS from_visit

	    ON from_cond.visit_occurrence_id = from_visit.visit_occurrence_id );
```



Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

Output:

|  Field |  Description |
| --- | --- |
| average_hosp_duration_count | Average length in days of all hospitalization where a certain condition was reported. +1 was added for partial days (e.g. 1.5 days were counted as 2 days). |

Sample output record:

| Field |  Description |
| --- | --- |
| average_hosp_duration_count | 7 |


CO09 :Is a condition seasonal, alergies for example
---

Returns the distribution of condition occurrence per season in the northern hemisphere, defined in the following way:

|  Spring |  March 21 - June 21 |
| --- | --- |
|  Summer |  June 22 - September 22 |
|  Fall |  September 23 - December 21 |
|  Winter |  December 22 - March 20 |

Sample query:

```sql
	SELECT season, COUNT(\*) as season_freq

	FROM (

	SELECT CASE

	WHEN (daymonth>0320

	AND daymonth<=0621) THEN 'Spring' WHEN (daymonth>0621

	AND daymonth<=0922) THEN 'Summer' WHEN (daymonth>0922

	AND daymonth<=1221) THEN 'Fall' WHEN (daymonth>1221

	OR (daymonth>0000

	AND daymonth<=0520)) THEN 'Winter' ELSE 'Unknown' end AS season

	FROM (

	SELECT cast(substring(condition_start_date

	from 6 for 2)|| substring(condition_start_date

	from 9 for 2) as int) AS daymonth,condition_start_date

	FROM condition_occurrence

	WHERE condition_concept_id = 31967 ) ) AS condition_season

	GROUP BY season

	ORDER BY season_freq;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

Output:

| Field |  Description |
| --- | --- |
| season | Season as defined in the northern hemisphere. |
| season_freq | Frequency of condition occurrence in the season. |

Sample output record:

|  Field |  Description |
| --- | --- |
| season | Summer |
| season_freq | 62924 |


CO12 : Distribution of condition end dates.
---

This query is used to to provide summary statistics for condition occurrence end dates (condition_occurrence_end_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
	with end_rank as (

	  SELECT

	    condition_end_date-'0001-01-01' as num_end_date,

	    condition_end_date,

	    sum(1) over (partition by 1 order by condition_end_date asc rows between unbounded preceding and current row) as rownumasc

	  FROM

	    condition_occurrence

	),

	other_stat as (

	  SELECT

	    count(condition_end_date) as condition_end_date_count,

	    min(condition_end_date) as condition_end_date_min,

	    max(condition_end_date) as condition_end_date_max,

	    to_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition_end_date-'0001-01-01') as int) as condition_end_date_average,

	    stddev((condition_end_date-'0001-01-01')) as condition_end_date_stddev

	  FROM

	    condition_occurrence

	  WHERE

	    condition_end_date is not null

	)

	SELECT

	  (SELECT count(condition_end_date) FROM condition_occurrence WHERE condition_end_date is null) AS condition_end_date_null_count,

	  \*

	FROM

	  other_stat,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_end_date-'0001-01-01') as int) AS condition_end_date_25percentile

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

	      (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

	  ) AS condition_end_date_25percentile,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_end_date-'0001-01-01') as int) as condition_end_date_median

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

	      (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

	  ) AS condition_end_date_median,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_end_date-'0001-01-01') as int) as condition_end_date_75percentile

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

	      (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

	  ) AS condition_end_date_75percentile;
```

Input:

None



Output:

| Field |  Description |
| --- | --- |
| condition_end_date_null_count | Number of condition occurrences where end date is null |
| condition_end_date_count | Number of condition occurrence end dates |
| condition_end_date_min | The earliest end date of a condition occurrence |
| condition_end_date_max | The latest end date of a condition occurrence |
| condition_end_date_average | The average end date (spanning from the earliest to the latest date and counted by days) |
| condition_end_date_stddev | The standard deviation of end dates, in number of days (spanning from the earliest to the latest date and counted by days) |
| condition_end_date_25percentile |  An end date where 25 percent of the other end dates are earlier |
| condition_end_date_median |  An end date where half of the other end dates are earlier and half are later |
| condition_end_date_75percentile |  An end date where 75 percent of the other end dates are earlier |

Sample output record:

|  Field |  Value |
| --- | --- |
| condition_end_date_null_count | 0 |
| condition_end_date_count | 224523674 |
| condition_end_date_min | 2003-01-01 |
| condition_end_date_max | 011-12-15 |
| condition_end_date_average | 2008-11-30 |
| condition_end_date_stddev | 651.19 |
| condition_end_date_25percentile | 2007-10-30 |
| condition_end_date_median | 2009-05-07 |
| condition_end_date_75percentile | 2010-05-04 |


CO13: Distribution of condition start dates
---

This query is used to to provide summary statistics for condition occurrence start dates (condition_occurrence_start_date) across all condition occurrence records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
	with end_rank as (

	  SELECT

	    condition_start_date-'0001-01-01' as num_start_date,

	    condition_start_date,

	    sum(1) over (partition by 1 order by condition_start_date asc rows between unbounded preceding and current row) as rownumasc

	  FROM

	    condition_occurrence

	),

	other_stat as (

	  SELECT

	    count(condition_start_date) as condition_start_date_count,

	    min(condition_start_date) as condition_start_date_min,

	    max(condition_start_date) as condition_start_date_max,

	    to_date('0001-01-01', 'yyyy/mm/dd')+ cast(avg(condition_start_date-'0001-01-01') as int) as condition_start_date_average,

	    stddev((condition_start_date-'0001-01-01')) as condition_start_date_stddev

	  FROM

	    condition_occurrence

	  WHERE

	    condition_start_date is not null

	)

	SELECT

	  (SELECT count(condition_start_date) FROM condition_occurrence WHERE condition_start_date is null) AS condition_start_date_null_count,

	  \*

	FROM

	  other_stat,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_start_date-'0001-01-01') as int) AS condition_start_date_25percentile

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

	      (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

	  ) AS condition_start_date_25percentile,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_start_date-'0001-01-01') as int) as condition_start_date_median

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

	      (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

	  ) AS condition_start_date_median,

	  ( SELECT

	      to_date('0001-01-01', 'yyyy/mm/dd')+cast(avg(condition_start_date-'0001-01-01') as int) as condition_start_date_75percentile

	    FROM

	      (select \*,(select count(\*) from end_rank) as rowno from end_rank)

	    WHERE

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

	      (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

	  ) AS condition_start_date_75percentile;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| condition_start_date_null_count | Number of condition occurrences where start date is null |
| condition_start_date_count | Number of condition occurrence start dates |
| condition_start_date_min | The earliest start date of a condition occurrence |
| condition_start_date_max | The latest start date of a condition occurrence |
| condition_start_date_average | The average start date (spanning from the earliest to the latest date and counted by days) |
| condition_start_date_stddev | The standard deviation of start dates, in number of days (spanning from the earliest to the latest date and counted by days) |
| condition_start_date_25percentile | A start date where 25 percent of the other end dates are earlier |
| condition_start_date_median | A start date where half of the other end dates are earlier and half are later |
| condition_start_date_75percentile | A start date where 75 percent of the other end dates are earlier |

Sample output record:

|  Field |  Value |
| --- | --- |
| condition_end_date_null_count | 0 |
| condition_end_date_count | 224523674 |
| condition_end_date_min | 2003-01-01 |
| condition_end_date_max | 2011-11-08 |
| condition_end_date_average | 2008-11-30 |
| condition_end_date_stddev | 651.27 |
| condition_end_date_25percentile | 2007-10-30 |
| condition_end_date_median | 2009-05-06 |
| condition_end_date_75percentile | 2010-05-03 |


CO14: Counts of condition types
---

This query is used to count the condition type concepts (condition_type_concept_id, in the CDM V2 condition_occurrence_type) across all condition occurrence records. The input to the query is a value of a condition_type_concept_id.

Sample query:

```sql
	SELECT condition_type_freq, condition_type_concept_id, concept_name

	FROM (

	SELECT condition_type_concept_id, count(\*) as condition_type_freq

	FROM (

	SELECT \*

	from condition_occurrence)

	WHERE condition_concept_id = 31967

	GROUP BY condition_type_concept_id) AS condition_type_count

	LEFT JOIN (

	SELECT concept_id, concept_name

	FROM concept) AS type_concept ON condition_type_count.condition_type_concept_id=type_concept.concept_id

	ORDER BY condition_type_freq;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 31967 | Yes | Condition concept identifier for 'Nausea' |

Output:

|  Field |  Description |
| --- | --- |
| condition_type_freq | Frequency of a specific condition_type |
| condition_type_concept_id | Unique ID for condition_type |
| concept_name |  Description of the condition's data source |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition_type_freq | 4735 |
| condition_type_concept_id | 38000235 |
| concept_name | Outpatient header - 6th position |


CO15: Distribution of number of distinct conditions persons have
---

This query is used to provide summary statistics for the number of different distinct conditions (condition_concept_id) of all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

```sql
	with ranked as (

	  SELECT

	    num_of_conditions,

	    row_number() over (order by num_of_conditions asc) AS rownumasc

	  FROM(

	    select

	      person_id,

	      count(distinct condition_concept_id) AS num_of_conditions

	    FROM condition_occurrence

	    where person_id!=0

	    GROUP BY person_id

	  )

	),

	other_stat AS (

	  SELECT

	    count(num_of_conditions) as condition_dist_num_count,

	    min(num_of_conditions) as condition_dist_num_min,

	    max(num_of_conditions) as condition_dist_num_max,

	    avg(num_of_conditions) as condition_dist_num_averege,

	    stddev(num_of_conditions) as condition_dist_num_stddev

	  FROM (

	    SELECT

	      count(distinct condition_concept_id) AS num_of_conditions,

	      person_id

	    FROM condition_occurrence

	    WHERE person_id!=0

	    GROUP BY person_id

	  )

	)

	SELECT

	  (SELECT count(distinct person_id) FROM condition_occurrence WHERE person_id!=0 and condition_occurrence_id is null) AS condition_null_count,

	  \*

	FROM

	  other_stat,

	  ( SELECT distinct

	      num_of_conditions as condition_dist_num_25percentile

	    FROM

	      (select \*,(select count(\*) from ranked) as rowno from ranked)

	    WHERE

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)=0) or

	      (rownumasc=cast (rowno\*0.25 as int) and mod(rowno\*25,100)>0) or

	      (rownumasc=cast (rowno\*0.25 as int)+1 and mod(rowno\*25,100)>0)

	  ) AS condition_end_date_25percentile,

	  ( SELECT distinct

	      num_of_conditions as condition_dist_num_median

	    FROM

	      (select \*,(select count(\*) from ranked) as rowno from ranked)

	    WHERE

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)=0) or

	      (rownumasc=cast (rowno\*0.50 as int) and mod(rowno\*50,100)>0) or

	      (rownumasc=cast (rowno\*0.50 as int)+1 and mod(rowno\*50,100)>0)

	  ) AS condition_end_date_median,

	  ( SELECT distinct

	      num_of_conditions as condition_dist_num_75percentile

	    FROM

	      (select \*,(select count(\*) from ranked) as rowno from ranked)

	    WHERE

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)=0) or

	      (rownumasc=cast (rowno\*0.75 as int) and mod(rowno\*75,100)>0) or

	      (rownumasc=cast (rowno\*0.75 as int)+1 and mod(rowno\*75,100)>0)

	  ) AS condition_end_date_75percentile;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| condition_null_count | Number of condition occurrences where condition_occurrence_id is null |
| condition_count | Number of condition occurrences |
| condition_dist_num_min | The lowest number of distinct condition occurrences |
| condition_dist_num_max | The highest number of distinct condition occurrences |
| condition_dist_num_averege | The avarege number of distinct condition occurrences |
| condition_dist_num_stddev | The standard deviation of distinct condition occurence numbers |
| condition_dist_num_25percentile | A distinct condition occurrence number where 25 percent of the other numbers are lower |
| condition_dist_num_median | A distinct condition occurrence number where half of the other numbers are lower and half are higher |
| condition_dist_num_75percentile | A distinct condition occurrence number where 75 percent of the other numbers are lower |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition_null_count | 0 |
| condition_count | 4395019 |
| condition_dist_num_min | 1 |
| condition_dist_num_max | 327 |
| condition_dist_num_averege | 17 |
| condition_dist_num_stddev | 16.94 |
| condition_dist_num_25percentile | 6 |
| condition_dist_num_median | 12 |
| condition_dist_num_75percentile | 23 |


CO16: Counts of number of distinct conditions persons have
---

This query is used to count the number of different distinct conditions (condition_concept_id) of all persons. The input to the query is a value for a concept identifier.

Sample query:

```sql
	SELECT count(c.condition_concept_id) conditions_count, c.person_id

	FROM condition_occurrence c

	WHERE condition_concept_id = 201820

	GROUP BY c.person_id

	ORDER BY 1

	DESC;
```

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 201820 | Yes | Condition concept identifier for 'Diabetes mellitus' |

Output:

|  Field |  Description |
| --- | --- |
| conditions_count | Number of conditions recorded for the person |
| person_id | Person identifier |

Sample output record:

|  Field |  Description |
| --- | --- |
| conditions_count |  39 |
| person_id |  20017834818 |


CO17: Distribution of condition occurrence records per person
---

This query is used to provide summary statistics for the number of condition occurrence records (condition_occurrence_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

Sample query:

```sql
	with ranked as

	  (

	  SELECT num_of_conditions, sum(1) over (partition by 1

	  ORDER BY num_of_conditions asc rows BETWEEN unbounded preceding AND current row) AS rownumasc

	  FROM (

                                        SELECT count(\*) as num_of_conditions

                                        FROM condition_occurrence

                                        WHERE person_id!=0

                                        GROUP BY person_id

                                )

	  ),

	  other_stat AS

	  (

	   SELECT count(num_of_conditions) AS condition_num_count,

                        min(num_of_conditions) AS condition_num_min,

      max(num_of_conditions) AS condition_num_max,

                        avg(num_of_conditions) AS condition_num_averege,

      stddev(num_of_conditions) as condition_num_stddev

	   FROM (

                                   SELECT count(\*) AS num_of_conditions, person_id

                                   FROM   condition_occurrence

                                   WHERE person_id!=0

                                   GROUP BY person_id

                           )

	  )

	SELECT

	 (

	        SELECT count(distinct person_id)

	        FROM condition_occurrence

	        WHERE person_id!=0 AND condition_occurrence_id IS NULL

	 ) AS condition_null_count,

	 \* FROM other_stat,

	 (

	  SELECT num_of_conditions AS condition_num_25percentile

	  FROM (SELECT \*,(SELECT count(\*) FROM ranked) as rowno FROM ranked)

	  WHERE (rownumasc=cast (rowno\*0.25 as int) AND mod(rowno\*25,100)=0) OR

	     (rownumasc=cast (rowno\*0.25 as int) AND mod(rowno\*25,100)>0) OR

	     (rownumasc=cast (rowno\*0.25 as int)+1 AND mod(rowno\*25,100)>0)

	 ) AS condition_num_25percentile,

	 (

	  SELECT num_of_conditions AS condition_num_median

	  FROM (SELECT \*,(SELECT count(\*) FROM ranked) AS rowno FROM ranked)

	  WHERE (rownumasc=cast (rowno\*0.50 AS int) AND mod(rowno\*50,100)=0) OR

	     (rownumasc=cast (rowno\*0.50 AS int) AND mod(rowno\*50,100)>0) OR

	     (rownumasc=cast (rowno\*0.50 AS int)+1 AND mod(rowno\*50,100)>0)

	 ) AS condition_num_median,

	 (

	  SELECT num_of_conditions AS condition_num_75percentile

	  FROM (SELECT \*,(SELECT count(\*) FROM ranked) as rowno FROM ranked)

	  WHERE (rownumasc=cast (rowno\*0.75 as int) AND mod(rowno\*75,100)=0) OR

	     (rownumasc=cast (rowno\*0.75 as int) AND mod(rowno\*75,100)>0) OR

	     (rownumasc=cast (rowno\*0.75 as int)+1 AND mod(rowno\*75,100)>0)

	 ) AS condition_num_75percentile
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| condition_null_count | Number of persons with at least one null condition_occurrence_id |
| condition_num_count | Number of distinct persons with conditions |
| condition_num_min | The lowest number of condition occurences |
| condition_num_max | The highest number of condition occurences |
| condition_num_averege | The average number of condition occurences |
| condition_num_stddev | The standard deviation of condition occurence numbers |
| condition_num_25percentile | A condition occurence number where 25 percent of the other numbers are lower |
| condition_num_median | A condition occurence number where half of the other numbers are lower and half are higher |
| condition_num_75percentile | A condition occurence number where 75 percent of the other numbers are lower |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition_null_count | 4395019 |
| condition_num_count |   |
| condition_num_min | 1 |
| condition_num_max | 7144 |
| condition_num_averege | 51 |
| condition_num_stddev | 86.63 |
| condition_num_25percentile | 11 |
| condition_num_median | 26 |
| condition_num_75percentile | 58 |


CO19: Counts of condition occurrence records stratified by observation month
---

This query is used to count the condition occurrence records stratified by observation month.

Sample query:

```sql
	SELECT extract(month

	from condition_start_date) month_number, count(\*) as number_of_conditions_in_month

	FROM condition_occurrence

	GROUP BY extract(month

	from condition_start_date)

	ORDER BY 1;
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| Month_number | Month number |
| Number_of_conditions_in_month |  The number of the condition occurrences is a specified month. |

Sample output record:

|  Field |  Description |
| --- | --- |
| Month_number |  3 |
| Number_of_conditions_in_month |  20643257 |


CO21: Distribution of age, stratified by condition
---

This query is used to provide summary statistics for the age across all condition occurrence records stratified by condition (condition_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest condition occurrence. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id.

Oracle specific query.

Sample query:

```sql
	SELECT concept_name AS condition

	     , condition_concept_id

	     , count(\*) AS condition_occurrences

	     , min( age ) over () AS min_age

	     , max( age ) over () AS max_age

	     , round( avg( age ), 2 ) AS avg_age

	     , round( stdDev( age ) over (), 1 ) AS stdDev_age

	     , PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY age ) over ()

	                                     AS percentile_25

	     , PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY age ) over ()

	                                     AS median_age

	     , PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY age ) over ()

	                                     AS percentile_75

	  FROM -- condition occurrences with age at time of condition

	     ( SELECT condition_concept_id

	            , EXTRACT( YEAR from condition_start_date ) AS age -- year_of_birth

	         FROM condition_occurrence

	         JOIN person USING( person_id )

	        WHERE condition_concept_id

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

	  JOIN concept ON concept_id = condition_concept_id

	GROUP BY concept_name, condition_concept_id, age

	ORDER BY condition_occurrences DESC
```

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id list | 192691, 193323, 194700, 195771, 200687, 201254, 201530, 201531, 201820, 201826 , 318712, 373999, 377821, 4008576, 4009780, 4024659, 4030061, 4034960, 4034962, 4047906 , 40480000, 4048202, 40482883, 40488810, 4058243, 4062685, 4062686, 4062687, 4063042, 4063043 , 4079850, 4096041, 4096042, 4096668, 4096670, 4096671, 4099214, 4099215, 4099217, 4099334 , 4099651, 4099652, 4099653, 4099741, 4102018, 4129378, 4129516, 4129519, 4130162, 4130164 , 4130166, 4136889, 4137214, 4140808, 4143529, 4143689, 4143857, 4144583, 4145827, 4151281 , 4151282, 4152858, 4155634, 4166381, 4178452, 4178790, 4192852, 4193704, 4196141, 4198296 , 4200873, 4200875, 4202383, 4212631, 4221344, 4222222, 4222410, 4222547, 4222553, 4222687 , 4222834, 4223303, 4223444, 4224254, 4224709, 4224723, 4225013, 4225055, 4225656, 4226245 , 4227210, 4228102, 4228112, 4230254, 4231917, 4235410, 4237068, 4240589, 4245270, 4252384, 4263902, 4295011, 4304377, 4312138, 4321756, 4322638, 4325113, 4326434, 4327944, 435216 , 439770, 443012, 443412, 443592 | Yes | SNOMED condition concept identifiers for dia |

Output:

|  Field |  Description |
| --- | --- |
| condition | Name of the condition |
| condition_concept_id | Condition concept identifier |
| min_age | Minimum age of the people with condition |
| max_age | Maximum age of the people with condition |
| avg_age | Average age of the people with condition |
| stdDev_age | Standard deviation of the people  with condition |
| percentile_25 | Age 25th percentile of the people with condition |
| median_age | Median age  of the people with condition |
| percentile_75 | Age 75th percentile of the people with condition |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition | Type 1 diabetes mellitus |
| condition_concept_id | 201826 |
| min_age | 2006 |
| max_age | 2017 |
| avg_age | 2014 |
| stdDev_age | 3.6 |
| percentile_25 | 2009 |
| median_age | 2013 |
| percentile_75 | 2015 |


CO22: Counts of conditions, stratified by condition type
---

This query is used to count conditions across all condition occurrence records stratified by condition occurrence type

Sample query:

```sql
	SELECT concept_name AS condition_occurrence_type , condition_type_concept_id , count(\*) AS occurrence_type_count

	FROM condition_occurrence

	JOIN concept ON concept_id = condition_type_concept_id

	GROUP BY concept_name, condition_type_concept_id;
```

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| condition_occurrence_type | Name of the condition occurrence type |
| condition_type_concept_id | Concept identifier for condition type |
| occurrence_types_count | Number of occurrence types |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition_occurrence_type |  EHR Chief Complaint |
| condition_type_concept_id |  42894222 |
| occurrence_types_count |  65445068 |


CO23: Distribution of condition occurrence month/year, stratified by condition.
---

This query is used to summary statistics of the condition month/year start dates across all condition occurrence records, stratified by condition (condition_concept_id).  The input to the query is a value  of a condition_concept_id.

Sample query:

```sql
	SELECT        condition_concept_id,

	                concept_name,

	                condition_month_year,

	                count(\*) AS count_occur

	FROM

	        (

	        SELECT        condition_concept_id,

	                        concept_name,

	                        to_char(date_trunc('month',condition_start_date),'MM-YYYY') AS condition_month_year,

	                        date_trunc('month',condition_start_date) AS m1

	                FROM        condition_occurrence, concept

	                WHERE        condition_occurrence.condition_concept_id        = concept.concept_id

	                AND                condition_concept_id                                                = 192279

	        ) AS        m1

	GROUP BY        condition_concept_id,

	                        concept_name,

	                        condition_month_year,

	                        m1

	ORDER BY        m1
```

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 192279 | Yes | Condition concept identifier for 'Diabetic Nephropathy' |

Output:

|  Field |  Description |
| --- | --- |
| condition_concept_id | Concept identifier for condition |
| condition_name | Meaningful and descriptive name for the concept. |
| condition_month_year | The month/year when the instance of the condition is recorded. |
| occurrences_count |  Number of condition occurrences |

Sample output record:

| Field |  Description |
| --- | --- |
| condition_concept_id |  192279 |
| condition_name |  Diabetic nephropathy |
| condition_month_year |  05-2004 |
| occurrences_count |  348 |


CO24: Counts of genders, stratified by condition
---

This query is used to count all genders (gender_concept_id), stratified by condition (condition_concept_id). All existing value combinations are summarized. Since some of the conditions have values only for one of the genders, in order not to present the concept id and name twice, a CASE clause is used.

Sample query:

```sql
	SELECT  ( CASE WHEN (male_id<> null)

	            THEN (male_id)

	            ELSE (female_id) END) as concept_id,

	        ( CASE WHEN (male_concept_name<> null)

	                        THEN (male_concept_name)

	                        ELSE (female_concept_name) END) AS name

	                        , count_male,

	                        count_female FROM (

	SELECT    male_list.condition_concept_id male_id,

	          male_list.concept_name male_concept_name,

	                       male_list.count_male count_male ,

	                       female_list.condition_concept_id female_id,

	                       female_list.concept_name female_concept_name,

	                       female_list.count_female count_female FROM (

	SELECT    condition_concept_id,

	          concept_name,

	          count(\*) AS count_male

	FROM      condition_occurrence, concept

	WHERE     condition_occurrence.condition_concept_id=concept.concept_id

	          AND person_id IN (SELECT person_id

	                           FROM   person

	                           WHERE  gender_concept_id=8507)

	GROUP BY  condition_concept_id, concept_name) male_list

	FULL JOIN (

	SELECT    condition_concept_id,

	          concept_name,

	          count(\*) AS count_female

	FROM      condition_occurrence, concept

	WHERE     condition_occurrence.condition_concept_id=concept.concept_id and

	          person_id in

	          (SELECT person_id

	FROM      person

	WHERE     gender_concept_id =8532)

	GROUP BY  condition_concept_id, concept_name) as female_list

	          on male_list.condition_concept_id=female_list.condition_concept_id)
```

Input:

None

Output:

| Field |  Description |
| --- | --- |
| concept_id | Condition concept identifier |
| name | Concept name |
| count_male | Number of concepts for male patients |
| count_female | Number of concepts for female patients |

Sample output record:

|  Field |  Description |
| --- | --- |
| concept_id |  26711 |
| name |  Chronic pharyngitis |
| count_male |  6234 |
|  count_female |  11598 |


CO25: Counts of condition records per person, stratified by condition.
---

Count number of condition per person stratified by condition.

Sample query:

```sql
	SELECT condition_concept_id, num_of_occurrences, count(\*) num_of_patients

	FROM (

	SELECT condition_concept_id, person_id, count(\*) num_of_occurrences

	FROM condition_occurrence co

	WHERE co.condition_concept_id = 200219

	GROUP BY person_id, condition_concept_id)

	GROUP BY condition_concept_id, num_of_occurrences;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 200219 | Yes | Condition concept identifier for 'Abdominal pain' |

Output:

|  Field |  Description |
| --- | --- |
| condition_concept_id | Condition concept identifier |
| num_occurrences | Number of condition occurrences |
| num_of_patients | Number of patients with num_occurrences |

Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |  200219 |
| num_occurrences |  10 |
| num_of_patients |  3681 |



---