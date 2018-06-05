### DEX01: Counts of persons with any number of exposures to a certain drug

| This query is used to count the persons with at least one exposures to a certain drug (drug\_concept\_id).  See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all drugs in the data table are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**.  set search\_path to full\_201706\_omop\_v5; SELECT concept.concept\_name, drug\_concept\_id, count(person\_id) as num\_persons FROMdrug\_exposure join conceptON drug\_concept\_id = concept.concept\_idwherelower(domain\_id)='drug' and vocabulary\_id='RxNorm' and standard\_concept='S'and drug\_concept\_id in ( **40165254** , **40165258** )GROUP BY concept.concept\_name, drug\_concept\_id;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept.  |
| --- | --- |
| num\_persons | The patients count |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drug\_name |  Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| --- | --- |
| drug\_concept\_id |  40165254 |
| --- | --- |
| num\_persons |  191244 |
| --- | --- |

  |
| --- |
### DEX02: Counts of persons taking a drug, by age, gender, and year of exposure

| This query is used to count the persons with exposure to a certain drug (drug\_concept\_id), grouped by age, gender, and year of exposure. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. If the input is omitted, all drugs in the data table are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. select drug.concept\_name,         EXTRACT( YEAR FROM drug\_exposure\_start\_date ) as year\_of\_exposure,        EXTRACT( YEAR FROM drug\_exposure\_start\_date ) - year\_of\_birth as age ,         gender.concept\_name as gender,        count(1) as num\_personsFromdrug\_exposure JOINperson USING( person\_id ) join concept drug ON drug.concept\_id = drug\_concept\_id JOINconcept gender ON gender.concept\_id = gender\_concept\_idwhere drug\_concept\_id IN ( **40165254** , **40165258** ) GROUP by drug.concept\_name, gender.concept\_name, EXTRACT( YEAR FROM drug\_exposure\_start\_date ),EXTRACT( YEAR FROM drug\_exposure\_start\_date ) - year\_of\_birth ORDER BY concept\_name, year\_of\_exposure, age, gender   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  concept\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
|  year\_of\_exposure |   |
| --- | --- |
|  age | The age of the person at the time of exposure |
| --- | --- |
|  gender | The gender of the person. |
| --- | --- |
|  num\_persons | The patient count |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| concept\_name |  Rosuvastatin calcium 40 MG Oral Tablet [Crestor] |
| --- | --- |
| year\_of\_exposure |  2010 |
| --- | --- |
| age |  69 |
| --- | --- |
| gender |  Male |
| --- | --- |
| num\_persons |  15 |
| --- | --- |

  |
| --- |
### DEX03: Distribution of age, stratified by drug

| This query is used to provide summary statistics for the age across all drug exposure records stratified by drug (drug\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. If the input is omitted, age is summarized for all existing drug\_concept\_id values.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 40165254, 40165258 | Yes | Crestor 20 and 40 mg tablets |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT         concept\_name AS drug\_name ,         drug\_concept\_id ,         COUNT(\*) AS patient\_count ,         MIN ( age ) AS min  ,         APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY age ) AS percentile\_25  ,         ROUND ( AVG ( age ), 2 ) AS mean,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY age ) AS median  ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY age ) AS percentile\_75 ,         MAX ( age ) AS max ,         ROUND ( STDDEV ( age ), 1 ) AS stdDev FROM /\*person, first drug exposure date\*/ (                 SELECT                         drug\_concept\_id , person\_id ,                         MIN( extract(year from drug\_exposure\_start\_date )) - year\_of\_birth as age                 FROM                         drug\_exposure JOIN full\_201706\_omop\_v5.person USING( person\_id )                 WHERE drug\_concept\_id IN /\*crestor 20 and 40 mg tablets \*/ ( **40165254** , **40165258** )                GROUP BY drug\_concept\_id, person\_id , year\_of\_birth         ) JOIN concept ON concept\_id = drug\_concept\_id WHERE domain\_id='Drug' and standard\_concept='S'GROUP BY concept\_name, drug\_concept\_id; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| patient\_count | The count of patients taking the drug |
| --- | --- |
| min | The age of the youngest patient taking the drug |
| --- | --- |
| percentile\_25 | The 25th age percentile |
| --- | --- |
| mean | The mean or average age of the patients taking the drug |
| --- | --- |
| median | The median age of the patients taking the drug |
| --- | --- |
| percentile\_75 | The 75th age percentile |
| --- | --- |
| max  | The age of the oldest patient taking the drug |
| --- | --- |
| stddev | The standard deviation of the age distribution |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drug\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| --- | --- |
| drug\_concept\_id | 40165254 |
| --- | --- |
| patient\_count | 30321 |
| --- | --- |
| min | 11 |
| --- | --- |
| percentile\_25 | 49 |
| --- | --- |
| mean | 53.87 |
| --- | --- |
| median | 55 |
| --- | --- |
| percentile\_75 | 60 |
| --- | --- |
| max | 93 |
| --- | --- |
| stddev | 8.8 |
| --- | --- |

  |
| --- |
### DEX04: Distribution of gender in persons taking a drug

| This query is used to obtain the gender distribution of persons exposed to a certain drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. If the input is omitted, all drugs in the data table are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. select drug.concept\_name as drug\_name,                 drug\_concept\_id,                        gender.concept\_name as gender,                count(1) as num\_personsFromdrug\_exposure JOIN person USING( person\_id ) join concept drug ON drug.concept\_id = drug\_concept\_id JOIN concept gender ON gender.concept\_id = gender\_concept\_idwhere drug\_concept\_id IN ( **40165254** , **40165258** ) GROUP by drug.concept\_name, drug\_concept\_id, gender.concept\_name ORDER BY drug\_name, drug\_concept\_id, gender;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | An unambiguous, meaningful and descriptive name for the drug concept. |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| gender | The gender of the counted persons exposed to drug. |
| --- | --- |
| num\_persons | The number of persons of a particular gender exposed to drug. |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drug\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| --- | --- |
| drug\_concept\_id | 40165254 |
| --- | --- |
| gender | FEMALE |
| --- | --- |
| num\_persons | 12590 |
| --- | --- |

  |
| --- |
### DEX05: Counts of drug records for a particular drug

| This query is used to count the drug exposure records for a certain drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. If the input is omitted, all drugs in the data table are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT concept\_name as drug\_name, drug\_concept\_id, count(\*) as num\_records FROM drug\_exposure JOIN concept ON concept\_id = drug\_concept\_id WHERE lower(domain\_id)='drug' and vocabulary\_id='RxNorm' and standard\_concept='S'and drug\_concept\_id IN ( **40165254** , **40165258** )GROUP BY concept\_name, drug\_concept\_id;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | An unambiguous, meaningful and descriptive name for the drug concept. |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| num\_records | The number of drug exposure records |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drug\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| --- | --- |
| drug\_concept\_id | 40165254 |
| --- | --- |
| num\_records | 191244 |
| --- | --- |

  |
| --- |
### DEX06: Counts of distinct drugs in the database

| This query is used to determine the number of distinct drugs (drug\_concept\_id). See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.
**Input:** None.
**Sample query run:**
The following is a sample run of the query.  SELECT count(distinct drug\_concept\_id) as number\_drugs FROM drug\_exposure JOIN concept ON concept\_id = drug\_concept\_id WHERE lower(domain\_id)='drug' and vocabulary\_id='RxNorm' and standard\_concept='S';   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| number\_drugs | The count of distinct drug concepts. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| number\_drugs | 10889 |
| --- | --- |

  |
| --- |
### DEX07: Maximum number of drug exposure events per person over some time period

| This query is to determine the maximum number of drug exposures that is recorded for a patient during a certain time period. If the time period is omitted, the entire time span of the database is considered. Instead of maximum, the query can be easily changed to obtained the average or the median number of drug records for all patients. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes | |
| --- | --- | --- | --- |
| date to | 31-Dec-2008 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. select max(exposures ) as exposures\_count from (SELECT drug\_exposure.person\_id, COUNT(\*) exposures FROM drug\_exposure JOIN personON drug\_exposure.person\_id = person.person\_idWHERE drug\_concept\_id in (select distinct concept\_id from concept                                                 WHERE lower(domain\_id)='drug' and vocabulary\_id='RxNorm' and standard\_concept='S')AND drug\_exposure\_start\_date BETWEEN **'2017-01-01'** AND **'2017-12-31'** GROUP BY drug\_exposure.person\_id);    **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| exposures\_count | The number of drug exposure records for the patient with the maximum number of such records. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| exposures\_count | 1137 |
| --- | --- |

  |
| --- |
### DEX08: Maximum number of distinct drugs per person over some time period

| This query is to determine the maximum number of distinct drugs a patient is exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes |   |
| --- | --- | --- | --- |
| date to | 31-Dec-2008 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. select max(drugs) as drugs\_count from (SELECT COUNT( DISTINCT drug\_concept\_id) drugs FROM drug\_exposure JOIN personON drug\_exposure.person\_id = person.person\_idWHERE drug\_concept\_id in (select distinct concept\_id from concept                                                 WHERE lower(domain\_id)='drug' and vocabulary\_id='RxNorm' and standard\_concept='S')AND drug\_exposure\_start\_date BETWEEN **'2017-01-01'** AND **'2017-12-31'** GROUP BY drug\_exposure.person\_id); **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drugs\_count | The maximum number of distinct drugs a patient is exposed to during the time period |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drugs\_count | 141 |
| --- | --- |

  |
| --- |
### DEX09: Distribution of distinct drugs per person over some time period

| This query is to determine the distribution of distinct drugs patients are exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes |   |
| --- | --- | --- | --- |
| date to | 31-Dec-2008 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**.  SELECT MIN ( drugs ) AS min , approximate  PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY drugs ) as percentile\_25, ROUND ( AVG ( drugs ), 2 ) AS mean, approximate PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY drugs ) AS median , approximate PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY drugs ) AS percential\_75, MAX ( drugs ) AS max,  ROUND ( STDDEV ( drugs ), 1 ) AS stdDev  FROM  (SELECT person\_id, NVL( drugs, 0 ) AS drugs FROM person  JOIN  ( SELECT person\_id, COUNT( DISTINCT drug\_concept\_id ) AS drugs FROM drug\_exposure  WHERE drug\_exposure\_start\_date BETWEEN **'2017-01-01'** AND **'2017-12-31'** GROUP BY person\_id ) USING( person\_id ) );  **Output:**
Output field list:

| **Field** | ** Description** |
| --- | --- |
| min | The minimum number of drugs taken by a patient |
| --- | --- |
| percentile\_25 | The 25th percentile of the distibution |
| --- | --- |
| mean | The mean or average of drugs taken by patients |
| --- | --- |
| median | The median number of drugs take |
| --- | --- |
| percentile\_75 | The 75th percentile of the distribution |
| --- | --- |
| max | The maximum number of drugs taken by a patient |
| --- | --- |
| stddev | The standard deviation of the age distribution |
| --- | --- |


Sample output record:

| **Field** | ** Content** |
| --- | --- |
| min | 0 |
| --- | --- |
| percentile\_25 | 0 |
| --- | --- |
| mean | 1.73 |
| --- | --- |
| median | 0 |
| --- | --- |
| percentile\_75 | 1 |
| --- | --- |
| max | 141 |
| --- | --- |
| stddev | 4.2 |
| --- | --- |

  |
| --- |
### DEX10: Other drugs (conmeds) patients exposed to a certain drug take over some time period

| This query is used to establish the medication (conmeds) taken by patients who also are exposed to a certain drug in a given time period. The query returns the number of patients taking the drug at least once. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id and the time period. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values. **Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug concept ids | 1336825, 19047763 | Yes | Bortezomib, Thalidomide 50 mg capsules |
| --- | --- | --- | --- |
| from\_date | 01-jan-2008 | Yes |   |
| --- | --- | --- | --- |
| to\_date | 31-dec-2009 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**.
SELECT concept\_name, COUNT(1) as personsFROM ( --Other drugs people are taking  SELECT DISTINCT cohort.person\_id, drug.drug\_concept\_id  FROM (   --person with specific drug in time frame  SELECT DISTINCT person\_id, drug\_concept\_id, from\_date, to\_date  FROM drug\_exposure  JOIN (   --date range   SELECT **'01-jan-2008'** AS from\_date , **'31-dec-2009'** AS to\_date )   ON drug\_exposure\_start\_date BETWEEN from\_date AND to\_date  WHERE drug\_concept\_id IN /\*bortezomib, Thalidomide 50 mg capsules \*/  ( **1336825** , **19047763** )  ) cohort  JOIN drug\_exposure drug   ON drug.person\_id = cohort.person\_id  AND drug.drug\_concept\_id != cohort.drug\_concept\_id  AND drug.drug\_exposure\_start\_date BETWEEN from\_date AND to\_date  WHERE drug.drug\_concept\_id != 0 /\* unmapped drug \*/  )JOIN concept ON concept\_id = drug\_concept\_idGROUP By concept\_name ORDER BY persons DESC;
**Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | An unambiguous, meaningful and descriptive name for the conmeds. |
| --- | --- |
| persons | count of patients taking the drug at least once |
| --- | --- |


