 CE01: Min/max/average length of condition
 ---

| Compute minimum, maximum an average length of the medical condition.


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |
|   |   |   |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT 
	  treatment, 
	  count(*), 
	  min( condition_days ) AS min , 
	  max( condition_days ) AS max, 
	  avg( condition_days ) As avg_condition_days 
	FROM ( 
	  SELECT 
	    CASE WHEN surgery = 1 THEN 'surgery' 
	         WHEN drug = 1 AND pt = 1 THEN 'PT Rx' 
	         WHEN drug = 1 THEN 'Rx Only' ELSE 'No Treatment' 
	    END AS treatment , 
	    condition_days 
	  FROM ( 
	    SELECT 
	      person_id, 
	      diag_date , 
	      max( drug ) AS drug, 
	      max( surgery ) AS surgery, 
	      max( pt ) AS PT , 
	      max( condition_days ) AS condition_days 
	    FROM /* back pain and treatments over following 60 days */ ( 
	      SELECT 
	        era.person_id, 
	        condition_era_start_date AS diag_date , 
	        condition_era_end_date - condition_era_start_date AS condition_days, 
	        NVL( drug, 0 ) AS drug, 
	        NVL( surgery, 0 ) AS surgery , 
	        NVL( pt, 0 ) AS pt 
	      FROM condition_era era 
	      JOIN /* SNOMed codes for back pain */ ( 
	        SELECT DISTINCT descendant_concept_id, concept_name 
	        FROM source_to_concept_map map 
	        JOIN concept_ancestor ON ancestor_concept_id = target_concept_id 
	        JOIN concept ON concept_id = descendant_concept_id 
	        WHERE 
	          source_code like '724%' AND 
	          source_vocabulary_id = 2 /* ICD9 */ AND 
	          target_vocabulary_id = 1 /* SNOMed */ AND 
	          sysdate BETWEEN map.valid_start_date AND 
	          map.valid_end_date 
	      ) ON descendant_concept_id = condition_concept_id 
	      LEFT OUTER JOIN /* surgery */ ( 
	        SELECT 
	          person_id, 
	          procedure_date, 
	          1 AS surgery 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE vocabulary_id = 4 /* CPT-4 */ AND 
	          concept_code IN( '22851','20936','22612','22523','22630','22614',
	                           '22842','22632','20930','22524','27130','22525' ) 
	      ) surgery ON 
	        surgery.person_id = era.person_id AND 
	        surgery.procedure_date BETWEEN condition_era_start_date AND condition_era_start_date + 60 
	      LEFT OUTER JOIN /* drugs */ ( 
	        SELECT 
	          person_id, 
	          procedure_date AS drug_date, 
	          1 AS drug 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 4 /* CPT-4 */ AND 
	          concept_code IN( '20610','20552','207096','20553','20550','20605' ,'20551','20600','23350' ) 
	        UNION SELECT 
	          person_id, 
	          drug_era_start_date, 
	          1 
	        FROM drug_era 
	        WHERE drug_concept_id IN( 1125315, 778711, 1115008, 1177480, 1112807, 1506270 ) 
	      ) drug ON 
	        drug.person_id = era.person_id AND 
	        drug.drug_date BETWEEN condition_era_start_date AND condition_era_start_date + 60 
	      LEFT OUTER JOIN /* pt */ ( 
	        SELECT
	          person_id, 
	          procedure_date AS pt_date, 
	          1 AS pt 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE vocabulary_id = 4 /* CPT-4 */ AND 
	          concept_code IN( '97001', '97140', '97002' ) 
	        UNION SELECT 
	          person_id, 
	          procedure_date AS pt_date, 
	          1 AS pt 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 5 /* HCPCS */ AND 
	          concept_code = 'G0283' 
	      ) pt ON 
	        pt.person_id = era.person_id AND 
	        pt.pt_date BETWEEN condition_era_start_date AND 
	        condition_era_start_date + 60 
	    ) 
	    WHERE diag_date > '01-jan-2011' 
	    GROUP by 
	      person_id, 
	      diag_date 
	    ORDER BY 
	      person_id, 
	      diag_date 
	  ) 
	) 
	GROUP BY treatment 
	ORDER BY treatment; 


