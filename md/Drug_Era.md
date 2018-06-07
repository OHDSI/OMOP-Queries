Drug Era Queries
---

DER01: Which drug_exposure records belong to a drug_era?
---

This query is used to count all gender values (gender_concept_id) for all exposed persons stratified by drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a gender_concept_id and drug_concept_id. If the input is omitted, all existing value combinations are summarized.

Sample query:

    select *

     from        drug_exposure e

     where

             exists

                    (

                    select 1

                    from

                            drug_era r ,

                            concept_ancestor m

                    where

                            r.drug_era_id = 20

                    and r.person_id = e.person_id

                    and r.drug_concept_id = m.ancestor_concept_id

                    and e.drug_concept_id = m.descendant_concept_id

                    and e.drug_exposure_start_date BETWEEN r.drug_era_start_date AND r.drug_era_end_date

                    )

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_era_id | 20 | Yes |   |

Output:

| Field |  Description |
| --- | --- |
| drug_exposure_id | A system-generated unique identifier for each drug exposure. |
| person_id | A foreign key identifier to the person who is subjected to the drug during the drug era. The demographic details of that person are stored in the person table. |
| drug_exposure_start_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| drug_exposure_end_date | The end date for the current instance of drug utilization. |

Sample output record:

|  Field |  Description |
| --- | --- |
| drug_exposure_id | 3052353648 |
| person_id | 690809963 |
| drug_exposure_start_date | 2014-05-01 00:00:00 |
| drug_exposure_end _date | 2014-05-01 00:00:00 |



DER02: What is cost of ERA? - era -> exposure -> cost
---

This query is used to count all gender values (gender_concept_id) for all exposed persons stratified by drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a gender_concept_id and drug_concept_id. If the input is omitted, all existing value combinations are summarized.

Sample query:

    SELECT        sum(nvl(c.total_paid, 0)) as total_cost4era

    FROM        drug_exposure e,

                    cost c

    WHERE

            exists

                    (

                    select        1

                    from        drug_era r,

                                    concept_ancestor m

                    where

                            r.drug_era_id = 20--&era_id

                            and r.person_id = e.person_id

                            and r.drug_concept_id = m.ancestor_concept_id

                            and e.drug_concept_id = m.descendant_concept_id

                            and e.drug_exposure_start_date BETWEEN r.drug_era_start_date AND r.drug_era_end_date

                    )

    AND e. drug_exposure_id = c.cost_event_id

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_era_id | 20 | Yes |   |

Output:

| Field |  Description |
| --- | --- |
| Total_cost4era | Total cost for drug era |

Sample output record:

| Field |  Description |
| --- | --- |
| Total_cost4era | 25.23 |



DER03: What is the number of distinct ingredients per patient?
---

Average number of distinct ingredients for all patients.

Sample query:

    SELECT

            avg(cnt)

    from

            (

                    select

                            count(distinct r.drug_concept_id) cnt,

                            r.person_id

                    FROM

                            drug_era r

                    GROUP BY

                            r.person_id

            )

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| avg |  Average count of distinct ingredient for all patients |

Sample output record:

|  Field |  Value |
| --- | --- |
| avg |  10 |



DER04: What proportion of observation time is a person exposed to a given drug?
---

Sample query:

    SELECT        decode(o.totalObs, 0, 0, 100\*(e.totExposure\*1.0/o.totalObs\*1.0)) as proportion

    FROM

            (

            SELECT        SUM(r.drug_era_end_date - r.drug_era_start_date) AS totExposure,

                            r.person_id

            FROM        drug_era r

            WHERE

                    r.person_id                 = 9717995

            AND        r.drug_concept_id         = 1549080

            group by        r.person_id

            ) e,

            (

            SELECT        sum(p.observation_period_end_date - p.observation_period_start_date) AS totalObs,

                            p.person_id FROM observation_period p

            group by p.person_id

            ) o

    where

            o.person_id = e.person_id

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_concept_id | 1549080 | Yes | Estrogens, Conjugated (USP) |

Output:

|  Field |  Description |
| --- | --- |
| proportion | proportion of observation time is a person exposed to a given drug |

Sample output record:

|  Field |  Value |
| --- | --- |
| proportion |  0.1 |



DER05: For a given indication, what proportion of patients take each indicated treatment?
---