Sample output record:

| **Field** | ** Value** |
| --- | --- |
| drug\_name | Dexamethasone 4 MG Oral Tablet |
| --- | --- |
| persons | 190 |
| --- | --- |

  |
| --- |
### DEX11: Distribution of brands used for a given generic drug

| This query provides the brands that are used for a generic drug. The input to the query is a value of a drug\_concept\_id. See [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.  Note that depending on the mapping available for the source\_values in the drug\_exposure table, branded drug information might only partially or not be provided. See the Standard Vocabulary Specifications at  [http://omop.org/Vocabularies](http://omop.org/Vocabularies).
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 19019306 | Yes | Nicotine Patch |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT        tt.drug\_name,                tt.brand\_name,                100.00\*tt.part\_brand/tt.total\_brand as perc\_brand\_countFROM        (        SELECT        t.drug\_name,                        t.brand\_name,                        t.cn\_3\_02 part\_brand,                        SUM(t.cn\_3\_02) OVER() total\_brand                        FROM                                (                                        SELECT        sum((select count(1) from drug\_exposure d where d.drug\_concept\_id = cr003.concept\_id\_2)) cn\_3\_02,                                                        A.Concept\_Name drug\_name,                                                        D.Concept\_Name brand\_name                                        FROM                                                concept AS A                                                INNER JOIN        concept\_relationship AS CR003                                                        ON CR003.concept\_id\_1        = A.concept\_id                                                INNER JOIN        concept\_relationship AS CR007                                                        ON        CR007.concept\_id\_2                = CR003.concept\_id\_2                                                INNER JOIN                                                        concept\_relationship AS CR006                                                                ON        CR007.concept\_id\_1                = CR006.concept\_id\_1                                                INNER JOIN                                                        concept D                                                                ON        CR006.concept\_id\_2                = D.concept\_id                                        WHERE                                                CR003.relationship\_ID        = 'Has tradename'                                        AND        A.concept\_class\_id                = 'Clinical Drug'                                        AND        CR007.relationship\_ID        = 'Constitutes'                                        AND        CR006.relationship\_ID        = 'Has brand name'                                        AND        D.concept\_class\_id                = 'Brand Name'                                        AND        A.concept\_id                        = **35606533**                                         GROUP BY        A.Concept\_Name,                                                                D.Concept\_Name                                ) t         ) ttWHERE tt.total\_brand > 0 ;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_name | The name of the query drug |
| --- | --- |
| brand\_name | The name of the brand |
| --- | --- |
| perc\_brand\_count | The market share for each brand |
| --- | --- |


Sample output record:

| ** Field** | ** Content** |
| --- | --- |
| drug\_name |   |
| --- | --- |
| brand\_name |   |
| --- | --- |
| perc\_brand\_count |   |
| --- | --- |

  |
| --- |
### DEX12: Distribution of forms used for a given ingredient

| This query determines the percent distribution of forms of drug products containing a given ingredient. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  ingredient.concept\_id |  1125315 |  Yes |  Acetaminophen |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameter is highlighted in  **blue**. SELECT tt.form\_name,(100.00 \* tt.part\_form / tt.total\_forms) as percent\_formsFROM (SELECT t.form\_name,t.cn part\_form,SUM(t.cn) OVER() total\_formsFROM (select count(1) as cn,drugform.concept\_name form\_nameFROM concept ingredient,concept\_ancestor a,concept drug,concept\_relationship r,concept drugformWHERE ingredient.concept\_id = **1125315** --AcetaminophenAND ingredient.concept\_class\_id = 'Ingredient'AND ingredient.concept\_id = a.ancestor\_concept\_idAND a.descendant\_concept\_id = drug.concept\_id--AND drug.concept\_level = 1 --ensure it is drug productANd drug.standard\_concept='S'AND drug.concept\_id = r.concept\_id\_1AND r.concept\_id\_2 = drugform.concept\_idAND drugform.concept\_class\_id = 'Dose Form' GROUP BY drugform.concept\_name) t WHERE t.cn>0 --don't count forms that exist but are not used in the data) ttWHERE tt.total\_forms > 0 --avoid division by 0ORDER BY percent\_forms desc;    **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| form\_name | The concept name of the dose form |
| --- | --- |
| percent\_forms | The percent of forms drug products have containing the ingredient |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| form\_name |  Oral Tablet |
| --- | --- |
| percent\_forms |  95.69 |
| --- | --- |

  |
| --- |
### DEX13: Distribution of provider specialities prescribing a given drug

| This query provides the provider specialties prescribing a given drug, and the frequencies for each provider prescribing the drug (drug exposure records). Note that many databases do not record the prescribing provider for drugs. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\_concept\_id values.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 2213473 | Yes | Influenza virus vaccine |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**.
SELECT  concept\_name AS specialty,   count(\*) AS prescriptions\_count  FROM   /\*first prescribing provider for statin\*/  ( SELECT person\_id, provider\_id  FROM drug\_exposure  WHERE NVL( drug\_exposure.provider\_id, 0 ) > 0  AND drug\_concept\_id = **2213473**  /\* Influenza virus vaccine \*/  ) drug  JOIN provider ON provider.provider\_id = drug.provider\_id   JOIN concept ON concept\_id = provider.specialty\_concept\_id  WHERE concept.vocabulary\_id='Specialty'  AND concept.standard\_concept='S'  GROUP BY concept\_name  ORDER BY prescriptions\_count desc;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| specialty | The concept name of the specialty concept |
| --- | --- |
| prescriptions\_count | The count of drug exposure records providers from the specialties are listed as prescribing provider. |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
| specialty |  Family Practice |
| --- | --- |
| prescriptions\_count |  214825 |
| --- | --- |

  |
| --- |
### DEX14: Among people who take drug A, how many take drug B at the same time?

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_id | 21502747 | Yes | Statins |
| --- | --- | --- | --- |
| ancestor\_concept\_id | 21500223 | Yes | Antihypertensive Therapy Agents |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT count(\*) AS num\_A\_users , SUM( bp\_also ) AS num\_also\_using\_B FROM /\* people taking statin and possible taking antihypertensive agent \*/         ( SELECT statin.person\_id, MAX( NVL( bp, 0 ) ) AS bp\_also                 FROM /\*people taking statin \*/                         ( SELECT  person\_id, drug\_exposure\_start\_date, drug\_exposure\_end\_date                                 FROM drug\_exposure statin                                 WHERE drug\_concept\_id IN /\*statins\*/                                         ( SELECT concept\_id                                                 FROM concept                                                 JOIN concept\_ancestor ON descendant\_concept\_id = concept\_id                                                 WHERE                                                 ancestor\_concept\_id = **21502747**                                                 AND standard\_concept = 'S'                                                 AND sysdate BETWEEN valid\_start\_date AND valid\_end\_date ) ) statin                                                                                LEFT OUTER JOIN /\* people taking antihypertensive agent \*/                         ( SELECT  person\_id, drug\_exposure\_start\_date, drug\_exposure\_end\_date , 1 AS bp                                 FROM drug\_exposure                                 WHERE drug\_concept\_id IN /\*Antihypertensive Therapy Agents \*/                                         ( SELECT concept\_id                                                 FROM concept                                                 JOIN concept\_ancestor ON descendant\_concept\_id = concept\_id                                                 WHERE                                                 ancestor\_concept\_id = **21500223**                                                 AND standard\_concept = 'S'                                                 AND sysdate BETWEEN valid\_start\_date AND valid\_end\_date ) ) bp         ON bp.person\_id = statin.person\_id         AND bp.drug\_exposure\_start\_date < statin.drug\_exposure\_end\_date         AND bp.drug\_exposure\_end\_date > statin.drug\_exposure\_start\_date         GROUP BY statin.person\_id );      **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
| person\_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |
| --- | --- |
| ancestor\_concept\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| --- | --- |
| drug\_exposure\_start\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| --- | --- |
| drug\_exposure\_end\_date | The end date for the current instance of drug utilization. It is not available from all sources. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| person\_id |   |
| --- | --- |
| ancestor\_concept\_id |   |
| --- | --- |
| drug\_exposure\_start\_date |   |
| --- | --- |
| drug\_exposure\_end\_date |   |
| --- | --- |

  |
| --- |
### DEX15: Number of persons taking a given drug having at least a 180 day period prior and a 365 day follow-up period

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_id | 21502747 | Yes | Statins |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT        floor( ( observation\_period\_end\_date - index\_date ) / 365 ) AS follow\_up\_years,         count(\*) AS persons FROM /\* statin users with 180 clean period and at least 1 year follow up period \*/         (         SELECT person\_id, index\_date , observation\_period\_start\_date , observation\_period\_end\_date         FROM /\*statin user start\_date \*/                 (                 SELECT                         person\_id,                         min( drug\_exposure\_start\_date ) AS index\_date                 FROM drug\_exposure statin                 WHERE drug\_concept\_id IN /\*statins \*/                          (                         SELECT concept\_id                         FROM concept                         JOIN concept\_ancestor ON descendant\_concept\_id = concept\_id                         WHERE ancestor\_concept\_id = **21502747**                         --AND vocabulary\_id = 8                         AND vocabulary\_id = 'RxNorm'                        AND standard\_concept = 'S'                         AND sysdate BETWEEN valid\_start\_date AND valid\_end\_date ) GROUP BY person\_id )         JOIN observation\_period USING( person\_id )         WHERE observation\_period\_start\_date + **180** < index\_date AND observation\_period\_end\_date > index\_date + 365        ) GROUP BY floor( ( observation\_period\_end\_date - index\_date ) / **365** ) ORDER BY 1;      **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
| person\_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |
| --- | --- |
| ancestor\_concept\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| --- | --- |
| descendant\_concept\_id | A foreign key to the concept code in the concept table for the lower-level concept that forms the descendant in the relationship. |
| --- | --- |
| observation\_period\_start\_date | The start date of the observation period for which data are available from the data source. |
| --- | --- |
| observation\_period\_end\_date | The end date of the observation period for which data are available from the data source. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| person\_id |   |
| --- | --- |
| ancestor\_concept\_id |   |
| --- | --- |
| descendant\_concept\_id |   |
| --- | --- |
| observation\_period\_start\_date |   |
| --- | --- |
| observation\_period\_end\_date |   |
| --- | --- |

  |
| --- |
### DEX16: Adherence/compliance - what is adherence rate for given drug?

| Define adherence as sum of days supply divided by length of treatment period.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 996416 | Yes | Finasteride |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT concept\_name, count(\*) AS number\_of\_eras , avg( treatment\_length ) AS average\_treatment\_length\_count , avg(adherence) avgerage\_adherence\_count FROM        ( SELECT person\_id, concept\_name, drug\_era\_start\_date , sum( days\_supply ), treatment\_length ,          sum( days\_supply ) / treatment\_length AS adherence , min( has\_null\_days\_supply ) AS null\_day\_supply          FROM /\* drug era and individual drug encounters making up the era \*/                 ( SELECT person\_id, ingredient\_concept\_id , drug\_era\_start\_date, drug\_era\_end\_date ,                  drug\_era\_end\_date - drug\_era\_start\_date AS treatment\_length , drug\_exposure\_start\_date , days\_supply ,                  DECODE( NVL( days\_supply, 0 ), 0, 0, 1 ) has\_null\_days\_supply                  FROM /\*drug era of people taking finasteride \*/                         ( SELECT person\_id, drug\_concept\_id as ingredient\_concept\_id , drug\_era\_start\_date, drug\_era\_end\_date                                 FROM drug\_era                                 --WHERE drug\_concept\_id = **996416** /\* Finasteride \*/                                 )                                 JOIN /\* drug exposures making up the era \*/                                 ( SELECT person\_id, days\_supply, drug\_exposure\_start\_date                                         FROM drug\_exposure                                         JOIN concept\_ancestor ON descendant\_concept\_id = drug\_concept\_id                                         JOIN concept ON concept\_id = ancestor\_concept\_id                                         WHERE LOWER(concept\_class\_id) = 'ingredient'                                         AND sysdate BETWEEN valid\_start\_date AND valid\_end\_date                                         AND ancestor\_concept\_id = 996416                                         /\*Finasteride\*/ ) USING( person\_id )                         WHERE drug\_exposure\_start\_date BETWEEN drug\_era\_start\_date AND drug\_era\_end\_date )                 JOIN concept ON concept\_id = ingredient\_concept\_id         GROUP BY person\_id, concept\_name, drug\_era\_start\_date, treatment\_length ) WHERE treatment\_length > 100 and null\_day\_supply > 0 GROUP BY concept\_name;      **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | An unambiguous, meaningful and descriptive name for the concept. |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| concept\_class | The category or class of the concept along both the hierarchical tree as well as different domains within a vocabulary. Examples are "Clinical Drug", "Ingredient", "Clinical Finding" etc. |
| --- | --- |
| treatment\_length |   |
| --- | --- |
| person\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| --- | --- |
| drug\_era\_start\_date | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |
| --- | --- |
| drug\_exposure\_start\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| --- | --- |
| days\_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |
| --- | --- |
| drug\_era\_end\_date | The end date for the drug era constructed from the individual instance of drug exposures. It is the end date of the final continuously recorded instance of utilization of a drug. |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| ancestor\_concept\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| concept\_class |   |
| --- | --- |
| treatment\_length |   |
| --- | --- |
| person\_id |   |
| --- | --- |
| drug\_era\_start\_date |   |
| --- | --- |
| drug\_exposure\_start\_date |   |
| --- | --- |
| days\_supply |   |
| --- | --- |
| drug\_era\_end\_date |   |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| ancestor\_concept\_id |   |
| --- | --- |

  |
| --- |
### DEX17: Why do people stop treatment?

| This query provides a list of stop treatment and their frequency.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT stop\_reason, count(\*) AS reason\_freq FROM drug\_exposure WHERE stop\_reason IS NOT null GROUP BY stop\_reason ORDER BY reason\_freq DESC;
**Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| stop\_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |
| --- | --- |
| reason\_freq |  Frequency of stop reason |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| stop\_reason |  Regimen Completed |
| --- | --- |
| reason\_freq |  14712428 |
| --- | --- |

  |
| --- |
### DEX18: What is the distribution of DRUG\_TYPE\_CONCEPT\_ID (modes of distribution) for a given drug?

|
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT concept\_name, count(\*) as drug\_type\_count FROM drug\_exposure JOIN concept ON concept\_id = drug\_type\_concept\_id GROUP BY concept\_name ORDER BY drug\_type\_count DESC;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_type\_concept\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| --- | --- |
| drug\_type\_count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_type\_concept\_id |   |
| --- | --- |
| drug\_type\_count |   |
| --- | --- |

  |
| --- |
### DEX19: How many people are taking a drug for a given indication?

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | Acute Tuberculosis | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT concept\_name, count( distinct person\_id )  FROM drug\_exposure JOIN /\* indication and associated drug ids \*/         (select indication.concept\_name, drug.concept\_id                from concept indication                 JOIN concept\_ancestor ON ancestor\_concept\_id = indication.concept\_id                 JOIN vocabulary indication\_vocab ON indication\_vocab.vocabulary\_id = indication.vocabulary\_id                JOIN concept drug ON drug.concept\_id = descendant\_concept\_id                 JOIN vocabulary drug\_vocab ON drug\_vocab.vocabulary\_id = drug.vocabulary\_id                 WHERE sysdate BETWEEN drug.valid\_start\_date AND drug.valid\_end\_date                AND drug\_vocab.vocabulary\_id = **'RxNorm'**                 AND indication.concept\_class\_id = 'Indication'                AND indication\_vocab.vocabulary\_name = 'Indications and Contraindications (FDB)'                AND indication.concept\_name = **'Active Tuberculosis'** /\*This filter can be changed or omitted if count need for all indication\*/                AND drug.standard\_concept='S'        )ON concept\_id = drug\_concept\_id GROUP BY concept\_name;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| concept\_name |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX20: How many people taking a drug for a given indicaton actually have that disease in their record prior to exposure?

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | Acute Tuberculosis | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT         count(\*) AS treated         FROM /\* person and tuberculosis treatment start date \*/         (                 SELECT                         person\_id,                         min( drug\_exposure\_start\_date ) AS treatment\_start                 FROM drug\_exposure         JOIN /\*indication and associated drug ids \*/                 ( SELECT                         indication.concept\_name,                         drug.concept\_id                         --, indication.domain\_id, drug.concept\_id                        FROM concept indication                         JOIN concept\_ancestor ON ancestor\_concept\_id = indication.concept\_id                         JOIN vocabulary indication\_vocab ON indication\_vocab.vocabulary\_id = indication.vocabulary\_id                         JOIN concept drug ON drug.concept\_id = descendant\_concept\_id                         JOIN vocabulary drug\_vocab ON drug\_vocab.vocabulary\_id = drug.vocabulary\_id                         WHERE                         indication\_vocab.vocabulary\_name = 'Indications and Contraindications (FDB)'                        AND indication.domain\_id = 'Drug'                        AND indication.concept\_name = **'Active Tuberculosis'**                         AND drug\_vocab.vocabulary\_name = **'RxNorm (NLM)**'                        AND drug.standard\_concept = 'S'                         AND sysdate BETWEEN drug.valid\_start\_date AND drug.valid\_end\_date )         ON concept\_id = drug\_concept\_id GROUP BY person\_id ) treated LEFT OUTER JOIN /\*patient with Acute Tuberculosis diagnosis \*/         ( SELECT                         person\_id, min( condition\_start\_date ) first\_diagnosis, 1 AS diagnosed                        FROM condition\_occurrence                         JOIN source\_to\_concept\_map ON target\_concept\_id = condition\_concept\_id                         JOIN vocabulary ON vocabulary\_id = source\_vocabulary\_id                         WHERE source\_code like '011.%'                         AND        vocabulary\_id ='ICD9CM'                        GROUP BY person\_id        ) diagnosed   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX21: How many people have a diagnosis of a contraindication for the drug they are taking?

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  ;WITH con\_rel AS        (        SELECT                r1.concept\_id\_1,                r2.concept\_id\_2        FROM                concept\_relationship AS r1                INNER JOIN concept\_relationship r2                        ON        r2.concept\_id\_1        = r1.concept\_id\_2        WHERE                r1.relationship\_id        = 'Has CI'        AND        r2.relationship\_id        = 'Ind/CI - SNOMED'        )SELECT        count(distinct d.person\_id)FROM        con\_rel AS cr                INNER JOIN        drug\_exposure AS d                        ON        cr.concept\_id\_1 = d.drug\_concept\_id                INNER JOIN        condition\_occurrence AS c                        ON        cr.concept\_id\_2        = c.condition\_concept\_id                        AND        d.person\_id                = c.person\_idwhere        d.drug\_exposure\_start\_date >= c.condition\_start\_date  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX22: How many poeple take a drug in a given class?

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| ancestor\_concept\_id | 4324992 |  Yes | Antithrombins |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT count(distinct d.person\_id) as person\_count FROM concept\_ancestor ca, drug\_exposure d WHERE d.drug\_concept\_id = ca.descendant\_concept\_id and ca.ancestor\_concept\_id = **4324992** group by ca.ancestor\_concept\_id ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| person\_count | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| person\_count |   |
| --- | --- |

  |
| --- |
### DEX23: Distribution of days supply

| This query is used to provide summary statistics for days supply (days\_supply) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT         min(tt.stat\_value) AS min\_value ,         max(tt.stat\_value) AS max\_value ,         avg(tt.stat\_value) AS avg\_value ,                (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,        APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) AS percentile\_25 ,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value ) AS median\_value ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value ) AS percential\_75 FROM         ( SELECT t.days\_supply AS stat\_value FROM drug\_exposure t where t.days\_supply > 0 ) tt ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

  |
| --- |
### DEX24: Counts of days supply

| This query is used to count days supply values across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a days\_supply. If the clause is omitted, all possible values of days\_supply are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| days\_supply | 2,3 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue.**  SELECT t.days\_supply, count(1) AS cntFROM drug\_exposure tWHERE t.days\_supply in ( **2** , **3** ) GROUP BY t.days\_supplyORDER BY days\_supply;
**Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| days\_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |
| --- | --- |
| cnt | Counts of records with the days\_supply value |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| days\_supply |  15 |
| --- | --- |
| cnt |  240179 |
| --- | --- |

  |
| --- |
### DEX25: Counts of drug records

| This query is used to count drugs (drug\_concept\_id) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes | Metoclopramid, Desmopressin, Cyclosprin |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**. SELECT count(1) as exposure\_occurrence\_count  FROM drug\_exposure WHERE drug\_concept\_id in ( **906805, 1517070, 19010522** );  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| exposure\_occurrence\_count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
| exposure\_occurrence\_count |  88318 |
| --- | --- |

  |
| --- |
### DEX26: Distribution of drug exposure end dates

| This query is used to to provide summary statistics for drug exposure end dates (drug\_exposure\_end\_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. SELECT        min(tt.end\_date) AS min\_date ,         max(tt.end\_date) AS max\_date ,         avg(tt.end\_date\_num) + tt.min\_date AS avg\_date ,         (round(stdDev(tt.end\_date\_num)) ) AS stdDev\_days ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.end\_date\_num ) ) AS percentile\_25\_date ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.end\_date\_num ) ) AS median\_date ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.end\_date\_num ) ) AS percentile\_75\_date         FROM                 ( SELECT                        (t.drug\_exposure\_end\_date - MIN(t.drug\_exposure\_end\_date) OVER()) AS end\_date\_num,                         t.drug\_exposure\_end\_date AS end\_date,                         MIN(t.drug\_exposure\_end\_date) OVER() min\_date                 FROM drug\_exposure t ) tt GROUP BY tt.min\_date ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX27: Distribution of drug exposure start dates

