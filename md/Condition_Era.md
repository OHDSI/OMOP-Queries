### CE01: Min/max/average length of condition

| Compute minimum, maximum an average length of the medical condition.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT   treatment,   count(\*),   min( condition\_days ) AS min ,   max( condition\_days ) AS max,   avg( condition\_days ) As avg\_condition\_days FROM (   SELECT     CASE WHEN surgery = 1 THEN 'surgery'          WHEN drug = 1 AND pt = 1 THEN 'PT Rx'          WHEN drug = 1 THEN 'Rx Only' ELSE 'No Treatment'     END AS treatment ,     condition\_days   FROM (     SELECT       person\_id,       diag\_date ,       max( drug ) AS drug,       max( surgery ) AS surgery,       max( pt ) AS PT ,       max( condition\_days ) AS condition\_days     FROM /\* back pain and treatments over following 60 days \*/ (       SELECT         era.person\_id,         condition\_era\_start\_date AS diag\_date ,         condition\_era\_end\_date - condition\_era\_start\_date AS condition\_days,         NVL( drug, 0 ) AS drug,         NVL( surgery, 0 ) AS surgery ,         NVL( pt, 0 ) AS pt       FROM condition\_era era       JOIN /\* SNOMed codes for back pain \*/ (         SELECT DISTINCT descendant\_concept\_id, concept\_name         FROM source\_to\_concept\_map map         JOIN concept\_ancestor ON ancestor\_concept\_id = target\_concept\_id         JOIN concept ON concept\_id = descendant\_concept\_id         WHERE           source\_code like '724%' AND           source\_vocabulary\_id = 2 /\* ICD9 \*/ AND           target\_vocabulary\_id = 1 /\* SNOMed \*/ AND           sysdate BETWEEN map.valid\_start\_date AND           map.valid\_end\_date       ) ON descendant\_concept\_id = condition\_concept\_id       LEFT OUTER JOIN /\* surgery \*/ (         SELECT           person\_id,           procedure\_date,           1 AS surgery         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE vocabulary\_id = 4 /\* CPT-4 \*/ AND           concept\_code IN( '22851','20936','22612','22523','22630','22614',                           '22842','22632','20930','22524','27130','22525' )       ) surgery ON         surgery.person\_id = era.person\_id AND         surgery.procedure\_date BETWEEN condition\_era\_start\_date AND condition\_era\_start\_date + 60       LEFT OUTER JOIN /\* drugs \*/ (         SELECT           person\_id,           procedure\_date AS drug\_date,           1 AS drug         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 4 /\* CPT-4 \*/ AND           concept\_code IN( '20610','20552','207096','20553','20550','20605' ,'20551','20600','23350' )         UNION SELECT           person\_id,           drug\_era\_start\_date,           1         FROM drug\_era         WHERE drug\_concept\_id IN( 1125315, 778711, 1115008, 1177480, 1112807, 1506270 )       ) drug ON         drug.person\_id = era.person\_id AND         drug.drug\_date BETWEEN condition\_era\_start\_date AND condition\_era\_start\_date + 60       LEFT OUTER JOIN /\* pt \*/ (         SELECT          person\_id,           procedure\_date AS pt\_date,           1 AS pt         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE vocabulary\_id = 4 /\* CPT-4 \*/ AND           concept\_code IN( '97001', '97140', '97002' )         UNION SELECT           person\_id,           procedure\_date AS pt\_date,           1 AS pt         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 5 /\* HCPCS \*/ AND           concept\_code = 'G0283'       ) pt ON         pt.person\_id = era.person\_id AND         pt.pt\_date BETWEEN condition\_era\_start\_date AND         condition\_era\_start\_date + 60     )     WHERE diag\_date > '01-jan-2011'     GROUP by       person\_id,       diag\_date     ORDER BY       person\_id,       diag\_date   ) ) GROUP BY treatment ORDER BY treatment;    **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg\_condition\_days |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg\_condition\_days |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE02: Age/gender of patients with condition