Sample query:

    SELECT tt.concept_id, tt.concept_name, 100\*(tt.cntPersons\*1.0/tt.total\*1.0) AS proportion FROM (

    SELECT c.concept_id, c.concept_name, t.cntPersons, sum(cntPersons) over() AS total

    FROM concept c,

    (SELECT er.drug_concept_id, count(DISTINCT er.person_id) AS cntPersons

    FROM  concept_relationship cr,

             concept_ancestor ca,

          drug_era er

    WHERE cr.concept_id_1 = ca.descendant_concept_id

      and er.drug_concept_id = ca.ancestor_concept_id

      and cr.concept_id_2 = 21001738--&era_id -- &Indication_id

      -- allow only indication relationships

      and cr.relationship_id IN ('Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by')

    GROUP BY er.drug_concept_id, cr.concept_id_2

    ) t

    WHERE t.drug_concept_id = c.concept_id

    ) tt

Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_id | 21001738 | Yes | Cold Symptoms |
| list of relationship_id | 'Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by' | Yes |   |



Output:

|  Field |  Description |
| --- | --- |
| Concept_id | Unique identifier for drug concept |
| Concept_name | Standardized drug name |
| Proportion | Drug that proportion of patients take |

Sample output record:

|  Field |  Value |
| --- | --- |
| Concept_id | 1126658 |
| Concept_name | Hydromorphone |
| Proportion | 0.63270536909000900 |



DER06: For a given class, what proportion of patients take each treatment in the class?
---

Sample query:

    select        tt.concept_id,

                    tt.concept_name,

                    100\*(tt.cntPersons\*1.0/tt.total\*1.0) as proportion_count

    from

            (

            select        c.concept_id,

                            c.concept_name,

                            t.cntPersons,

                            sum(cntPersons) over() as total

            from        concept c,

                            (

                            select        r.drug_concept_id,

                                            count(distinct r.person_id) as cntPersons

                            FROM        concept_ancestor ca,

                                            drug_era r

                            WHERE

                                    ca.ancestor_concept_id        = 4324992

                            AND        r.drug_concept_id                = ca.descendant_concept_id

                            group by

                                    r.drug_concept_id

                            ) t

            where

                    t.drug_concept_id = c.concept_id

            ) tt;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| ancestor_concept_id | 4324992 | Yes | Antithrombins |

Output:

|  Field |  Description |
| --- | --- |
| Concept_id | Unique identifier for drug concept |
| Concept_name | Standardized drug name |
| Proportion_count | Proportion of patients take each treatment in the class |

Sample output record:

|  Field |  Description |
| --- | --- |
| Concept_id | 1301025 |
| Concept_name | Enoxaparin |
| Proportion_count | 90.94584530269177500 |



DER07: What is the average time between eras for a given ingredient? ex. steroids for RA
---

Sample query:

    select

            avg(t.next_era_start - t.drug_era_end_date) as num_days

    from

            (

                    select

                            r.drug_era_end_date,

                            lead(r.drug_era_start_date) over(partition by r.person_id, r.drug_concept_id order by r.drug_era_start_date) as next_era_start

                    from

                            drug_era r

                    where r.drug_concept_id = 1304643

            ) t

    where

            t.next_era_start is not null

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_concept_id | 1304643 | Yes | darbepoetin alfa |

Output:

|  Field |  Description |
| --- | --- |
| Num_days |  Average number of days between drug eras |

Sample output record:

|  Field |  Value |
| --- | --- |
| Num_days |  82 |



DER08: Counts of drug records
---

This query is used to count the drug concepts across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all possible values are summarized. values are summarized.

Sample query:

    SELECT count(1) AS total_count FROM drug_era r WHERE r.drug_concept_id in (1304643, 1549080);

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_concept_id | 1304643, 1549080 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| Total_count |  Total count of the drug concepts for all drug era records |

Sample output record:

|  Field |  Value |
| --- | --- |
| Total_count |  9984588 |



DER09: Counts of persons taking drugs
---

This query is used to count the persons with any number of eras with exposure to a certain drug (drug_concept_id) . The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all possible values are summarized.

Sample query:

    select count(distinct r.person_id) as persons_count

    from drug_era r

    where r.drug_concept_id in (1304643, 1549080);

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_concept_id | 1304643, 1549080 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| persons_count |  Count of persons with any number of eras with exposure to certain drug |

Sample output record:

|  Field |  Value |
| --- | --- |
| persons_count |  1658496 |