| This query is used to to provide summary statistics for drug exposure start dates (drug\_exposure\_start\_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query.  SELECT        min(tt.start\_date) AS min\_date ,         max(tt.start\_date) AS max\_date ,         avg(tt.start\_date\_num) + tt.min\_date AS avg\_date ,         (round(stdDev(tt.start\_date\_num)) ) AS stdDev\_days ,         tt.min\_date + (approximate PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\_date\_num ) ) AS percentile\_25\_date ,         tt.min\_date + (approximate PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\_date\_num ) ) AS median\_date ,         tt.min\_date + (approximate PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\_date\_num ) ) AS percentile\_75\_date FROM (         SELECT                (t.drug\_exposure\_start\_date - MIN(t.drug\_exposure\_start\_date) OVER()) AS start\_date\_num,                 t.drug\_exposure\_start\_date AS start\_date,                 MIN(t.drug\_exposure\_start\_date) OVER() min\_date         FROM drug\_exposure t         ) tt GROUP BY tt.min\_date ;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX28: Counts of drug types

| This query is used to count the drug type concepts (drug\_type\_concept\_id, in CDM V2 drug\_exposure\_type) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug\_type\_concept\_id. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_type\_concept\_id | 38000175, 38000180 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT count(1) as exposure\_occurrence\_count , drug\_type\_concept\_id FROM drug\_exposure WHERE drug\_concept\_id in (select distinct drug\_concept\_id from drug\_era)AND drug\_type\_concept\_id in ( **38000175** , **38000180** ) GROUP BY drug\_type\_concept\_id ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_type\_concept\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| --- | --- |
| exposure\_occurrence\_count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_type\_concept\_id |   |
| --- | --- |
| exposure\_occurrence\_count |   |
| --- | --- |

  |
| --- |
### DEX29: Distribution of number of distinct drugs persons take

| This query is used to provide summary statistics for the number of number of different distinct drugs (drug\_concept\_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT          min(tt.stat\_value) AS min\_value ,         max(tt.stat\_value) AS max\_value ,         avg(tt.stat\_value) AS avg\_value ,         (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,         APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) AS percentile\_25 ,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value ) AS median\_value ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value ) AS percential\_75 FROM (                 SELECT count(distinct t.drug\_concept\_id) AS stat\_value                 FROM drug\_exposure t                  where nvl(t.drug\_concept\_id, 0) > 0                 group by t.person\_id ) tt ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX30: Counts of number of distinct drugs persons take

