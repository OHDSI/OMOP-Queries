Drug Exposure Queries
---

DEX01: Counts of persons with any number of exposures to a certain drug
---

| This query is used to count the persons with at least one exposures to a certain drug (drug_concept_id).  See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all drugs in the data table are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.  

```sql
	set search_path to full_201706_omop_v5;

	SELECT concept.concept_name, drug_concept_id, count(person_id) as num_persons 
	FROMdrug_exposure join concept
	ON drug_concept_id = concept.concept_id
	where
	lower(domain_id)='drug' and vocabulary_id='RxNorm' and standard_concept='S'
	and drug_concept_id in (40165254, 40165258 )
	GROUP BY concept.concept_name, drug_concept_id;
```
   
Output:

Output field list:

|  Field |  Description |
| --- | --- |
| drug_name | An unambiguous, meaningful and descriptive name for the concept. |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept.  |
| num_persons | The patients count |

Sample output record:

|  Field |  Content |
| --- | --- | 
| drug_name |  Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| drug_concept_id |  40165254 |
| num_persons |  191244 |

DEX02: Counts of persons taking a drug, by age, gender, and year of exposure
---

| This query is used to count the persons with exposure to a certain drug (drug_concept_id), grouped by age, gender, and year of exposure. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. If the input is omitted, all drugs in the data table are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. s

```sql
	select drug.concept_name, 
		EXTRACT( YEAR FROM drug_exposure_start_date ) as year_of_exposure,
		EXTRACT( YEAR FROM drug_exposure_start_date ) - year_of_birth as age , 
		gender.concept_name as gender,
		count(1) as num_persons
	From
	drug_exposure JOINperson USING( person_id ) 
	join concept drug ON drug.concept_id = drug_concept_id 
	JOINconcept gender ON gender.concept_id = gender_concept_id
	where drug_concept_id IN ( 40165254, 40165258 ) 
	GROUP by drug.concept_name, gender.concept_name, EXTRACT( YEAR FROM drug_exposure_start_date ),
	EXTRACT( YEAR FROM drug_exposure_start_date ) - year_of_birth 
	ORDER BY concept_name, year_of_exposure, age, gender
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  concept_name | An unambiguous, meaningful and descriptive name for the concept. |
|  year_of_exposure |   |
|  age | The age of the person at the time of exposure |
|  gender | The gender of the person. |
|  num_persons | The patient count |

Sample output record:

|  Field |  Content |
| --- | --- | 
| concept_name |  Rosuvastatin calcium 40 MG Oral Tablet [Crestor] |
| year_of_exposure |  2010 |
| age |  69 |
| gender |  Male |
| num_persons |  15 |

DEX03: Distribution of age, stratified by drug
---

| This query is used to provide summary statistics for the age across all drug exposure records stratified by drug (drug_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The age value is defined by the earliest exposure. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. If the input is omitted, age is summarized for all existing drug_concept_id values.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| drug_concept_id | 40165254, 40165258 | Yes | Crestor 20 and 40 mg tablets |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. 

```sql
	SELECT 
		concept_name AS drug_name , 
		drug_concept_id , 
		COUNT(*) AS patient_count , 
		MIN ( age ) AS min  , 
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY age ) AS percentile_25  , 
		ROUND ( AVG ( age ), 2 ) AS mean, 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY age ) AS median  , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY age ) AS percentile_75 , 
		MAX ( age ) AS max , 
		ROUND ( STDDEV ( age ), 1 ) AS stdDev 
	FROM /*person, first drug exposure date*/ ( 
			SELECT 
				drug_concept_id , person_id , 
				MIN( extract(year from drug_exposure_start_date )) - year_of_birth as age 
			FROM 
				drug_exposure JOIN full_201706_omop_v5.person USING( person_id ) 
			WHERE drug_concept_id IN /*crestor 20 and 40 mg tablets */ ( 40165254, 40165258 )
			GROUP BY drug_concept_id, person_id , year_of_birth 
		) 
	JOIN concept ON concept_id = drug_concept_id 
	WHERE domain_id='Drug' and standard_concept='S'
	GROUP BY concept_name, drug_concept_id;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_name | An unambiguous, meaningful and descriptive name for the concept. |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| patient_count | The count of patients taking the drug |
| min | The age of the youngest patient taking the drug |
| percentile_25 | The 25th age percentile |
| mean | The mean or average age of the patients taking the drug |
| median | The median age of the patients taking the drug |
| percentile_75 | The 75th age percentile |
| max  | The age of the oldest patient taking the drug |
| stddev | The standard deviation of the age distribution |


Sample output record:

|  Field |  Content |
| --- | --- | 
| drug_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| drug_concept_id | 40165254 |
| patient_count | 30321 |
| min | 11 |
| percentile_25 | 49 |
| mean | 53.87 |
| median | 55 |
| percentile_75 | 60 |
| max | 93 |
| stddev | 8.8 |

DEX04: Distribution of gender in persons taking a drug
---

| This query is used to obtain the gender distribution of persons exposed to a certain drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. If the input is omitted, all drugs in the data table are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. 

```sql
	select drug.concept_name as drug_name, 
			drug_concept_id,	
			gender.concept_name as gender,
			count(1) as num_persons
	From
	drug_exposure JOIN person USING( person_id ) 
	join concept drug ON drug.concept_id = drug_concept_id 
	JOIN concept gender ON gender.concept_id = gender_concept_id
	where drug_concept_id IN ( 40165254, 40165258 ) 
	GROUP by drug.concept_name, drug_concept_id, gender.concept_name 
	ORDER BY drug_name, drug_concept_id, gender;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| drug_name | An unambiguous, meaningful and descriptive name for the drug concept. |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| gender | The gender of the counted persons exposed to drug. |
| num_persons | The number of persons of a particular gender exposed to drug. |


Sample output record:

|  Field |  Content |
| --- | --- | 
| drug_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| drug_concept_id | 40165254 |
| gender | FEMALE |
| num_persons | 12590 |

DEX05: Counts of drug records for a particular drug
---

This query is used to count the drug exposure records for a certain drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. If the input is omitted, all drugs in the data table are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_concept_id | 40165254, 40165258 | No | Crestor 20 and 40 mg tablets | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. S


```sql
	SELECT 
	concept_name as drug_name, drug_concept_id, count(*) as num_records 
	FROM 
	drug_exposure JOIN concept 
	ON concept_id = drug_concept_id 
	WHERE 
	lower(domain_id)='drug' and vocabulary_id='RxNorm' and standard_concept='S'
	and drug_concept_id IN (40165254,40165258)
	GROUP BY concept_name, drug_concept_id;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| drug_name | An unambiguous, meaningful and descriptive name for the drug concept. |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| num_records | The number of drug exposure records |