Output:

Output field list:

|  Field |  Description |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg_condition_days |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg_condition_days |   |
| --- | --- |

  |
| --- |



 CE02: Age/gender of patients with condition
 ---

| List of patient counts of specific age and gender for specific medical condition


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Hip Fraction 1 |  Yes |  Concept ID=500000601 |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	SELECT gender, age, count(*) num_patients 
	FROM -- patient with hip fracture, age, gender 
	( 
	SELECT DISTINCT condition.person_id , gender.concept_name As GENDER , EXTRACT( YEAR 
	FROM CONDITION_ERA_START_DATE ) - year_of_birth AS age 
	FROM condition_era condition 
	JOIN -- definition of Hip Fracture 
	( 
	SELECT DISTINCT descendant_concept_id 
	FROM relationship 
	JOIN concept_relationship rel 
	USING( relationship_id ) 
	JOIN concept concept1 ON concept1.concept_id = concept_id_1 
	JOIN concept_ancestor ON ancestor_concept_id = concept_id_2 
	WHERE relationship_name = 'HOI contains SNOMED (OMOP)' AND concept1.concept_name = 'OMOP Hip Fracture 1' AND sysdate BETWEEN rel.valid_start_date 
	AND rel.valid_end_date ) ON descendant_concept_id = condition_concept_id 
	JOIN person ON person.person_id = condition.person_id 
	JOIN concept gender ON gender.concept_id = gender_concept_id ) 
	GROUP BY gender, age 
	ORDER BY gender, age;

Output field list:

|  Field |  Description |
| --- | --- |
| gender | Patients gender, i.e. MALE, FEMALE |
| --- | --- |
| age | The year of birth of the person. For data sources with date of birth, the year is extracted. For data sources where the year of birth is not available, the approximate year of birth is derived based on any age group categorization available. |
| --- | --- |
| num_patients | Number of patients for specific gender and age and selected condition |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| gender |  FEMALE |
| --- | --- |
| age |  16 |
| --- | --- |
| num_patients |  22 |
| --- | --- |

  |
| --- |



 CE03: Min/max, average length of condition stratified by age/gender
 ---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Hip Fracture 1 |  Yes |  concept_id=500000601 |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT 
	  gender, 
	  CASE 
	    WHEN age_grp = 0 THEN '0-9' 
	    WHEN age_grp = 1 THEN '10-19' 
	    WHEN age_grp = 2 THEN '20-29' 
	    WHEN age_grp = 3 THEN '30-39' 
	    WHEN age_grp = 4 THEN '40-49' 
	    WHEN age_grp = 5 THEN '50-59' 
	    WHEN age_grp = 6 THEN '60-69' 
	    WHEN age_grp = 7 THEN '70-79' 
	    WHEN age_grp = 8 THEN '80-89' 
	    WHEN age_grp = 9 THEN '90-99' 
	    WHEN age_grp > 9 THEN '100+' 
	  END age_grp, 
	  count(*) AS num_patients, 
	  min( duration ) AS min_duration_count, 
	  max( duration ) AS max_duration_count, 
	  avg( duration ) AS avg_duration_count 
	FROM -- patient with hip fracture, age, gender 
	( 
	  SELECT DISTINCT 
	    condition.person_id , 
	    gender.concept_name As gender , 
	    EXTRACT( YEAR FROM condition_era_start_date ) - year_of_birth AS age, 
	    condition_era_end_date - condition_era_start_date + 1 AS duration, 
	    (EXTRACT( YEAR FROM condition_era_start_date) - person.year_of_birth)/10 AS age_grp 
	  FROM condition_era condition 
	  JOIN -- definition of Hip Fracture 
	  ( 
	    SELECT DISTINCT descendant_concept_id 
	    FROM relationship 
	    JOIN concept_relationship rel USING( relationship_id ) 
	    JOIN concept concept1 ON concept1.concept_id = concept_id_1 
	    JOIN concept_ancestor ON ancestor_concept_id = concept_id_2 
	    WHERE 
	      relationship_name = 'HOI contains SNOMED (OMOP)' AND 
	      concept1.concept_name = 'OMOP Hip Fracture 1' AND 
	      SYSDATE BETWEEN rel.valid_start_date and rel.valid_end_date 
	  ) ON descendant_concept_id = condition_concept_id 
	  JOIN person ON person.person_id = condition.person_id 
	  JOIN concept gender ON gender.concept_id = gender_concept_id 
	) t1 
	GROUP BY 
	  gender, 
	  age_grp, 
	  age 
	ORDER BY age_grp, gender