| List of patient counts of specific age and gender for specific medical condition
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Hip Fraction 1 |  Yes |  Concept ID=500000601 |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT gender, age, count(\*) num\_patients FROM -- patient with hip fracture, age, gender ( SELECT DISTINCT condition.person\_id , gender.concept\_name As GENDER , EXTRACT( YEAR FROM CONDITION\_ERA\_START\_DATE ) - year\_of\_birth AS age FROM condition\_era condition JOIN -- definition of Hip Fracture ( SELECT DISTINCT descendant\_concept\_id FROM relationship JOIN concept\_relationship rel USING( relationship\_id ) JOIN concept concept1 ON concept1.concept\_id = concept\_id\_1 JOIN concept\_ancestor ON ancestor\_concept\_id = concept\_id\_2 WHERE relationship\_name = 'HOI contains SNOMED (OMOP)' AND concept1.concept\_name = **'OMOP Hip Fracture** 1' AND sysdate BETWEEN rel.valid\_start\_date AND rel.valid\_end\_date ) ON descendant\_concept\_id = condition\_concept\_id JOIN person ON person.person\_id = condition.person\_id JOIN concept gender ON gender.concept\_id = gender\_concept\_id ) GROUP BY gender, age ORDER BY gender, age;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| gender | Patients gender, i.e. MALE, FEMALE |
| --- | --- |
| age | The year of birth of the person. For data sources with date of birth, the year is extracted. For data sources where the year of birth is not available, the approximate year of birth is derived based on any age group categorization available. |
| --- | --- |
| num\_patients | Number of patients for specific gender and age and selected condition |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| gender |  FEMALE |
| --- | --- |
| age |  16 |
| --- | --- |
| num\_patients |  22 |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE03: Min/max, average length of condition stratified by age/gender

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Hip Fracture 1 |  Yes |  concept\_id=500000601 |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT   gender,   CASE     WHEN age\_grp = 0 THEN '0-9'     WHEN age\_grp = 1 THEN '10-19'     WHEN age\_grp = 2 THEN '20-29'     WHEN age\_grp = 3 THEN '30-39'     WHEN age\_grp = 4 THEN '40-49'     WHEN age\_grp = 5 THEN '50-59'     WHEN age\_grp = 6 THEN '60-69'     WHEN age\_grp = 7 THEN '70-79'     WHEN age\_grp = 8 THEN '80-89'     WHEN age\_grp = 9 THEN '90-99'     WHEN age\_grp > 9 THEN '100+'   END age\_grp,   count(\*) AS num\_patients,   min( duration ) AS min\_duration\_count,   max( duration ) AS max\_duration\_count,   avg( duration ) AS avg\_duration\_count FROM -- patient with hip fracture, age, gender (   SELECT DISTINCT     condition.person\_id ,     gender.concept\_name As gender ,     EXTRACT( YEAR FROM condition\_era\_start\_date ) - year\_of\_birth AS age,     condition\_era\_end\_date - condition\_era\_start\_date + 1 AS duration,     (EXTRACT( YEAR FROM condition\_era\_start\_date) - person.year\_of\_birth)/10 AS age\_grp   FROM condition\_era condition   JOIN -- definition of Hip Fracture   (     SELECT DISTINCT descendant\_concept\_id     FROM relationship     JOIN concept\_relationship rel USING( relationship\_id )     JOIN concept concept1 ON concept1.concept\_id = concept\_id\_1     JOIN concept\_ancestor ON ancestor\_concept\_id = concept\_id\_2     WHERE       relationship\_name = 'HOI contains SNOMED (OMOP)' AND       concept1.concept\_name = **'OMOP Hip Fracture 1'** AND       SYSDATE BETWEEN rel.valid\_start\_date and rel.valid\_end\_date   ) ON descendant\_concept\_id = condition\_concept\_id   JOIN person ON person.person\_id = condition.person\_id   JOIN concept gender ON gender.concept\_id = gender\_concept\_id ) t1 GROUP BY   gender,   age\_grp,   age ORDER BY age\_grp, gender  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| gender | Patient gender name. i.e. MALE, FEMALE... |
| --- | --- |
| age\_grp | Age group in increments of 10 years |
| --- | --- |
| num\_patients | Number of patients withing gender and age group with associated condition |
| --- | --- |
| min\_duration | Minimum duration of condition in days |
| --- | --- |
| max\_duration | Maximum duration of condition in days |
| --- | --- |
| avg\_duration | Average duration of condition in days |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| gender |  FEMALE |
| --- | --- |
| age\_grp |  10-19 |
| --- | --- |
| num\_patients |  518 |
| --- | --- |
| min\_duration |  1 |
| --- | --- |
| max\_duration | 130  |
| --- | --- |
| avg\_duration |  8 |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE04: Conditions, stratified by year, age group and gender