Sample output record:

|  Field |  Content |
| --- | --- | 
| drug_name | Rosuvastatin calcium 20 MG Oral Tablet [Crestor] |
| drug_concept_id | 40165254 |
| num_records | 191244 |

DEX06: Counts of distinct drugs in the database
---

| This query is used to determine the number of distinct drugs (drug_concept_id). See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.

Input: None.

Sample query run:

The following is a sample run of the query.  

```sql
	SELECT 
	count(distinct drug_concept_id) as number_drugs 
	FROM 
	drug_exposure JOIN concept 
	ON concept_id = drug_concept_id 
	WHERE 
	lower(domain_id)='drug' and vocabulary_id='RxNorm' and standard_concept='S'; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| number_drugs | The count of distinct drug concepts. |

Sample output record:

|  Field |  Description |
| --- | --- | 
| number_drugs | 10889 |

DEX07: Maximum number of drug exposure events per person over some time period
---

| This query is to determine the maximum number of drug exposures that is recorded for a patient during a certain time period. If the time period is omitted, the entire time span of the database is considered. Instead of maximum, the query can be easily changed to obtained the average or the median number of drug records for all patients. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes | | 
| date to | 31-Dec-2008 | Yes |   | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. 

```sql
	select max(exposures ) as exposures_count from 
	(SELECT 
	drug_exposure.person_id, COUNT(*) exposures 
	FROM drug_exposure JOIN person
	ON drug_exposure.person_id = person.person_id
	WHERE 
	drug_concept_id in (select distinct concept_id from concept 
							WHERE lower(domain_id)='drug' and vocabulary_id='RxNorm' and standard_concept='S')
	AND drug_exposure_start_date BETWEEN '2017-01-01' AND '2017-12-31' 
	GROUP BY drug_exposure.person_id);
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| exposures_count | The number of drug exposure records for the patient with the maximum number of such records. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| exposures_count | 1137 |

DEX08: Maximum number of distinct drugs per person over some time period
---

| This query is to determine the maximum number of distinct drugs a patient is exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes |   |
| date to | 31-Dec-2008 | Yes |   | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. s

```sql
	select max(drugs) as drugs_count from 
	(SELECT 
	COUNT( DISTINCT drug_concept_id) drugs 
	FROM drug_exposure JOIN person
	ON drug_exposure.person_id = person.person_id
	WHERE 
	drug_concept_id in (select distinct concept_id from concept 
							WHERE lower(domain_id)='drug' and vocabulary_id='RxNorm' and standard_concept='S')
	AND drug_exposure_start_date BETWEEN '2017-01-01' AND '2017-12-31' 
	GROUP BY drug_exposure.person_id);
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drugs_count | The maximum number of distinct drugs a patient is exposed to during the time period |

Sample output record:

|  Field |  Content |
| --- | --- | 
| drugs_count | 141 |

DEX09: Distribution of distinct drugs per person over some time period
---

| This query is to determine the distribution of distinct drugs patients are exposed to during a certain time period. If the time period is omitted, the entire time span of the database is considered.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| date from | 01-Jan-2008 | Yes |   |
| date to | 31-Dec-2008 | Yes |   | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.  

```sql
	SELECT MIN ( drugs ) AS min , 
	approximate  PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY drugs ) as percentile_25, 
	ROUND ( AVG ( drugs ), 2 ) AS mean, 
	approximate PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY drugs ) AS median , 
	approximate PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY drugs ) AS percential_75, 
	MAX ( drugs ) AS max, 
	 ROUND ( STDDEV ( drugs ), 1 ) AS stdDev 
	 FROM  (SELECT person_id, NVL( drugs, 0 ) AS drugs FROM person  JOIN 
	 ( SELECT person_id, COUNT( DISTINCT drug_concept_id ) AS drugs FROM drug_exposure 
	 WHERE drug_exposure_start_date BETWEEN '2017-01-01' AND '2017-12-31' GROUP BY person_id ) USING( person_id ) );
```

Output:


Output field list:

| Field |  Description |
| --- | --- | 
| min | The minimum number of drugs taken by a patient |
| percentile_25 | The 25th percentile of the distibution |
| mean | The mean or average of drugs taken by patients |
| median | The median number of drugs take |
| percentile_75 | The 75th percentile of the distribution |
| max | The maximum number of drugs taken by a patient |
| stddev | The standard deviation of the age distribution |


Sample output record:

| Field |  Content |
| --- | --- |
| min | 0 |
| percentile_25 | 0 |
| mean | 1.73 |
| median | 0 |
| percentile_75 | 1 |
| max | 141 |
| stddev | 4.2 |

DEX10: Other drugs (conmeds) patients exposed to a certain drug take over some time period
---

This query is used to establish the medication (conmeds) taken by patients who also are exposed to a certain drug in a given time period. The query returns the number of patients taking the drug at least once. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id and the time period. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values. 
Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug concept ids | 1336825, 19047763 | Yes | Bortezomib, Thalidomide 50 mg capsules |
| from_date | 01-jan-2008 | Yes |   |
| to_date | 31-dec-2009 | Yes |   |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.

```sql
	SELECT concept_name, COUNT(1) as persons
	FROM ( 
	--Other drugs people are taking
	  SELECT DISTINCT cohort.person_id, drug.drug_concept_id
	  FROM ( 
	  --person with specific drug in time frame
	  SELECT DISTINCT person_id, drug_concept_id, from_date, to_date
	  FROM drug_exposure
	  JOIN ( 
	  --date range 
	  SELECT '01-jan-2008' AS from_date , '31-dec-2009' AS to_date ) 
	  ON drug_exposure_start_date BETWEEN from_date AND to_date
	  WHERE drug_concept_id IN /*bortezomib, Thalidomide 50 mg capsules */  (1336825, 19047763)
	  ) cohort
	  JOIN drug_exposure drug 
	  ON drug.person_id = cohort.person_id
	  AND drug.drug_concept_id != cohort.drug_concept_id
	  AND drug.drug_exposure_start_date BETWEEN from_date AND to_date
	  WHERE drug.drug_concept_id != 0 /* unmapped drug */
	  )
	JOIN concept ON concept_id = drug_concept_id
	GROUP By concept_name ORDER BY persons DESC;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_name | An unambiguous, meaningful and descriptive name for the conmeds. |