Output field list:

|  Field |  Description |
| --- | --- |
| gender | Patient gender name. i.e. MALE, FEMALE... |
| --- | --- |
| age_grp | Age group in increments of 10 years |
| --- | --- |
| num_patients | Number of patients withing gender and age group with associated condition |
| --- | --- |
| min_duration | Minimum duration of condition in days |
| --- | --- |
| max_duration | Maximum duration of condition in days |
| --- | --- |
| avg_duration | Average duration of condition in days |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| gender |  FEMALE |
| --- | --- |
| age_grp |  10-19 |
| --- | --- |
| num_patients |  518 |
| --- | --- |
| min_duration |  1 |
| --- | --- |
| max_duration | 130  |
| --- | --- |
| avg_duration |  8 |
| --- | --- |

  |
| --- |



 CE04: Conditions, stratified by year, age group and gender
 ---

| This query is used to count conditions (condition_concept_id) across all condition era records stratified by year, age group and gender (gender_concept_id). The age groups are calculated as 10 year age bands from the age of a person at the condition era start date. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id , year, age_group (10 year age band) and gender_concept_id. If the input is ommitted, all existing value combinations are summarized..


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id |   |   |   |
| --- | --- | --- | --- |
| gender_concept_id |   |   |   |
| --- | --- | --- | --- |
| gender_concept_id |   |   |   |
| --- | --- | --- | --- |
| age_group |   |   |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	CREATE TEMP TABLE
		age_age_grp
	(
		age INT,
		age_grp VARCHAR(100)
	)
	;

	INSERT INTO
		age_age_grp
	VALUES
	(1, '0 to 9'),
	(2, '0 to 9'),
	(3, '0 to 9'),
	(4, '0 to 9'),
	(5, '0 to 9'),
	(6, '0 to 9'),
	(7, '0 to 9'),
	(8, '0 to 9'),
	(9, '0 to 9'),
	(10, '10 to 19'),
	(11, '10 to 19'),
	(12, '10 to 19'),
	(13, '10 to 19'),
	(14, '10 to 19'),
	(15, '10 to 19'),
	(16, '10 to 19'),
	(17, '10 to 19'),
	(18, '10 to 19'),
	(19, '10 to 19'),
	(20, '20 to 29'),
	(21, '20 to 29'),
	(22, '20 to 29'),
	(23, '20 to 29'),
	(24, '20 to 29'),
	(25, '20 to 29'),
	(26, '20 to 29'),
	(27, '20 to 29'),
	(28, '20 to 29'),
	(29, '20 to 29'),
	(30, '30 to 39'),
	(31, '30 to 39'),
	(32, '30 to 39'),
	(33, '30 to 39'),
	(34, '30 to 39'),
	(35, '30 to 39'),
	(36, '30 to 39'),
	(37, '30 to 39'),
	(38, '30 to 39'),
	(39, '30 to 39'),
	(40, '40 to 49'),
	(41, '40 to 49'),
	(42, '40 to 49'),
	(43, '40 to 49'),
	(44, '40 to 49'),
	(45, '40 to 49'),
	(46, '40 to 49'),
	(47, '40 to 49'),
	(48, '40 to 49'),
	(49, '40 to 49'),
	(50, '50 to 59'),
	(51, '50 to 59'),
	(52, '50 to 59'),
	(53, '50 to 59'),
	(54, '50 to 59'),
	(55, '50 to 59'),
	(56, '50 to 59'),
	(57, '50 to 59'),
	(58, '50 to 59'),
	(59, '50 to 59'),
	(60, '60 to 69'),
	(61, '60 to 69'),
	(62, '60 to 69'),
	(63, '60 to 69'),
	(64, '60 to 69'),
	(65, '60 to 69'),
	(66, '60 to 69'),
	(67, '60 to 69'),
	(68, '60 to 69'),
	(69, '60 to 69'),
	(70, '70 to 79'),
	(71, '70 to 79'),
	(72, '70 to 79'),
	(73, '70 to 79'),
	(74, '70 to 79'),
	(75, '70 to 79'),
	(76, '70 to 79'),
	(77, '70 to 79'),
	(78, '70 to 79'),
	(79, '70 to 79'),
	(80, '80 to 89'),
	(81, '80 to 89'),
	(82, '80 to 89'),
	(83, '80 to 89'),
	(84, '80 to 89'),
	(85, '80 to 89'),
	(86, '80 to 89'),
	(87, '80 to 89'),
	(88, '80 to 89'),
	(89, '80 to 89'),
	(90, '90 to 99'),
	(91, '90 to 99'),
	(92, '90 to 99'),
	(93, '90 to 99'),
	(94, '90 to 99'),
	(95, '90 to 99'),
	(96, '90 to 99'),
	(97, '90 to 99'),
	(98, '90 to 99'),
	(99, '90 to 99'),
	(100, '100 to 109'),
	(101, '100 to 109'),
	(102, '100 to 109'),
	(103, '100 to 109'),
	(104, '100 to 109'),
	(105, '100 to 109'),
	(106, '100 to 109'),
	(107, '100 to 109'),
	(108, '100 to 109'),
	(109, '100 to 109'),
	(110, '110 to 119'),
	(111, '110 to 119'),
	(112, '110 to 119'),
	(113, '110 to 119'),
	(114, '110 to 119'),
	(115, '110 to 119'),
	(116, '110 to 119'),
	(117, '110 to 119'),
	(118, '110 to 119'),
	(119, '110 to 119')
	;


	SELECT
		condition,
		year,
		age_grp,
		gender,
		count(*)
	FROM
		(
		SELECT
			person.person_id ,
			cond_name.concept_name AS condition ,
			EXTRACT( YEAR FROM condition_era_start_date ) AS year ,
			gender.concept_name As GENDER ,
			EXTRACT( YEAR FROM condition_era_start_date ) - year_of_birth AS age ,
			age_grp
			FROM condition_era condition
				JOIN concept cond_name
					ON cond_name.concept_id = condition_concept_id
				JOIN person
					ON person.person_id = condition.person_id
				JOIN concept gender
					ON gender.concept_id = 8507
				JOIN age_age_grp
					ON age = EXTRACT( YEAR FROM CONDITION_ERA_START_DATE ) - year_of_birth 
		)
	GROUP BY
		condition,
		year,
		age_grp,
		gender
	ORDER BY
		condition,
		year,
		age_grp,
		gender;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition |   |