| This query is used to count the number of different distinct drugs (drug\_concept\_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of drug concepts. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 15, 22 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT count(distinct t.drug\_concept\_id) AS stat\_value, t.person\_idFROM drug\_exposure tGROUP BY t.person\_id HAVING count(DISTINCT t.drug\_concept\_id) in ( **15** , **22** );  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| person\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |
| --- | --- |
| stat\_value | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| person |   |
| --- | --- |
| stat\_value |   |
| --- | --- |

  |
| --- |
### DEX31: Distribution of drug exposure records per person

| This query is used to provide summary statistics for the number of drug exposure records (drug\_exposure\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. SELECT         min(tt.stat\_value) AS min\_value ,         max(tt.stat\_value) AS max\_value ,         avg(tt.stat\_value) AS avg\_value ,         (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,         APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) AS percentile\_25 ,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value ) AS median\_value ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value ) AS percential\_75 FROM (                 SELECT count(1) AS stat\_value                 FROM drug\_exposure t                 group by t.person\_id         ) tt ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX32: Counts of drug exposure records per person

| This query is used to count the number of drug exposure records (drug\_exposure\_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| count | 3, 4 |  Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT count(1) AS stat\_value, person\_idFROM drug\_exposuregroup by person\_idhaving count(1) in ( **3** , **4** ); **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| person\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |
| --- | --- |
| count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| person\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX33: Counts of drug exposure records stratified by observation month

| This query is used to count the drug exposure records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of month numbers | 3, 5 |  Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  select extract(month from d.drug\_exposure\_start\_date) month\_num, COUNT(1) as exp\_in\_month\_count from drug\_exposure d where extract(month from d.drug\_exposure\_start\_date) in ( **3, 5** ) group by extract(month from d.drug\_exposure\_start\_date) order by 1   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_exposure\_start\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| --- | --- |
| month |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_exposure\_start\_date |   |
| --- | --- |
| month |   |
| --- | --- |

  |
| --- |
### DEX34: Distribution of drug quantity

| This query is used to provide summary statistics for drug quantity (quantity) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. SELECT         min(tt.stat\_value) AS min\_value ,         max(tt.stat\_value) AS max\_value ,         avg(tt.stat\_value) AS avg\_value ,         (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,         APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) AS percentile\_25 ,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value ) AS median\_value ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value ) AS percentile\_75 FROM (                 SELECT t.quantity AS stat\_value                 FROM drug\_exposure t                 where t.quantity > 0         ) tt ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX35: Counts of drug quantity

| This query is used to count the drug quantity (quantity) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a quantity. If the input is omitted, all possible values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| quantity (list of numbers) | 10,20 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. SELECT count(1) as drug\_quantity\_count, d.quantityFROM drug\_exposure d WHERE d.quantity in (10, 20) GROUP BY d.quantity ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_quantity\_count |   |
| --- | --- |
| quantity | The quantity of drug as recorded in the original prescription or dispensing record. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_quantity\_count |   |
| --- | --- |
| quantity |   |
| --- | --- |

  |
| --- |
### DEX36: Distribution of drug refills

| This query is used to provide summary statistics for drug refills (refills) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.
**Input:** <None>
**Sample query run:**
The following is a sample run of the query. SELECT         min(tt.stat\_value) AS min\_value ,         max(tt.stat\_value) AS max\_value ,         avg(tt.stat\_value) AS avg\_value ,         (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,         APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\_value ) AS percentile\_25 ,         APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value ) AS median\_value ,         APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value ) AS percentile\_75 FROM (                 SELECT                        t.refills AS stat\_value                 FROM drug\_exposure t                 where t.refills > 0         ) tt ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

 |
| --- |
### DEX37: Counts of drug refills

| This query is used to count the drug refills (refills) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of refills. If the input is omitted, all existing values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| refills count (list of numbers) | 10,20 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT count(1) as drug\_exposure\_count, d.refills AS refills\_count FROM drug\_exposure d WHERE d.refills in ( **10, 20** ) GROUP BY d.refills ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_exposure\_count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |
| Refills\_Count | The number of refills after the initial prescription. The initial prescription is not counted, values start with 0. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_exposure\_count |   |
| --- | --- |
| Refills\_Count |   |
| --- | --- |

  |
| --- |
### DEX38: Counts of stop reasons

| This query is used to count stop reasons (stop\_reason) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a stop\_reason. If the input is omitted, all existing values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| stop\_reason | 1 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  select count(1) as totExp , d.stop\_reason from drug\_exposure d where d.stop\_reason in ('INVALID') group by d.stop\_reason ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| Count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |
| stop\_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| Count |   |
| --- | --- |
| stop\_reason |   |
| --- | --- |

  |
| --- |
### DEX39: Counts of drugs, stratified by drug type

| This query is used to count drugs (drug\_concept\_id) across all drug exposure records stratified by drug exposure type (drug\_type\_concept\_id, in CDM V2 drug\_exposure\_type). The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id or a drug\_type\_concept\_id. If the input is omitted, all existing value combinations are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |
| --- | --- | --- | --- |
| list of drug\_type\_concept\_id | 38000180 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT t.drug\_concept\_id, count(1) as drugs\_count, t.drug\_TYPE\_concept\_id FROM drug\_exposure t where    t.drug\_concept\_id in ( **906805, 1517070, 19010522** ) and t.drug\_TYPE\_concept\_id in ( **38000175** , **38000179** ) group by t.drug\_TYPE\_concept\_id, t.drug\_concept\_id ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| drug\_type\_concept\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |
| --- | --- |
| count | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| drug\_type\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX40: Counts of drugs, stratified by relevant condition

| This query is used to count all drugs (drug\_concept\_id) across all drug exposure records stratified by condition (relevant\_condition\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id and a relevant\_condition\_concept\_id. If the input is omitted, all existing value combinations are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |
| --- | --- | --- | --- |
| list of relevant\_condition\_concept\_id | 26052, 258375 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT   t.drug\_concept\_id,  count(1) as drugs\_count,  p.procedure\_concept\_id as relevant\_condition\_concept\_idFROM drug\_exposure t        inner join procedure\_occurrence as p                on        t.visit\_occurrence\_id = p.visit\_occurrence\_id                and        t.person\_id = p.person\_idwhere   t.drug\_concept\_id in ( **906805, 1517070, 19010522** )   and p.procedure\_concept\_id in ( **26052, 258375** )group by  p.procedure\_concept\_id, t.drug\_concept\_id;   t.drug\_concept\_id in ( **906805, 1517070, 19010522** )   and t.relevant\_condition\_concept\_id in ( **26052, 258375** )group by  t.relevant\_condition\_concept\_id, t.drug\_concept\_id; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| relevant\_condition\_concept\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the condition that was the cause for initiation of the procedure. Note that this is not a direct reference to a specific condition record in the condition table, but rather a condition concept in the vocabulary |
| --- | --- |
| Count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| relevant\_condition\_concept\_id |   |
| --- | --- |
| Count |   |
| --- | --- |

  |
| --- |
### DEX41: Distribution of drug exposure start date, stratified by drug

| This query is used to provide summary statistics for start dates (drug\_exposure\_start\_date) across all drug exposure records stratified by drug (drug\_concept\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, the drug\_exposure\_start\_date for all existing values of drug\_concept\_id are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT         tt.drug\_concept\_id ,         min(tt.start\_date) AS min\_date ,         max(tt.start\_date) AS max\_date ,         avg(tt.start\_date\_num) + tt.min\_date AS avg\_date ,         (round(stdDev(tt.start\_date\_num)) ) AS stdDev\_days ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\_date\_num ) ) AS percentile\_25\_date ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\_date\_num ) ) AS median\_date ,         tt.min\_date + (APPROXIMATE PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\_date\_num ) ) AS percential\_75\_date FROM (                 SELECT                         (t.drug\_exposure\_start\_date - MIN(t.drug\_exposure\_start\_date) OVER(partition by t.drug\_concept\_id)) AS start\_date\_num,                         t.drug\_exposure\_start\_date AS start\_date,                        MIN(t.drug\_exposure\_start\_date) OVER(partition by t.drug\_concept\_id) min\_date,                        t.drug\_concept\_id                 FROM                         drug\_exposure t                 where t.drug\_concept\_id in ( **906805, 1517070, 19010522** )         ) tt GROUP BY tt.min\_date , tt.drug\_concept\_id order by tt.drug\_concept\_id ;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| min\_value |   |
| --- | --- |
| max\_value |   |
| --- | --- |
| avg\_value |   |
| --- | --- |
| stdDev\_value |   |
| --- | --- |
| percentile\_25 |   |
| --- | --- |
| median\_value |   |
| --- | --- |
| percentile\_75 |   |
| --- | --- |

  |
| --- |
### DEX42: Counts of genders, stratified by drug

| This query is used to count all gender values (gender\_concept\_id) for all exposed persons stratified by drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a gender\_concept\_id and drug\_concept\_id. If the input is omitted, all existing value combinations are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |
| --- | --- | --- | --- |
| list of gender\_concept\_id | 8507, 8532 | Yes | Male, Female |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT p.gender\_concept\_id, count(1) as gender\_count, t.drug\_concept\_id FROM drug\_exposure t, person p where p.person\_id = t.person\_idand t.drug\_concept\_id in ( **906805, 1517070, 19010522** )  and p.gender\_concept\_id in ( **8507, 8532** )group by t.drug\_concept\_id, p.gender\_concept\_idorder by t.drug\_concept\_id, p.gender\_concept\_id;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| gender\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |
| --- | --- |
| Count | The number of individual drug exposure occurrences used to construct the drug era. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| gender\_concept\_id |   |
| --- | --- |
| Count |   |
| --- | --- |

  |
| --- |
### DEX43: Counts of drug exposure records per person, stratified by drug

| This query is used to count the number of drug exposure records for all exposed persons stratified by drug (drug\_concept\_id). The input to the query is a value (or a comma-separated list of values) of a drug\_concept\_id. If the input is omitted, all existing values are summarized.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT t.drug\_concept\_id, t.person\_id, count(1) as drug\_exposure\_count FROM drug\_exposure t where t.drug\_concept\_id in ( **906805, 1517070, 19010522** ) group by t.person\_id, t.drug\_concept\_id order by t.drug\_concept\_id, t.person\_id;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| --- | --- |
| person\_id | A system-generated unique identifier for each person. |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id |   |
| --- | --- |
| person\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### DEX01: Counts of persons with any number of exposures to a certain drug

| This query is used to count the persons with at least one exposures to a certain drug (drug\\_concept\\_id).  See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all drugs in the data table are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*.  set search\\_path to full\\_201706\\_omop\\_v5; SELECT concept.concept\\_name, drug\\_concept\\_id, count(person\\_id) as num\\_persons FROMdrug\\_exposure join conceptON drug\\_concept\\_id = concept.concept\\_idwherelower(domain\\_id)='drug' and vocabulary\\_id='RxNorm' and standard\\_concept='S'and drug\\_concept\\_id in ( \*\*40165254\*\* , \*\*40165258\*\* )GROUP BY concept.concept\\_name, drug\\_concept\\_id;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept.  |

| --- | --- |

| num\\_persons | The patients count |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drug\\_name |  Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |

| --- | --- |

| drug\\_concept\\_id |  40165254 |

| --- | --- |

| num\\_persons |  191244 |

| --- | --- |

  |

| --- |

### DEX02: Counts of persons taking a drug, by age, gender, and year of exposure

| This query is used to count the persons with exposure to a certain drug (drug\\_concept\\_id), grouped by age, gender, and year of exposure. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. If the input is omitted, all drugs in the data table are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |

| --- | --- | --- | --- |

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. select drug.concept\\_name,         EXTRACT( YEAR FROM drug\\_exposure\\_start\\_date ) as year\\_of\\_exposure,        EXTRACT( YEAR FROM drug\\_exposure\\_start\\_date ) - year\\_of\\_birth as age ,         gender.concept\\_name as gender,        count(1) as num\\_personsFromdrug\\_exposure JOINperson USING( person\\_id ) join concept drug ON drug.concept\\_id = drug\\_concept\\_id JOINconcept gender ON gender.concept\\_id = gender\\_concept\\_idwhere drug\\_concept\\_id IN ( \*\*40165254\*\* , \*\*40165258\*\* ) GROUP by drug.concept\\_name, gender.concept\\_name, EXTRACT( YEAR FROM drug\\_exposure\\_start\\_date ),EXTRACT( YEAR FROM drug\\_exposure\\_start\\_date ) - year\\_of\\_birth ORDER BY concept\\_name, year\\_of\\_exposure, age, gender   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  concept\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