| persons | count of patients taking the drug at least once |


Sample output record:

| Field |  Value |
| --- | --- | 
| drug_name | Dexamethasone 4 MG Oral Tablet |
| persons | 190 |

DEX11: Distribution of brands used for a given generic drug
---

| This query provides the brands that are used for a generic drug. The input to the query is a value of a drug_concept_id. See [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.  Note that depending on the mapping available for the source_values in the drug_exposure table, branded drug information might only partially or not be provided. See the Standard Vocabulary Specifications at  [http://omop.org/Vocabularies](http://omop.org/Vocabularies).

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| drug_concept_id | 19019306 | Yes | Nicotine Patch | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. S

```sql
	SELECT	tt.drug_name,
			tt.brand_name,
			100.00*tt.part_brand/tt.total_brand as perc_brand_count
	FROM
		(
		SELECT	t.drug_name,
				t.brand_name,
				t.cn_3_02 part_brand,
				SUM(t.cn_3_02) OVER() total_brand
				FROM
					(
						SELECT	sum((select count(1) from drug_exposure d where d.drug_concept_id = cr003.concept_id_2)) cn_3_02,
								A.Concept_Name drug_name,
								D.Concept_Name brand_name
						FROM
							concept AS A
							INNER JOIN	concept_relationship AS CR003
								ON CR003.concept_id_1	= A.concept_id
							INNER JOIN	concept_relationship AS CR007
								ON	CR007.concept_id_2		= CR003.concept_id_2
							INNER JOIN
								concept_relationship AS CR006
									ON	CR007.concept_id_1		= CR006.concept_id_1
							INNER JOIN
								concept D
									ON	CR006.concept_id_2		= D.concept_id
						WHERE
							CR003.relationship_ID	= 'Has tradename'
						AND	A.concept_class_id		= 'Clinical Drug'
						AND	CR007.relationship_ID	= 'Constitutes'
						AND	CR006.relationship_ID	= 'Has brand name'
						AND	D.concept_class_id		= 'Brand Name'
						AND	A.concept_id			= 35606533
						GROUP BY	A.Concept_Name,
									D.Concept_Name
					) t 
		) tt
	WHERE tt.total_brand > 0 ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_name | The name of the query drug |
| brand_name | The name of the brand |
| perc_brand_count | The market share for each brand |

Sample output record:

|  Field |  Content |
| --- | --- | 
| drug_name |   |
| brand_name |   |
| perc_brand_count |   |

DEX12: Distribution of forms used for a given ingredient
---

| This query determines the percent distribution of forms of drug products containing a given ingredient. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  ingredient.concept_id |  1125315 |  Yes |  Acetaminophen |

Sample query run:

The following is a sample run of the query. The input parameter is highlighted in  blue. 

```sql
	SELECT tt.form_name,
	(100.00 * tt.part_form / tt.total_forms) as percent_forms
	FROM (
	SELECT 
	t.form_name,
	t.cn part_form,
	SUM(t.cn) OVER() total_forms
	FROM (
	select 
	count(1) as cn,
	drugform.concept_name form_name
	FROM concept ingredient,
	concept_ancestor a,
	concept drug,
	concept_relationship r,
	concept drugform
	WHERE ingredient.concept_id = 1125315 --Acetaminophen
	AND ingredient.concept_class_id = 'Ingredient'
	AND ingredient.concept_id = a.ancestor_concept_id
	AND a.descendant_concept_id = drug.concept_id
	--AND drug.concept_level = 1 --ensure it is drug product
	ANd drug.standard_concept='S'
	AND drug.concept_id = r.concept_id_1
	AND r.concept_id_2 = drugform.concept_id
	AND drugform.concept_class_id = 'Dose Form'

	GROUP BY drugform.concept_name
	) t 
	WHERE t.cn>0 --don't count forms that exist but are not used in the data
	) tt
	WHERE tt.total_forms > 0 --avoid division by 0
	ORDER BY percent_forms desc;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| form_name | The concept name of the dose form |
| percent_forms | The percent of forms drug products have containing the ingredient |


Sample output record:

|  Field |  Description |
| --- | --- | 
| form_name |  Oral Tablet |
| percent_forms |  95.69 |

DEX13: Distribution of provider specialities prescribing a given drug
---

| This query provides the provider specialties prescribing a given drug, and the frequencies for each provider prescribing the drug (drug exposure records). Note that many databases do not record the prescribing provider for drugs. See  [vocabulary queries](http://vocabqueries.omop.org/drug-queries) for obtaining valid drug_concept_id values.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| drug_concept_id | 2213473 | Yes | Influenza virus vaccine |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.

```sql
	SELECT  concept_name AS specialty, 
	  count(*) AS prescriptions_count
	  FROM 
	  /*first prescribing provider for statin*/
	  ( SELECT person_id, provider_id
	  FROM drug_exposure
	  WHERE NVL( drug_exposure.provider_id, 0 ) > 0
	  AND drug_concept_id = 2213473  /* Influenza virus vaccine */
	  ) drug
	  JOIN provider ON provider.provider_id = drug.provider_id 
	  JOIN concept ON concept_id = provider.specialty_concept_id
	  WHERE concept.vocabulary_id='Specialty'
	  AND concept.standard_concept='S'
	  GROUP BY concept_name
	  ORDER BY prescriptions_count desc;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| specialty | The concept name of the specialty concept |
| prescriptions_count | The count of drug exposure records providers from the specialties are listed as prescribing provider. |


Sample output record:

|  Field |  Value |
| --- | --- |
| specialty |  Family Practice |
| prescriptions_count |  214825 |

DEX14: Among people who take drug A, how many take drug B at the same time?
---

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| concept_id | 21502747 | Yes | Statins | 
| ancestor_concept_id | 21500223 | Yes | Antihypertensive Therapy Agents |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  S

```sql
	SELECT count(*) AS num_A_users , SUM( bp_also ) AS num_also_using_B 
	FROM /* people taking statin and possible taking antihypertensive agent */ 
		( SELECT statin.person_id, MAX( NVL( bp, 0 ) ) AS bp_also 
			FROM /*people taking statin */ 
				( SELECT  person_id, drug_exposure_start_date, drug_exposure_end_date 
					FROM drug_exposure statin 
					WHERE drug_concept_id IN /*statins*/ 
						( SELECT concept_id 
							FROM concept 
							JOIN concept_ancestor ON descendant_concept_id = concept_id 
							WHERE 
							ancestor_concept_id = 21502747
							AND standard_concept = 'S' 
							AND sysdate BETWEEN valid_start_date AND valid_end_date ) ) statin							
				LEFT OUTER JOIN /* people taking antihypertensive agent */ 
				( SELECT  person_id, drug_exposure_start_date, drug_exposure_end_date , 1 AS bp 
					FROM drug_exposure 
					WHERE drug_concept_id IN /*Antihypertensive Therapy Agents */ 
						( SELECT concept_id 
							FROM concept 
							JOIN concept_ancestor ON descendant_concept_id = concept_id 
							WHERE 
							ancestor_concept_id = 21500223 
							AND standard_concept = 'S' 
							AND sysdate BETWEEN valid_start_date AND valid_end_date ) ) bp 
		ON bp.person_id = statin.person_id 
		AND bp.drug_exposure_start_date < statin.drug_exposure_end_date 
		AND bp.drug_exposure_end_date > statin.drug_exposure_start_date 
		GROUP BY statin.person_id );
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| concept_name | An unambiguous, meaningful and descriptive name for the concept. |
| person_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |
| ancestor_concept_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| drug_exposure_start_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| drug_exposure_end_date | The end date for the current instance of drug utilization. It is not available from all sources. |


Sample output record:

|  Field |  Description |
| --- | --- |
| concept_name |   |
| person_id |   |
| ancestor_concept_id |   |
| drug_exposure_start_date |   |
| drug_exposure_end_date |   |

DEX15: Number of persons taking a given drug having at least a 180 day period prior and a 365 day follow-up period
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_id | 21502747 | Yes | Statins |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.

```sql
	SELECT
		floor( ( observation_period_end_date - index_date ) / 365 ) AS follow_up_years, 
		count(*) AS persons FROM /* statin users with 180 clean period and at least 1 year follow up period */ 
		( 
		SELECT person_id, index_date , observation_period_start_date , observation_period_end_date 
		FROM /*statin user start_date */ 
			( 
			SELECT 
				person_id, 
				min( drug_exposure_start_date ) AS index_date 
			FROM drug_exposure statin 
			WHERE drug_concept_id IN /*statins */ 
			  	( 
				SELECT concept_id 
				FROM concept 
				JOIN concept_ancestor ON descendant_concept_id = concept_id 
				WHERE ancestor_concept_id = 21502747 
				--AND vocabulary_id = 8 
				AND vocabulary_id = 'RxNorm'
				AND standard_concept = 'S' 
				AND sysdate BETWEEN valid_start_date AND valid_end_date ) GROUP BY person_id ) 
		JOIN observation_period USING( person_id ) 
		WHERE observation_period_start_date + 180 < index_date AND observation_period_end_date > index_date + 365
		) 
	GROUP BY floor( ( observation_period_end_date - index_date ) / 365 ) 
	ORDER BY 1; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| concept_name | An unambiguous, meaningful and descriptive name for the concept. |
| person_id | A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table. |
| ancestor_concept_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| descendant_concept_id | A foreign key to the concept code in the concept table for the lower-level concept that forms the descendant in the relationship. |
| observation_period_start_date | The start date of the observation period for which data are available from the data source. |
| observation_period_end_date | The end date of the observation period for which data are available from the data source. |

Sample output record:

|  Field |  Description |
| --- | --- | 
| concept_name |   |
| person_id |   |
| ancestor_concept_id |   |
| descendant_concept_id |   |
| observation_period_start_date |   |
| observation_period_end_date |   |

DEX16: Adherence/compliance - what is adherence rate for given drug?
---

Define adherence as sum of days supply divided by length of treatment period.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- | 
| drug_concept_id | 996416 | Yes | Finasteride | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  S

```sql
	SELECT concept_name, 
	count(*) AS number_of_eras , 
	avg( treatment_length ) AS average_treatment_length_count , 
	avg(adherence) avgerage_adherence_count 
	FROM
		( SELECT person_id, concept_name, drug_era_start_date , sum( days_supply ), treatment_length , 
		  sum( days_supply ) / treatment_length AS adherence , min( has_null_days_supply ) AS null_day_supply 
		  FROM /* drug era and individual drug encounters making up the era */ 
			( SELECT person_id, ingredient_concept_id , drug_era_start_date, drug_era_end_date , 
			  drug_era_end_date - drug_era_start_date AS treatment_length , drug_exposure_start_date , days_supply , 
			  DECODE( NVL( days_supply, 0 ), 0, 0, 1 ) has_null_days_supply 
			  FROM /*drug era of people taking finasteride */ 
				( SELECT person_id, drug_concept_id as ingredient_concept_id , drug_era_start_date, drug_era_end_date 
					FROM drug_era 
					--WHERE drug_concept_id = 996416 /* Finasteride */ 
					) 
					JOIN /* drug exposures making up the era */ 
					( SELECT person_id, days_supply, drug_exposure_start_date 
						FROM drug_exposure 
						JOIN concept_ancestor ON descendant_concept_id = drug_concept_id 
						JOIN concept ON concept_id = ancestor_concept_id 
						WHERE LOWER(concept_class_id) = 'ingredient' 
						AND sysdate BETWEEN valid_start_date AND valid_end_date 
						AND ancestor_concept_id = 996416 
						/*Finasteride*/ ) USING( person_id ) 
				WHERE drug_exposure_start_date BETWEEN drug_era_start_date AND drug_era_end_date ) 
			JOIN concept ON concept_id = ingredient_concept_id 
		GROUP BY person_id, concept_name, drug_era_start_date, treatment_length ) 
	WHERE treatment_length > 100 and null_day_supply > 0 
	GROUP BY concept_name;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| concept_name | An unambiguous, meaningful and descriptive name for the concept. |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| concept_class | The category or class of the concept along both the hierarchical tree as well as different domains within a vocabulary. Examples are "Clinical Drug", "Ingredient", "Clinical Finding" etc. |
| treatment_length |   |
| person_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |
| drug_era_start_date | The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug. |
| drug_exposure_start_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| days_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |
| drug_era_end_date | The end date for the drug era constructed from the individual instance of drug exposures. It is the end date of the final continuously recorded instance of utilization of a drug. |
| ingredient_concept_id |   |
| ancestor_concept_id | A foreign key to the concept code in the concept table for the higher-level concept that forms the ancestor in the relationship. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| concept_name |   |
| drug_concept_id |   |
| concept_class |   |
| treatment_length |   |
| person_id |   |
| drug_era_start_date |   |
| drug_exposure_start_date |   |
| days_supply |   |
| drug_era_end_date |   |
| ingredient_concept_id |   |
| ancestor_concept_id |   |

DEX17: Why do people stop treatment?
---

| This query provides a list of stop treatment and their frequency.

Input: <None>
Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue. S

```sql
	SELECT stop_reason, count(*) AS reason_freq 
	FROM drug_exposure 
	WHERE 
	stop_reason IS NOT null GROUP BY stop_reason ORDER BY reason_freq DESC;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| stop_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |
| reason_freq |  Frequency of stop reason |


Sample output record:

|  Field |  Description |
| --- | --- | 
| stop_reason |  Regimen Completed |
| reason_freq |  14712428 |

DEX18: What is the distribution of DRUG_TYPE_CONCEPT_ID (modes of distribution) for a given drug?
---

Input: <None>

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in blue.

```sql
	SELECT 
	concept_name, count(*) as drug_type_count 
	FROM 
	drug_exposure JOIN concept 
	ON concept_id = drug_type_concept_id 
	GROUP BY concept_name ORDER BY drug_type_count DESC; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_type_concept_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| drug_type_count |   |


Sample output record:

|  Field |  Description |
| --- | --- |
| drug_type_concept_id |   |
| drug_type_count |   |

DEX19: How many people are taking a drug for a given indication?
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | Acute Tuberculosis | Yes | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in 

```sql
	SELECT concept_name, count( distinct person_id ) 
	 FROM drug_exposure JOIN /* indication and associated drug ids */
	 	(select indication.concept_name, drug.concept_id
			from concept indication 
			JOIN concept_ancestor ON ancestor_concept_id = indication.concept_id 
			JOIN vocabulary indication_vocab ON indication_vocab.vocabulary_id = indication.vocabulary_id
			JOIN concept drug ON drug.concept_id = descendant_concept_id 
			JOIN vocabulary drug_vocab ON drug_vocab.vocabulary_id = drug.vocabulary_id 
			WHERE sysdate BETWEEN drug.valid_start_date AND drug.valid_end_date
			AND drug_vocab.vocabulary_id = 'RxNorm'
			AND indication.concept_class_id = 'Indication'
			AND indication_vocab.vocabulary_name = 'Indications and Contraindications (FDB)'
			AND indication.concept_name = 'Active Tuberculosis' /*This filter can be changed or omitted if count need for all indication*/
			AND drug.standard_concept='S'
		)
	ON concept_id = drug_concept_id GROUP BY concept_name;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| concept_name | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |
| count |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| concept_name |   |
| count |   |

DEX20: How many people taking a drug for a given indicaton actually have that disease in their record prior to exposure?
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | Acute Tuberculosis | Yes |   


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue 


```sql
	SELECT 
		count(*) AS treated 
		FROM /* person and tuberculosis treatment start date */ 
		( 
			SELECT 
				person_id, 
				min( drug_exposure_start_date ) AS treatment_start 
			FROM drug_exposure 
		JOIN /*indication and associated drug ids */ 
			( SELECT 
				indication.concept_name, 
				drug.concept_id 
				--, indication.domain_id, drug.concept_id
				FROM concept indication 
				JOIN concept_ancestor ON ancestor_concept_id = indication.concept_id 
				JOIN vocabulary indication_vocab ON indication_vocab.vocabulary_id = indication.vocabulary_id 
				JOIN concept drug ON drug.concept_id = descendant_concept_id 
				JOIN vocabulary drug_vocab ON drug_vocab.vocabulary_id = drug.vocabulary_id 
				WHERE 
				indication_vocab.vocabulary_name = 'Indications and Contraindications (FDB)'
				AND indication.domain_id = 'Drug'
				AND indication.concept_name = 'Active Tuberculosis'
				AND drug_vocab.vocabulary_name = 'RxNorm (NLM)'
				AND drug.standard_concept = 'S' 
				AND sysdate BETWEEN drug.valid_start_date AND drug.valid_end_date ) 
		ON concept_id = drug_concept_id GROUP BY person_id ) treated 
	LEFT OUTER JOIN /*patient with Acute Tuberculosis diagnosis */ 
		( SELECT 
				person_id, min( condition_start_date ) first_diagnosis, 1 AS diagnosed
				FROM condition_occurrence 
				JOIN source_to_concept_map ON target_concept_id = condition_concept_id 
				JOIN vocabulary ON vocabulary_id = source_vocabulary_id 
				WHERE source_code like '011.%' 
				AND	vocabulary_id ='ICD9CM'
				GROUP BY person_id
		) diagnosed 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| count |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| count |   |

DEX21: How many people have a diagnosis of a contraindication for the drug they are taking?
---

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
|   |   |   |  |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue  ;


```sql
	;WITH con_rel AS		
		(
		SELECT
			r1.concept_id_1,
			r2.concept_id_2
		FROM
			concept_relationship AS r1
			INNER JOIN concept_relationship r2
				ON	r2.concept_id_1	= r1.concept_id_2
		WHERE
			r1.relationship_id	= 'Has CI'
		AND	r2.relationship_id	= 'Ind/CI - SNOMED'
		)
	SELECT	count(distinct d.person_id)
	FROM
		con_rel AS cr
			INNER JOIN	drug_exposure AS d
				ON	cr.concept_id_1 = d.drug_concept_id
			INNER JOIN	condition_occurrence AS c
				ON	cr.concept_id_2	= c.condition_concept_id
				AND	d.person_id		= c.person_id
	where
		d.drug_exposure_start_date >= c.condition_start_date 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| count |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| count |   |

DEX22: How many poeple take a drug in a given class?
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| ancestor_concept_id | 4324992 |  Yes | Antithrombins | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue. S

```sql
	SELECT count(distinct d.person_id) as person_count FROM concept_ancestor ca, drug_exposure d 
	WHERE 
	d.drug_concept_id = ca.descendant_concept_id 
	and ca.ancestor_concept_id = 4324992
	group by ca.ancestor_concept_id ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| person_count | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |

Sample output record:

|  Field |  Description |
| --- | --- | 
| person_count |   |

DEX23: Distribution of days supply
---

| This query is used to provide summary statistics for days supply (days_supply) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT 
		min(tt.stat_value) AS min_value , 
		max(tt.stat_value) AS max_value , 
		avg(tt.stat_value) AS avg_value ,	
		(round(stdDev(tt.stat_value)) ) AS stdDev_value ,
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) AS percentile_25 , 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value ) AS median_value , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value ) AS percential_75 
	FROM 
		( SELECT t.days_supply AS stat_value FROM drug_exposure t where t.days_supply > 0 ) tt ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

DEX24: Counts of days supply
---

| This query is used to count days supply values across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a days_supply. If the clause is omitted, all possible values of days_supply are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| days_supply | 2,3 | Yes |   | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.  

```sql
	SELECT t.days_supply, count(1) AS cnt
	FROM drug_exposure t
	WHERE t.days_supply in (2,3) 
	GROUP BY t.days_supply
	ORDER BY days_supply;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| days_supply | The number of days of supply of the medication as recorded in the original prescription or dispensing record. |
| cnt | Counts of records with the days_supply value |

Sample output record:

|  Field |  Description |
| --- | --- | 
| days_supply |  15 |
| cnt |  240179 |

DEX25: Counts of drug records
---

| This query is used to count drugs (drug_concept_id) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes | Metoclopramid, Desmopressin, Cyclosprin |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue.

```sql
	SELECT count(1) as exposure_occurrence_count  
	FROM drug_exposure 
	WHERE 
	drug_concept_id in (906805, 1517070, 19010522);
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| exposure_occurrence_count | The number of individual drug exposure occurrences used to construct the drug era. |

Sample output record:

|  Field |  Value |
| --- | --- | 
| exposure_occurrence_count |  88318 |

DEX26: Distribution of drug exposure end dates
---

| This query is used to to provide summary statistics for drug exposure end dates (drug_exposure_end_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>

Sample query run:

The following is a sample run of the query. 

```sql
	SELECT			
		min(tt.end_date) AS min_date , 
		max(tt.end_date) AS max_date , 
		avg(tt.end_date_num) + tt.min_date AS avg_date , 
		(round(stdDev(tt.end_date_num)) ) AS stdDev_days , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.end_date_num ) ) AS percentile_25_date , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.end_date_num ) ) AS median_date , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.end_date_num ) ) AS percentile_75_date 
		FROM 
			( SELECT
				(t.drug_exposure_end_date - MIN(t.drug_exposure_end_date) OVER()) AS end_date_num, 
				t.drug_exposure_end_date AS end_date, 
				MIN(t.drug_exposure_end_date) OVER() min_date 
			 FROM drug_exposure t ) tt 
	GROUP BY tt.min_date ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

DEX27: Distribution of drug exposure start dates
---

| This query is used to to provide summary statistics for drug exposure start dates (drug_exposure_start_date) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>
Sample query run:

The following is a sample run of the query.  

```sql
	SELECT
		min(tt.start_date) AS min_date , 
		max(tt.start_date) AS max_date , 
		avg(tt.start_date_num) + tt.min_date AS avg_date , 
		(round(stdDev(tt.start_date_num)) ) AS stdDev_days , 
		tt.min_date + (approximate PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.start_date_num ) ) AS percentile_25_date , 
		tt.min_date + (approximate PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.start_date_num ) ) AS median_date , 
		tt.min_date + (approximate PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.start_date_num ) ) AS percentile_75_date 
	FROM ( 
		SELECT
			(t.drug_exposure_start_date - MIN(t.drug_exposure_start_date) OVER()) AS start_date_num, 
			t.drug_exposure_start_date AS start_date, 
			MIN(t.drug_exposure_start_date) OVER() min_date 
		FROM drug_exposure t 
		) tt 
	GROUP BY tt.min_date ; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