| This query is used to count conditions (condition\_concept\_id) across all condition era records stratified by year, age group and gender (gender\_concept\_id). The age groups are calculated as 10 year age bands from the age of a person at the condition era start date. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id , year, age\_group (10 year age band) and gender\_concept\_id. If the input is ommitted, all existing value combinations are summarized..
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id |   |   |   |
| --- | --- | --- | --- |
| gender\_concept\_id |   |   |   |
| --- | --- | --- | --- |
| gender\_concept\_id |   |   |   |
| --- | --- | --- | --- |
| age\_group |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**         CREATE TEMP TABLE        age\_age\_grp(        age INT,        age\_grp VARCHAR(100)); INSERT INTO        age\_age\_grpVALUES(1, '0 to 9'),(2, '0 to 9'),(3, '0 to 9'),(4, '0 to 9'),(5, '0 to 9'),(6, '0 to 9'),(7, '0 to 9'),(8, '0 to 9'),(9, '0 to 9'),(10, '10 to 19'),(11, '10 to 19'),(12, '10 to 19'),(13, '10 to 19'),(14, '10 to 19'),(15, '10 to 19'),(16, '10 to 19'),(17, '10 to 19'),(18, '10 to 19'),(19, '10 to 19'),(20, '20 to 29'),(21, '20 to 29'),(22, '20 to 29'),(23, '20 to 29'),(24, '20 to 29'),(25, '20 to 29'),(26, '20 to 29'),(27, '20 to 29'),(28, '20 to 29'),(29, '20 to 29'),(30, '30 to 39'),(31, '30 to 39'),(32, '30 to 39'),(33, '30 to 39'),(34, '30 to 39'),(35, '30 to 39'),(36, '30 to 39'),(37, '30 to 39'),(38, '30 to 39'),(39, '30 to 39'),(40, '40 to 49'),(41, '40 to 49'),(42, '40 to 49'),(43, '40 to 49'),(44, '40 to 49'),(45, '40 to 49'),(46, '40 to 49'),(47, '40 to 49'),(48, '40 to 49'),(49, '40 to 49'),(50, '50 to 59'),(51, '50 to 59'),(52, '50 to 59'),(53, '50 to 59'),(54, '50 to 59'),(55, '50 to 59'),(56, '50 to 59'),(57, '50 to 59'),(58, '50 to 59'),(59, '50 to 59'),(60, '60 to 69'),(61, '60 to 69'),(62, '60 to 69'),(63, '60 to 69'),(64, '60 to 69'),(65, '60 to 69'),(66, '60 to 69'),(67, '60 to 69'),(68, '60 to 69'),(69, '60 to 69'),(70, '70 to 79'),(71, '70 to 79'),(72, '70 to 79'),(73, '70 to 79'),(74, '70 to 79'),(75, '70 to 79'),(76, '70 to 79'),(77, '70 to 79'),(78, '70 to 79'),(79, '70 to 79'),(80, '80 to 89'),(81, '80 to 89'),(82, '80 to 89'),(83, '80 to 89'),(84, '80 to 89'),(85, '80 to 89'),(86, '80 to 89'),(87, '80 to 89'),(88, '80 to 89'),(89, '80 to 89'),(90, '90 to 99'),(91, '90 to 99'),(92, '90 to 99'),(93, '90 to 99'),(94, '90 to 99'),(95, '90 to 99'),(96, '90 to 99'),(97, '90 to 99'),(98, '90 to 99'),(99, '90 to 99'),(100, '100 to 109'),(101, '100 to 109'),(102, '100 to 109'),(103, '100 to 109'),(104, '100 to 109'),(105, '100 to 109'),(106, '100 to 109'),(107, '100 to 109'),(108, '100 to 109'),(109, '100 to 109'),(110, '110 to 119'),(111, '110 to 119'),(112, '110 to 119'),(113, '110 to 119'),(114, '110 to 119'),(115, '110 to 119'),(116, '110 to 119'),(117, '110 to 119'),(118, '110 to 119'),(119, '110 to 119');  SELECT        condition,        year,        age\_grp,        gender,        count(\*)FROM        (        SELECT                person.person\_id ,                cond\_name.concept\_name AS condition ,                EXTRACT( YEAR FROM condition\_era\_start\_date ) AS year ,                gender.concept\_name As GENDER ,                EXTRACT( YEAR FROM condition\_era\_start\_date ) - year\_of\_birth AS age ,                age\_grp                FROM condition\_era condition                        JOIN concept cond\_name                                ON cond\_name.concept\_id = condition\_concept\_id                        JOIN person                                ON person.person\_id = condition.person\_id                        JOIN concept gender                                ON gender.concept\_id = 8507                        JOIN age\_age\_grp                                ON age = EXTRACT( YEAR FROM CONDITION\_ERA\_START\_DATE ) - year\_of\_birth         )GROUP BY        condition,        year,        age\_grp,        genderORDER BY        condition,        year,        age\_grp,        gender;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition |   |
| --- | --- |
| year |   |
| --- | --- |
| age\_grp |   |
| --- | --- |
| gender |   |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition |   |
| --- | --- |
| year |   |
| --- | --- |
| age\_grp |   |
| --- | --- |
| gender |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE05: Conditions that are seasonally dependent