| --- | --- |
| year |   |
| --- | --- |
| age_grp |   |
| --- | --- |
| gender |   |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition |   |
| --- | --- |
| year |   |
| --- | --- |
| age_grp |   |
| --- | --- |
| gender |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |



 CE05: Conditions that are seasonally dependent
 ---

| This query is used to count conditions (condition_concept_id) across all condition era records stratified by year, age group and gender (gender_concept_id). The age groups are calculated as 10 year age bands from the age of a person at the condition era start date. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id , year, age_group (10 year age band) and gender_concept_id. If the input is ommitted, all existing value combinations are summarized..


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id |   |   |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT season, count(*) AS cases
	FROM /* Extrinsic Asthma/season */
	( SELECT CASE 

	WHEN condition_era_start_date
	BETWEEN to_date( '01-01-2017', 'DD-MM-YYYY' ) AND to_date( '21-03-2017', 'DD-MM-YYYY' )
	THEN 'Winter'

	WHEN condition_era_start_date
	BETWEEN to_date( '22-03-2017', 'DD-MM-YYYY' ) AND to_date( '21-06-2017', 'DD-MM-YYYY' )
	THEN 'Spring'

	WHEN condition_era_start_date
	BETWEEN to_date( '22-06-2017', 'DD-MM-YYYY' ) AND to_date( '21-09-2017', 'DD-MM-YYYY' )
	THEN 'Summer'

	WHEN condition_era_start_date
	BETWEEN to_date( '22-09-2017', 'DD-MM-YYYY' ) AND to_date( '21-12-2017', 'DD-MM-YYYY' )
	THEN 'Fall'

	WHEN condition_era_start_date
	BETWEEN to_date( '22-12-2017', 'DD-MM-YYYY' ) AND to_date( '31-12-2017', 'DD-MM-YYYY' )
	THEN 'Winter'
	END AS season
	FROM condition_era
	JOIN /* Extrinsic Asthma ICD-9 493.* Get associated SNOMed codes
	with their 12endents */
	(
	-- descendant standard concept id for asthma
	SELECT DISTINCT ca.descendant_concept_id AS snomed_asthma
	FROM concept_ancestor ca 
	JOIN
	(SELECT c2.concept_id FROM concept c1 
	JOIN concept_relationship cr ON c1.concept_id = cr.concept_id_1 
	AND cr.relationship_id = 'Maps to'
	JOIN concept c2 ON cr.concept_id_2 = c2.concept_id
	WHERE c1.concept_code LIKE '493.0%') t -- standard concept id for asthma
	ON ca.ancestor_concept_id = t.concept_id)

	ON snomed_asthma = condition_concept_id
	) GROUP BY season;