|  year\\_of\\_exposure |   |

| --- | --- |

|  age | The age of the person at the time of exposure |

| --- | --- |

|  gender | The gender of the person. |

| --- | --- |

|  num\\_persons | The patient count |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| concept\\_name |  Rosuvastatin calcium 40 MG Oral Tablet [Crestor] |

| --- | --- |

| year\\_of\\_exposure |  2010 |

| --- | --- |

| age |  69 |

| --- | --- |

| gender |  Male |

| --- | --- |

| num\\_persons |  15 |

| --- | --- |

  |

| --- |

### DEX03: Distribution of age, stratified by drug

| This query is used to provide summary statistics for the age across all drug exposure records stratified by drug (drug\\_concept\\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. If the input is omitted, age is summarized for all existing drug\\_concept\\_id values.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 40165254, 40165258 | Yes | Crestor 20 and 40 mg tablets |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT         concept\\_name AS drug\\_name ,         drug\\_concept\\_id ,         COUNT(\\*) AS patient\\_count ,         MIN ( age ) AS min  ,         APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY age ) AS percentile\\_25  ,         ROUND ( AVG ( age ), 2 ) AS mean,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY age ) AS median  ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY age ) AS percentile\\_75 ,         MAX ( age ) AS max ,         ROUND ( STDDEV ( age ), 1 ) AS stdDev FROM /\\*person, first drug exposure date\\*/ (                 SELECT                         drug\\_concept\\_id , person\\_id ,                         MIN( extract(year from drug\\_exposure\\_start\\_date )) - year\\_of\\_birth as age                 FROM                         drug\\_exposure JOIN full\\_201706\\_omop\\_v5.person USING( person\\_id )                 WHERE drug\\_concept\\_id IN /\\*crestor 20 and 40 mg tablets \\*/ ( \*\*40165254\*\* , \*\*40165258\*\* )                GROUP BY drug\\_concept\\_id, person\\_id , year\\_of\\_birth         ) JOIN concept ON concept\\_id = drug\\_concept\\_id WHERE domain\\_id='Drug' and standard\\_concept='S'GROUP BY concept\\_name, drug\\_concept\\_id; \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| patient\\_count | The count of patients taking the drug |

| --- | --- |

| min | The age of the youngest patient taking the drug |

| --- | --- |

| percentile\\_25 | The 25th age percentile |

| --- | --- |

| mean | The mean or average age of the patients taking the drug |

| --- | --- |

| median | The median age of the patients taking the drug |

| --- | --- |

| percentile\\_75 | The 75th age percentile |

| --- | --- |

| max  | The age of the oldest patient taking the drug |

| --- | --- |

| stddev | The standard deviation of the age distribution |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drug\\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |

| --- | --- |

| drug\\_concept\\_id | 40165254 |

| --- | --- |

| patient\\_count | 30321 |

| --- | --- |

| min | 11 |

| --- | --- |

| percentile\\_25 | 49 |

| --- | --- |

| mean | 53.87 |

| --- | --- |

| median | 55 |

| --- | --- |

| percentile\\_75 | 60 |

| --- | --- |

| max | 93 |

| --- | --- |

| stddev | 8.8 |

| --- | --- |

  |

| --- |

### DEX04: Distribution of gender in persons taking a drug

| This query is used to obtain the gender distribution of persons exposed to a certain drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. If the input is omitted, all drugs in the data table are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. select drug.concept\\_name as drug\\_name,                 drug\\_concept\\_id,                        gender.concept\\_name as gender,                count(1) as num\\_personsFromdrug\\_exposure JOIN person USING( person\\_id ) join concept drug ON drug.concept\\_id = drug\\_concept\\_id JOIN concept gender ON gender.concept\\_id = gender\\_concept\\_idwhere drug\\_concept\\_id IN ( \*\*40165254\*\* , \*\*40165258\*\* ) GROUP by drug.concept\\_name, drug\\_concept\\_id, gender.concept\\_name ORDER BY drug\\_name, drug\\_concept\\_id, gender;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | An unambiguous, meaningful and descriptive name for the drug concept. |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| gender | The gender of the counted persons exposed to drug. |

| --- | --- |

| num\\_persons | The number of persons of a particular gender exposed to drug. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drug\\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |

| --- | --- |

| drug\\_concept\\_id | 40165254 |

| --- | --- |

| gender | FEMALE |

| --- | --- |

| num\\_persons | 12590 |

| --- | --- |

  |

| --- |

### DEX05: Counts of drug records for a particular drug

| This query is used to count the drug exposure records for a certain drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. If the input is omitted, all drugs in the data table are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT concept\\_name as drug\\_name, drug\\_concept\\_id, count(\\*) as num\\_records FROM drug\\_exposure JOIN concept ON concept\\_id = drug\\_concept\\_id WHERE lower(domain\\_id)='drug' and vocabulary\\_id='RxNorm' and standard\\_concept='S'and drug\\_concept\\_id IN ( \*\*40165254\*\* , \*\*40165258\*\* )GROUP BY concept\\_name, drug\\_concept\\_id;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | An unambiguous, meaningful and descriptive name for the drug concept. |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| num\\_records | The number of drug exposure records |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drug\\_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |

| --- | --- |

| drug\\_concept\\_id | 40165254 |

| --- | --- |

| num\\_records | 191244 |

| --- | --- |

  |

| --- |

### DEX06: Counts of distinct drugs in the database

| This query is used to determine the number of distinct drugs (drug\\_concept\\_id). See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.

\*\*Input:\*\* None.

\*\*Sample query run:\*\*

The following is a sample run of the query.  SELECT count(distinct drug\\_concept\\_id) as number\\_drugs FROM drug\\_exposure JOIN concept ON concept\\_id = drug\\_concept\\_id WHERE lower(domain\\_id)='drug' and vocabulary\\_id='RxNorm' and standard\\_concept='S';   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| number\\_drugs | The count of distinct drug concepts. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| number\\_drugs | 10889 |

| --- | --- |

  |

| --- |

### DEX07: Maximum number of drug exposure events per person over some time period

| This query is to determine the maximum number of drug exposures that is recorded for a patient during a certain time period. If the time period is omitted, the entire time span of the database is considered. Instead of maximum, the query can be easily changed to obtained the average or the median number of drug records for all patients. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| date from | 01-Jan-2008 | Yes | |

| --- | --- | --- | --- |

| date to | 31-Dec-2008 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. select max(exposures ) as exposures\\_count from (SELECT drug\\_exposure.person\\_id, COUNT(\\*) exposures FROM drug\\_exposure JOIN personON drug\\_exposure.person\\_id = person.person\\_idWHERE drug\\_concept\\_id in (select distinct concept\\_id from concept                                                 WHERE lower(domain\\_id)='drug' and vocabulary\\_id='RxNorm' and standard\\_concept='S')AND drug\\_exposure\\_start\\_date BETWEEN \*\*'2017-01-01'\*\* AND \*\*'2017-12-31'\*\* GROUP BY drug\\_exposure.person\\_id);    \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| exposures\\_count | The number of drug exposure records for the patient with the maximum number of such records. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| exposures\\_count | 1137 |

| --- | --- |

  |

| --- |

### DEX08: Maximum number of distinct drugs per person over some time period

| This query is to determine the maximum number of distinct drugs a patient is exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| date from | 01-Jan-2008 | Yes |   |

| --- | --- | --- | --- |

| date to | 31-Dec-2008 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. select max(drugs) as drugs\\_count from (SELECT COUNT( DISTINCT drug\\_concept\\_id) drugs FROM drug\\_exposure JOIN personON drug\\_exposure.person\\_id = person.person\\_idWHERE drug\\_concept\\_id in (select distinct concept\\_id from concept                                                 WHERE lower(domain\\_id)='drug' and vocabulary\\_id='RxNorm' and standard\\_concept='S')AND drug\\_exposure\\_start\\_date BETWEEN \*\*'2017-01-01'\*\* AND \*\*'2017-12-31'\*\* GROUP BY drug\\_exposure.person\\_id); \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drugs\\_count | The maximum number of distinct drugs a patient is exposed to during the time period |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drugs\\_count | 141 |

| --- | --- |

  |

| --- |

### DEX09: Distribution of distinct drugs per person over some time period

| This query is to determine the distribution of distinct drugs patients are exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| date from | 01-Jan-2008 | Yes |   |

| --- | --- | --- | --- |

| date to | 31-Dec-2008 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*.  SELECT MIN ( drugs ) AS min , approximate  PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY drugs ) as percentile\\_25, ROUND ( AVG ( drugs ), 2 ) AS mean, approximate PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY drugs ) AS median , approximate PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY drugs ) AS percential\\_75, MAX ( drugs ) AS max,  ROUND ( STDDEV ( drugs ), 1 ) AS stdDev  FROM  (SELECT person\\_id, NVL( drugs, 0 ) AS drugs FROM person  JOIN  ( SELECT person\\_id, COUNT( DISTINCT drug\\_concept\\_id ) AS drugs FROM drug\\_exposure  WHERE drug\\_exposure\\_start\\_date BETWEEN \*\*'2017-01-01'\*\* AND \*\*'2017-12-31'\*\* GROUP BY person\\_id ) USING( person\\_id ) );  \*\*Output:\*\*

Output field list:

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

| min | The minimum number of drugs taken by a patient |

| --- | --- |

| percentile\\_25 | The 25th percentile of the distibution |

| --- | --- |

| mean | The mean or average of drugs taken by patients |

| --- | --- |

| median | The median number of drugs take |

| --- | --- |

| percentile\\_75 | The 75th percentile of the distribution |

| --- | --- |

| max | The maximum number of drugs taken by a patient |

| --- | --- |

| stddev | The standard deviation of the age distribution |

| --- | --- |



Sample output record:

| \*\*Field\*\* | \*\* Content\*\* |

| --- | --- |

| min | 0 |

| --- | --- |

| percentile\\_25 | 0 |

| --- | --- |

| mean | 1.73 |

| --- | --- |

| median | 0 |

| --- | --- |

| percentile\\_75 | 1 |

| --- | --- |

| max | 141 |

| --- | --- |

| stddev | 4.2 |

| --- | --- |

  |

| --- |

### DEX10: Other drugs (conmeds) patients exposed to a certain drug take over some time period

| This query is used to establish the medication (conmeds) taken by patients who also are exposed to a certain drug in a given time period. The query returns the number of patients taking the drug at least once. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id and the time period. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values. \*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug concept ids | 1336825, 19047763 | Yes | Bortezomib, Thalidomide 50 mg capsules |

| --- | --- | --- | --- |

| from\\_date | 01-jan-2008 | Yes |   |

| --- | --- | --- | --- |

| to\\_date | 31-dec-2009 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*.

SELECT concept\\_name, COUNT(1) as personsFROM ( --Other drugs people are taking  SELECT DISTINCT cohort.person\\_id, drug.drug\\_concept\\_id  FROM (   --person with specific drug in time frame  SELECT DISTINCT person\\_id, drug\\_concept\\_id, from\\_date, to\\_date  FROM drug\\_exposure  JOIN (   --date range   SELECT \*\*'01-jan-2008'\*\* AS from\\_date , \*\*'31-dec-2009'\*\* AS to\\_date )   ON drug\\_exposure\\_start\\_date BETWEEN from\\_date AND to\\_date  WHERE drug\\_concept\\_id IN /\\*bortezomib, Thalidomide 50 mg capsules \\*/  ( \*\*1336825\*\* , \*\*19047763\*\* )  ) cohort  JOIN drug\\_exposure drug   ON drug.person\\_id = cohort.person\\_id  AND drug.drug\\_concept\\_id != cohort.drug\\_concept\\_id  AND drug.drug\\_exposure\\_start\\_date BETWEEN from\\_date AND to\\_date  WHERE drug.drug\\_concept\\_id != 0 /\\* unmapped drug \\*/  )JOIN concept ON concept\\_id = drug\\_concept\\_idGROUP By concept\\_name ORDER BY persons DESC;

\*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | An unambiguous, meaningful and descriptive name for the conmeds. |

| --- | --- |

| persons | count of patients taking the drug at least once |

| --- | --- |



Sample output record:

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

| drug\\_name | Dexamethasone 4 MG Oral Tablet |

| --- | --- |

| persons | 190 |

| --- | --- |

  |

| --- |

### DEX11: Distribution of brands used for a given generic drug