| This query is used to count conditions (condition\_concept\_id) across all condition era records stratified by year, age group and gender (gender\_concept\_id). The age groups are calculated as 10 year age bands from the age of a person at the condition era start date. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id , year, age\_group (10 year age band) and gender\_concept\_id. If the input is ommitted, all existing value combinations are summarized..
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT season, count(\*) AS casesFROM /\* Extrinsic Asthma/season \*/( SELECT CASE  WHEN condition\_era\_start\_dateBETWEEN to\_date( '01-01-2017', 'DD-MM-YYYY' ) AND to\_date( '21-03-2017', 'DD-MM-YYYY' )THEN 'Winter' WHEN condition\_era\_start\_dateBETWEEN to\_date( '22-03-2017', 'DD-MM-YYYY' ) AND to\_date( '21-06-2017', 'DD-MM-YYYY' )THEN 'Spring' WHEN condition\_era\_start\_dateBETWEEN to\_date( '22-06-2017', 'DD-MM-YYYY' ) AND to\_date( '21-09-2017', 'DD-MM-YYYY' )THEN 'Summer' WHEN condition\_era\_start\_dateBETWEEN to\_date( '22-09-2017', 'DD-MM-YYYY' ) AND to\_date( '21-12-2017', 'DD-MM-YYYY' )THEN 'Fall' WHEN condition\_era\_start\_dateBETWEEN to\_date( '22-12-2017', 'DD-MM-YYYY' ) AND to\_date( '31-12-2017', 'DD-MM-YYYY' )THEN 'Winter'END AS seasonFROM condition\_eraJOIN /\* Extrinsic Asthma ICD-9 493.\* Get associated SNOMed codeswith their 12endents \*/(-- descendant standard concept id for asthmaSELECT DISTINCT ca.descendant\_concept\_id AS snomed\_asthmaFROM concept\_ancestor ca JOIN(SELECT c2.concept\_id FROM concept c1 JOIN concept\_relationship cr ON c1.concept\_id = cr.concept\_id\_1 AND cr.relationship\_id = 'Maps to'JOIN concept c2 ON cr.concept\_id\_2 = c2.concept\_idWHERE c1.concept\_code LIKE '493.0%') t -- standard concept id for asthmaON ca.ancestor\_concept\_id = t.concept\_id) ON snomed\_asthma = condition\_concept\_id) GROUP BY season;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| season |   |
| --- | --- |
| cases |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| season |   |
| --- | --- |
| cases |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE06: Conditions most likely to result in death