DEX28: Counts of drug types
---

| This query is used to count the drug type concepts (drug_type_concept_id, in CDM V2 drug_exposure_type) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a drug_type_concept_id. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_type_concept_id | 38000175, 38000180 | Yes | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	SELECT count(1) as exposure_occurrence_count , drug_type_concept_id FROM drug_exposure 
	WHERE 
	drug_concept_id in (select distinct drug_concept_id from drug_era)
	AND drug_type_concept_id in (38000175, 38000180) 
	GROUP BY drug_type_concept_id ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_type_concept_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the type of drug exposure recorded. It indicates how the drug exposure was represented in the source data: as medication history, filled prescriptions, etc. |
| exposure_occurrence_count | The number of individual drug exposure occurrences used to construct the drug era. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_type_concept_id |   |
| exposure_occurrence_count |   |

DEX29: Distribution of number of distinct drugs persons take
---

| This query is used to provide summary statistics for the number of number of different distinct drugs (drug_concept_id) of all exposed persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>
Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

```sql
	SELECT 
	 	min(tt.stat_value) AS min_value , 
		max(tt.stat_value) AS max_value , 
		avg(tt.stat_value) AS avg_value , 
		(round(stdDev(tt.stat_value)) ) AS stdDev_value , 
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) AS percentile_25 , 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value ) AS median_value , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value ) AS percential_75 
	FROM ( 
			SELECT count(distinct t.drug_concept_id) AS stat_value 
			FROM drug_exposure t 
	 		where nvl(t.drug_concept_id, 0) > 0 
			group by t.person_id ) tt ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

DEX30: Counts of number of distinct drugs persons take
---

| This query is used to count the number of different distinct drugs (drug_concept_id) of all exposed persons. The input to the query is a value (or a comma-separated list of values) for a number of drug concepts. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| drug_concept_id | 15, 22 | Yes |   | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  S

```sql
	SELECT count(distinct t.drug_concept_id) AS stat_value, t.person_id
	FROM drug_exposure t
	GROUP BY t.person_id HAVING count(DISTINCT t.drug_concept_id) in (15,22);
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| person_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |
| stat_value | The number of individual drug exposure occurrences used to construct the drug era. |