| This query provides the brands that are used for a generic drug. The input to the query is a value of a drug\\_concept\\_id. See [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.  Note that depending on the mapping available for the source\\_values in the drug\\_exposure table, branded drug information might only partially or not be provided. See the Standard Vocabulary Specifications at  [http://omop.org/Vocabularies](http://omop.org/Vocabularies).

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 19019306 | Yes | Nicotine Patch |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT        tt.drug\\_name,                tt.brand\\_name,                100.00\\*tt.part\\_brand/tt.total\\_brand as perc\\_brand\\_countFROM        (        SELECT        t.drug\\_name,                        t.brand\\_name,                        t.cn\\_3\\_02 part\\_brand,                        SUM(t.cn\\_3\\_02) OVER() total\\_brand                        FROM                                (                                        SELECT        sum((select count(1) from drug\\_exposure d where d.drug\\_concept\\_id = cr003.concept\\_id\\_2)) cn\\_3\\_02,                                                        A.Concept\\_Name drug\\_name,                                                        D.Concept\\_Name brand\\_name                                        FROM                                                concept AS A                                                INNER JOIN        concept\\_relationship AS CR003                                                        ON CR003.concept\\_id\\_1        = A.concept\\_id                                                INNER JOIN        concept\\_relationship AS CR007                                                        ON        CR007.concept\\_id\\_2                = CR003.concept\\_id\\_2                                                INNER JOIN                                                        concept\\_relationship AS CR006                                                                ON        CR007.concept\\_id\\_1                = CR006.concept\\_id\\_1                                                INNER JOIN                                                        concept D                                                                ON        CR006.concept\\_id\\_2                = D.concept\\_id                                        WHERE                                                CR003.relationship\\_ID        = 'Has tradename'                                        AND        A.concept\\_class\\_id                = 'Clinical Drug'                                        AND        CR007.relationship\\_ID        = 'Constitutes'                                        AND        CR006.relationship\\_ID        = 'Has brand name'                                        AND        D.concept\\_class\\_id                = 'Brand Name'                                        AND        A.concept\\_id                        = \*\*35606533\*\*                                         GROUP BY        A.Concept\\_Name,                                                                D.Concept\\_Name                                ) t         ) ttWHERE tt.total\\_brand > 0 ;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_name | The name of the query drug |

| --- | --- |

| brand\\_name | The name of the brand |

| --- | --- |

| perc\\_brand\\_count | The market share for each brand |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Content\*\* |

| --- | --- |

| drug\\_name |   |

| --- | --- |

| brand\\_name |   |

| --- | --- |

| perc\\_brand\\_count |   |

| --- | --- |

  |

| --- |

### DEX12: Distribution of forms used for a given ingredient

| This query determines the percent distribution of forms of drug products containing a given ingredient. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  ingredient.concept\\_id |  1125315 |  Yes |  Acetaminophen |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameter is highlighted in  \*\*blue\*\*. SELECT tt.form\\_name,(100.00 \\* tt.part\\_form / tt.total\\_forms) as percent\\_formsFROM (SELECT t.form\\_name,t.cn part\\_form,SUM(t.cn) OVER() total\\_formsFROM (select count(1) as cn,drugform.concept\\_name form\\_nameFROM concept ingredient,concept\\_ancestor a,concept drug,concept\\_relationship r,concept drugformWHERE ingredient.concept\\_id = \*\*1125315\*\* --AcetaminophenAND ingredient.concept\\_class\\_id = 'Ingredient'AND ingredient.concept\\_id = a.ancestor\\_concept\\_idAND a.descendant\\_concept\\_id = drug.concept\\_id--AND drug.concept\\_level = 1 --ensure it is drug productANd drug.standard\\_concept='S'AND drug.concept\\_id = r.concept\\_id\\_1AND r.concept\\_id\\_2 = drugform.concept\\_idAND drugform.concept\\_class\\_id = 'Dose Form' GROUP BY drugform.concept\\_name) t WHERE t.cn>0 --don't count forms that exist but are not used in the data) ttWHERE tt.total\\_forms > 0 --avoid division by 0ORDER BY percent\\_forms desc;    \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| form\\_name | The concept name of the dose form |

| --- | --- |

| percent\\_forms | The percent of forms drug products have containing the ingredient |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| form\\_name |  Oral Tablet |

| --- | --- |

| percent\\_forms |  95.69 |

| --- | --- |

  |

| --- |

### DEX13: Distribution of provider specialities prescribing a given drug

| This query provides the provider specialties prescribing a given drug, and the frequencies for each provider prescribing the drug (drug exposure records). Note that many databases do not record the prescribing provider for drugs. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug\\_concept\\_id values.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 2213473 | Yes | Influenza virus vaccine |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*.

SELECT  concept\\_name AS specialty,   count(\\*) AS prescriptions\\_count  FROM   /\\*first prescribing provider for statin\\*/  ( SELECT person\\_id, provider\\_id  FROM drug\\_exposure  WHERE NVL( drug\\_exposure.provider\\_id, 0 ) > 0  AND drug\\_concept\\_id = \*\*2213473\*\*  /\\* Influenza virus vaccine \\*/  ) drug  JOIN provider ON provider.provider\\_id = drug.provider\\_id   JOIN concept ON concept\\_id = provider.specialty\\_concept\\_id  WHERE concept.vocabulary\\_id='Specialty'  AND concept.standard\\_concept='S'  GROUP BY concept\\_name  ORDER BY prescriptions\\_count desc;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| specialty | The concept name of the specialty concept |

| --- | --- |

| prescriptions\\_count | The count of drug exposure records providers from the specialties are listed as prescribing provider. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| specialty |  Family Practice |

| --- | --- |

| prescriptions\\_count |  214825 |

| --- | --- |

  |

| --- |

### DEX14: Among people who take drug A, how many take drug B at the same time?

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_id | 21502747 | Yes | Statins |

| --- | --- | --- | --- |

| ancestor\\_concept\\_id | 21500223 | Yes | Antihypertensive Therapy Agents |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT count(\\*) AS num\\_A\\_users , SUM( bp\\_also ) AS num\\_also\\_using\\_B FROM /\\* people taking statin and possible taking antihypertensive agent \\*/         ( SELECT statin.person\\_id, MAX( NVL( bp, 0 ) ) AS bp\\_also                 FROM /\\*people taking statin \\*/                         ( SELECT  person\\_id, drug\\_exposure\\_start\\_date, drug\\_exposure\\_end\\_date                                 FROM drug\\_exposure statin                                 WHERE drug\\_concept\\_id IN /\\*statins\\*/                                         ( SELECT concept\\_id                                                 FROM concept                                                 JOIN concept\\_ancestor ON descendant\\_concept\\_id = concept\\_id                                                 WHERE                                                 ancestor\\_concept\\_id = \*\*21502747\*\*                                                 AND standard\\_concept = 'S'                                                 AND sysdate BETWEEN valid\\_start\\_date AND valid\\_end\\_date ) ) statin                                                                                LEFT OUTER JOIN /\\* people taking antihypertensive agent \\*/                         ( SELECT  person\\_id, drug\\_exposure\\_start\\_date, drug\\_exposure\\_end\\_date , 1 AS bp                                 FROM drug\\_exposure                                 WHERE drug\\_concept\\_id IN /\\*Antihypertensive Therapy Agents \\*/                                         ( SELECT concept\\_id                                                 FROM concept                                                 JOIN concept\\_ancestor ON descendant\\_concept\\_id = concept\\_id                                                 WHERE                                                 ancestor\\_concept\\_id = \*\*21500223\*\*                                                 AND standard\\_concept = 'S'                                                 AND sysdate BETWEEN valid\\_start\\_date AND valid\\_end\\_date ) ) bp         ON bp.person\\_id = statin.person\\_id         AND bp.drug\\_exposure\\_start\\_date < statin.drug\\_exposure\\_end\\_date         AND bp.drug\\_exposure\\_end\\_date > statin.drug\\_exposure\\_start\\_date         GROUP BY statin.person\\_id );      \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

| person\\_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |

| --- | --- |

| ancestor\\_concept\\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |

| --- | --- |

| drug\\_exposure\\_start\\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |

| --- | --- |

| drug\\_exposure\\_end\\_date | The end date for the current instance of drug utilization. It is not available from all sources. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name |   |

| --- | --- |

| person\\_id |   |

| --- | --- |

| ancestor\\_concept\\_id |   |

| --- | --- |

| drug\\_exposure\\_start\\_date |   |

| --- | --- |

| drug\\_exposure\\_end\\_date |   |

| --- | --- |

  |

| --- |

### DEX15: Number of persons taking a given drug having at least a 180 day period prior and a 365 day follow-up period

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_id | 21502747 | Yes | Statins |

| --- | --- | --- | --- |

|   |   |   |   |

| --- | --- | --- | --- |

|   |   |   |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT        floor( ( observation\\_period\\_end\\_date - index\\_date ) / 365 ) AS follow\\_up\\_years,         count(\\*) AS persons FROM /\\* statin users with 180 clean period and at least 1 year follow up period \\*/         (         SELECT person\\_id, index\\_date , observation\\_period\\_start\\_date , observation\\_period\\_end\\_date         FROM /\\*statin user start\\_date \\*/                 (                 SELECT                         person\\_id,                         min( drug\\_exposure\\_start\\_date ) AS index\\_date                 FROM drug\\_exposure statin                 WHERE drug\\_concept\\_id IN /\\*statins \\*/                          (                         SELECT concept\\_id                         FROM concept                         JOIN concept\\_ancestor ON descendant\\_concept\\_id = concept\\_id                         WHERE ancestor\\_concept\\_id = \*\*21502747\*\*                         --AND vocabulary\\_id = 8                         AND vocabulary\\_id = 'RxNorm'                        AND standard\\_concept = 'S'                         AND sysdate BETWEEN valid\\_start\\_date AND valid\\_end\\_date ) GROUP BY person\\_id )         JOIN observation\\_period USING( person\\_id )         WHERE observation\\_period\\_start\\_date + \*\*180\*\* < index\\_date AND observation\\_period\\_end\\_date > index\\_date + 365        ) GROUP BY floor( ( observation\\_period\\_end\\_date - index\\_date ) / \*\*365\*\* ) ORDER BY 1;      \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

| person\\_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |

| --- | --- |

| ancestor\\_concept\\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |

| --- | --- |

| descendant\\_concept\\_id | A foreign key to the concept code in the concept table for the lower-level concept that forms the descendant in the relationship. |

| --- | --- |

| observation\\_period\\_start\\_date | The start date of the observation period for which data are available from the data source. |

| --- | --- |

| observation\\_period\\_end\\_date | The end date of the observation period for which data are available from the data source. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name |   |

| --- | --- |

| person\\_id |   |

| --- | --- |

| ancestor\\_concept\\_id |   |

| --- | --- |

| descendant\\_concept\\_id |   |

| --- | --- |

| observation\\_period\\_start\\_date |   |

| --- | --- |

| observation\\_period\\_end\\_date |   |

| --- | --- |

  |

| --- |

### DEX16: Adherence/compliance - what is adherence rate for given drug?

| Define adherence as sum of days supply divided by length of treatment period.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 996416 | Yes | Finasteride |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT concept\\_name, count(\\*) AS number\\_of\\_eras , avg( treatment\\_length ) AS average\\_treatment\\_length\\_count , avg(adherence) avgerage\\_adherence\\_count FROM        ( SELECT person\\_id, concept\\_name, drug\\_era\\_start\\_date , sum( days\\_supply ), treatment\\_length ,          sum( days\\_supply ) / treatment\\_length AS adherence , min( has\\_null\\_days\\_supply ) AS null\\_day\\_supply          FROM /\\* drug era and individual drug encounters making up the era \\*/                 ( SELECT person\\_id, ingredient\\_concept\\_id , drug\\_era\\_start\\_date, drug\\_era\\_end\\_date ,                  drug\\_era\\_end\\_date - drug\\_era\\_start\\_date AS treatment\\_length , drug\\_exposure\\_start\\_date , days\\_supply ,                  DECODE( NVL( days\\_supply, 0 ), 0, 0, 1 ) has\\_null\\_days\\_supply                  FROM /\\*drug era of people taking finasteride \\*/                         ( SELECT person\\_id, drug\\_concept\\_id as ingredient\\_concept\\_id , drug\\_era\\_start\\_date, drug\\_era\\_end\\_date                                 FROM drug\\_era                                 --WHERE drug\\_concept\\_id = \*\*996416\*\* /\\* Finasteride \\*/                                 )                                 JOIN /\\* drug exposures making up the era \\*/                                 ( SELECT person\\_id, days\\_supply, drug\\_exposure\\_start\\_date                                         FROM drug\\_exposure                                         JOIN concept\\_ancestor ON descendant\\_concept\\_id = drug\\_concept\\_id                                         JOIN concept ON concept\\_id = ancestor\\_concept\\_id                                         WHERE LOWER(concept\\_class\\_id) = 'ingredient'                                         AND sysdate BETWEEN valid\\_start\\_date AND valid\\_end\\_date                                         AND ancestor\\_concept\\_id = 996416                                         /\\*Finasteride\\*/ ) USING( person\\_id )                         WHERE drug\\_exposure\\_start\\_date BETWEEN drug\\_era\\_start\\_date AND drug\\_era\\_end\\_date )                 JOIN concept ON concept\\_id = ingredient\\_concept\\_id         GROUP BY person\\_id, concept\\_name, drug\\_era\\_start\\_date, treatment\\_length ) WHERE treatment\\_length > 100 and null\\_day\\_supply > 0 GROUP BY concept\\_name;      \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name | An unambiguous, meaningful and descriptive name for the concept. |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| concept\\_class | The category or class of the concept along both the hierarchical tree as well as different domains within a vocabulary. Examples are "Clinical Drug", "Ingredient", "Clinical Finding" etc. |

| --- | --- |

| treatment\\_length |   |

| --- | --- |

| person\\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |

| --- | --- |

| drug\\_era\\_start\\_date | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |

| --- | --- |

| drug\\_exposure\\_start\\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |

| --- | --- |

| days\\_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |

| --- | --- |

| drug\\_era\\_end\\_date | The end date for the drug era constructed from the individual instance of drug exposures. It is the end date of the final continuously recorded instance of utilization of a drug. |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| ancestor\\_concept\\_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name |   |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| concept\\_class |   |

| --- | --- |

| treatment\\_length |   |

| --- | --- |

| person\\_id |   |

| --- | --- |

| drug\\_era\\_start\\_date |   |

| --- | --- |

| drug\\_exposure\\_start\\_date |   |

| --- | --- |

| days\\_supply |   |

| --- | --- |

| drug\\_era\\_end\\_date |   |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| ancestor\\_concept\\_id |   |

| --- | --- |

  |

| --- |

### DEX17: Why do people stop treatment?

| This query provides a list of stop treatment and their frequency.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT stop\\_reason, count(\\*) AS reason\\_freq FROM drug\\_exposure WHERE stop\\_reason IS NOT null GROUP BY stop\\_reason ORDER BY reason\\_freq DESC;

\*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| stop\\_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |

| --- | --- |

| reason\\_freq |  Frequency of stop reason |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| stop\\_reason |  Regimen Completed |

| --- | --- |

| reason\\_freq |  14712428 |

| --- | --- |

  |

| --- |

### DEX18: What is the distribution of DRUG\\_TYPE\\_CONCEPT\\_ID (modes of distribution) for a given drug?

|

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT concept\\_name, count(\\*) as drug\\_type\\_count FROM drug\\_exposure JOIN concept ON concept\\_id = drug\\_type\\_concept\\_id GROUP BY concept\\_name ORDER BY drug\\_type\\_count DESC;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_type\\_concept\\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |

| --- | --- |

| drug\\_type\\_count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_type\\_concept\\_id |   |

| --- | --- |

| drug\\_type\\_count |   |

| --- | --- |

  |

| --- |

### DEX19: How many people are taking a drug for a given indication?

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | Acute Tuberculosis | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT concept\\_name, count( distinct person\\_id )  FROM drug\\_exposure JOIN /\\* indication and associated drug ids \\*/         (select indication.concept\\_name, drug.concept\\_id                from concept indication                 JOIN concept\\_ancestor ON ancestor\\_concept\\_id = indication.concept\\_id                 JOIN vocabulary indication\\_vocab ON indication\\_vocab.vocabulary\\_id = indication.vocabulary\\_id                JOIN concept drug ON drug.concept\\_id = descendant\\_concept\\_id                 JOIN vocabulary drug\\_vocab ON drug\\_vocab.vocabulary\\_id = drug.vocabulary\\_id                 WHERE sysdate BETWEEN drug.valid\\_start\\_date AND drug.valid\\_end\\_date                AND drug\\_vocab.vocabulary\\_id = \*\*'RxNorm'\*\*                 AND indication.concept\\_class\\_id = 'Indication'                AND indication\\_vocab.vocabulary\\_name = 'Indications and Contraindications (FDB)'                AND indication.concept\\_name = \*\*'Active Tuberculosis'\*\* /\\*This filter can be changed or omitted if count need for all indication\\*/                AND drug.standard\\_concept='S'        )ON concept\\_id = drug\\_concept\\_id GROUP BY concept\\_name;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |

| --- | --- |

| count |   |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| concept\\_name |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### DEX20: How many people taking a drug for a given indicaton actually have that disease in their record prior to exposure?

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | Acute Tuberculosis | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT         count(\\*) AS treated         FROM /\\* person and tuberculosis treatment start date \\*/         (                 SELECT                         person\\_id,                         min( drug\\_exposure\\_start\\_date ) AS treatment\\_start                 FROM drug\\_exposure         JOIN /\\*indication and associated drug ids \\*/                 ( SELECT                         indication.concept\\_name,                         drug.concept\\_id                         --, indication.domain\\_id, drug.concept\\_id                        FROM concept indication                         JOIN concept\\_ancestor ON ancestor\\_concept\\_id = indication.concept\\_id                         JOIN vocabulary indication\\_vocab ON indication\\_vocab.vocabulary\\_id = indication.vocabulary\\_id                         JOIN concept drug ON drug.concept\\_id = descendant\\_concept\\_id                         JOIN vocabulary drug\\_vocab ON drug\\_vocab.vocabulary\\_id = drug.vocabulary\\_id                         WHERE                         indication\\_vocab.vocabulary\\_name = 'Indications and Contraindications (FDB)'                        AND indication.domain\\_id = 'Drug'                        AND indication.concept\\_name = \*\*'Active Tuberculosis'\*\*                         AND drug\\_vocab.vocabulary\\_name = \*\*'RxNorm (NLM)\*\*'                        AND drug.standard\\_concept = 'S'                         AND sysdate BETWEEN drug.valid\\_start\\_date AND drug.valid\\_end\\_date )         ON concept\\_id = drug\\_concept\\_id GROUP BY person\\_id ) treated LEFT OUTER JOIN /\\*patient with Acute Tuberculosis diagnosis \\*/         ( SELECT                         person\\_id, min( condition\\_start\\_date ) first\\_diagnosis, 1 AS diagnosed                        FROM condition\\_occurrence                         JOIN source\\_to\\_concept\\_map ON target\\_concept\\_id = condition\\_concept\\_id                         JOIN vocabulary ON vocabulary\\_id = source\\_vocabulary\\_id                         WHERE source\\_code like '011.%'                         AND        vocabulary\\_id ='ICD9CM'                        GROUP BY person\\_id        ) diagnosed   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### DEX21: How many people have a diagnosis of a contraindication for the drug they are taking?

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|   |   |   |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  ;WITH con\\_rel AS        (        SELECT                r1.concept\\_id\\_1,                r2.concept\\_id\\_2        FROM                concept\\_relationship AS r1                INNER JOIN concept\\_relationship r2                        ON        r2.concept\\_id\\_1        = r1.concept\\_id\\_2        WHERE                r1.relationship\\_id        = 'Has CI'        AND        r2.relationship\\_id        = 'Ind/CI - SNOMED'        )SELECT        count(distinct d.person\\_id)FROM        con\\_rel AS cr                INNER JOIN        drug\\_exposure AS d                        ON        cr.concept\\_id\\_1 = d.drug\\_concept\\_id                INNER JOIN        condition\\_occurrence AS c                        ON        cr.concept\\_id\\_2        = c.condition\\_concept\\_id                        AND        d.person\\_id                = c.person\\_idwhere        d.drug\\_exposure\\_start\\_date >= c.condition\\_start\\_date  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### DEX22: How many poeple take a drug in a given class?

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| ancestor\\_concept\\_id | 4324992 |  Yes | Antithrombins |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT count(distinct d.person\\_id) as person\\_count FROM concept\\_ancestor ca, drug\\_exposure d WHERE d.drug\\_concept\\_id = ca.descendant\\_concept\\_id and ca.ancestor\\_concept\\_id = \*\*4324992\*\* group by ca.ancestor\\_concept\\_id ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_count | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_count |   |

| --- | --- |

  |

| --- |

### DEX23: Distribution of days supply

| This query is used to provide summary statistics for days supply (days\\_supply) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT         min(tt.stat\\_value) AS min\\_value ,         max(tt.stat\\_value) AS max\\_value ,         avg(tt.stat\\_value) AS avg\\_value ,                (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,        APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) AS percentile\\_25 ,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS median\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS percential\\_75 FROM         ( SELECT t.days\\_supply AS stat\\_value FROM drug\\_exposure t where t.days\\_supply > 0 ) tt ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

  |

| --- |

### DEX24: Counts of days supply

| This query is used to count days supply values across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a days\\_supply. If the clause is omitted, all possible values of days\\_supply are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| days\\_supply | 2,3 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue.\*\*  SELECT t.days\\_supply, count(1) AS cntFROM drug\\_exposure tWHERE t.days\\_supply in ( \*\*2\*\* , \*\*3\*\* ) GROUP BY t.days\\_supplyORDER BY days\\_supply;

\*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| days\\_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |

| --- | --- |

| cnt | Counts of records with the days\\_supply value |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| days\\_supply |  15 |

| --- | --- |

| cnt |  240179 |

| --- | --- |

  |

| --- |

### DEX25: Counts of drug records

| This query is used to count drugs (drug\\_concept\\_id) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes | Metoclopramid, Desmopressin, Cyclosprin |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*. SELECT count(1) as exposure\\_occurrence\\_count  FROM drug\\_exposure WHERE drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* );  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| exposure\\_occurrence\\_count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

| exposure\\_occurrence\\_count |  88318 |

| --- | --- |

  |

| --- |

### DEX26: Distribution of drug exposure end dates

| This query is used to to provide summary statistics for drug exposure end dates (drug\\_exposure\\_end\\_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. SELECT        min(tt.end\\_date) AS min\\_date ,         max(tt.end\\_date) AS max\\_date ,         avg(tt.end\\_date\\_num) + tt.min\\_date AS avg\\_date ,         (round(stdDev(tt.end\\_date\\_num)) ) AS stdDev\\_days ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.end\\_date\\_num ) ) AS percentile\\_25\\_date ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.end\\_date\\_num ) ) AS median\\_date ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.end\\_date\\_num ) ) AS percentile\\_75\\_date         FROM                 ( SELECT                        (t.drug\\_exposure\\_end\\_date - MIN(t.drug\\_exposure\\_end\\_date) OVER()) AS end\\_date\\_num,                         t.drug\\_exposure\\_end\\_date AS end\\_date,                         MIN(t.drug\\_exposure\\_end\\_date) OVER() min\\_date                 FROM drug\\_exposure t ) tt GROUP BY tt.min\\_date ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX27: Distribution of drug exposure start dates