DER10: Distribution of drug era end dates
---

This query is used to to provide summary statistics for drug era end dates (drug_era_end_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

    SELECT DISTINCT min(tt.end_date) over () AS min_date

         , max(tt.end_date) over () AS max_date

         , (avg(tt.end_date_num) over ()) + tt.min_date AS avg_date

         , (round(stdDev(tt.end_date_num)) ) AS stdDev_days

         , tt.min_date + (PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.end_date_num ) over ())

                    AS percentile_25_date

         , tt.min_date + (PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY tt.end_date_num ) over ())

             AS median_date

         , tt.min_date + (PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.end_date_num ) over ())

             AS percential_75_date

      FROM

        ( SELECT (t.drug_era_end_date - MIN(t.drug_era_end_date) OVER()) AS end_date_num,

                 t.drug_era_end_date AS end_date,

                 MIN(t.drug_era_end_date) OVER() min_date

          FROM drug_era t

        ) tt

            GROUP BY tt.min_date, tt.end_date, tt.end_date_num;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Min_date | Minimum drug era end date across all drug era records |
| Max_date | Maximum drug era end date across all drug era records |
| Avg_date | Average drug era end date across all drug era records |
| percentile_25_date | 25th percentile of the drug era end date |
| median_date | Median of the drug era end date |
| percentile_75_date | the 75th percentile of the drug era end date |

Sample output record:

|  Field |  Description |
| --- | --- |
| Min_date | 2006-01-01 00:00:00 |
| Max_date | 2017-09-30 00:00:00 |
| Avg_date | 2011-11-16 00:00:00 |
| percentile_25_date | 2008-12-08 00:00:00 |
| median_date | 2011-11-16 00:00:00 |
| percentile_75_date | 2014-10-24 00:00:00 |



DER11: Distribution of drug era start dates
---

This query is used to to provide summary statistics for drug era start dates (drug_era_start_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

    SELECT distinct min(tt.start_date) over () AS min_date , max(tt.start_date) over () AS max_date ,

    avg(tt.start_date_num) over () + tt.min_date AS avg_date , (round(stdDev(tt.start_date_num) over ())) AS stdDev_days ,

    tt.min_date +

    (PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.start_date_num ) over ()) AS percentile_25_date

    , tt.min_date + (PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.start_date_num ) over() ) AS median_date

    , tt.min_date + (PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.start_date_num ) over() ) AS percential_75_date

    FROM (

    SELECT (t.drug_era_start_date - MIN(t.drug_era_start_date) OVER()) AS start_date_num, t.drug_era_start_date AS start_date, MIN(t.drug_era_start_date) OVER() min_date

    FROM drug_era t ) tt

    GROUP BY tt.start_date, tt.start_date_num, tt.min_date;

Input:

None

Output:

|  Field |  Description |
| --- | --- | 
| Min_date | Minimum drug era start date across all drug era records |
| Max_date | Maximum drug era start date across all drug era records |
| Avg_date | Average drug era start date across all drug era records |
| Stddev_days | Standard deviation of drug era start date across all drug era records |
| percentile_25_date | 25th percentile of the drug era start date |
| median_date | Median of the drug era start date |
| percentile_75_date | the 75th percentile of the drug era start date |

Sample output record:

|  Field |  Description |
| --- | --- |
| Min_date | 1997-01-01 00:00:00 |
| Max_date | 2017-12-31 00:00:00 |
| Avg_date | 2007-07-02 00:00:00 |
| Stddev_days | 2214 |
| percentile_25_date | 2002-04-02 00:00:00 |
| median_date | 2007-07-02 00:00:00 |
| percentile_75_date | 2012-10-01 00:00:00 |



DER12: Counts of drug types
---

This query is used to count the drug types (drug_type_concept_id) across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug_type_concept_id. If the input is ommitted, all possible values are summarized.

Sample query:

    select count(1) as cntRecs, r.drug_type_concept_id

    from drug_exposure r

    group by r.drug_type_concept_id;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| cntrecs |  Count of drug types |
| drug_type_concept_id | Drug type standardized unique identifier |

Sample output record:

|  Field |  Value |
| --- | --- |
| cntrecs | 6544017 |
| drug_type_concept_id | 38000179 |

DER13: Distribution of number of distinct drugs persons take
---

This query is used to provide summary statistics for the number of number of different distinct drugs (drug_concept_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

    with tt as (

      SELECT

        count(distinct t.drug_concept_id) AS stat_value

      FROM drug_era t

      where nvl(t.drug_concept_id, 0) > 0

      group by t.person_id

    )

    SELECT

      min(tt.stat_value) AS min_value,

      max(tt.stat_value) AS max_value,

      avg(tt.stat_value) AS avg_value,

      (round(stdDev(tt.stat_value)) ) AS stdDev_value ,

      (select distinct PERCENTILE_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat_value) OVER() from tt) AS percentile_25,

      (select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS median_value,

      (select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS percential_75

    FROM tt

    ;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Min_value | Minimum number of distinct drugs persons take |
| Max_value | Maximum number of distinct drugs persons take |
| Avg_value | Average number of distinct drugs persons take |
| Stdev_value | Standard deviation of drug era start date across all drug era records |
| percentile_25_date | 25th percentile number of distinct drugs persons take |
| median_date | Median number of distinct drugs persons take |
| percentile_75_date | the 75th percentile number of distinct drugs persons take |

Sample output record:

|  Field |  Description |
| --- | --- |
| Min_value | 1 |
| Max_value | 580 |
| Avg_value | 12 |
| Stdev_value | 17 |
| percentile_25_date | 3 |
| median_date | 6 |
| percentile_75_date | 16 |



DER14: Counts of number of distinct drugs persons take
---

This query is used to count the number of different distinct drugs (drug_concept_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of concepts. If the input is ommitted, all possible values are summarized.

Sample query:

    SELECT count(

    distinct t.drug_concept_id) AS drug_count, t.person_id

    FROM drug_era t

    group by t.person_id

    having count(

    distinct t.drug_concept_id)

    in (3, 4);

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_type_concept_id | 3, 4 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| Drug_count | Counts of number of distinct drugs |
| Person_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |

Sample output record:

|  Field |  Description |
| --- | --- |
| Drug_count | 3 |
| Person_id | 17 |



DER15: Distribution of drug era records per person
---

This query is used to provide summary statistics for the number of drug era records (drug_era_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

Sample query:

    with tt as

    (

      SELECT count(1) AS stat_value

      FROM drug_era t

      group by t.person_id

    )

    SELECT

      min(tt.stat_value) AS min_value ,

      max(tt.stat_value) AS max_value ,

      avg(tt.stat_value) AS avg_value ,

      (round(stdDev(tt.stat_value)) ) AS stdDev_value,

      (select distinct PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS percentile_25,

      (select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS median_value,

      (select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS percential_75

    FROM tt;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| Min_value | Minimum number of drug era records for all persons |
| Max_value | Maximum number of drug era records for all persons |
| Avg_value | Average number of drug era records for all persons |
| Stdev_value | Standard deviation of drug era record count across all drug era records |
| percentile_25_date | 25th percentile number of drug era record count for all persons |
| median_date | Median number of drug era record for all persons |
| percentile_75_date | the 75th percentile number of drug era record for all persons |

Sample output record:

|  Field |  Description |
| --- | --- |
| Min_value | 1 |
| Max_value | 1908 |
| Avg_value | 23 |
| Stdev_value | 47 |
| percentile_25_date | 3 |
| median_date | 7 |
| percentile_75_date | 22 |



DER16: Counts of drug era records per person
---

This query is used to count the number of drug era records (drug_era_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is ommitted, all possible values are summarized.

Sample query:

    SELECT

      count(1) AS s_count,

      t.person_id

    FROM drug_era t

    group by t.person_id

    having count(1) in (3, 4);

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_type_concept_id | 3, 4 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| s_count | number of drug era records for all persons. |
| person_id | Person unique identifier |

Sample output record:

|  Field |  Description |
| --- | --- |
| s_count |  4 |
| person_id | 10015532 |



DER17: Counts of drug era records stratified by observation month
---

This query is used to count the drug era records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is ommitted, all possible values are summarized.

Sample query:

    SELECT extract(month

    FROM er.drug_era_start_date) month_num, COUNT(1) as eras_in_month_count

    FROM drug_era er

    WHERE extract(month

    FROM er.drug_era_start_date)

    IN (3, 5)

    GROUP BY extract(month

    FROM er.drug_era_start_date)

    ORDER BY 1;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of month numbers | 3, 5 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| month_num | Month number (ex. 3 is March) |
| eras_in_month_count | Number of drug era count per month |

Sample output record:

|  Field |  Description |
| --- | --- |
| month_num |  3 |
| eras_in_month_count | 19657680 |



DER18: Distribution of age, stratified by drug
---

This query is used to provide summary statistics for the age across all drug era records stratified by drug (drug_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, age is summarized for all existing drug_concept_id values.

Sample query:

    SELECT DISTINCT tt.drug_concept_id,

            min(tt.stat_value) over () AS min_value,

            max(tt.stat_value) over () AS max_value,

            avg(tt.stat_value) over () AS avg_value,

            PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) over() AS percentile_25,

            PERCENTILE_DISC(0.5)  WITHIN GROUP( ORDER BY tt.stat_value ) over() AS median_value,

            PERCENTILE_DISC(0.75) WITHIN GROUP( ORDER BY tt.stat_value ) over() AS percential_75

            FROM

        (

            SELECT

          extract(year from (min(t.drug_era_start_date) over(partition by t.person_id, t.drug_concept_id) )) - p.year_of_birth as stat_value,

          t.drug_concept_id

          FROM drug_era t, person p

          WHERE t.person_id = p.person_id

           and t.drug_concept_id in (1300978, 1304643, 1549080)

        ) tt



Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of concept_id | 1300978, 1304643, 1549080 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| Drug_concept_id | Unique identifier for drug |
| Min_value | Minimum number of drug era records for drug |
| Max_value | Maximum number of drug era records for drug |
| Avg_value | Average number of drug era records for drug |
| percentile_25_date | 25th percentile number of drug era records for drug |
| median_date | Median number of drug era records for drug |
| percentile_75_date | the 75th percentile number of drug era records for drug |

Sample output record:

|  Field |  Description |
| --- | --- |
| Drug_concept_id | 1304643 |
| Min_value | 0 |
| Max_value | 108 |
| Avg_value | 69 |
| percentile_25_date | 59 |
| median_date | 70 |
| percentile_75_date | 80 |

DER20: Counts of drugs, stratified by drug type and drug exposure count
---

This query is used to count drugs (drug_concept_id) across all drug exposure records stratified by drug exposure type (drug_type_concept_id, in CDM V2 drug_exposure_type) and drug exposure count (drug_exposure_count) for each era. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id, a drug_type_concept_id and a drug_exposure_count. If the input is omitted, all existing value combinations are summarized.

Sample query:

    with tt as (

      SELECT

        extract(year from (min(t.drug_era_start_date) over(partition by t.person_id, t.drug_concept_id))) - p.year_of_birth as stat_value,

        t.drug_concept_id

      FROM

        drug_era t,

        person p

      where

        t.person_id = p.person_id and

        t.drug_concept_id in (1300978, 1304643, 1549080)   --input

    )

    SELECT

      tt.drug_concept_id,

      min(tt.stat_value) AS min_value,

      max(tt.stat_value) AS max_value,

      avg(tt.stat_value) AS avg_value,

      (round(stdDev(tt.stat_value)) ) AS stdDev_value ,

      (select distinct PERCENTILE_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat_value) OVER() from tt) AS percentile_25,

      (select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS median_value,

      (select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS percential_75

    FROM tt

    group by drug_concept_id;



Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_id |   | Yes |   |
| drug_exposure_count |   | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| drug_concept_id |  A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| min_value |   |
| max_value |   |
| avg_value |   |
| stddev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| drug_concept_id |  1300978 |
| min_value | 0 |
| max_value | 89 |
| avg_value | 65 |
| stddev_value | 14 |
| percentile_25 | 59 |
| median_value | 70 |
| percentile_75 | 80 |



DER21: Counts of drugs, stratified by year, age group and gender
---

This query is used to count drugs (drug_concept_id) across all drug era records stratified by year, age group and gender (gender_concept_id). The age groups are calculated as 10 year age bands from the age of a person at the drug era start date. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id , year, age_group (10 year age band) and gender_concept_id. If the input is omitted, all existing value combinations are summarized.

Sample query:

    SELECT

      tt.drug_concept_id,

      count(1) as s_count,

      tt.age_band,

      tt.year_of_Era,

      tt.gender_concept_id

    from (

      SELECT

        floor( (extract(year from t.drug_era_start_date ) - p.year_of_birth )/10 ) as age_band,

            extract(year from t.drug_era_start_date) as year_of_era,

            p.gender_concept_id,

            t.drug_concept_id

      FROM

        drug_era t,

        person p

      where

        t.person_id = p.person_id and

        t.drug_concept_id in (1300978, 1304643, 1549080)

    ) tt

    where

      tt.age_band in(3,4) and

      tt.year_of_Era in( 2007, 2008)

    group by

      tt.age_band,

      tt.year_of_Era,

      tt.gender_concept_id,

      tt.drug_concept_id

    order by

      tt.age_band,

      tt.year_of_Era,

      tt.gender_concept_id,

      tt.drug_concept_id

    ;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of concept_id | 1300978, 1304643, 1549080 | Yes |   |
| list of year_of_era | 2007, 2008 | Yes |   |

Output:

| Field |  Description |
| --- | --- |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| s_count | Count of drug group by age and gender |
| age_band | The number of individual drug exposure occurrences used to construct the drug era. |
| year_of_era | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| gender_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |

Sample output record:

|  Field |  Description |
| --- | --- |
| drug_concept_id | 1304643 |
| s_count | 5 |
| age_band | 3 |
| year_of_era | 2007 |
| gender_concept_id | 8507 |



DER23: Distribution of drug era start dates, stratified by drug
---

This query is used to summary statistics of the drug era start dates (drug_era_start_date) across all drug era records, stratified by drug (drug_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all possible values are summarized.

Sample query:

    with tt as (

      SELECT

        (t.drug_era_start_date - MIN(t.drug_era_start_date) OVER(partition by t.drug_concept_id)) AS start_date_num,

        t.drug_era_start_date AS start_date, MIN(t.drug_era_start_date) OVER(partition by t.drug_concept_id) min_date,

        t.drug_concept_id

      FROM drug_era t

      where t.drug_concept_id in (1300978, 1304643, 1549080)

    )

    SELECT

      tt.drug_concept_id,

      min(tt.start_date_num) AS min_value,

      max(tt.start_date_num) AS max_value,

      tt.min_date+avg(tt.start_date_num) AS avg_value,

      (round(stdDev(tt.start_date_num)) ) AS stdDev_value ,

      tt.min_date+(select distinct PERCENTILE_DISC(0.25) WITHIN GROUP(ORDER BY tt.start_date_num) OVER() from tt) AS percentile_25,

      tt.min_date+(select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.start_date_num) OVER() from tt) AS median_value,

      tt.min_date+(select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.start_date_num) OVER() from tt) AS percential_75

    FROM tt

    group by

      drug_concept_id,

      tt.min_date

    order by

      drug_concept_id

    ;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_concept_id | 1300978, 1304643, 1549080 | Yes |   |

Output:

| Field |  Description |
| --- | --- |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| min_value |   |
| max_value |   |
| avg_value | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |
| stddev_value |   |
| percentile_25 |      |
| median_value |      |
| percentile_75 |      |

Sample output record:

| Field |  Description |
| --- | --- |
| drug_concept_id | 1300978 |
| min_value | 0 |
| max_value | 7156 |
| avg_value | 2006-04-13 00:00:00 |
| stddev_value | 1808 |
| percentile_25 | 2000-03-21 00:00:00 |
| median_value | 2002-07-29 00:00:00 |
| percentile_75 | 2005-01-15 00:00:00 |



DER26: Counts of genders, stratified by drug
---

This query is used to count all genders (gender concept_id), stratified by drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a gender_concept_id and a drug_concept_id. If the input is ommitted, all existing value combinations are summarized.

Sample query:

    SELECT p.gender_concept_id, count(1) AS stat_value, t.drug_concept_id

    FROM drug_era t, person p

    WHERE t.drug_concept_id

    IN (1300978, 1304643, 1549080)

    AND p.person_id = t.person_id

    AND p.gender_concept_id

    IN (8507, 8532)

    GROUP BY t.drug_concept_id, p.gender_concept_id

    ORDER BY t.drug_concept_id, p.gender_concept_id;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of gender_concept_id | 8507, 8532 | Yes | Male, Female |
| list of drug_concept_id | 1300978, 1304643, 1549080 | Yes |   |

Output:

|  Field |  Description |
| --- | --- | 
| gender_concept_id |   |
| stat_valu |   |
| drug_concept_id |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| gender_concept_id | 8507 |
| stat_value | 60 |
| drug_concept_id | 1300978 |