Output field list:

|  Field |  Description |
| --- | --- |
| season |   |
| --- | --- |
| cases |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| season |   |
| --- | --- |
| cases |   |
| --- | --- |

  |
| --- |



 CE06: Conditions most likely to result in death
 ---

| Most prevalent conditions within thirty days of death


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| Number of days since condition era end | 30 |  Yes |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	SELECT concept_name, count(*) as conditions_count 
	FROM  ( 
	SELECT death.person_id, concept_name 
	FROM death 
	JOIN condition_era condition ON condition.person_id = death.person_id 
	AND death_date - condition_era_end_date <= 30 
	JOIN concept ON concept_id = condition_concept_id ) 
	GROUP BY concept_name 
	ORDER BY conditions_count 
	DESC;


Output field list:

|  Field |  Description |
| --- | --- |
| concept_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| count |   |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| concept_name |   |
| --- | --- |
| count |   |
| --- | --- |
| condition_concept_id |   |
| --- | --- |

  |
| --- |



 CE07: Comorbidities of patient with condition
 ---

| This query counts the top ten comorbidities for patients with diabetes


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_era_end_date |   |   |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	WITH SNOMed_diabetes AS ( 
	  SELECT DISTINCT 
	    descendant_concept_id AS snomed_diabetes_id 
	  FROM source_to_concept_map map 
	  JOIN concept_ancestor ON ancestor_concept_id = target_concept_id 
	  WHERE 
	    source_vocabulary_id = 2 /* icd9 */ AND 
	    target_vocabulary_id = 1 /* SNOMed */ AND 
	    source_code LIKE '250.%' AND 
	    sysdate BETWEEN valid_start_date AND valid_end_date
	) 
	SELECT 
	  comorbidity, 
	  frequency 
	FROM /* top 10 */ ( 
	  SELECT 
	    comorbidity, 
	    count(*) frequency 
	  FROM /* commorbidities for patients with diabetes */ ( 
	    SELECT DISTINCT 
	      diabetic.person_id, 
	      concept_name AS comorbidity 
	    FROM /* people with diabetes/onset date */ ( 
	      SELECT 
	        person_id, 
	        MIN( condition_era_start_date ) AS onset_date 
	      FROM condition_era 
	      JOIN SNOMed_diabetes ON snomed_diabetes_id = condition_concept_id 
	      GROUP BY person_id 
	    ) diabetic 
	    JOIN /* condition after onset date, that are not diabetes */ ( 
	      SELECT 
	        person_id, 
	        condition_concept_id, 
	        condition_era_start_date 
	      FROM condition_era 
	      WHERE 
	        condition_concept_id NOT IN( SELECT snomed_diabetes_id FROM SNOMed_diabetes ) 
	    ) comorb ON 
	      comorb.person_id = diabetic.person_id AND 
	      comorb.condition_era_start_date > diabetic.onset_date 
	    JOIN concept ON concept_id = comorb.condition_concept_id 
	  ) 
	  GROUP BY comorbidity 
	  ORDER BY frequency DESC 
	) 
	limit 10;