| This query is used to to provide summary statistics for drug exposure start dates (drug\\_exposure\\_start\\_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query.  SELECT        min(tt.start\\_date) AS min\\_date ,         max(tt.start\\_date) AS max\\_date ,         avg(tt.start\\_date\\_num) + tt.min\\_date AS avg\\_date ,         (round(stdDev(tt.start\\_date\\_num)) ) AS stdDev\\_days ,         tt.min\\_date + (approximate PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\\_date\\_num ) ) AS percentile\\_25\\_date ,         tt.min\\_date + (approximate PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) ) AS median\\_date ,         tt.min\\_date + (approximate PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) ) AS percentile\\_75\\_date FROM (         SELECT                (t.drug\\_exposure\\_start\\_date - MIN(t.drug\\_exposure\\_start\\_date) OVER()) AS start\\_date\\_num,                 t.drug\\_exposure\\_start\\_date AS start\\_date,                 MIN(t.drug\\_exposure\\_start\\_date) OVER() min\\_date         FROM drug\\_exposure t         ) tt GROUP BY tt.min\\_date ;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX28: Counts of drug types

| This query is used to count the drug type concepts (drug\\_type\\_concept\\_id, in CDM V2 drug\\_exposure\\_type) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug\\_type\\_concept\\_id. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_type\\_concept\\_id | 38000175, 38000180 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT count(1) as exposure\\_occurrence\\_count , drug\\_type\\_concept\\_id FROM drug\\_exposure WHERE drug\\_concept\\_id in (select distinct drug\\_concept\\_id from drug\\_era)AND drug\\_type\\_concept\\_id in ( \*\*38000175\*\* , \*\*38000180\*\* ) GROUP BY drug\\_type\\_concept\\_id ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_type\\_concept\\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |

| --- | --- |

| exposure\\_occurrence\\_count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_type\\_concept\\_id |   |

| --- | --- |

| exposure\\_occurrence\\_count |   |

| --- | --- |

  |

| --- |

### DEX29: Distribution of number of distinct drugs persons take

| This query is used to provide summary statistics for the number of number of different distinct drugs (drug\\_concept\\_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT          min(tt.stat\\_value) AS min\\_value ,         max(tt.stat\\_value) AS max\\_value ,         avg(tt.stat\\_value) AS avg\\_value ,         (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) AS percentile\\_25 ,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS median\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS percential\\_75 FROM (                 SELECT count(distinct t.drug\\_concept\\_id) AS stat\\_value                 FROM drug\\_exposure t                  where nvl(t.drug\\_concept\\_id, 0) > 0                 group by t.person\\_id ) tt ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX30: Counts of number of distinct drugs persons take

| This query is used to count the number of different distinct drugs (drug\\_concept\\_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of drug concepts. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 15, 22 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT count(distinct t.drug\\_concept\\_id) AS stat\\_value, t.person\\_idFROM drug\\_exposure tGROUP BY t.person\\_id HAVING count(DISTINCT t.drug\\_concept\\_id) in ( \*\*15\*\* , \*\*22\*\* );  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |

| --- | --- |

| stat\\_value | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person |   |

| --- | --- |

| stat\\_value |   |

| --- | --- |

  |

| --- |

### DEX31: Distribution of drug exposure records per person

| This query is used to provide summary statistics for the number of drug exposure records (drug\\_exposure\\_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. SELECT         min(tt.stat\\_value) AS min\\_value ,         max(tt.stat\\_value) AS max\\_value ,         avg(tt.stat\\_value) AS avg\\_value ,         (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) AS percentile\\_25 ,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS median\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS percential\\_75 FROM (                 SELECT count(1) AS stat\\_value                 FROM drug\\_exposure t                 group by t.person\\_id         ) tt ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX32: Counts of drug exposure records per person

| This query is used to count the number of drug exposure records (drug\\_exposure\\_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| count | 3, 4 |  Yes |   |

| --- | --- | --- | --- |

\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT count(1) AS stat\\_value, person\\_idFROM drug\\_exposuregroup by person\\_idhaving count(1) in ( \*\*3\*\* , \*\*4\*\* ); \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |

| --- | --- |

| count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### DEX33: Counts of drug exposure records stratified by observation month

| This query is used to count the drug exposure records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of month numbers | 3, 5 |  Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  select extract(month from d.drug\\_exposure\\_start\\_date) month\\_num, COUNT(1) as exp\\_in\\_month\\_count from drug\\_exposure d where extract(month from d.drug\\_exposure\\_start\\_date) in ( \*\*3, 5\*\* ) group by extract(month from d.drug\\_exposure\\_start\\_date) order by 1   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_start\\_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |

| --- | --- |

| month |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_start\\_date |   |

| --- | --- |

| month |   |

| --- | --- |

  |

| --- |

### DEX34: Distribution of drug quantity

| This query is used to provide summary statistics for drug quantity (quantity) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. SELECT         min(tt.stat\\_value) AS min\\_value ,         max(tt.stat\\_value) AS max\\_value ,         avg(tt.stat\\_value) AS avg\\_value ,         (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) AS percentile\\_25 ,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS median\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS percentile\\_75 FROM (                 SELECT t.quantity AS stat\\_value                 FROM drug\\_exposure t                 where t.quantity > 0         ) tt ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX35: Counts of drug quantity

| This query is used to count the drug quantity (quantity) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a quantity. If the input is omitted, all possible values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| quantity (list of numbers) | 10,20 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. SELECT count(1) as drug\\_quantity\\_count, d.quantityFROM drug\\_exposure d WHERE d.quantity in (10, 20) GROUP BY d.quantity ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_quantity\\_count |   |

| --- | --- |

| quantity | The quantity of drug as recorded in the original prescription or dispensing record. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_quantity\\_count |   |

| --- | --- |

| quantity |   |

| --- | --- |

  |

| --- |

### DEX36: Distribution of drug refills

| This query is used to provide summary statistics for drug refills (refills) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

\*\*Input:\*\* <None>

\*\*Sample query run:\*\*

The following is a sample run of the query. SELECT         min(tt.stat\\_value) AS min\\_value ,         max(tt.stat\\_value) AS max\\_value ,         avg(tt.stat\\_value) AS avg\\_value ,         (round(stdDev(tt.stat\\_value)) ) AS stdDev\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat\\_value ) AS percentile\\_25 ,         APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS median\\_value ,         APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\\_value ) AS percentile\\_75 FROM (                 SELECT                        t.refills AS stat\\_value                 FROM drug\\_exposure t                 where t.refills > 0         ) tt ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

 |

| --- |

### DEX37: Counts of drug refills

| This query is used to count the drug refills (refills) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of refills. If the input is omitted, all existing values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| refills count (list of numbers) | 10,20 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT count(1) as drug\\_exposure\\_count, d.refills AS refills\\_count FROM drug\\_exposure d WHERE d.refills in ( \*\*10, 20\*\* ) GROUP BY d.refills ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |

| Refills\\_Count | The number of refills after the initial prescription. The initial prescription is not counted, values start with 0. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_exposure\\_count |   |

| --- | --- |

| Refills\\_Count |   |

| --- | --- |

  |

| --- |

### DEX38: Counts of stop reasons

| This query is used to count stop reasons (stop\\_reason) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a stop\\_reason. If the input is omitted, all existing values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| stop\\_reason | 1 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  select count(1) as totExp , d.stop\\_reason from drug\\_exposure d where d.stop\\_reason in ('INVALID') group by d.stop\\_reason ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |

| stop\\_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| Count |   |

| --- | --- |

| stop\\_reason |   |

| --- | --- |

  |

| --- |

### DEX39: Counts of drugs, stratified by drug type

| This query is used to count drugs (drug\\_concept\\_id) across all drug exposure records stratified by drug exposure type (drug\\_type\\_concept\\_id, in CDM V2 drug\\_exposure\\_type). The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id or a drug\\_type\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes |   |

| --- | --- | --- | --- |

| list of drug\\_type\\_concept\\_id | 38000180 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT t.drug\\_concept\\_id, count(1) as drugs\\_count, t.drug\\_TYPE\\_concept\\_id FROM drug\\_exposure t where    t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* ) and t.drug\\_TYPE\\_concept\\_id in ( \*\*38000175\*\* , \*\*38000179\*\* ) group by t.drug\\_TYPE\\_concept\\_id, t.drug\\_concept\\_id ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| drug\\_type\\_concept\\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |

| --- | --- |

| count | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| drug\\_type\\_concept\\_id |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### DEX40: Counts of drugs, stratified by relevant condition

| This query is used to count all drugs (drug\\_concept\\_id) across all drug exposure records stratified by condition (relevant\\_condition\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id and a relevant\\_condition\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes |   |

| --- | --- | --- | --- |

| list of relevant\\_condition\\_concept\\_id | 26052, 258375 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT   t.drug\\_concept\\_id,  count(1) as drugs\\_count,  p.procedure\\_concept\\_id as relevant\\_condition\\_concept\\_idFROM drug\\_exposure t        inner join procedure\\_occurrence as p                on        t.visit\\_occurrence\\_id = p.visit\\_occurrence\\_id                and        t.person\\_id = p.person\\_idwhere   t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* )   and p.procedure\\_concept\\_id in ( \*\*26052, 258375\*\* )group by  p.procedure\\_concept\\_id, t.drug\\_concept\\_id;   t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* )   and t.relevant\\_condition\\_concept\\_id in ( \*\*26052, 258375\*\* )group by  t.relevant\\_condition\\_concept\\_id, t.drug\\_concept\\_id; \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| relevant\\_condition\\_concept\\_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the condition that was the cause for initiation of the procedure. Note that this is not a direct reference to a specific condition record in the condition table, but rather a condition concept in the vocabulary |

| --- | --- |

| Count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| relevant\\_condition\\_concept\\_id |   |

| --- | --- |

| Count |   |

| --- | --- |

  |

| --- |

### DEX41: Distribution of drug exposure start date, stratified by drug

| This query is used to provide summary statistics for start dates (drug\\_exposure\\_start\\_date) across all drug exposure records stratified by drug (drug\\_concept\\_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, the drug\\_exposure\\_start\\_date for all existing values of drug\\_concept\\_id are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT         tt.drug\\_concept\\_id ,         min(tt.start\\_date) AS min\\_date ,         max(tt.start\\_date) AS max\\_date ,         avg(tt.start\\_date\\_num) + tt.min\\_date AS avg\\_date ,         (round(stdDev(tt.start\\_date\\_num)) ) AS stdDev\\_days ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.25) WITHIN GROUP( ORDER BY tt.start\\_date\\_num ) ) AS percentile\\_25\\_date ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.5) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) ) AS median\\_date ,         tt.min\\_date + (APPROXIMATE PERCENTILE\\_DISC(0.75) WITHIN GROUP (ORDER BY tt.start\\_date\\_num ) ) AS percential\\_75\\_date FROM (                 SELECT                         (t.drug\\_exposure\\_start\\_date - MIN(t.drug\\_exposure\\_start\\_date) OVER(partition by t.drug\\_concept\\_id)) AS start\\_date\\_num,                         t.drug\\_exposure\\_start\\_date AS start\\_date,                        MIN(t.drug\\_exposure\\_start\\_date) OVER(partition by t.drug\\_concept\\_id) min\\_date,                        t.drug\\_concept\\_id                 FROM                         drug\\_exposure t                 where t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* )         ) tt GROUP BY tt.min\\_date , tt.drug\\_concept\\_id order by tt.drug\\_concept\\_id ;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| min\\_value |   |

| --- | --- |

| max\\_value |   |

| --- | --- |

| avg\\_value |   |

| --- | --- |

| stdDev\\_value |   |

| --- | --- |

| percentile\\_25 |   |

| --- | --- |

| median\\_value |   |

| --- | --- |

| percentile\\_75 |   |

| --- | --- |

  |

| --- |

### DEX42: Counts of genders, stratified by drug

| This query is used to count all gender values (gender\\_concept\\_id) for all exposed persons stratified by drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a gender\\_concept\\_id and drug\\_concept\\_id. If the input is omitted, all existing value combinations are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes |   |

| --- | --- | --- | --- |

| list of gender\\_concept\\_id | 8507, 8532 | Yes | Male, Female |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT p.gender\\_concept\\_id, count(1) as gender\\_count, t.drug\\_concept\\_id FROM drug\\_exposure t, person p where p.person\\_id = t.person\\_idand t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* )  and p.gender\\_concept\\_id in ( \*\*8507, 8532\*\* )group by t.drug\\_concept\\_id, p.gender\\_concept\\_idorder by t.drug\\_concept\\_id, p.gender\\_concept\\_id;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| gender\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |

| --- | --- |

| Count | The number of individual drug exposure occurrences used to construct the drug era. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| gender\\_concept\\_id |   |

| --- | --- |

| Count |   |

| --- | --- |

  |

| --- |

### DEX43: Counts of drug exposure records per person, stratified by drug

| This query is used to count the number of drug exposure records for all exposed persons stratified by drug (drug\\_concept\\_id). The input to the query is a value (or a comma-separated list of values) of a drug\\_concept\\_id. If the input is omitted, all existing values are summarized.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of drug\\_concept\\_id | 906805, 1517070, 19010522 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT t.drug\\_concept\\_id, t.person\\_id, count(1) as drug\\_exposure\\_count FROM drug\\_exposure t where t.drug\\_concept\\_id in ( \*\*906805, 1517070, 19010522\*\* ) group by t.person\\_id, t.drug\\_concept\\_id order by t.drug\\_concept\\_id, t.person\\_id;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

| --- | --- |

| person\\_id | A system-generated unique identifier for each person. |

| --- | --- |

| count |   |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| drug\\_concept\\_id |   |

| --- | --- |

| person\\_id |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |
