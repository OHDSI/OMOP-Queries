**DER01:** Which drug\_exposure records belong to a drug\_era?

This query is used to count all gender values (gender\_concept\_id) for all exposed persons stratified by drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a gender\_concept\_id and drug\_concept\_id. If the input is omitted, all existing value combinations are summarized.

**Sample query:**

select \*

 from        drug\_exposure e

 where

         exists

                (

                select 1

                from

                        drug\_era r ,

                        concept\_ancestor m

                where

                        r.drug\_era\_id = 20

                and r.person\_id = e.person\_id

                and r.drug\_concept\_id = m.ancestor\_concept\_id

                and e.drug\_concept\_id = m.descendant\_concept\_id

                and e.drug\_exposure\_start\_date BETWEEN r.drug\_era\_start\_date AND r.drug\_era\_end\_date

                )

**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| drug\_era\_id | 20 | Yes |   |

**Output:**

| **Field** | ** Description** |
| --- | --- |
| drug\_exposure\_id | A system-generated unique identifier for each drug exposure. |
| person\_id | A foreign key identifier to the person who is subjected to the drug during the drug era. The demographic details of that person are stored in the person table. |
| drug\_exposure\_start\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| drug\_exposure\_end\_date | The end date for the current instance of drug utilization. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_exposure\_id | 3052353648 |
| person\_id | 690809963 |
| drug\_exposure\_start\_date | 2014-05-01 00:00:00 |
| drug\_exposure\_end \_date | 2014-05-01 00:00:00 |
**DER02:** What is cost of ERA? - era -> exposure -> cost

This query is used to count all gender values (gender\_concept\_id) for all exposed persons stratified by drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a gender\_concept\_id and drug\_concept\_id. If the input is omitted, all existing value combinations are summarized.

**Sample query:**

SELECT        sum(nvl(c.total\_paid, 0)) as total\_cost4era

FROM        drug\_exposure e,

                cost c

WHERE

        exists

                (

                select        1

                from        drug\_era r,

                                concept\_ancestor m

                where

                        r.drug\_era\_id = 20--&era\_id

                        and r.person\_id = e.person\_id

                        and r.drug\_concept\_id = m.ancestor\_concept\_id

                        and e.drug\_concept\_id = m.descendant\_concept\_id

                        and e.drug\_exposure\_start\_date BETWEEN r.drug\_era\_start\_date AND r.drug\_era\_end\_date

                )

AND e. drug\_exposure\_id = c.cost\_event\_id

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_era\_id | 20 | Yes |   |

**Output:**

| **Field** | ** Description** |
| --- | --- |
| Total\_cost4era | Total cost for drug era |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| Total\_cost4era | 25.23 |
**DER03:** What is the number of distinct ingredients per patient?

Average number of distinct ingredients for all patients.

**Sample query:**

SELECT

        avg(cnt)

from

        (

                select

                        count(distinct r.drug\_concept\_id) cnt,

                        r.person\_id

                FROM

                        drug\_era r

                GROUP BY

                        r.person\_id

        )

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| avg |  Average count of distinct ingredient for all patients |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| avg |  10 |
**DER04:** What proportion of observation time is a person exposed to a given drug?

**Sample query:**

SELECT        decode(o.totalObs, 0, 0, 100\*(e.totExposure\*1.0/o.totalObs\*1.0)) as proportion

FROM

        (

        SELECT        SUM(r.drug\_era\_end\_date - r.drug\_era\_start\_date) AS totExposure,

                        r.person\_id

        FROM        drug\_era r

        WHERE

                r.person\_id                 = 9717995

        AND        r.drug\_concept\_id         = 1549080

        group by        r.person\_id

        ) e,

        (

        SELECT        sum(p.observation\_period\_end\_date - p.observation\_period\_start\_date) AS totalObs,

                        p.person\_id FROM observation\_period p

        group by p.person\_id

        ) o

where

        o.person\_id = e.person\_id

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 1549080 | Yes | Estrogens, Conjugated (USP) |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| proportion |
###  proportion of observation time is a person exposed to a given drug
 |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| proportion |  0.1 |
**DER05:** For a given indication, what proportion of patients take each indicated treatment?

**Sample query:**

SELECT tt.concept\_id, tt.concept\_name, 100\*(tt.cntPersons\*1.0/tt.total\*1.0) AS proportion FROM (

SELECT c.concept\_id, c.concept\_name, t.cntPersons, sum(cntPersons) over() AS total

FROM concept c,

(SELECT er.drug\_concept\_id, count(DISTINCT er.person\_id) AS cntPersons

FROM  concept\_relationship cr,

         concept\_ancestor ca,

      drug\_era er

WHERE cr.concept\_id\_1 = ca.descendant\_concept\_id

  and er.drug\_concept\_id = ca.ancestor\_concept\_id

  and cr.concept\_id\_2 = 21001738--&era\_id -- &Indication\_id

  -- allow only indication relationships

  and cr.relationship\_id IN ('Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by')

GROUP BY er.drug\_concept\_id, cr.concept\_id\_2

) t

WHERE t.drug\_concept\_id = c.concept\_id

) tt

**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| concept\_id | 21001738 | Yes | Cold Symptoms |
| list of relationship\_id | 'Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by' | Yes |   |



**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Concept\_id | Unique identifier for drug concept |
| Concept\_name | Standardized drug name |
| Proportion | Drug that proportion of patients take |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| Concept\_id | 1126658 |
| Concept\_name | Hydromorphone |
| Proportion | 0.63270536909000900 |
**DER06:** For a given class, what proportion of patients take each treatment in the class?

**Sample query:**

select        tt.concept\_id,

                tt.concept\_name,

                100\*(tt.cntPersons\*1.0/tt.total\*1.0) as proportion\_count

from

        (

        select        c.concept\_id,

                        c.concept\_name,

                        t.cntPersons,

                        sum(cntPersons) over() as total

        from        concept c,

                        (

                        select        r.drug\_concept\_id,

                                        count(distinct r.person\_id) as cntPersons

                        FROM        concept\_ancestor ca,

                                        drug\_era r

                        WHERE

                                ca.ancestor\_concept\_id        = 4324992

                        AND        r.drug\_concept\_id                = ca.descendant\_concept\_id

                        group by

                                r.drug\_concept\_id

                        ) t

        where

                t.drug\_concept\_id = c.concept\_id

        ) tt;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| ancestor\_concept\_id | 4324992 | Yes | Antithrombins |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Concept\_id | Unique identifier for drug concept |
| Concept\_name | Standardized drug name |
| Proportion\_count | Proportion of patients take each treatment in the class |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Concept\_id | 1301025 |
| Concept\_name | Enoxaparin |
| Proportion\_count | 90.94584530269177500 |
**DER07:** What is the average time between eras for a given ingredient? ex. steroids for RA

**Sample query:**

select

        avg(t.next\_era\_start - t.drug\_era\_end\_date) as num\_days