Output field list:

|  Field |  Description |
| --- | --- |
| comorbidity |   |
| --- | --- |
| frequency |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| comorbidity |   |
| --- | --- |
| frequency |   |
| --- | --- |

  |
| --- |



  CE08: Number of comorbidity for patients with condition
  ---

| Meaningful text


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_era_end_date |   |   |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	WITH SNOMed_diabetes AS ( 
	  SELECT DISTINCT descendant_concept_id AS snomed_diabetes_id 
	  FROM source_to_concept_map map 
	  JOIN concept_ancestor ON ancestor_concept_id = target_concept_id 
	  WHERE 
	    source_vocabulary_id = 2 /* icd9 */ AND 
	    target_vocabulary_id = 1 /* SNOMed */ AND 
	    source_code LIKE '250.%' AND 
	    sysdate BETWEEN valid_start_date AND valid_end_date
	),
	tt as ( 
	  SELECT 
	    diabetic.person_id, 
	    count( distinct condition_concept_id ) AS comorbidities 
	  FROM /* people with diabetes/onset date */ ( 
	    SELECT 
	      person_id, 
	      MIN( condition_era_start_date ) AS onset_date 
	    FROM condition_era 
	    JOIN SNOMed_diabetes ON snomed_diabetes_id = condition_concept_id 
	    GROUP BY person_id 
	  ) diabetic 
	  JOIN /* condition after onset date, that are not diabetes */ ( 
	    SELECT 
	      person_id, 
	      condition_concept_id, 
	      condition_era_start_date 
	    FROM condition_era 
	    WHERE condition_concept_id NOT IN( SELECT snomed_diabetes_id FROM SNOMed_diabetes ) 
	  ) comorb ON 
	    comorb.person_id = diabetic.person_id AND 
	    comorb.condition_era_start_date > diabetic.onset_date 
	  JOIN concept ON concept_id = comorb.condition_concept_id 
	  GROUP BY diabetic.person_id 
	)
	SELECT 
	  MIN( comorbidities ) AS min , 
	  max( comorbidities ) AS max, 
	  avg( comorbidities ) AS average , 
	  (select distinct PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS percentile_25 , 
	  (select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS median , 
	  (select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY comorbidities) over() from tt) AS percential_75 
	FROM tt;


Output:

Output field list:

|  Field |  Description |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| average |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| average |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



 CE09: Counts of condition record
 ---

| This query is used to count conditions (condition_concept_id) across all condition era records. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id. If the input is omitted, all possible values are summarized.


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of condition_concept_id | 254761, 257011, 320128, 432867, 25297 | No |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT condition_concept_id, concept_name, count(*) records_count
	  FROM condition_era
	  JOIN concept ON concept_id = condition_concept_id
	 WHERE condition_concept_id 
	    IN /* top five condition concepts */
	       ( 254761, 257011, 320128, 432867, 25297 )
	 GROUP BY condition_concept_id, concept_name
	 ORDER BY records_count DESC;

Output: 

Output field list:

|  Field |  Description |
| --- | --- |
| concept_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| concept_name |   |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |



 CE10: Counts of persons with conditions
 ---

| This query is used to count the persons with any number of eras of a certain condition (condition_concept_id). The input to the query is a value (or a comma-separated list of values) of a condition_concept_id. If the input is omitted, all possible values are summarized.


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of condition_concept_id | 320128, 432867, 254761, 257011, 257007 | No |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT condition_concept_id, concept_name, count( distinct person_id ) num_people
	  FROM condition_era
	  JOIN concept ON concept_id = condition_concept_id
	 WHERE condition_concept_id 
	    IN /* top five condition concepts by number of people */
	       ( 320128, 432867, 254761, 257011, 257007 )
	 GROUP BY condition_concept_id, concept_name
	 ORDER BY num_people DESC;

Output: 

Output field list:

|  Field |  Description |
| --- | --- |
| concept_name | An unambiguous, meaningful and descriptive name for the concept |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| num_people |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| concept_name |   |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| num_people |   |
| --- | --- |

  |
| --- |



 CE11: Distribution of condition era end dates
 ---

| This query is used to to provide summary statistics for condition era end dates (condition_era_end_date) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.


Input: <None>

Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	SELECT condition_concept_id
	     , min(condition_era_end_date)
	     , max(condition_era_end_date)
		 , to_date( round( avg( to_char( condition_era_end_date, 'J' ))), 'J')
		 , round( stdDev( to_number( to_char( condition_era_end_date, 'J' ), 9999999 ))) AS std_dev_days
		 , ( SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY condition_era_end_date ) over () 
		 FROM condition_era) AS percentile_25
		 , ( SELECT DISTINCT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY condition_era_end_date ) over ()
		 FROM condition_era) AS median
	     , ( SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY condition_era_end_date ) over ()
		 FROM condition_era) AS percential_75
	  FROM condition_era
	 WHERE condition_concept_id IN( 254761, 257011, 320128, 432867, 25297 )
	  GROUP BY condition_concept_id;
 

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



 CE12: Distribution of condition era start dates
 ---

