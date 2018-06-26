Condition Occurrence Combinations Queries
---

COC01: Determines first line of therapy for a condition
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of condition_concept_id | 432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742, 4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366, 4292524, 4299298, 4299302, 4301157, 4307793 | Yes | Angioedema 1 |
| ancestor_concept_id | 21003378 | Yes | Angioedema |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT 
	  ingredient_name, 
	  ingredient_concept_id, 
	  count(*) num_patients 
	FROM /*Drugs started by people up to 30 days after Angioedema diagnosis */ ( 
	  SELECT 
	    condition.person_id, 
	    condition_start_date , 
	    drug_era_start_date , 
	    ingredient_name, 
	    ingredient_concept_id 
	  FROM /* people with Angioedema with 180 clean period and 180 day follow-up */ ( 
	    SELECT 
	      era.person_id, 
	      condition_era_start_date AS condition_start_date 
	    FROM condition_era era 
	    JOIN observation_period obs 
	      ON obs.person_id = era.person_id AND 
	         condition_era_start_date BETWEEN observation_period_start_date + 180 AND observation_period_end_date - 180 
	    WHERE 
	      condition_concept_id IN -- SNOMed codes for OMOP Angioedema 1 
	      ( 432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742, 
	        4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366, 
	        4292524, 4299298, 4299302, 4301157, 4307793 ) 
	  ) condition 
	  JOIN drug_era rx /* Drug_era has drugs at ingredient level */ 
	    ON rx.person_id = condition.person_id AND 
	       rx.drug_era_start_date BETWEEN condition_start_date AND condition_start_date + 30 
	  JOIN /* Ingredients for indication Angioedema */ ( 
	    SELECT 
	      ingredient.concept_id AS ingredient_concept_id , 
	      ingredient.concept_name AS ingredient_name 
	    FROM concept ingredient 
	    JOIN concept_ancestor a ON a.descendant_concept_id = ingredient.concept_id 
	    WHERE 
	      a.ancestor_concept_id = 21003378 /* indication for angioedema */ AND 
	      ingredient.vocabulary_id = 8 AND 
	      sysdate BETWEEN ingredient.valid_start_date AND ingredient.valid_end_date 
	  ) ON ingredient_concept_id = drug_concept_id 
	) 
	GROUP by ingredient_name, ingredient_concept_id 
	ORDER BY num_patients DESC;
```



 Output:

Output field list:

|  Field |  Description |
| --- | --- |
| ingredient_name |   |
| ingredient_concept_id |   |
| count |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| ingredient_name |   |
| ingredient_concept_id |   |
| count |   |

COC02: Determines length of course of therapy for a condition
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| condition_concept_id | 500000201 | Yes | SNOMed codes for OMOP Aplastic Anemia 1 |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT	ingredient_name,
			ingredient_concept_id,
			count(*) AS num_patients,
			min( length_of_therapy ) AS min_length_of_therapy_count,
			max( length_of_therapy ) AS max_length_of_therapy_count,
			avg( length_of_therapy ) AS average_length_of_therapy_count
	FROM 
		(
		SELECT	condition.person_id,
				condition_start_date,
				drug_era_start_date,
				drug_era_end_date - drug_era_start_date + 1 AS length_of_therapy,
				ingredient_name,
				ingredient_concept_id
		FROM
			(
			SELECT	era.person_id,
					condition_era_start_date AS condition_start_date
			FROM	condition_era era
						JOIN	observation_period AS obs
							ON	obs.person_id = era.person_id
							AND condition_era_start_date BETWEEN observation_period_start_date + 180
							AND observation_period_end_date - 180
			WHERE
				condition_concept_id IN ( 137829,138723,140065,140681,4031699,4098027,4098028, 4098145,4098760,4100998,4101582,4101583,4120453,4125496, 4125497,4125498,4125499,4146086,4146087,4146088,4148471, 4177177,4184200,4184758,4186108,4187773,4188208,4211348, 4211695,4225810,4228194,4234973,4298690,4345236 )
			) condition
				JOIN	drug_era rx
					ON	rx.person_id = condition.person_id
					AND rx.drug_era_start_date BETWEEN condition_start_date AND condition_start_date + 30
				JOIN 
					(
					SELECT DISTINCT	ingredient.concept_id as ingredient_concept_id,
									ingredient.concept_name as ingredient_name
					FROM	concept_ancestor ancestor
								JOIN	concept indication
									ON	ancestor.ancestor_concept_id = indication.concept_id
								JOIN concept ingredient
									ON	ingredient.concept_id = ancestor.descendant_concept_id
					WHERE
						lower( indication.concept_name ) like( '%anemia%' )
					AND	indication.vocabulary_id = 'Indication'
					AND ingredient.vocabulary_id = 'RxNorm'
					AND sysdate BETWEEN indication.valid_start_date AND indication.valid_end_date
					AND sysdate BETWEEN ingredient.valid_start_date AND ingredient.valid_end_date 
					)
						ON ingredient_concept_id = drug_concept_id 
		)
	GROUP BY	ingredient_name,
				ingredient_concept_id
	ORDER BY	num_patients DESC;
```


Output:

Output field list:

|  Field |  Description |
| --- | --- |
| ingredient_name |   |
| ingredient_concept_id |   |
| count |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| ingredient_name |   |
| ingredient_concept_id |   |
| count |   |

COC05: Mortality rate after initial diagnosis
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Acute Myocardial Infarction 1 | Yes |   |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT 
	  COUNT( DISTINCT diagnosed.person_id ) AS all_infarctions , 
	  SUM( CASE WHEN death.person_id IS NULL THEN 0 ELSE 1 END ) AS death_from_infarction 
	FROM -- Initial diagnosis of Acute Myocardial Infarction 
	( 
	  SELECT DISTINCT 
	    person_id, 
	    condition_era_start_date 
	  FROM /* diagnosis of Acute Myocardial Infarction, ranked by date, 6 month clean period with 1 year follow-up */ 
	  ( 
	    SELECT 
	      condition.person_id, 
	      condition.condition_era_start_date , 
	      sum(1) OVER(PARTITION BY condition.person_id ORDER BY condition_era_start_date ROWS UNBOUNDED PRECEDING) AS ranking 
	    FROM 
	      condition_era condition 
	    JOIN --definition of Acute Myocardial Infarction 1 
	    ( 
	      SELECT DISTINCT descendant_concept_id 
	      FROM relationship 
	      JOIN concept_relationship rel USING( relationship_id ) 
	      JOIN concept concept1 ON concept1.concept_id = concept_id_1 
	      JOIN concept_ancestor ON ancestor_concept_id = concept_id_2 
	      WHERE 
	        relationship_name = 'HOI contains SNOMED (OMOP)' AND 
	        concept1.concept_name = 'OMOP Acute Myocardial Infarction 1' AND 
	        sysdate BETWEEN rel.valid_start_date and rel.valid_end_date 
	    ) ON descendant_concept_id = condition_concept_id 
	    JOIN observation_period obs 
	      ON obs.person_id = condition.person_id AND 
	         condition_era_start_date BETWEEN observation_period_start_date + 180 AND observation_period_end_date - 360 
	  ) WHERE ranking = 1 
	) diagnosed 
	LEFT OUTER JOIN death /* death within a year */ 
	  ON death.person_id = diagnosed.person_id AND 
	  death.death_date <= condition_era_start_date + 360; 
```


Output:

Output field list:

|  Field |  Description |
| --- | --- |
| all_infarctions |   |
| death_from_infarction |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| all_infarctions |   |
| death_from_infarction |   |

COC06: Time until death after initial diagnosis
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Acute Myocardial Infarction 1 | Yes |   |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT COUNT( DISTINCT diagnosed.person_id ) AS all_infarction_deaths
	     , ROUND( min( death_date - condition_era_start_date )/365, 1 ) AS min_years
	     , ROUND( max( death_date - condition_era_start_date )/365, 1 ) AS max_years
	     , ROUND( avg( death_date - condition_era_start_date )/365, 1 ) AS avg_years
	  FROM -- Initial diagnosis of Acute Myocardial Infarction
	     ( SELECT DISTINCT person_id, condition_era_start_date
	         FROM  /* diagnosis of Acute Myocardial Infarction, ranked by
	                  date, 6 month clean
	                */
	            ( SELECT condition.person_id, condition.condition_era_start_date
	                   , rank() OVER( PARTITION BY condition.person_id
	                                      ORDER BY condition_era_start_date
	                                ) AS ranking
	                FROM condition_era condition
	                JOIN -- definition of Acute Myocardial Infarction 1
	                   ( SELECT DISTINCT descendant_concept_id
	                       FROM relationship
	                       JOIN concept_relationship rel USING( relationship_id ) 
	                       JOIN concept concept1 ON concept1.concept_id = concept_id_1
	                       JOIN concept_ancestor ON ancestor_concept_id = concept_id_2
	                      WHERE relationship_name = 'HOI contains SNOMED (OMOP)'
	                        AND concept1.concept_name = 'OMOP Acute Myocardial Infarction 1'
	                        AND sysdate BETWEEN rel.valid_start_date and rel.valid_end_date
	                   ) ON descendant_concept_id = condition_concept_id
	                JOIN observation_period obs
	                  ON obs.person_id = condition.person_id
	                 AND condition_era_start_date >= observation_period_start_date + 180
	            )
	        WHERE ranking = 1
	     ) diagnosed
	  JOIN death 
	    ON death.person_id = diagnosed.person_id
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| all_infarction_deaths |   |
| min_years |   |
| max_years |   |
| avg_years |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| all_infarction_deaths |   |
| min_years |   |
| max_years |   |
| avg_years |   |

COC07: Patients with condition in conjunction with a procedure some number of days prior to or after initial condition.
---

Aplastic Anemia AND Occurrence of at least one diagnostic procedure code for bone marrow aspiration or biopsy within 60 days prior to the diagnostic code.
Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Aplastic Anemia 1 | Yes |   |
| list of procedure_concept_id | 2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142 , 3048879, 36359239, 37586183 |   | Bone marrow aspiration or biopsy |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  


```sql
	SELECT DISTINCT	condition.person_id,
					procedure_date,
					condition_era_start_date
	FROM
		procedure_occurrence proc
			JOIN	condition_era condition
						ON condition.person_id = proc.person_id
			JOIN	
					(
					SELECT DISTINCT	descendant_concept_id
					FROM	relationship
							JOIN	concept_relationship rel USING( relationship_id )
							JOIN	concept concept1
										ON	concept1.concept_id = concept_id_1
							JOIN	concept_ancestor
										ON	ancestor_concept_id = concept_id_2
					WHERE	relationship_name = 'HOI contains SNOMED (OMOP)'
					AND		concept1.concept_name = 'OMOP Aplastic Anemia 1'
					AND		sysdate BETWEEN rel.valid_start_date and rel.valid_end_date
					) 
						ON descendant_concept_id = condition_concept_id
	WHERE
		proc.procedure_concept_id IN ( 2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142, 3048879, 36359239, 37586183 )
	AND procedure_date BETWEEN condition_era_start_date - 60 AND condition_era_start_date;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| condition_concept_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| person_id |   |
| procedure_date |   |
| condition_era_start_date |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| person_id |   |
| procedure_date |   |
| condition_era_start_date |   |

COC08: Patients with condition and some observation criteria some number of days prior to or after initial condition
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_name | OMOP Aplastic Anemia 1 | Yes |   |
| list of observation_concept_id | 3000905, 3003282, 3010813 |   | Leukocytes #/volume in blood |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT DISTINCT 
	  condition.person_id , 
	  observation_date, 
	  condition_era_start_date 
	FROM 
	  condition_era condition 
	JOIN -- definition of Aplastic Anemia 
	( 
	  SELECT DISTINCT descendant_concept_id 
	  FROM relationship 
	  JOIN concept_relationship rel USING( relationship_id ) 
	  JOIN concept concept1 ON concept1.concept_id = concept_id_1 
	  JOIN concept_ancestor ON ancestor_concept_id = concept_id_2 
	  WHERE 
	    relationship_name = 'HOI contains SNOMED (OMOP)' AND 
	    concept1.concept_name = 'OMOP Aplastic Anemia 1' AND 
	    sysdate BETWEEN rel.valid_start_date and rel.valid_end_date 
	) ON descendant_concept_id = condition_concept_id 
	JOIN observation 
	  ON observation.person_id = condition.person_id AND 
	     observation_date BETWEEN condition_era_start_date - 7 AND condition_era_start_date + 7 
	WHERE 
	  observation_concept_id IN /* leukocytes #/volume in blood */ ( 3000905, 3003282, 3010813 ) AND 
	  unit_concept_id = 8961 /* Thousand per cubic millimeter */ AND 
	  value_as_number <= 3.5;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| person_id |   |
| observation_date |   |
| condition_era_start_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |

Sample output record:

|  Field |  Description |
| --- | --- |
| person_id |   |
| observation_date |   |
| condition_era_start_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |

COC09: Condition that is regionally dependent
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| source_code | 088.81 | Yes | lyme disease |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT	state,
			count(*) AS total_enroled,
			sum( lymed ) AS lyme_cases,
			TRUNC( ( sum(lymed) /count(*) ) * 100, 2 ) AS percentages
	FROM
		(
		SELECT	person_id,
				state,
				NVL( lymed, 0 ) lymed
		FROM person
			JOIN location USING( location_id )
			LEFT OUTER JOIN
				(
				SELECT DISTINCT	person_id,
								1 AS lymed
				FROM
					condition_era
						JOIN source_to_concept_map
							ON	target_concept_id = condition_concept_id
				WHERE
					source_vocabulary_id 	= 'ICD9CM'
				AND	target_vocabulary_id 	= 'SNOMED'
				AND	source_code 			= '088.81'
				AND sysdate 				BETWEEN valid_start_date and valid_end_date
				) USING( person_id ) 
		)
	GROUP BY	state
	ORDER BY	4 DESC;
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| state | The state field as it appears in the source data. |
| count |   |
| lyme_cases |   |
| percent |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| state |   |
| count |   |
| lyme_cases |   |
| percent |   |

COC10: Lenght of condition as function of treatment
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_code | '22851','20936','22612','22523','22630','22614','22842' , '22632', '20930','22524','27130','22525' | Yes |   |
| concept_code | 20610','20552','207096','20553','20550','20605' | Yes |   |
| drug_concept_id | 1125315, 778711, 115008, 1177480, 1112807, 1506270 | Yes |   |
| concept_code | '97001', '97140', '97002' | Yes |   |
| concept_code | G0283 | Yes |   |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
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
	         WHEN drug = 1 THEN 'Rx Only' 
	         ELSE 'No Treatment' 
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
	        SELECT DISTINCT 
	          descendant_concept_id -- concept_name 
	        FROM source_to_concept_map map 
	        JOIN concept_ancestor ON ancestor_concept_id = target_concept_id 
	        JOIN concept ON concept_id = descendant_concept_id 
	        WHERE 
	          source_code like '724%' AND 
	          source_vocabulary_id = 'ICD9CM' AND 
	          target_vocabulary_id = 'SNOMED' AND 
	          sysdate BETWEEN map.valid_start_date AND map.valid_end_date 
	      ) ON descendant_concept_id = condition_concept_id 
	      LEFT OUTER JOIN ( 
	        SELECT 
	          person_id, 
	          procedure_date, 
	          1 AS surgery 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 'CPT4' AND 
	          concept_code IN( '22851','20936','22612','22523','22630','22614*','22842','22632','20930','22524','27130','22525' ) 
	      ) surgery 
	        ON surgery.person_id = era.person_id AND 
	           surgery.procedure_date BETWEEN condition_era_start_date AND condition_era_start_date + 60 
	      LEFT OUTER JOIN ( 
	        SELECT 
	          person_id, 
	          procedure_date AS drug_date, 
	          1 AS drug 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 'CPT4' AND 
	          concept_code IN( '20610','20552','207096','20553','20550','20605' ,'20551','20600','23350' ) 
	        UNION SELECT 
	          person_id, 
	          drug_era_start_date, 
	          1 
	        FROM drug_era 
	        WHERE drug_concept_id IN(1125315, 778711, 1115008, 1177480, 1112807,1506270 ) 
	      ) drug 
	        ON drug.person_id = era.person_id AND 
	           drug.drug_date BETWEEN condition_era_start_date AND condition_era_start_date + 60 
	      LEFT OUTER JOIN ( 
	        SELECT 
	          person_id, 
	          procedure_date AS pt_date, 
	          1 AS pt 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 'CPT4' AND 
	          concept_code IN( '97001', '97140', '97002' ) 
	        UNION SELECT 
	          person_id, 
	          procedure_date AS pt_date, 
	          1 AS pt 
	        FROM procedure_occurrence proc 
	        JOIN concept ON concept_id = procedure_concept_id 
	        WHERE 
	          vocabulary_id = 'HCPCS' AND 
	          concept_code = 'G0283' 
	      ) pt 
	        ON pt.person_id = era.person_id AND 
	           pt.pt_date BETWEEN condition_era_start_date AND condition_era_start_date + 60 
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
```

Output:

Output field list:

|  Field |  Description |
| --- | --- |
| treatment |   |
| count |   |
| min |   |
| max |   |
| avg_condition_days |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| treatment |   |
| count |   |
| min |   |
| max |   |
| avg_condition_days |   |

COC11: Given a condition, what treatment did patient receive
---

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| concept_code | '22851', '20936', '22612', '22523', '22630', '22614', '22842' , '22632', '20930', '22524', '27130', '22525' | Yes |   |

Sample query run:

The following is a sample run of the query. The input parameters are highlighted in  blue  

```sql
	SELECT treatment, count(*) 
	FROM
	(
	SELECT CASE WHEN surgery = 1
	            THEN 'surgery'
	            WHEN drug = 1 AND pt = 1 
	            THEN 'PT Rx'
	            WHEN drug = 1
	            THEN 'Rx Only'
	            ELSE 'No Treatment'
	       END AS treatment
	FROM
	(
	SELECT person_id, diag_date
	     , max( drug ) AS drug, max( surgery ) AS surgery, max( pt ) AS PT
	  FROM /* back pain and treatments over following 60 days */
	     ( 
	     SELECT era.person_id, condition_era_start_date AS diag_date
	          , NVL( drug, 0 ) AS drug, NVL( surgery, 0 ) AS surgery
	          , NVL( pt, 0 ) AS pt
	       FROM condition_era era
		   
	       JOIN /* SNOMed codes for back pain */
				( SELECT DISTINCT ca.descendant_concept_id
				FROM concept_ancestor ca JOIN
				( SELECT cr.concept_id_2 AS target_concept_id
					FROM concept_relationship cr
					JOIN concept c1 ON cr.concept_id_1 = c1.concept_id
					JOIN concept c2 ON cr.concept_id_2 = c2.concept_id
					JOIN vocabulary v1 ON c1.vocabulary_id = v1.vocabulary_id
					JOIN vocabulary v2 ON c2.vocabulary_id = v2.vocabulary_id
					WHERE cr.relationship_id = 'Maps to'
					AND c1.concept_code like '724%'
					AND c2.standard_concept = 'S'
					AND v1.vocabulary_id = 'ICD9CM'
					AND v2.vocabulary_id = 'SNOMED'
					AND sysdate BETWEEN cr.valid_start_date AND cr.valid_end_date
				) t ON ca.ancestor_concept_id = t.target_concept_id			
				
	          ) ON descendant_concept_id = condition_concept_id
	      LEFT OUTER JOIN /* surgery */
	         ( SELECT person_id, procedure_date, 1 AS surgery
	             FROM procedure_occurrence proc
	             JOIN concept ON concept_id = procedure_concept_id
	            WHERE vocabulary_id = 'CPT4' /* CPT-4 */
	              AND concept_code
	               IN( '22851', '20936', '22612', '22523', '22630',
	                   '22614', '22842', '22632', '20930', '22524',
	                   '27130', '22525'
	                 )
	         ) surgery
	        ON surgery.person_id = era.person_id
	       AND surgery.procedure_date BETWEEN condition_era_start_date
	                                      AND condition_era_start_date + 60
	      LEFT OUTER JOIN /* drugs */
	         ( SELECT person_id, procedure_date AS drug_date, 1 AS drug
	             FROM procedure_occurrence proc
	             JOIN concept ON concept_id = procedure_concept_id
	            WHERE vocabulary_id = 'CPT4' /* CPT-4 */
	              AND concept_code
	               IN( '20610','20552','207096','20553','20550','20605'
	                 ,'20551','20600','23350' )
	          UNION 
	          SELECT person_id, drug_era_start_date, 1
	            FROM drug_era
	           WHERE drug_concept_id
	              IN( 1125315, 778711, 1115008, 1177480, 1112807, 1506270 )
	         ) drug 
	        ON drug.person_id = era.person_id
	       AND drug.drug_date BETWEEN condition_era_start_date
	                              AND condition_era_start_date + 60
	      LEFT OUTER JOIN /* pt */
	         ( SELECT person_id, procedure_date AS pt_date, 1 AS pt
	             FROM procedure_occurrence proc
	             JOIN concept ON concept_id = procedure_concept_id
	            WHERE vocabulary_id = 'CPT4' /* CPT-4 */
	              AND concept_code
	               IN( '97001', '97140', '97002' )
	           UNION
	           SELECT person_id, procedure_date AS pt_date, 1 AS pt
	             FROM procedure_occurrence proc
	             JOIN concept ON concept_id = procedure_concept_id
	            WHERE vocabulary_id = 'HCPCS' /* HCPCS */
	              AND concept_code = 'G0283'
	         ) pt
	        ON pt.person_id = era.person_id
	       AND pt.pt_date BETWEEN condition_era_start_date
	                          AND condition_era_start_date + 60
	     )
	 WHERE diag_date > '2011-01-01'
	 GROUP by person_id, diag_date
	 ORDER BY person_id, diag_date
	)
	)
	GROUP BY treatment ORDER BY treatment;
```



 Output:

Output field list:

|  Field |  Description |
| --- | --- |
| treatment |   |
| count |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| treatment |   |
| count |   |