| Most prevalent conditions within thirty days of death
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| Number of days since condition era end | 30 |  Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT concept\_name, count(\*) as conditions\_count FROM  ( SELECT death.person\_id, concept\_name FROM death JOIN condition\_era condition ON condition.person\_id = death.person\_id AND death\_date - condition\_era\_end\_date <= **30** JOIN concept ON concept\_id = condition\_concept\_id ) GROUP BY concept\_name ORDER BY conditions\_count DESC; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| count |   |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| count |   |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE07: Comorbidities of patient with condition

| This query counts the top ten comorbidities for patients with diabetes
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_era\_end\_date |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** WITH SNOMed\_diabetes AS (   SELECT DISTINCT     descendant\_concept\_id AS snomed\_diabetes\_id   FROM source\_to\_concept\_map map   JOIN concept\_ancestor ON ancestor\_concept\_id = target\_concept\_id   WHERE     source\_vocabulary\_id = 2 /\* icd9 \*/ AND     target\_vocabulary\_id = 1 /\* SNOMed \*/ AND     source\_code LIKE '250.%' AND     sysdate BETWEEN valid\_start\_date AND valid\_end\_date) SELECT   comorbidity,   frequency FROM /\* top 10 \*/ (   SELECT     comorbidity,     count(\*) frequency   FROM /\* commorbidities for patients with diabetes \*/ (     SELECT DISTINCT       diabetic.person\_id,       concept\_name AS comorbidity     FROM /\* people with diabetes/onset date \*/ (       SELECT         person\_id,         MIN( condition\_era\_start\_date ) AS onset\_date       FROM condition\_era       JOIN SNOMed\_diabetes ON snomed\_diabetes\_id = condition\_concept\_id       GROUP BY person\_id     ) diabetic     JOIN /\* condition after onset date, that are not diabetes \*/ (       SELECT         person\_id,         condition\_concept\_id,         condition\_era\_start\_date       FROM condition\_era       WHERE         condition\_concept\_id NOT IN( SELECT snomed\_diabetes\_id FROM SNOMed\_diabetes )     ) comorb ON       comorb.person\_id = diabetic.person\_id AND       comorb.condition\_era\_start\_date > diabetic.onset\_date     JOIN concept ON concept\_id = comorb.condition\_concept\_id   )   GROUP BY comorbidity   ORDER BY frequency DESC ) limit 10; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| comorbidity |   |
| --- | --- |
| frequency |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| comorbidity |   |
| --- | --- |
| frequency |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
###  CE08: Number of comorbidity for patients with condition

| Meaningful text
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_era\_end\_date |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** WITH SNOMed\_diabetes AS (   SELECT DISTINCT descendant\_concept\_id AS snomed\_diabetes\_id   FROM source\_to\_concept\_map map   JOIN concept\_ancestor ON ancestor\_concept\_id = target\_concept\_id   WHERE     source\_vocabulary\_id = 2 /\* icd9 \*/ AND     target\_vocabulary\_id = 1 /\* SNOMed \*/ AND     source\_code LIKE '250.%' AND     sysdate BETWEEN valid\_start\_date AND valid\_end\_date),tt as (   SELECT     diabetic.person\_id,     count( distinct condition\_concept\_id ) AS comorbidities   FROM /\* people with diabetes/onset date \*/ (     SELECT       person\_id,       MIN( condition\_era\_start\_date ) AS onset\_date     FROM condition\_era     JOIN SNOMed\_diabetes ON snomed\_diabetes\_id = condition\_concept\_id     GROUP BY person\_id   ) diabetic   JOIN /\* condition after onset date, that are not diabetes \*/ (     SELECT       person\_id,       condition\_concept\_id,       condition\_era\_start\_date     FROM condition\_era     WHERE condition\_concept\_id NOT IN( SELECT snomed\_diabetes\_id FROM SNOMed\_diabetes )   ) comorb ON     comorb.person\_id = diabetic.person\_id AND     comorb.condition\_era\_start\_date > diabetic.onset\_date   JOIN concept ON concept\_id = comorb.condition\_concept\_id   GROUP BY diabetic.person\_id )SELECT   MIN( comorbidities ) AS min ,   max( comorbidities ) AS max,   avg( comorbidities ) AS average ,   (select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS percentile\_25 ,   (select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS median ,   (select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS percential\_75 FROM tt;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| average |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| average |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE09: Counts of condition record

| This query is used to count conditions (condition\_concept\_id) across all condition era records. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of condition\_concept\_id | 254761, 257011, 320128, 432867, 25297 | No |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT condition\_concept\_id, concept\_name, count(\*) records\_count  FROM condition\_era  JOIN concept ON concept\_id = condition\_concept\_id WHERE condition\_concept\_id     IN /\* top five condition concepts \*/       ( **254761, 257011, 320128, 432867, 25297** ) GROUP BY condition\_concept\_id, concept\_name ORDER BY records\_count DESC;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE10: Counts of persons with conditions

| This query is used to count the persons with any number of eras of a certain condition (condition\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of condition\_concept\_id | 320128, 432867, 254761, 257011, 257007 | No |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT condition\_concept\_id, concept\_name, count( distinct person\_id ) num\_people  FROM condition\_era  JOIN concept ON concept\_id = condition\_concept\_id WHERE condition\_concept\_id     IN /\* top five condition concepts by number of people \*/       ( **320128, 432867, 254761, 257011, 257007** ) GROUP BY condition\_concept\_id, concept\_name ORDER BY num\_people DESC;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| num\_people |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| num\_people |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE11: Distribution of condition era end dates

| This query is used to to provide summary statistics for condition era end dates (condition\_era\_end\_date) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT condition\_concept\_id     , min(condition\_era\_end\_date)     , max(condition\_era\_end\_date)        , to\_date( round( avg( to\_char( condition\_era\_end\_date, 'J' ))), 'J')        , round( stdDev( to\_number( to\_char( condition\_era\_end\_date, 'J' ), 9999999 ))) AS std\_dev\_days        , ( SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY condition\_era\_end\_date ) over ()         FROM condition\_era) AS percentile\_25        , ( SELECT DISTINCT PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY condition\_era\_end\_date ) over ()        FROM condition\_era) AS median     , ( SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY condition\_era\_end\_date ) over ()        FROM condition\_era) AS percential\_75  FROM condition\_era WHERE condition\_concept\_id IN( 254761, 257011, 320128, 432867, 25297 )  GROUP BY condition\_concept\_id; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE12: Distribution of condition era start dates

| This query is used to to provide summary statistics for condition era start dates (condition\_era\_start\_date) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT condition\_concept\_id     , min(condition\_era\_start\_date)     , max(condition\_era\_start\_date)        , to\_date( round( avg( to\_char( condition\_era\_start\_date, 'J' ))), 'J')        , round( stdDev( to\_number( to\_char( condition\_era\_start\_date, 'J' ), 9999999 ))) AS std\_dev\_days        , ( SELECT DISTINCT PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY condition\_era\_start\_date ) over ()         FROM condition\_era) AS percentile\_25        , ( SELECT DISTINCT PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY condition\_era\_start\_date ) over ()        FROM condition\_era) AS median     , ( SELECT DISTINCT PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY condition\_era\_start\_date ) over ()        FROM condition\_era) AS percential\_75  FROM condition\_era WHERE condition\_concept\_id IN( 254761, 257011, 320128, 432867, 25297 )  GROUP BY condition\_concept\_id;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE13: Distribution of condition occurrence count

| This query is used to to provide summary statistics for condition occurrence counts (condition\_occurrence\_count) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT   condition\_concept\_id,  MIN( condition\_occurrence\_count ) AS min ,   max( condition\_occurrence\_count ) AS max,   avg( condition\_occurrence\_count ) AS average ,   round( stdDev( condition\_occurrence\_count ) ) AS stdDev,  percentile\_25,  median,  percentile\_75FROM (  select    condition\_concept\_id,    condition\_occurrence\_count,    PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS percentile\_25,    PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS median ,     PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS percentile\_75  from condition\_era   WHERE condition\_concept\_id IN( 254761, 257011, 320128, 432867, 25297 ) )GROUP BY   condition\_concept\_id,  percentile\_25,  median,  percentile\_75; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std\_dev\_days |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE16: Distribution of condition era length, stratified by condition and condition type

| This query is used to provide summary statistics for the condition era length across all condition era records stratified by condition (condition\_concept\_id) and condition type (condition\_type\_concept\_id, in CDM V2 condition\_occurrence\_type): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an era is defined as the difference between the start date and the end date. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id and a condition\_type\_concept\_id. If the input is omitted, all existing value combinations are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id |   | No |   |
| --- | --- | --- | --- |
| condition\_type\_concept\_id |   | No |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT   condition\_concept\_id,  MIN( condition\_occurrence\_count ) AS min ,   max( condition\_occurrence\_count ) AS max,   avg( condition\_occurrence\_count ) AS average ,   round( stdDev( condition\_occurrence\_count ) ) AS stdDev,  percentile\_25,  median,  percentile\_75FROM (  select    condition\_concept\_id,    condition\_occurrence\_count,    PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS percentile\_25,    PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS median ,     PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY condition\_occurrence\_count) over() AS percentile\_75  from condition\_era   WHERE condition\_concept\_id IN( **254761, 257011, 320128, 432867, 25297** ) )GROUP BY   condition\_concept\_id,  percentile\_25,  median,  percentile\_75;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
### CE17: Distribution of condition occurrence count, stratified by condition and condition type

| This query is used to provide summary statistics for condition occurrence count (condition\_occurrence\_count) across all condition era records stratified by condition (condition\_concept\_id) and condition type (condition\_type\_concept\_id, in CDM V2 condition\_occurrence\_type): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a condition\_concept\_id and a condition\_type\_concept\_id. If the input is omitted, all existing value combinations are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 254761, 257011, 320128, 432867, 25297 | No |   |
| --- | --- | --- | --- |
| condition\_type\_concept\_id |   | No |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue** SELECT   condition\_concept\_id,  MIN( occurrences ) AS min ,   max( occurrences ) AS max,   avg( occurrences ) AS average ,   round( stdDev( occurrences ) ) AS stdDev,  percentile\_25,  median,  percentile\_75FROM (  select    condition\_concept\_id,     occurrences,    PERCENTILE\_DISC(0.25) WITHIN GROUP (ORDER BY occurrences) over() AS percentile\_25,    PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY occurrences) over() AS median ,     PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY occurrences) over() AS percentile\_75  from (    select       person\_id,       condition\_concept\_id,      count(\*) AS occurrences    from condition\_era     WHERE condition\_concept\_id IN( **254761, 257011, 320128, 432867, 25297** )     group by       person\_id,      condition\_concept\_id  ))GROUP BY   condition\_concept\_id,  percentile\_25,  median,  percentile\_75 **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential\_75 |   |
| --- | --- |

  |
| --- |
*-*-*-*-*