Sample output record:

|  Field |  Description |
| --- | --- | 
| person |   |
| stat_value |   |

DEX31: Distribution of drug exposure records per person
---

| This query is used to provide summary statistics for the number of drug exposure records (drug_exposure_id) for all persons: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. There is no input required for this query.

Input: <None>
Sample query run:

The following is a sample run of the query. 

```sql
	SELECT 
		min(tt.stat_value) AS min_value , 
		max(tt.stat_value) AS max_value , 
		avg(tt.stat_value) AS avg_value , 
		(round(stdDev(tt.stat_value)) ) AS stdDev_value , 
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) AS percentile_25 , 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value ) AS median_value , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value ) AS percential_75 
	FROM ( 
			SELECT count(1) AS stat_value 
			FROM drug_exposure t 
			group by t.person_id 
		) tt ; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

DEX32: Counts of drug exposure records per person
---

| This query is used to count the number of drug exposure records (drug_exposure_id) for all persons. The input to the query is a value (or a comma-separated list of values) for a number of records per person. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| count | 3, 4 |  Yes |   

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  S

```sql
	SELECT count(1) AS stat_value, person_id
	FROM drug_exposure
	group by person_id
	having count(1) in (3,4);
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| person_id | A foreign key identifier to the person who is subjected to the drug. The demographic details of that person are stored in the person table. |
| count | The number of individual drug exposure occurrences used to construct the drug era. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| person_id |   |
| count |   |


DEX33: Counts of drug exposure records stratified by observation month
---

| This query is used to count the drug exposure records stratified by observation month. The input to the query is a value (or a comma-separated list of values) of a month. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of month numbers | 3, 5 |  Yes |  

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	select extract(month from d.drug_exposure_start_date) month_num, COUNT(1) as exp_in_month_count 
	from drug_exposure d 
	where extract(month from d.drug_exposure_start_date) in (3, 5) 
	group by extract(month from d.drug_exposure_start_date) order by 1 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_exposure_start_date | The start date for the current instance of drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a drug administration procedure was recorded. |
| month |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_exposure_start_date |   |
| month |   |

DEX34: Distribution of drug quantity
---

| This query is used to provide summary statistics for drug quantity (quantity) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>
Sample query run:


The following is a sample run of the query. 

```sql
	SELECT 
		min(tt.stat_value) AS min_value , 
		max(tt.stat_value) AS max_value , 
		avg(tt.stat_value) AS avg_value , 
		(round(stdDev(tt.stat_value)) ) AS stdDev_value , 
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) AS percentile_25 , 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value ) AS median_value , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value ) AS percentile_75 
	FROM ( 
			SELECT t.quantity AS stat_value 
			FROM drug_exposure t 
			where t.quantity > 0 
		) tt ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


DEX35: Counts of drug quantity
---

This query is used to count the drug quantity (quantity) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a quantity. If the input is omitted, all possible values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| quantity (list of numbers) | 10,20 | Yes |  

Sample query run:

The following is a sample run of the query. 

```sql
	SELECT count(1) as drug_quantity_count, d.quantity
	FROM drug_exposure d 
	WHERE d.quantity in (10, 20) 
	GROUP BY d.quantity ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_quantity_count |   |
| quantity | The quantity of drug as recorded in the original prescription or dispensing record. |

Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_quantity_count |   |
| quantity |   |


DEX36: Distribution of drug refills
---

| This query is used to provide summary statistics for drug refills (refills) across all drug exposure records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Input: <None>
Sample query run:

The following is a sample run of the query. 

```sql
	SELECT 
		min(tt.stat_value) AS min_value , 
		max(tt.stat_value) AS max_value , 
		avg(tt.stat_value) AS avg_value , 
		(round(stdDev(tt.stat_value)) ) AS stdDev_value , 
		APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.stat_value ) AS percentile_25 , 
		APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value ) AS median_value , 
		APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value ) AS percentile_75 
	FROM ( 
			SELECT
				t.refills AS stat_value 
			FROM drug_exposure t 
			where t.refills > 0 
		) tt ; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

Sample output record:

|  Field |  Description |
| --- | --- | 
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |

DEX37: Counts of drug refills
---

| This query is used to count the drug refills (refills) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of refills. If the input is omitted, all existing values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| refills count (list of numbers) | 10,20 | Yes |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	SELECT count(1) as drug_exposure_count, d.refills AS refills_count 
	FROM drug_exposure d 
	WHERE d.refills in (10, 20) 
	GROUP BY d.refills ;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| drug_exposure_count | The number of individual drug exposure occurrences used to construct the drug era. |
| Refills_Count | The number of refills after the initial prescription. The initial prescription is not counted, values start with 0. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_exposure_count |   |
| Refills_Count |   |

DEX38: Counts of stop reasons
---

| This query is used to count stop reasons (stop_reason) across all drug exposure records. The input to the query is a value (or a comma-separated list of values) of a stop_reason. If the input is omitted, all existing values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| stop_reason | 1 | Yes |   


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	select count(1) as totExp , d.stop_reason from drug_exposure d 
	where d.stop_reason in ('INVALID') 
	group by d.stop_reason ;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| Count | The number of individual drug exposure occurrences used to construct the drug era. |
| stop_reason | The reason the medication was stopped, where available. Reasons include regimen completed, changed, removed, etc. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| Count |   |
| stop_reason |   |


DEX39: Counts of drugs, stratified by drug type
---

| This query is used to count drugs (drug_concept_id) across all drug exposure records stratified by drug exposure type (drug_type_concept_id, in CDM V2 drug_exposure_type). The input to the query is a value (or a comma-separated list of values) of a drug_concept_id or a drug_type_concept_id. If the input is omitted, all existing value combinations are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |
| list of drug_type_concept_id | 38000180 | Yes | 


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	SELECT t.drug_concept_id, count(1) as drugs_count, t.drug_TYPE_concept_id 
	FROM drug_exposure t 
	where
	    t.drug_concept_id in (906805, 1517070, 19010522) 
	and t.drug_TYPE_concept_id in ( 38000175,38000179 ) 
	group by t.drug_TYPE_concept_id, t.drug_concept_id ;
```

Output:


Output field list:

|  Field |  Description |
| --- | --- | 
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| drug_type_concept_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |
| count | A foreign key to the predefined concept identifier in the vocabulary reflecting the parameters used to construct the drug era. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_concept_id |   |
| drug_type_concept_id |   |
| count |   |

DEX40: Counts of drugs, stratified by relevant condition
---

| This query is used to count all drugs (drug_concept_id) across all drug exposure records stratified by condition (relevant_condition_concept_id). The input to the query is a value (or a comma-separated list of values) of a drug_concept_id and a relevant_condition_concept_id. If the input is omitted, all existing value combinations are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |  
| list of relevant_condition_concept_id | 26052, 258375 | Yes |   

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	SELECT 
	  t.drug_concept_id,
	  count(1) as drugs_count,
	  p.procedure_concept_id as relevant_condition_concept_id
	FROM drug_exposure t
		inner join procedure_occurrence as p
			on	t.visit_occurrence_id = p.visit_occurrence_id
			and	t.person_id = p.person_id
	where 
	  t.drug_concept_id in (906805, 1517070, 19010522) 
	  and p.procedure_concept_id in (26052, 258375)
	group by  p.procedure_concept_id, t.drug_concept_id
	;

	  t.drug_concept_id in (906805, 1517070, 19010522) 
	  and t.relevant_condition_concept_id in (26052, 258375)
	group by  t.relevant_condition_concept_id, t.drug_concept_id
	;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| relevant_condition_concept_id | A foreign key to the predefined concept identifier in the vocabulary reflecting the condition that was the cause for initiation of the procedure. Note that this is not a direct reference to a specific condition record in the condition table, but rather a condition concept in the vocabulary |
| Count | The number of individual drug exposure occurrences used to construct the drug era. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_concept_id |   
| relevant_condition_concept_id |   
| Count |   |

DEX41: Distribution of drug exposure start date, stratified by drug
---

| This query is used to provide summary statistics for start dates (drug_exposure_start_date) across all drug exposure records stratified by drug (drug_concept_id): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, the drug_exposure_start_date for all existing values of drug_concept_id are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| drug_concept_id | 906805, 1517070, 19010522 | Yes |   

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue

```sql
	SELECT 
		tt.drug_concept_id , 
		min(tt.start_date) AS min_date , 
		max(tt.start_date) AS max_date , 
		avg(tt.start_date_num) + tt.min_date AS avg_date , 
		(round(stdDev(tt.start_date_num)) ) AS stdDev_days , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY tt.start_date_num ) ) AS percentile_25_date , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.start_date_num ) ) AS median_date , 
		tt.min_date + (APPROXIMATE PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.start_date_num ) ) AS percential_75_date 
	FROM ( 
			SELECT 
				(t.drug_exposure_start_date - MIN(t.drug_exposure_start_date) OVER(partition by t.drug_concept_id)) AS start_date_num, 
				t.drug_exposure_start_date AS start_date,
				MIN(t.drug_exposure_start_date) OVER(partition by t.drug_concept_id) min_date,
				t.drug_concept_id 
			FROM 
				drug_exposure t 
			where t.drug_concept_id in (906805, 1517070, 19010522) 
		) tt 
	GROUP BY tt.min_date , tt.drug_concept_id order by tt.drug_concept_id ;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_concept_id |   |
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |
| percentile_25 |   |
| median_value |   |
| percentile_75 |   |


DEX42: Counts of genders, stratified by drug
---

| This query is used to count all gender values (gender_concept_id) for all exposed persons stratified by drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a gender_concept_id and drug_concept_id. If the input is omitted, all existing value combinations are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |   
| list of gender_concept_id | 8507, 8532 | Yes | Male, Female | 

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue

```sql
	SELECT p.gender_concept_id, count(1) as gender_count, t.drug_concept_id 
	FROM drug_exposure t, person p 
	where p.person_id = t.person_id
	and t.drug_concept_id in (906805, 1517070, 19010522)  
	and p.gender_concept_id in (8507, 8532)
	group by t.drug_concept_id, p.gender_concept_id
	order by t.drug_concept_id, p.gender_concept_id; 
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| gender_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the gender of the person. |
| Count | The number of individual drug exposure occurrences used to construct the drug era. |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_concept_id |   |
| gender_concept_id |   |
| Count |   |

DEX43: Counts of drug exposure records per person, stratified by drug
---

| This query is used to count the number of drug exposure records for all exposed persons stratified by drug (drug_concept_id). The input to the query is a value (or a comma-separated list of values) of a drug_concept_id. If the input is omitted, all existing values are summarized.

Input:

|  Parameter |  Example |  Mandatory |  Notes | 
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |  

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue 

```sql
	SELECT t.drug_concept_id, t.person_id, count(1) as drug_exposure_count 
	FROM drug_exposure t 
	where t.drug_concept_id in (906805, 1517070, 19010522) 
	group by t.person_id, t.drug_concept_id 
	order by t.drug_concept_id, t.person_id;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- | 
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| person_id | A system-generated unique identifier for each person. |
| count |   |


Sample output record:

|  Field |  Description |
| --- | --- | 
| drug_concept_id |   |
| person_id |   |
| count |   |