from

        (

                select

                        r.drug\_era\_end\_date,

                        lead(r.drug\_era\_start\_date) over(partition by r.person\_id, r.drug\_concept\_id order by r.drug\_era\_start\_date) as next\_era\_start

                from

                        drug\_era r

                where r.drug\_concept\_id = 1304643

        ) t

where

        t.next\_era\_start is not null

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 1304643 | Yes | darbepoetin alfa |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Num\_days |  Average number of days between drug eras |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| Num\_days |  82 |
**DER08:** Counts of drug records

This query is used to count the drug concepts across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all possible values are summarized. values are summarized.

**Sample query:**

SELECT count(1) AS total\_count FROM drug\_era r WHERE r.drug\_concept\_id in (1304643, 1549080);

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 1304643, 1549080 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Total\_count |  Total count of the drug concepts for all drug era records |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| Total\_count |  9984588 |
**DER09:** Counts of persons taking drugs

This query is used to count the persons with any number of eras with exposure to a certain drug (drug\_concept\_id) . The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all possible values are summarized.

**Sample query:**

select count(distinct r.person\_id) as persons\_count

from drug\_era r

where r.drug\_concept\_id in (1304643, 1549080);

**Input:**

|   |
| --- |
| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of drug\_concept\_id | 1304643, 1549080 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| persons\_count |  Count of persons with any number of eras with exposure to certain drug |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| persons\_count |  1658496 |
**DER10:** Distribution of drug era end dates

This query is used to to provide summary statistics for drug era end dates (drug\_era\_end\_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

SELECT DISTINCT min(tt.end\_date) over () AS min\_date

     , max(tt.end\_date) over () AS max\_date

     , (avg(tt.end\_date\_num) over ()) + tt.min\_date AS avg\_date

     , (round(stdDev(tt.end\_date\_num)) ) AS stdDev\_days

     , tt.min\_date + (PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.end\_date\_num ) over ())

                AS percentile\_25\_date

     , tt.min\_date + (PERCENTILE\_DISC(0.5)  WITHIN GROUP (ORDER BY tt.end\_date\_num ) over ())

         AS median\_date

     , tt.min\_date + (PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.end\_date\_num ) over ())

         AS percential\_75\_date

  FROM

    ( SELECT (t.drug\_era\_end\_date - MIN(t.drug\_era\_end\_date) OVER()) AS end\_date\_num,

             t.drug\_era\_end\_date AS end\_date,

             MIN(t.drug\_era\_end\_date) OVER() min\_date

      FROM drug\_era t

    ) tt

        GROUP BY tt.min\_date, tt.end\_date, tt.end\_date\_num;

**Input:**

None

**Output:**

|   |
| --- |
| ** Field** | ** Description** |
| Min\_date | Minimum drug era end date across all drug era records |
| Max\_date | Maximum drug era end date across all drug era records |
| Avg\_date | Average drug era end date across all drug era records |
| percentile\_25\_date | 25th percentile of the drug era end date |
| median\_date | Median of the drug era end date |
| percentile\_75\_date | the 75th percentile of the drug era end date |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_date | 2006-01-01 00:00:00 |
| Max\_date | 2017-09-30 00:00:00 |
| Avg\_date | 2011-11-16 00:00:00 |
| percentile\_25\_date | 2008-12-08 00:00:00 |
| median\_date | 2011-11-16 00:00:00 |
| percentile\_75\_date | 2014-10-24 00:00:00 |
**DER11:** Distribution of drug era start dates

This query is used to to provide summary statistics for drug era start dates (drug\_era\_start\_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

SELECT distinct min(tt.start\_date) over () AS min\_date , max(tt.start\_date) over () AS max\_date ,

avg(tt.start\_date\_num) over () + tt.min\_date AS avg\_date , (round(stdDev(tt.start\_date\_num) over ())) AS stdDev\_days ,

tt.min\_date +

(PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\_date\_num ) over ()) AS percentile\_25\_date

, tt.min\_date + (PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\_date\_num ) over() ) AS median\_date

, tt.min\_date + (PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\_date\_num ) over() ) AS percential\_75\_date

FROM (

SELECT (t.drug\_era\_start\_date - MIN(t.drug\_era\_start\_date) OVER()) AS start\_date\_num, t.drug\_era\_start\_date AS start\_date, MIN(t.drug\_era\_start\_date) OVER() min\_date

FROM drug\_era t ) tt

GROUP BY tt.start\_date, tt.start\_date\_num, tt.min\_date;

**Input:**

None

**Output:**

|   |
| --- |
| ** Field** | ** Description** |
| Min\_date | Minimum drug era start date across all drug era records |
| Max\_date | Maximum drug era start date across all drug era records |
| Avg\_date | Average drug era start date across all drug era records |
| Stddev\_days | Standard deviation of drug era start date across all drug era records |
| percentile\_25\_date | 25th percentile of the drug era start date |
| median\_date | Median of the drug era start date |
| percentile\_75\_date | the 75th percentile of the drug era start date |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_date | 1997-01-01 00:00:00 |
| Max\_date | 2017-12-31 00:00:00 |
| Avg\_date | 2007-07-02 00:00:00 |
| Stddev\_days | 2214 |
| percentile\_25\_date | 2002-04-02 00:00:00 |
| median\_date | 2007-07-02 00:00:00 |
| percentile\_75\_date | 2012-10-01 00:00:00 |
**DER12:** Counts of drug types

This query is used to count the drug types (drug\_type\_concept\_id) across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug\_type\_concept\_id. If the input is ommitted, all possible values are summarized.

**Sample query:**

select count(1) as cntRecs, r.drug\_type\_concept\_id

from drug\_exposure r

group by r.drug\_type\_concept\_id;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| cntrecs |  Count of drug types |
| drug\_type\_concept\_id | Drug type standardized unique identifier |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| cntrecs | 6544017 |
| drug\_type\_concept\_id | 38000179 |
**DER13:** Distribution of number of distinct drugs persons take

This query is used to provide summary statistics for the number of number of different distinct drugs (drug\_concept\_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

with tt as (

  SELECT

    count(distinct t.drug\_concept\_id) AS stat\_value

  FROM drug\_era t

  where nvl(t.drug\_concept\_id, 0) > 0

  group by t.person\_id

)

SELECT

  min(tt.stat\_value) AS min\_value,

  max(tt.stat\_value) AS max\_value,

  avg(tt.stat\_value) AS avg\_value,

  (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,

  (select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat\_value) OVER() from tt) AS percentile\_25,

  (select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS median\_value,

  (select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS percential\_75

FROM tt

;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_value | Minimum number of distinct drugs persons take |
| Max\_value | Maximum number of distinct drugs persons take |
| Avg\_value | Average number of distinct drugs persons take |
| Stdev\_value | Standard deviation of drug era start date across all drug era records |
| percentile\_25\_date | 25th percentile number of distinct drugs persons take |
| median\_date | Median number of distinct drugs persons take |
| percentile\_75\_date | the 75th percentile number of distinct drugs persons take |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_value | 1 |
| Max\_value | 580 |
| Avg\_value | 12 |
| Stdev\_value | 17 |
| percentile\_25\_date | 3 |
| median\_date | 6 |
| percentile\_75\_date | 16 |
**DER14:** Counts of number of distinct drugs persons take

This query is used to count the number of different distinct drugs (drug\_concept\_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of concepts. If the input is ommitted, all possible values are summarized.

**Sample query:**

SELECT count(

distinct t.drug\_concept\_id) AS drug\_count, t.person\_id

FROM drug\_era t

group by t.person\_id

having count(

distinct t.drug\_concept\_id)

in (3, 4);

**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of drug\_type\_concept\_id | 3, 4 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Drug\_count | Counts of number of distinct drugs |
| Person\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Drug\_count | 3 |
| Person\_id | 17 |
**DER15:** Distribution of drug era records per person

This query is used to provide summary statistics for the number of drug era records (drug\_era\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

**Sample query:**

with tt as

(

  SELECT count(1) AS stat\_value

  FROM drug\_era t

  group by t.person\_id

)

SELECT

  min(tt.stat\_value) AS min\_value ,

  max(tt.stat\_value) AS max\_value ,

  avg(tt.stat\_value) AS avg\_value ,

  (round(stdDev(tt.stat\_value)) ) AS stdDev\_value,

  (select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS percentile\_25,

  (select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS median\_value,

  (select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS percential\_75

FROM tt;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_value | Minimum number of drug era records for all persons |
| Max\_value | Maximum number of drug era records for all persons |
| Avg\_value | Average number of drug era records for all persons |
| Stdev\_value | Standard deviation of drug era record count across all drug era records |
| percentile\_25\_date | 25th percentile number of drug era record count for all persons |
| median\_date | Median number of drug era record for all persons |
| percentile\_75\_date | the 75th percentile number of drug era record for all persons |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Min\_value | 1 |
| Max\_value | 1908 |
| Avg\_value | 23 |
| Stdev\_value | 47 |
| percentile\_25\_date | 3 |
| median\_date | 7 |
| percentile\_75\_date | 22 |
**DER16:** Counts of drug era records per person

### This query is used to count the number of drug era records (drug\_era\_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is ommitted, all possible values are summarized.

**Sample query:**

SELECT

  count(1) AS s\_count,

  t.person\_id

FROM drug\_era t

group by t.person\_id

having count(1) in (3, 4);

**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of drug\_type\_concept\_id | 3, 4 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| s\_count | number of drug era records for all persons. |
| person\_id | Person unique identifier |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| s\_count |  4 |
| person\_id | 10015532 |
**DER17:** Counts of drug era records stratified by observation month

This query is used to count the drug era records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is ommitted, all possible values are summarized.

**Sample query:**

SELECT extract(month

FROM er.drug\_era\_start\_date) month\_num, COUNT(1) as eras\_in\_month\_count

FROM drug\_era er

WHERE extract(month

FROM er.drug\_era\_start\_date)

IN (3, 5)

GROUP BY extract(month

FROM er.drug\_era\_start\_date)

ORDER BY 1;

**Input:**

|   |
| --- |
| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of month numbers | 3, 5 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| month\_num | Month number (ex. 3 is March) |
| eras\_in\_month\_count | Number of drug era count per month |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| month\_num |  3 |
| eras\_in\_month\_count | 19657680 |
**DER18:** Distribution of age, stratified by drug

This query is used to provide summary statistics for the age across all drug era records stratified by drug (drug\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, age is summarized for all existing drug\_concept\_id values.

**Sample query:**

SELECT DISTINCT tt.drug\_concept\_id,

        min(tt.stat\_value) over () AS min\_value,

        max(tt.stat\_value) over () AS max\_value,

        avg(tt.stat\_value) over () AS avg\_value,

        PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) over() AS percentile\_25,

        PERCENTILE\_DISC(0.5)  WITHIN GROUP( ORDER BY tt.stat\_value ) over() AS median\_value,

        PERCENTILE\_DISC(0.75) WITHIN GROUP( ORDER BY tt.stat\_value ) over() AS percential\_75

        FROM

    (

        SELECT

      extract(year from (min(t.drug\_era\_start\_date) over(partition by t.person\_id, t.drug\_concept\_id) )) - p.year\_of\_birth as stat\_value,

      t.drug\_concept\_id

      FROM drug\_era t, person p

      WHERE t.person\_id = p.person\_id

       and t.drug\_concept\_id in (1300978, 1304643, 1549080)

    ) tt



**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of concept\_id | 1300978, 1304643, 1549080 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| Drug\_concept\_id | Unique identifier for drug |
| Min\_value | Minimum number of drug era records for drug |
| Max\_value | Maximum number of drug era records for drug |
| Avg\_value | Average number of drug era records for drug |
| percentile\_25\_date | 25th percentile number of drug era records for drug |
| median\_date | Median number of drug era records for drug |
| percentile\_75\_date | the 75th percentile number of drug era records for drug |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| Drug\_concept\_id | 1304643 |
| Min\_value | 0 |
| Max\_value | 108 |
| Avg\_value | 69 |
| percentile\_25\_date | 59 |
| median\_date | 70 |
| percentile\_75\_date | 80 |
**DER20:** Counts of drugs, stratified by drug type and drug exposure count

This query is used to count drugs (drug\_concept\_id) across all drug exposure records stratified by drug exposure type (drug\_type\_concept\_id, in CDM V2 drug\_exposure\_type) and drug exposure count (drug\_exposure\_count) for each era. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id, a drug\_type\_concept\_id and a drug\_exposure\_count. If the input is omitted, all existing value combinations are summarized.

**Sample query:**

with tt as (

  SELECT

    extract(year from (min(t.drug\_era\_start\_date) over(partition by t.person\_id, t.drug\_concept\_id))) - p.year\_of\_birth as stat\_value,

    t.drug\_concept\_id

  FROM

    drug\_era t,

    person p

  where

    t.person\_id = p.person\_id and

    t.drug\_concept\_id in (1300978, 1304643, 1549080)   --input

)

SELECT

  tt.drug\_concept\_id,

  min(tt.stat\_value) AS min\_value,

  max(tt.stat\_value) AS max\_value,

  avg(tt.stat\_value) AS avg\_value,

  (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,

  (select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat\_value) OVER() from tt) AS percentile\_25,

  (select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS median\_value,

  (select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS percential\_75

FROM tt

group by drug\_concept\_id;



**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_id |   | Yes |   |
| drug\_exposure\_count |   | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |  A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| min\_value |   |
| max\_value |   |
| avg\_value |   |
| stddev\_value |   |
| percentile\_25 |   |
| median\_value |   |
| percentile\_75 |   |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |  1300978 |
| min\_value | 0 |
| max\_value | 89 |
| avg\_value | 65 |
| stddev\_value | 14 |
| percentile\_25 | 59 |
| median\_value | 70 |
| percentile\_75 | 80 |
**DER21:** Counts of drugs, stratified by year, age group and gender

This query is used to count drugs (drug\_concept\_id) across all drug era records stratified by year, age group and gender (gender\_concept\_id). The age groups are calculated as 10 year age bands from the age of a person at the drug era start date. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id , year, age\_group (10 year age band) and gender\_concept\_id. If the input is omitted, all existing value combinations are summarized.

**Sample query:**

SELECT

  tt.drug\_concept\_id,

  count(1) as s\_count,

  tt.age\_band,

  tt.year\_of\_Era,

  tt.gender\_concept\_id

from (

  SELECT

    floor( (extract(year from t.drug\_era\_start\_date ) - p.year\_of\_birth )/10 ) as age\_band,

        extract(year from t.drug\_era\_start\_date) as year\_of\_era,

        p.gender\_concept\_id,

        t.drug\_concept\_id

  FROM

    drug\_era t,

    person p

  where

    t.person\_id = p.person\_id and

    t.drug\_concept\_id in (1300978, 1304643, 1549080)

) tt

where

  tt.age\_band in(3,4) and

  tt.year\_of\_Era in( 2007, 2008)

group by

  tt.age\_band,

  tt.year\_of\_Era,

  tt.gender\_concept\_id,

  tt.drug\_concept\_id

order by

  tt.age\_band,

  tt.year\_of\_Era,

  tt.gender\_concept\_id,

  tt.drug\_concept\_id

;

**Input:**

|   |
| --- |
| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of concept\_id | 1300978, 1304643, 1549080 | Yes |   |
| list of year\_of\_era | 2007, 2008 | Yes |   |

**Output:**

| **Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| s\_count | Count of drug group by age and gender |
| age\_band | The number of individual drug exposure occurrences used to construct the drug era. |
| year\_of\_era | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| gender\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | 1304643 |
| s\_count | 5 |
| age\_band | 3 |
| year\_of\_era | 2007 |
| gender\_concept\_id | 8507 |
**DER23:** Distribution of drug era start dates, stratified by drug

This query is used to summary statistics of the drug era start dates (drug\_era\_start\_date) across all drug era records, stratified by drug (drug\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all possible values are summarized.

**Sample query:**

with tt as (

  SELECT

    (t.drug\_era\_start\_date - MIN(t.drug\_era\_start\_date) OVER(partition by t.drug\_concept\_id)) AS start\_date\_num,

    t.drug\_era\_start\_date AS start\_date, MIN(t.drug\_era\_start\_date) OVER(partition by t.drug\_concept\_id) min\_date,

    t.drug\_concept\_id

  FROM drug\_era t

  where t.drug\_concept\_id in (1300978, 1304643, 1549080)

)

SELECT

  tt.drug\_concept\_id,

  min(tt.start\_date\_num) AS min\_value,

  max(tt.start\_date\_num) AS max\_value,

  tt.min\_date+avg(tt.start\_date\_num) AS avg\_value,

  (round(stdDev(tt.start\_date\_num)) ) AS stdDev\_value ,

  tt.min\_date+(select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP(ORDER BY tt.start\_date\_num) OVER() from tt) AS percentile\_25,

  tt.min\_date+(select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\_date\_num) OVER() from tt) AS median\_value,

  tt.min\_date+(select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\_date\_num) OVER() from tt) AS percential\_75

FROM tt

group by

  drug\_concept\_id,

  tt.min\_date

order by

  drug\_concept\_id

;

**Input:**

|   |
| --- |
| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| drug\_concept\_id | 1300978, 1304643, 1549080 | Yes |   |

**Output:**

| **Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| min\_value |   |
| max\_value |   |
| avg\_value | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |
| stddev\_value |   |
| percentile\_25 |      |
| median\_value |      |
| percentile\_75 |      |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | 1300978 |
| min\_value | 0 |
| max\_value | 7156 |
| avg\_value | 2006-04-13 00:00:00 |
| stddev\_value | 1808 |
| percentile\_25 | 2000-03-21 00:00:00 |
| median\_value | 2002-07-29 00:00:00 |
| percentile\_75 | 2005-01-15 00:00:00 |
**DER26:** Counts of genders, stratified by drug

This query is used to count all genders (gender concept\_id), stratified by drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a gender\_concept\_id and a drug\_concept\_id. If the input is ommitted, all existing value combinations are summarized.

**Sample query:**

SELECT p.gender\_concept\_id, count(1) AS stat\_value, t.drug\_concept\_id

FROM drug\_era t, person p

WHERE t.drug\_concept\_id

IN (1300978, 1304643, 1549080)

AND p.person\_id = t.person\_id

AND p.gender\_concept\_id

IN (8507, 8532)

GROUP BY t.drug\_concept\_id, p.gender\_concept\_id

ORDER BY t.drug\_concept\_id, p.gender\_concept\_id;

**Input:**

|   |
| --- |
| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of gender\_concept\_id | 8507, 8532 | Yes | Male, Female |
| list of drug\_concept\_id | 1300978, 1304643, 1549080 | Yes |   |

**Output:**

|   |
| --- |
| ** Field** | ** Description** |
| gender\_concept\_id |   |
| stat\_valu |   |
| drug\_concept\_id |   |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| gender\_concept\_id | 8507 |
| stat\_value | 60 |
| drug\_concept\_id | 1300978 |
\*\*DER01:\*\* Which drug\\_exposure records belong to a drug\\_era?

This query is used to count all gender values (gender\\_concept\\_id) for all exposed persons stratified by drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a gender\\_concept\\_id and drug\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Sample query:\*\*

select \\*

 from        drug\\_exposure e

 where

         exists

                (

                select 1

                from

                        drug\\_era r ,

                        concept\\_ancestor m

                where

                        r.drug\\_era\\_id = 20

                and r.person\\_id = e.person\\_id

                and r.drug\\_concept\\_id = m.ancestor\\_concept\\_id

                and e.drug\\_concept\\_id = m.descendant\\_concept\\_id

                and e.drug\\_exposure\\_start\\_date BETWEEN r.drug\\_era\\_start\\_date AND r.drug\\_era\\_end\\_date

                )

\*\*Input:\*\*

|   |

| --- |

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| drug\\_era\\_id | 20 | Yes |   |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_id | A system-generated unique identifier for each drug exposure. |

| person\\_id | A foreign key identifier to the person who is subjected to the drug during the drug era. The demographic details of that person are stored in the person table. |

| drug\\_exposure\\_start\\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |

| drug\\_exposure\\_end\\_date | The end date for the current instance of drug utilization. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_id | 3052353648 |

| person\\_id | 690809963 |

| drug\\_exposure\\_start\\_date | 2014-05-01 00:00:00 |

| drug\\_exposure\\_end \\_date | 2014-05-01 00:00:00 |

\*\*DER02:\*\* What is cost of ERA? - era -> exposure -> cost

This query is used to count all gender values (gender\\_concept\\_id) for all exposed persons stratified by drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a gender\\_concept\\_id and drug\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Sample query:\*\*

SELECT        sum(nvl(c.total\\_paid, 0)) as total\\_cost4era

FROM        drug\\_exposure e,

                cost c

WHERE

        exists

                (

                select        1

                from        drug\\_era r,

                                concept\\_ancestor m

                where

                        r.drug\\_era\\_id = 20--&era\\_id

                        and r.person\\_id = e.person\\_id

                        and r.drug\\_concept\\_id = m.ancestor\\_concept\\_id

                        and e.drug\\_concept\\_id = m.descendant\\_concept\\_id

                        and e.drug\\_exposure\\_start\\_date BETWEEN r.drug\\_era\\_start\\_date AND r.drug\\_era\\_end\\_date

                )

AND e. drug\\_exposure\\_id = c.cost\\_event\\_id

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_era\\_id | 20 | Yes |   |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| Total\\_cost4era | Total cost for drug era |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| Total\\_cost4era | 25.23 |

\*\*DER03:\*\* What is the number of distinct ingredients per patient?

Average number of distinct ingredients for all patients.

\*\*Sample query:\*\*

SELECT

        avg(cnt)

from

        (

                select

                        count(distinct r.drug\\_concept\\_id) cnt,

                        r.person\\_id

                FROM

                        drug\\_era r

                GROUP BY

                        r.person\\_id

        )

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| avg |  Average count of distinct ingredient for all patients |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| avg |  10 |

\*\*DER04:\*\* What proportion of observation time is a person exposed to a given drug?

\*\*Sample query:\*\*

SELECT        decode(o.totalObs, 0, 0, 100\\*(e.totExposure\\*1.0/o.totalObs\\*1.0)) as proportion

FROM

        (

        SELECT        SUM(r.drug\\_era\\_end\\_date - r.drug\\_era\\_start\\_date) AS totExposure,

                        r.person\\_id

        FROM        drug\\_era r

        WHERE

                r.person\\_id                 = 9717995

        AND        r.drug\\_concept\\_id         = 1549080

        group by        r.person\\_id

        ) e,

        (

        SELECT        sum(p.observation\\_period\\_end\\_date - p.observation\\_period\\_start\\_date) AS totalObs,

                        p.person\\_id FROM observation\\_period p

        group by p.person\\_id

        ) o

where

        o.person\\_id = e.person\\_id

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 1549080 | Yes | Estrogens, Conjugated (USP) |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| proportion |

###  proportion of observation time is a person exposed to a given drug

 |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| proportion |  0.1 |

\*\*DER05:\*\* For a given indication, what proportion of patients take each indicated treatment?

\*\*Sample query:\*\*

SELECT tt.concept\\_id, tt.concept\\_name, 100\\*(tt.cntPersons\\*1.0/tt.total\\*1.0) AS proportion FROM (

SELECT c.concept\\_id, c.concept\\_name, t.cntPersons, sum(cntPersons) over() AS total

FROM concept c,

(SELECT er.drug\\_concept\\_id, count(DISTINCT er.person\\_id) AS cntPersons

FROM  concept\\_relationship cr,

         concept\\_ancestor ca,

      drug\\_era er

WHERE cr.concept\\_id\\_1 = ca.descendant\\_concept\\_id

  and er.drug\\_concept\\_id = ca.ancestor\\_concept\\_id

  and cr.concept\\_id\\_2 = 21001738--&era\\_id -- &Indication\\_id

  -- allow only indication relationships

  and cr.relationship\\_id IN ('Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by')

GROUP BY er.drug\\_concept\\_id, cr.concept\\_id\\_2

) t

WHERE t.drug\\_concept\\_id = c.concept\\_id

) tt

\*\*Input:\*\*

|   |

| --- |

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| concept\\_id | 21001738 | Yes | Cold Symptoms |

| list of relationship\\_id | 'Has FDA-appr ind', 'Has off-label ind', 'May treat', 'May prevent', 'CI by', 'Is off-label ind of', 'Is FDA-appr ind of', 'May be treated by' | Yes |   |



\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Concept\\_id | Unique identifier for drug concept |

| Concept\\_name | Standardized drug name |

| Proportion | Drug that proportion of patients take |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| Concept\\_id | 1126658 |

| Concept\\_name | Hydromorphone |

| Proportion | 0.63270536909000900 |

\*\*DER06:\*\* For a given class, what proportion of patients take each treatment in the class?

\*\*Sample query:\*\*

select        tt.concept\\_id,

                tt.concept\\_name,

                100\\*(tt.cntPersons\\*1.0/tt.total\\*1.0) as proportion\\_count

from

        (

        select        c.concept\\_id,

                        c.concept\\_name,

                        t.cntPersons,

                        sum(cntPersons) over() as total

        from        concept c,

                        (

                        select        r.drug\\_concept\\_id,

                                        count(distinct r.person\\_id) as cntPersons

                        FROM        concept\\_ancestor ca,

                                        drug\\_era r

                        WHERE

                                ca.ancestor\\_concept\\_id        = 4324992

                        AND        r.drug\\_concept\\_id                = ca.descendant\\_concept\\_id

                        group by

                                r.drug\\_concept\\_id

                        ) t

        where

                t.drug\\_concept\\_id = c.concept\\_id

        ) tt;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| ancestor\\_concept\\_id | 4324992 | Yes | Antithrombins |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Concept\\_id | Unique identifier for drug concept |

| Concept\\_name | Standardized drug name |

| Proportion\\_count | Proportion of patients take each treatment in the class |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Concept\\_id | 1301025 |

| Concept\\_name | Enoxaparin |

| Proportion\\_count | 90.94584530269177500 |

\*\*DER07:\*\* What is the average time between eras for a given ingredient? ex. steroids for RA

\*\*Sample query:\*\*

select

        avg(t.next\\_era\\_start - t.drug\\_era\\_end\\_date) as num\\_days

from

        (

                select

                        r.drug\\_era\\_end\\_date,

                        lead(r.drug\\_era\\_start\\_date) over(partition by r.person\\_id, r.drug\\_concept\\_id order by r.drug\\_era\\_start\\_date) as next\\_era\\_start

                from

                        drug\\_era r

                where r.drug\\_concept\\_id = 1304643

        ) t

where

        t.next\\_era\\_start is not null

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 1304643 | Yes | darbepoetin alfa |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Num\\_days |  Average number of days between drug eras |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| Num\\_days |  82 |

\*\*DER08:\*\* Counts of drug records

This query is used to count the drug concepts across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all possible values are summarized. values are summarized.

\*\*Sample query:\*\*

SELECT count(1) AS total\\_count FROM drug\\_era r WHERE r.drug\\_concept\\_id in (1304643, 1549080);

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 1304643, 1549080 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Total\\_count |  Total count of the drug concepts for all drug era records |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| Total\\_count |  9984588 |

\*\*DER09:\*\* Counts of persons taking drugs

This query is used to count the persons with any number of eras with exposure to a certain drug (drug\\_concept\\_id) . The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all possible values are summarized.

\*\*Sample query:\*\*

select count(distinct r.person\\_id) as persons\\_count

from drug\\_era r

where r.drug\\_concept\\_id in (1304643, 1549080);

\*\*Input:\*\*

|   |

| --- |

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of drug\\_concept\\_id | 1304643, 1549080 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| persons\\_count |  Count of persons with any number of eras with exposure to certain drug |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| persons\\_count |  1658496 |

\*\*DER10:\*\* Distribution of drug era end dates

This query is used to to provide summary statistics for drug era end dates (drug\\_era\\_end\\_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

SELECT DISTINCT min(tt.end\\_date) over () AS min\\_date

     , max(tt.end\\_date) over () AS max\\_date

     , (avg(tt.end\\_date\\_num) over ()) + tt.min\\_date AS avg\\_date

     , (round(stdDev(tt.end\\_date\\_num)) ) AS stdDev\\_days

     , tt.min\\_date + (PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.end\\_date\\_num ) over ())

                AS percentile\\_25\\_date

     , tt.min\\_date + (PERCENTILE\\_DISC(0.5)  WITHIN GROUP (ORDER BY tt.end\\_date\\_num ) over ())

         AS median\\_date

     , tt.min\\_date + (PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.end\\_date\\_num ) over ())

         AS percential\\_75\\_date

  FROM

    ( SELECT (t.drug\\_era\\_end\\_date - MIN(t.drug\\_era\\_end\\_date) OVER()) AS end\\_date\\_num,

             t.drug\\_era\\_end\\_date AS end\\_date,

             MIN(t.drug\\_era\\_end\\_date) OVER() min\\_date

      FROM drug\\_era t

    ) tt

        GROUP BY tt.min\\_date, tt.end\\_date, tt.end\\_date\\_num;

\*\*Input:\*\*

None

\*\*Output:\*\*

|   |

| --- |

| \*\* Field\*\* | \*\* Description\*\* |

| Min\\_date | Minimum drug era end date across all drug era records |

| Max\\_date | Maximum drug era end date across all drug era records |

| Avg\\_date | Average drug era end date across all drug era records |

| percentile\\_25\\_date | 25th percentile of the drug era end date |

| median\\_date | Median of the drug era end date |

| percentile\\_75\\_date | the 75th percentile of the drug era end date |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_date | 2006-01-01 00:00:00 |

| Max\\_date | 2017-09-30 00:00:00 |

| Avg\\_date | 2011-11-16 00:00:00 |

| percentile\\_25\\_date | 2008-12-08 00:00:00 |

| median\\_date | 2011-11-16 00:00:00 |

| percentile\\_75\\_date | 2014-10-24 00:00:00 |

\*\*DER11:\*\* Distribution of drug era start dates

This query is used to to provide summary statistics for drug era start dates (drug\\_era\\_start\\_date) across all drug era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

SELECT distinct min(tt.start\\_date) over () AS min\\_date , max(tt.start\\_date) over () AS max\\_date ,

avg(tt.start\\_date\\_num) over () + tt.min\\_date AS avg\\_date , (round(stdDev(tt.start\\_date\\_num) over ())) AS stdDev\\_days ,

tt.min\\_date +

(PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\\_date\\_num ) over ()) AS percentile\\_25\\_date

, tt.min\\_date + (PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) over() ) AS median\\_date

, tt.min\\_date + (PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) over() ) AS percential\\_75\\_date

FROM (

SELECT (t.drug\\_era\\_start\\_date - MIN(t.drug\\_era\\_start\\_date) OVER()) AS start\\_date\\_num, t.drug\\_era\\_start\\_date AS start\\_date, MIN(t.drug\\_era\\_start\\_date) OVER() min\\_date

FROM drug\\_era t ) tt

GROUP BY tt.start\\_date, tt.start\\_date\\_num, tt.min\\_date;

\*\*Input:\*\*

None

\*\*Output:\*\*

|   |

| --- |

| \*\* Field\*\* | \*\* Description\*\* |

| Min\\_date | Minimum drug era start date across all drug era records |

| Max\\_date | Maximum drug era start date across all drug era records |

| Avg\\_date | Average drug era start date across all drug era records |

| Stddev\\_days | Standard deviation of drug era start date across all drug era records |

| percentile\\_25\\_date | 25th percentile of the drug era start date |

| median\\_date | Median of the drug era start date |

| percentile\\_75\\_date | the 75th percentile of the drug era start date |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_date | 1997-01-01 00:00:00 |

| Max\\_date | 2017-12-31 00:00:00 |

| Avg\\_date | 2007-07-02 00:00:00 |

| Stddev\\_days | 2214 |

| percentile\\_25\\_date | 2002-04-02 00:00:00 |

| median\\_date | 2007-07-02 00:00:00 |

| percentile\\_75\\_date | 2012-10-01 00:00:00 |

\*\*DER12:\*\* Counts of drug types

This query is used to count the drug types (drug\\_type\\_concept\\_id) across all drug era records. The input to the query is a value (or a comma-separated list of values) of a drug\\_type\\_concept\\_id. If the input is ommitted, all possible values are summarized.

\*\*Sample query:\*\*

select count(1) as cntRecs, r.drug\\_type\\_concept\\_id

from drug\\_exposure r

group by r.drug\\_type\\_concept\\_id;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| cntrecs |  Count of drug types |

| drug\\_type\\_concept\\_id | Drug type standardized unique identifier |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| cntrecs | 6544017 |

| drug\\_type\\_concept\\_id | 38000179 |

\*\*DER13:\*\* Distribution of number of distinct drugs persons take

This query is used to provide summary statistics for the number of number of different distinct drugs (drug\\_concept\\_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Sample query:\*\*

with tt as (

  SELECT

    count(distinct t.drug\\_concept\\_id) AS stat\\_value

  FROM drug\\_era t

  where nvl(t.drug\\_concept\\_id, 0) > 0

  group by t.person\\_id

)

SELECT

  min(tt.stat\\_value) AS min\\_value,

  max(tt.stat\\_value) AS max\\_value,

  avg(tt.stat\\_value) AS avg\\_value,

  (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,

  (select distinct PERCENTILE\\_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat\\_value) OVER() from tt) AS percentile\\_25,

  (select distinct PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS median\\_value,

  (select distinct PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS percential\\_75

FROM tt

;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_value | Minimum number of distinct drugs persons take |

| Max\\_value | Maximum number of distinct drugs persons take |

| Avg\\_value | Average number of distinct drugs persons take |

| Stdev\\_value | Standard deviation of drug era start date across all drug era records |

| percentile\\_25\\_date | 25th percentile number of distinct drugs persons take |

| median\\_date | Median number of distinct drugs persons take |

| percentile\\_75\\_date | the 75th percentile number of distinct drugs persons take |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_value | 1 |

| Max\\_value | 580 |

| Avg\\_value | 12 |

| Stdev\\_value | 17 |

| percentile\\_25\\_date | 3 |

| median\\_date | 6 |

| percentile\\_75\\_date | 16 |

\*\*DER14:\*\* Counts of number of distinct drugs persons take

This query is used to count the number of different distinct drugs (drug\\_concept\\_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of concepts. If the input is ommitted, all possible values are summarized.

\*\*Sample query:\*\*

SELECT count(

distinct t.drug\\_concept\\_id) AS drug\\_count, t.person\\_id

FROM drug\\_era t

group by t.person\\_id

having count(

distinct t.drug\\_concept\\_id)

in (3, 4);

\*\*Input:\*\*

|   |

| --- |

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of drug\\_type\\_concept\\_id | 3, 4 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Drug\\_count | Counts of number of distinct drugs |

| Person\\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Drug\\_count | 3 |

| Person\\_id | 17 |

\*\*DER15:\*\* Distribution of drug era records per person

This query is used to provide summary statistics for the number of drug era records (drug\\_era\\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

\*\*Sample query:\*\*

with tt as

(

  SELECT count(1) AS stat\\_value

  FROM drug\\_era t

  group by t.person\\_id

)

SELECT

  min(tt.stat\\_value) AS min\\_value ,

  max(tt.stat\\_value) AS max\\_value ,

  avg(tt.stat\\_value) AS avg\\_value ,

  (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value,

  (select distinct PERCENTILE\\_DISC(0.25) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS percentile\\_25,

  (select distinct PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS median\\_value,

  (select distinct PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS percential\\_75

FROM tt;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_value | Minimum number of drug era records for all persons |

| Max\\_value | Maximum number of drug era records for all persons |

| Avg\\_value | Average number of drug era records for all persons |

| Stdev\\_value | Standard deviation of drug era record count across all drug era records |

| percentile\\_25\\_date | 25th percentile number of drug era record count for all persons |

| median\\_date | Median number of drug era record for all persons |

| percentile\\_75\\_date | the 75th percentile number of drug era record for all persons |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Min\\_value | 1 |

| Max\\_value | 1908 |

| Avg\\_value | 23 |

| Stdev\\_value | 47 |

| percentile\\_25\\_date | 3 |

| median\\_date | 7 |

| percentile\\_75\\_date | 22 |

\*\*DER16:\*\* Counts of drug era records per person

### This query is used to count the number of drug era records (drug\\_era\\_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is ommitted, all possible values are summarized.

\*\*Sample query:\*\*

SELECT

  count(1) AS s\\_count,

  t.person\\_id

FROM drug\\_era t

group by t.person\\_id

having count(1) in (3, 4);

\*\*Input:\*\*

|   |

| --- |

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of drug\\_type\\_concept\\_id | 3, 4 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| s\\_count | number of drug era records for all persons. |

| person\\_id | Person unique identifier |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| s\\_count |  4 |

| person\\_id | 10015532 |

\*\*DER17:\*\* Counts of drug era records stratified by observation month

This query is used to count the drug era records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is ommitted, all possible values are summarized.

\*\*Sample query:\*\*

SELECT extract(month

FROM er.drug\\_era\\_start\\_date) month\\_num, COUNT(1) as eras\\_in\\_month\\_count

FROM drug\\_era er

WHERE extract(month

FROM er.drug\\_era\\_start\\_date)

IN (3, 5)

GROUP BY extract(month

FROM er.drug\\_era\\_start\\_date)

ORDER BY 1;

\*\*Input:\*\*

|   |

| --- |

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of month numbers | 3, 5 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| month\\_num | Month number (ex. 3 is March) |

| eras\\_in\\_month\\_count | Number of drug era count per month |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| month\\_num |  3 |

| eras\\_in\\_month\\_count | 19657680 |

\*\*DER18:\*\* Distribution of age, stratified by drug

This query is used to provide summary statistics for the age across all drug era records stratified by drug (drug\\_concept\\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, age is summarized for all existing drug\\_concept\\_id values.

\*\*Sample query:\*\*

SELECT DISTINCT tt.drug\\_concept\\_id,

        min(tt.stat\\_value) over () AS min\\_value,

        max(tt.stat\\_value) over () AS max\\_value,

        avg(tt.stat\\_value) over () AS avg\\_value,

        PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) over() AS percentile\\_25,

        PERCENTILE\\_DISC(0.5)  WITHIN GROUP( ORDER BY tt.stat\\_value ) over() AS median\\_value,

        PERCENTILE\\_DISC(0.75) WITHIN GROUP( ORDER BY tt.stat\\_value ) over() AS percential\\_75

        FROM

    (

        SELECT

      extract(year from (min(t.drug\\_era\\_start\\_date) over(partition by t.person\\_id, t.drug\\_concept\\_id) )) - p.year\\_of\\_birth as stat\\_value,

      t.drug\\_concept\\_id

      FROM drug\\_era t, person p

      WHERE t.person\\_id = p.person\\_id

       and t.drug\\_concept\\_id in (1300978, 1304643, 1549080)

    ) tt



\*\*Input:\*\*

|   |

| --- |

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of concept\\_id | 1300978, 1304643, 1549080 | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Drug\\_concept\\_id | Unique identifier for drug |

| Min\\_value | Minimum number of drug era records for drug |

| Max\\_value | Maximum number of drug era records for drug |

| Avg\\_value | Average number of drug era records for drug |

| percentile\\_25\\_date | 25th percentile number of drug era records for drug |

| median\\_date | Median number of drug era records for drug |

| percentile\\_75\\_date | the 75th percentile number of drug era records for drug |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Drug\\_concept\\_id | 1304643 |

| Min\\_value | 0 |

| Max\\_value | 108 |

| Avg\\_value | 69 |

| percentile\\_25\\_date | 59 |

| median\\_date | 70 |

| percentile\\_75\\_date | 80 |

\*\*DER20:\*\* Counts of drugs, stratified by drug type and drug exposure count

This query is used to count drugs (drug\\_concept\\_id) across all drug exposure records stratified by drug exposure type (drug\\_type\\_concept\\_id, in CDM V2 drug\\_exposure\\_type) and drug exposure count (drug\\_exposure\\_count) for each era. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id, a drug\\_type\\_concept\\_id and a drug\\_exposure\\_count. If the input is omitted, all existing value combinations are summarized.

\*\*Sample query:\*\*

with tt as (

  SELECT

    extract(year from (min(t.drug\\_era\\_start\\_date) over(partition by t.person\\_id, t.drug\\_concept\\_id))) - p.year\\_of\\_birth as stat\\_value,

    t.drug\\_concept\\_id

  FROM

    drug\\_era t,

    person p

  where

    t.person\\_id = p.person\\_id and

    t.drug\\_concept\\_id in (1300978, 1304643, 1549080)   --input

)

SELECT

  tt.drug\\_concept\\_id,

  min(tt.stat\\_value) AS min\\_value,

  max(tt.stat\\_value) AS max\\_value,

  avg(tt.stat\\_value) AS avg\\_value,

  (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,

  (select distinct PERCENTILE\\_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat\\_value) OVER() from tt) AS percentile\\_25,

  (select distinct PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS median\\_value,

  (select distinct PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value) OVER() from tt) AS percential\\_75

FROM tt

group by drug\\_concept\\_id;



\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_id |   | Yes |   |

| drug\\_exposure\\_count |   | Yes |   |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |  A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| min\\_value |   |

| max\\_value |   |

| avg\\_value |   |

| stddev\\_value |   |

| percentile\\_25 |   |

| median\\_value |   |

| percentile\\_75 |   |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |  1300978 |

| min\\_value | 0 |

| max\\_value | 89 |

| avg\\_value | 65 |

| stddev\\_value | 14 |

| percentile\\_25 | 59 |

| median\\_value | 70 |

| percentile\\_75 | 80 |

\*\*DER21:\*\* Counts of drugs, stratified by year, age group and gender

This query is used to count drugs (drug\\_concept\\_id) across all drug era records stratified by year, age group and gender (gender\\_concept\\_id). The age groups are calculated as 10 year age bands from the age of a person at the drug era start date. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id , year, age\\_group (10 year age band) and gender\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Sample query:\*\*

SELECT

  tt.drug\\_concept\\_id,

  count(1) as s\\_count,

  tt.age\\_band,

  tt.year\\_of\\_Era,

  tt.gender\\_concept\\_id

from (

  SELECT

    floor( (extract(year from t.drug\\_era\\_start\\_date ) - p.year\\_of\\_birth )/10 ) as age\\_band,

        extract(year from t.drug\\_era\\_start\\_date) as year\\_of\\_era,

        p.gender\\_concept\\_id,

        t.drug\\_concept\\_id

  FROM

    drug\\_era t,

    person p

  where

    t.person\\_id = p.person\\_id and

    t.drug\\_concept\\_id in (1300978, 1304643, 1549080)

) tt

where

  tt.age\\_band in(3,4) and

  tt.year\\_of\\_Era in( 2007, 2008)

group by

  tt.age\\_band,

  tt.year\\_of\\_Era,

  tt.gender\\_concept\\_id,

  tt.drug\\_concept\\_id

order by

  tt.age\\_band,

  tt.year\\_of\\_Era,

  tt.gender\\_concept\\_id,

  tt.drug\\_concept\\_id

;

\*\*Input:\*\*

|   |

| --- |

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of concept\\_id | 1300978, 1304643, 1549080 | Yes |   |

| list of year\\_of\\_era | 2007, 2008 | Yes |   |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| s\\_count | Count of drug group by age and gender |

| age\\_band | The number of individual drug exposure occurrences used to construct the drug era. |

| year\\_of\\_era | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |

| gender\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | 1304643 |

| s\\_count | 5 |

| age\\_band | 3 |

| year\\_of\\_era | 2007 |

| gender\\_concept\\_id | 8507 |

\*\*DER23:\*\* Distribution of drug era start dates, stratified by drug

This query is used to summary statistics of the drug era start dates (drug\\_era\\_start\\_date) across all drug era records, stratified by drug (drug\\_concept\\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all possible values are summarized.

\*\*Sample query:\*\*

with tt as (

  SELECT

    (t.drug\\_era\\_start\\_date - MIN(t.drug\\_era\\_start\\_date) OVER(partition by t.drug\\_concept\\_id)) AS start\\_date\\_num,

    t.drug\\_era\\_start\\_date AS start\\_date, MIN(t.drug\\_era\\_start\\_date) OVER(partition by t.drug\\_concept\\_id) min\\_date,

    t.drug\\_concept\\_id

  FROM drug\\_era t

  where t.drug\\_concept\\_id in (1300978, 1304643, 1549080)

)

SELECT

  tt.drug\\_concept\\_id,

  min(tt.start\\_date\\_num) AS min\\_value,

  max(tt.start\\_date\\_num) AS max\\_value,

  tt.min\\_date+avg(tt.start\\_date\\_num) AS avg\\_value,

  (round(stdDev(tt.start\\_date\\_num)) ) AS stdDev\\_value ,

  tt.min\\_date+(select distinct PERCENTILE\\_DISC(0.25) WITHIN GROUP(ORDER BY tt.start\\_date\\_num) OVER() from tt) AS percentile\\_25,

  tt.min\\_date+(select distinct PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\\_date\\_num) OVER() from tt) AS median\\_value,

  tt.min\\_date+(select distinct PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\\_date\\_num) OVER() from tt) AS percential\\_75

FROM tt

group by

  drug\\_concept\\_id,

  tt.min\\_date

order by

  drug\\_concept\\_id

;

\*\*Input:\*\*

|   |

| --- |

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| drug\\_concept\\_id | 1300978, 1304643, 1549080 | Yes |   |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| min\\_value |   |

| max\\_value |   |

| avg\\_value | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |

| stddev\\_value |   |

| percentile\\_25 |      |

| median\\_value |      |

| percentile\\_75 |      |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | 1300978 |

| min\\_value | 0 |

| max\\_value | 7156 |

| avg\\_value | 2006-04-13 00:00:00 |

| stddev\\_value | 1808 |

| percentile\\_25 | 2000-03-21 00:00:00 |

| median\\_value | 2002-07-29 00:00:00 |

| percentile\\_75 | 2005-01-15 00:00:00 |

\*\*DER26:\*\* Counts of genders, stratified by drug

This query is used to count all genders (gender concept\\_id), stratified by drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a gender\\_concept\\_id and a drug\\_concept\\_id. If the input is ommitted, all existing value combinations are summarized.

\*\*Sample query:\*\*

SELECT p.gender\\_concept\\_id, count(1) AS stat\\_value, t.drug\\_concept\\_id

FROM drug\\_era t, person p

WHERE t.drug\\_concept\\_id

IN (1300978, 1304643, 1549080)

AND p.person\\_id = t.person\\_id

AND p.gender\\_concept\\_id

IN (8507, 8532)

GROUP BY t.drug\\_concept\\_id, p.gender\\_concept\\_id

ORDER BY t.drug\\_concept\\_id, p.gender\\_concept\\_id;

\*\*Input:\*\*

|   |

| --- |

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| list of gender\\_concept\\_id | 8507, 8532 | Yes | Male, Female |

| list of drug\\_concept\\_id | 1300978, 1304643, 1549080 | Yes |   |

\*\*Output:\*\*

|   |

| --- |

| \*\* Field\*\* | \*\* Description\*\* |

| gender\\_concept\\_id |   |

| stat\\_valu |   |

| drug\\_concept\\_id |   |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| gender\\_concept\\_id | 8507 |

| stat\\_value | 60 |

| drug\\_concept\\_id | 1300978 |