| This query is used to to provide summary statistics for condition era start dates (condition_era_start_date) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.


Input: <None>

Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	SELECT condition_concept_id
	     , min(condition_era_start_date)
	     , max(condition_era_start_date)
		 , to_date( round( avg( to_char( condition_era_start_date, 'J' ))), 'J')
		 , round( stdDev( to_number( to_char( condition_era_start_date, 'J' ), 9999999 ))) AS std_dev_days
		 , ( SELECT DISTINCT PERCENTILE_DISC(0.25) WITHIN GROUP( ORDER BY condition_era_start_date ) over () 
		 FROM condition_era) AS percentile_25
		 , ( SELECT DISTINCT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY condition_era_start_date ) over ()
		 FROM condition_era) AS median
	     , ( SELECT DISTINCT PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY condition_era_start_date ) over ()
		 FROM condition_era) AS percential_75
	  FROM condition_era
	 WHERE condition_concept_id IN( 254761, 257011, 320128, 432867, 25297 )
	  GROUP BY condition_concept_id;
 

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



 CE13: Distribution of condition occurrence count
 ---

| This query is used to to provide summary statistics for condition occurrence counts (condition_occurrence_count) across all condition era records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.


Input: <None>

Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue


	SELECT 
	  condition_concept_id,
	  MIN( condition_occurrence_count ) AS min , 
	  max( condition_occurrence_count ) AS max, 
	  avg( condition_occurrence_count ) AS average , 
	  round( stdDev( condition_occurrence_count ) ) AS stdDev,
	  percentile_25,
	  median,
	  percentile_75
	FROM (
	  select
	    condition_concept_id,
	    condition_occurrence_count,
	    PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS percentile_25,
	    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS median , 
	    PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS percentile_75
	  from condition_era 
	  WHERE condition_concept_id IN( 254761, 257011, 320128, 432867, 25297 ) 
	)
	GROUP BY 
	  condition_concept_id,
	  percentile_25,
	  median,
	  percentile_75
	;
 

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| std_dev_days |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



 CE16: Distribution of condition era length, stratified by condition and condition type
 ---

| This query is used to provide summary statistics for the condition era length across all condition era records stratified by condition (condition_concept_id) and condition type (condition_type_concept_id, in CDM V2 condition_occurrence_type): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The length of an era is defined as the difference between the start date and the end date. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id and a condition_type_concept_id. If the input is omitted, all existing value combinations are summarized.


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id |   | No |   |
| --- | --- | --- | --- |
| condition_type_concept_id |   | No |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT 
	  condition_concept_id,
	  MIN( condition_occurrence_count ) AS min , 
	  max( condition_occurrence_count ) AS max, 
	  avg( condition_occurrence_count ) AS average , 
	  round( stdDev( condition_occurrence_count ) ) AS stdDev,
	  percentile_25,
	  median,
	  percentile_75
	FROM (
	  select
	    condition_concept_id,
	    condition_occurrence_count,
	    PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS percentile_25,
	    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS median , 
	    PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY condition_occurrence_count) over() AS percentile_75
	  from condition_era 
	  WHERE condition_concept_id IN( 254761, 257011, 320128, 432867, 25297 ) 
	)
	GROUP BY 
	  condition_concept_id,
	  percentile_25,
	  median,
	  percentile_75
	;



Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



 CE17: Distribution of condition occurrence count, stratified by condition and condition type
 ---
 ---

| This query is used to provide summary statistics for condition occurrence count (condition_occurrence_count) across all condition era records stratified by condition (condition_concept_id) and condition type (condition_type_concept_id, in CDM V2 condition_occurrence_type): the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. The input to the query is a value (or a comma-separated list of values) of a condition_concept_id and a condition_type_concept_id. If the input is omitted, all existing value combinations are summarized.


Input:


|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 254761, 257011, 320128, 432867, 25297 | No |   |
| --- | --- | --- | --- |
| condition_type_concept_id |   | No |   |
| --- | --- | --- | --- |


Sample query run:


The following is a sample run of the query. The input parameters are highlighted in  blue

	SELECT 
	  condition_concept_id,
	  MIN( occurrences ) AS min , 
	  max( occurrences ) AS max, 
	  avg( occurrences ) AS average , 
	  round( stdDev( occurrences ) ) AS stdDev,
	  percentile_25,
	  median,
	  percentile_75
	FROM (
	  select
	    condition_concept_id, 
	    occurrences,
	    PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY occurrences) over() AS percentile_25,
	    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY occurrences) over() AS median , 
	    PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY occurrences) over() AS percentile_75
	  from (
	    select 
	      person_id, 
	      condition_concept_id,
	      count(*) AS occurrences
	    from condition_era 
	    WHERE condition_concept_id IN( 254761, 257011, 320128, 432867, 25297 ) 
	    group by 
	      person_id,
	      condition_concept_id
	  )
	)
	GROUP BY 
	  condition_concept_id,
	  percentile_25,
	  median,
	  percentile_75



Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |


Sample output record:

|  Field |  Description |
| --- | --- |
| condition_concept_id |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg |   |
| --- | --- |
| stdDev |   |
| --- | --- |
| percentile_25 |   |
| --- | --- |
| median |   |
| --- | --- |
| percential_75 |   |
| --- | --- |

  |
| --- |



