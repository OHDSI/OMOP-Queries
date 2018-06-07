Condition Queries
---

C01: Find condition by concept ID
---

Find condition by condition ID is the lookup for obtaining condition or disease concept details associated with a concept identifier. This query is a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier, either SNOMED-CT clinical finding or MedDRA.
This query is equivalent to  [G01](http://vocabqueries.omop.org/general-queries/g1), but if the concept is not in the condition domain the query still returns the concept details with the Is_Disease_Concept_Flag field set to 'No'.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | Concept Identifier for 'GI - Gastrointestinal haemorrhage' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to run a search for specific disease concept ID. 

The input parameters are highlighted in  blue.

	SELECT 
	  C.concept_id Condition_concept_id, 
	  C.concept_name Condition_concept_name, 
	  C.concept_code Condition_concept_code, 
	  C.concept_class_id Condition_concept_class,
	  C.vocabulary_id Condition_concept_vocab_ID, 
	  V.vocabulary_name Condition_concept_vocab_name, 
	  CASE C.vocabulary_id 
	    WHEN 'SNOMED' THEN CASE lower(C.concept_class_id)   
		  WHEN 'clinical finding' THEN 'Yes' ELSE 'No' END 
		WHEN 'MedDRA' THEN 'Yes'
		ELSE 'No' 
	  END Is_Disease_Concept_flag 
	FROM concept C, vocabulary V 
	WHERE 
	  C.concept_id = 192671 AND 
	  C.vocabulary_id = V.vocabulary_id AND 
	  sysdate BETWEEN valid_start_date AND valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Condition_Concept_ID |  Condition concept Identifier entered as input |
|  Condition_Concept_Name |  Name of the standard condition concept |
|  Condition_Concept_Code |  Concept code of the standard concept in the source vocabulary |
|  Condition_Concept_Class |  Concept class of standard vocabulary concept |
|  Condition_Concept_Vocab_ID  |  Vocabulary the standard concept is derived from as vocabulary code |
|  Condition_Concept_Vocab_Name |  Name of the vocabulary the standard concept is derived from |
|  Is_Disease_Concept_Flag |  Flag indicating whether the Concept ID belongs to a disease concept. 'Yes' if disease concept, 'No' if not a disease concept |


Sample output record:

|  Field |  Value |
|  Condition_Concept_ID |  192671 |
|  Condition_Concept_Name |  GI - Gastrointestinal hemorrhage |
|  Condition_Concept_Code |  74474003 |
|  Condition_Concept_Class |  Clinical finding |
|  Condition_Concept_Vocab_ID |  SNOMED |
|  Condition_Concept_Vocab_Name | Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
|  Is_Disease_Concept_Flag |  Yes |

C02: Find a condition by keyword
---

This query enables search of vocabulary entities by keyword. The query does a search of standard concepts names in the CONDITION domain (SNOMED-CT clinical findings and MedDRA concepts) and their synonyms to return all related concepts.

It does not require prior knowledge of where in the logic of the vocabularies the entity is situated.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword |  'myocardial infarction' |  Yes | Keyword should be placed in a single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to run a search of the Condition domain for keyword 'myocardial infarction'. The input parameters are highlighted in  blue.

	SELECT 
	  T.Entity_Concept_Id, 
	  T.Entity_Name, 
	  T.Entity_Code, 
	  T.Entity_Type, 
	  T.Entity_concept_class, 
	  T.Entity_vocabulary_id, 
	  T.Entity_vocabulary_name 
	FROM ( 
	  SELECT 
	    C.concept_id Entity_Concept_Id, 
		C.concept_name Entity_Name, 
		C.CONCEPT_CODE Entity_Code, 
		'Concept' Entity_Type, 
		C.concept_class_id Entity_concept_class, 
		C.vocabulary_id Entity_vocabulary_id, 
		V.vocabulary_name Entity_vocabulary_name, 
		NULL Entity_Mapping_Type, 
		C.valid_start_date, 
		C.valid_end_date 
	  FROM concept C 
	  JOIN vocabulary V ON C.vocabulary_id = V.vocabulary_id 
	  LEFT JOIN concept_synonym S ON C.concept_id = S.concept_id 
	  WHERE 
	    (C.vocabulary_id IN ('SNOMED', 'MedDRA') OR LOWER(C.concept_class_id) = 'clinical finding' ) AND 
		C.concept_class_id IS NOT NULL AND 
		( LOWER(C.concept_name) like '%myocardial infarction%' OR 
		  LOWER(S.concept_synonym_name) like '%myocardial infarction%' ) 
	  ) T
	WHERE sysdate BETWEEN valid_start_date AND valid_end_date 
	ORDER BY 6,2;


Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Entity_Concept_ID |  Concept ID of entity with string match on name or synonym concept |
|  Entity_Name |  Concept name of entity with string match on name or synonym concept |
|  Entity_Code |  Concept code of entity with string match on name or synonym concept  |
|  Entity_Type |  Concept type |
|  Entity_Concept_Class |  Concept class of entity with string match on name or synonym concept |
|  Entity_Vocabulary_ID |  ID of vocabulary associated with the concept |
|  Entity_Vocabulary_Name |  Name of the vocabulary associated with the concept |


Sample output record:

|  Field |  Value |
| --- | --- |
|  Entity_Concept_ID |  35205180 |
|  Entity_Name |  Acute myocardial infarction |
|  Entity_Code |  10000891 |
|  Entity_Type |  Concept |
|  Entity_Concept_Class |  Preferred Term |
|  Entity_Vocabulary_ID |  MedDRA |
|  Entity_Vocabulary_Name |  Medical Dictionary for Regulatory Activities (MSSO) |

This is a comprehensive query to find relevant terms in the vocabulary. To constrain, additional clauses can be added to the query. However, it is recommended to do a filtering after the result set is produced to avoid syntactical mistakes.

The query only returns concepts that are part of the Standard Vocabulary, ie. they have concept level that is not 0. If all concepts are needed, including the non-standard ones, the clause in the query restricting the concept level and concept class can be commented out. 

C03: Translate a SNOMED-CT concept into a MedDRA concept
---

This query accepts a SNOMED-CT concept ID as input and returns details of the equivalent MedDRA concepts.

The relationships in the vocabulary associate MedDRA 'Preferred Term' to SNOMED-CT 'clinical findings'. The respective hierarchy for MedDRA and SNOMED-CT can be used to traverse up and down the hierarchy of each of these individual vocabularies.

Also, not all SNOMED-CT clinical findings are mapped to a MedDRA concept in the vocabulary.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  312327 |  Yes | Concept Identifier for 'Acute myocardial infarction' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list MedDRA equivalents for SNOMED-CT concept whose concept ID is entered as input. 

	SELECT	D.concept_id Snomed_concept_id,
			D.concept_name Snomed_concept_name,
			D.concept_code Snomed_concept_code,
			D.concept_class_id Snomed_concept_class,
			CR.relationship_id,
			RT.relationship_name,
			A.Concept_id MedDRA_concept_id,
			A.Concept_name MedDRA_concept_name,
			A.Concept_code MedDRA_concept_code,
			A.Concept_class_id MedDRA_concept_class 
	FROM concept_relationship CR, concept A, concept D, relationship RT 
	WHERE CR.relationship_id =  'SNOMED - MedDRA eq'
	AND CR.concept_id_2 = A.concept_id 
	AND CR.concept_id_1 = 312327
	AND CR.concept_id_1 = D.concept_id 
	AND CR.relationship_id = RT.relationship_id 
	AND sysdate BETWEEN CR.valid_start_date 
	AND CR.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  SNOMED-CT_Concept_ID |  Concept ID of SNOMED-CT concept entered as input |
|  SNOMED-CT_Concept_Name |  Name of SNOMED-CT concept |
|  SNOMED-CT_Concept_Code |  Concept code of SNOMED-CT concept |
|  SNOMED-CT_Concept_Class |  Concept class of SNOMED-CT concept |
|  Relationship_ID |  Identifier for the type of relationship |
|  Relationship_Name |  Description of the type of relationship |
|  MedDRA_Concept_ID |  Concept ID of matching MedDRA concept |
|  MedDRA_Concept_Name |  Concept name of matching MedDRA concept |
|  MedDRA_Concept_Code |  Concept code of matching MedDRA concept |
|  MedDRA_Concept_Class |  Concept class of matching MedDRA concept |

Sample output record:

|  Field |  Value |
| --- | --- |
|  SNOMED-CT_Concept_ID |  312327 |
|  SNOMED-CT_Concept_Name |  Acute myocardial infarction |
|  SNOMED-CT_Concept_Code |  57054005 |
|  SNOMED-CT_Concept_Class |  Clinical finding |
|  Relationship_ID |  SNOMED - MedDRA eq |
|  Relationship_Name |  SNOMED-CT to MedDRA equivalent (OMOP) |
|  MedDRA_Concept_ID |  35205180 |
|  MedDRA_Concept_Name |  Acute myocardial infarction |
|  MedDRA_Concept_Code |  10000891 |
|  MedDRA_Concept_Class |  Preferred Term |

C04: Translate a MedDRA concept into a SNOMED-CT concept
---

This query accepts a MedDRA concept ID as input and returns details of the equivalent SNOMED-CT concepts.
The existing relationships in the vocabulary associate MedDRA 'Preferred Term' to SNOMED-CT 'clinical findings'. The respective hierarchy for MedDRA and SNOMED-CT can be used to traverse up and down the hierarchy of each of these individual vocabularies.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  MedDRA Concept ID |  35205180 |  Yes | Concept Identifier for 'Acute myocardial infarction' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list all MedDRA concepts that have SNOMED-CT equivalents. Sample parameter substitution is highlighted in  blue.

	SELECT	D.concept_id MedDRA_concept_id,
			D.concept_name MedDRA_concept_name,
			D.concept_code MedDRA_concept_code,
			D.concept_class_id MedDRA_concept_class,
			CR.relationship_id,
			RT.relationship_name,
			A.concept_id Snomed_concept_id,
			A.concept_name Snomed_concept_name,
			A.concept_code Snomed_concept_code,
			A.concept_class_id Snomed_concept_class 
	FROM concept_relationship CR, concept A, concept D, relationship RT 
	WHERE CR.relationship_id = 'MedDRA to SNOMED equivalent (OMOP)'
	AND CR.concept_id_2 = A.concept_id 
	AND CR.concept_id_1 = 35205180

	AND CR.concept_id_1 = D.concept_id 
	AND CR.relationship_id = RT.relationship_id 
	AND sysdate BETWEEN CR.valid_start_date 
	AND CR.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  MedDRA_Concept_ID |  Concept ID of MedDRA concept entered as input |
|  MedDRA_Concept_Name |  Concept name of MedDRA concept |
|  MedDRA_Concept_Code |  Concept code of MedDRA concept |
|  MedDRA_Concept_Class |  Concept class of MedDRA concept |
|  Relationship_ID |  Identifier for the type of relationship |
|  Relationship_Name |  Description of the type of relationship |
|  SNOMED-CT_Concept_ID |  Concept ID of matching SNOMED-CT concept |
|  SNOMED-CT_Concept_Name |  Name of matching SNOMED-CT concept |
|  SNOMED-CT_Concept_Code |  Concept Code of matching SNOMED-CT concept |
|  SNOMED-CT_Concept_Class |  Concept class of matching SNOMED-CT concept |

Sample output record:

|  Field |  Value |
| --- | --- |
|  MedDRA_Concept_ID |  35205180 |
|  MedDRA_Concept_Name |  Acute myocardial infarction |
|  MedDRA_Concept_Code |  10000891 |
|  MedDRA_Concept_Class |  Preferred Term |
|  Relationship_ID |  MedDRA to SNOMED equivalent (OMOP) |
|  Relationship_Name |  MedDRA to SNOMED-CT equivalent (OMOP) |
|  SNOMED-CT_Concept_ID |  312327 |
|  SNOMED-CT_Concept_Name |  Acute myocardial infarction |
|  SNOMED-CT_Concept_Code |  57054005 |
|  SNOMED-CT_Concept_Class |  Clinical finding |


C05: Translate a source code to condition concepts
---

This query enables to search all Standard SNOMED-CT concepts that are mapped to a condition (disease) source code. It can be used to translate e.g. ICD-9-CM, ICD-10-CM or Read codes to SNOMED-CT.

Source codes are not unique across different source vocabularies, therefore the source vocabulary ID must also be provided.

The following source vocabularies have condition/disease codes that map to SNOMED-CT concepts:

-  ICD-9-CM,    Vocabulary_id=2
- Read,            Vocabulary_id=17
- OXMIS,         Vocabulary_id=18
- ICD-10-CM,   Vocabulary_id=34

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Source Code List |  '070.0' |  Yes | Source codes are alphanumeric and need to be entered as a string enclosed by a single quote. If more than one source code needs to be entered an IN clause or a JOIN can be used. |
|  Source Vocabulary ID |  2 |  Yes | The source vocabulary is mandatory, because the source ID is not unique across different vocabularies. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list SNOMED-CT concepts that a set of mapped codes entered as input map to. The sample parameter substitutions are highlighted in  blue 

	set search_path to full_201612_omop_v5;

	SELECT DISTINCT 
	  c1.concept_code, 
	  c1.concept_name, 
	  c1.vocabulary_id source_vocabulary_id, 
	  VS.vocabulary_name source_vocabulary_description, 
	  C1.domain_id, 
	  C2.concept_id target_concept_id, 
	  C2.concept_name target_Concept_Name, 
	  C2.concept_code target_Concept_Code, 
	  C2.concept_class_id target_Concept_Class, 
	  C2.vocabulary_id target_Concept_Vocab_ID, 
	  VT.vocabulary_name target_Concept_Vocab_Name 
	FROM 
	  concept_relationship cr, 
	  concept c1, 
	  concept c2,
	  vocabulary VS, 
	  vocabulary VT 
	WHERE 
	  cr.concept_id_1 = c1.concept_id AND
	  cr.relationship_id = 'Maps to' AND
	  cr.concept_id_2 = c2.concept_id AND
	  c1.vocabulary_id = VS.vocabulary_id AND 
	  c1.domain_id = 'Condition' AND 
	  c2.vocabulary_id = VT.vocabulary_id AND 
	  c1.concept_code IN (
	'070.0'                                           
	) AND c2.vocabulary_id =
	'SNOMED'                                          
	AND
	sysdate                                           
	BETWEEN c1.valid_start_date AND c1.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Source_Code |  Source code for the disease entered as input |
|  Source_Code_Description |  Description of the source code entered as input |
|  Source_Vocabulary_ID |  Vocabulary the disease source code is derived from as vocabulary ID |
|  Source_Vocabulary_Description |  Name of the vocabulary the disease source code is derived from |
|  Mapping_Type |  Type of mapping or mapping domain, from source code to target concept. Example Condition, Procedure, Drug etc. |
|  Target_Concept_ID |  Concept ID of the target condition concept mapped to the disease source code |
|  Target_Concept_Name |  Name of the target condition concept mapped to the disease source code |
|  Target_Concept_Code |  Concept code of the target condition concept mapped to the disease source code |
|  Target_Concept_Class |  Concept class of the target condition concept mapped to the disease source code |
|  Target_Concept_Vocab_ID |  Vocabulary the target condition concept is derived from as vocabulary code |
|  Target_Concept_Vocab_Name |  Name of the vocabulary the condition concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Source_Code |  070.0 |
|  Source_Code_Description |  Viral hepatitis |
|  Source_Vocabulary_ID |  ICD9CM |
|  Source_Vocabulary_Description |  International Classification of Diseases, Ninth Revision, Clinical Modification, Volume 1 and 2 (NCHS) |
|  Mapping_Type |  CONDITION |
|  Target_Concept_ID |  4291005 |
|  Target_Concept_Name |  VH - Viral hepatitis |
|  Target_Concept_Code |  3738000 |
|  Target_Concept_Class |  Clinical finding |
|  Target_Concept_Vocab_ID |  SNOMED |
|  Target_Concept_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C06: Translate a given condition to source codes
---

This query allows to search all source codes that are mapped to a SNOMED-CT clinical finding concept. It can be used to translate SNOMED-CT to ICD-9-CM, ICD-10-CM, Read or OXMIS codes.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  312327 |  Yes | Concept IDs are numeric. If more than one concept code needs to be translated an IN clause or a JOIN can be used. |
|  Source Vocabulary ID |  2 |  Yes | 2 represents ICD9-CM |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run: 

The following is a sample run of the query to list all source codes that map to a SNOMED-CT concept entered as input. The sample parameter substitutions are highlighted in  blue.

	SELECT DISTINCT
	  c1.concept_code,
	  c1.concept_name,
	  c1.vocabulary_id source_vocabulary_id,
	  VS.vocabulary_name source_vocabulary_description,
	  C1.domain_id,
	  C2.concept_id target_concept_id,
	  C2.concept_name target_Concept_Name,
	  C2.concept_code target_Concept_Code,
	  C2.concept_class_id target_Concept_Class,
	  C2.vocabulary_id target_Concept_Vocab_ID,
	  VT.vocabulary_name target_Concept_Vocab_Name
	FROM
	  concept_relationship cr,
	  concept c1,
	  concept c2,
	  vocabulary VS,
	  vocabulary VT
	WHERE
	  cr.concept_id_1 = c1.concept_id AND
	  cr.relationship_id = 'Maps to' AND
	  cr.concept_id_2 = c2.concept_id AND
	  c1.vocabulary_id = VS.vocabulary_id AND
	  c1.domain_id = 'Condition' AND
	  c2.vocabulary_id = VT.vocabulary_id AND
	  c1.concept_id =
	312327                                            
	  AND c1.vocabulary_id =
	'SNOMED'                                          
	AND
	sysdate                                           
	BETWEEN c2.valid_start_date AND c2.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Source_Code |  Source code for the disease entered as input |
|  Source_Code_Description |  Description of the source code entered as input |
|  Source_Vocabulary_ID |  Vocabulary the disease source code is derived from as vocabulary code |
|  Source_Vocabulary_Description |  Name of the vocabulary the disease source code is derived from |
|  Mapping_Type |  Type of mapping or mapping domain, from source code to target concept. Example Condition, Procedure, Drug etc. |
|  Target_Concept_ID |  Concept ID of the SNOMED-CT concept entered as input |
|  Target_Concept_Name |  Name of the SNOMED-CT concept entered as input |
|  Target_Concept_Code |  Concept code of the SNOMED-CT concept entered as input |
|  Target_Concept_Class |  Concept class of the SNOMED-CT concept entered as input |
|  Target_Concept_Vocab_ID |  Vocabulary of concept entered as input is derived from, as vocabulary ID |
|  Target_Concept_Vocab_Name |  Name of vocabulary the concept entered as input is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Source_Code |  410.92 |
|  Source_Code_Description |  Acute myocardial infarction, unspecified site, subsequent episode of care |
|  Source_Vocabulary_ID |  SNOMED |
|  Source_Vocabulary_Description |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
|  Mapping_Type |  CONDITION |
|  Target_Concept_ID |  312327 |
|  Target_Concept_Name |  Acute myocardial infarction |
|  Target_Concept_Code |  57054005 |
|  Target_Concept_Class |  Clinical finding |
|  Target_Concept_Vocab_ID |  SNOMED |
|  Target_Concept_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C07: Find a pathogen by keyword
---

This query enables a search of all pathogens using a keyword as input. The resulting concepts could be used in query  [C09](http://vocabqueries.omop.org/condition-queries/c9) to identify diseases caused by a certain pathogen.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Trypanosoma' |  Yes | Keyword should be placed in a single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list all pathogens specified using a keyword as input. The sample parameter substitutions are highlighted in  blue.

	SELECT 
	  C.concept_id Pathogen_Concept_ID, 
	  C.concept_name Pathogen_Concept_Name, 
	  C.concept_code Pathogen_concept_code, 
	  C.concept_class_id Pathogen_concept_class, 
	  C.standard_concept Pathogen_Standard_Concept, 
	  C.vocabulary_id Pathogen_Concept_Vocab_ID, 
	  V.vocabulary_name Pathogen_Concept_Vocab_Name 
	FROM 
	  concept C, 
	  vocabulary V
	WHERE 
	  LOWER(C.concept_class_id) = 'organism' AND 
	  LOWER(C.concept_name) like
	'%trypanosoma%'                                
	AND C.vocabulary_id = V.vocabulary_id AND
	sysdate                                        
	BETWEEN C.valid_start_date AND C.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Pathogen_Concept_ID |  Concept ID of SNOMED-CT pathogen concept |
|  Pathogen_Concept_Name |  Name of SNOMED-CT pathogen concept with keyword entered as input |
|  Pathogen_Concept_Code |  Concept Code of SNOMED-CT pathogen concept |
|  Pathogen_Concept_Class |  Concept class of SNOMED-CT pathogen concept |
|  Pathogen_Standard_Concept |  Indicator of standard concept of SNOMED-CT pathogen concept |
|  Pathogen_Vocab_ID |  Vocabulary ID of the vocabulary from which the pathogen concept is derived from (1 for SNOMED-CT) |
|  Pathogen_Vocab_Name |  Name of the vocabulary from which the pathogen concept is derived from (SNOMED-CT) |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Pathogen_Concept_ID |  4085768 |
|  Pathogen_Concept_Name |  Trypanosoma brucei |
|  Pathogen_Concept_Code |  243659009 |
|  Pathogen_Concept_Class |  Organism |
| Pathogen_Standard_Concept |  S |
|  Pathogen_Vocab_ID |  SNOMED |
|  Pathogen_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C08: Find a disease causing agent by keyword
---

This query enables a search of various agents that can cause disease by keyword as input. Apart from pathogens (see query  [C07](http://vocabqueries.omop.org/condition-queries/c7)), these agents can be SNOMED-CT concepts of the following classes:
- Pharmaceutical / biologic product
- Physical object
- Special concept
- Event
- Physical force
- Substance

The resulting concepts could be used in query  [C09](http://vocabqueries.omop.org/condition-queries/c9) to identify diseases caused by the agent.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Radiation' |  Yes | Keyword should be placed in a single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list all pathogens specified using a keyword as input. The sample parameter substitutions are highlighted in  blue.

	SELECT
	  C.concept_id Agent_Concept_ID,
	  C.concept_name Agent_Concept_Name,
	  C.concept_code Agent_concept_code,
	  C.concept_class_id Agent_concept_class,
	  C.standard_concept Agent_Standard_Concept,
	  C.vocabulary_id Agent_Concept_Vocab_ID,
	  V.vocabulary_name Agent_Concept_Vocab_Name
	FROM
	  concept C,
	  vocabulary V
	WHERE
	  LOWER(C.concept_class_id) in ('pharmaceutical / biologic product','physical object',
	                                'special concept','event', 'physical force','substance') AND
	  LOWER(C.concept_name) like
	'%radiation%'                                  
	AND C.vocabulary_id = V.vocabulary_id AND
	sysdate                                        
	BETWEEN C.valid_start_date AND C.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Agent_Concept_ID |  Concept ID of SNOMED-CT agent concept |
|  Agent_Concept_Name |  Name of SNOMED-CT concept |
|  Agent_Concept_Code |  Concept Code of SNOMED-CT concept |
|  Agent_Concept_Class |  Concept class of SNOMED-CT concept |
|  Agent_Standard_Concept |  Indicator of standard concept for SNOMED-CT concept |
|  Agent_Vocab_ID |  Vocabulary ID of the vocabulary from which the agent concept is derived from (1 for SNOMED-CT) |
|  Agent_Vocab_Name |  Name of the vocabulary from which the agent concept is derived from (SNOMED-CT) |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Agent_Concept_ID |  4220084 |
|  Agent_Concept_Name |  Radiation |
|  Agent_Concept_Code |  82107009 |
|  Agent_Concept_Class |  Physical force |
|  Agent_Standard_Concept |  S |
|  Agent_Vocab_ID |  SNOMED |
|  Agent_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C09: Find all SNOMED-CT condition concepts that can be caused by a given pathogen or causative agent
---

This query accepts a SNOMED-CT pathogen ID as input and returns all conditions caused by the pathogen or disease causing agent identified using queries  [C07](http://vocabqueries.omop.org/condition-queries/c7) or  [C08](http://vocabqueries.omop.org/condition-queries/c8).

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  4248851 |  Yes | Concept Identifier for 'Treponema pallidum' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list conditions caused by pathogen or causative agent. Sample parameter substitution is highlighted in  blue.

	SELECT 
	  A.concept_Id Condition_ID, 
	  A.concept_Name Condition_name, 
	  A.concept_Code Condition_code, 
	  A.concept_Class_id Condition_class, 
	  A.vocabulary_id Condition_vocab_ID, 
	  VA.vocabulary_name Condition_vocab_name, 
	  D.concept_Id Causative_agent_ID, 
	  D.concept_Name Causative_agent_Name, 
	  D.concept_Code Causative_agent_Code, 
	  D.concept_Class_id Causative_agent_Class, 
	  D.vocabulary_id Causative_agent_vocab_ID, 
	  VS.vocabulary_name Causative_agent_vocab_name 
	FROM 
	  concept_relationship CR, 
	  concept A, 
	  concept D, 
	  vocabulary VA, 
	  vocabulary VS
	WHERE 
	  CR.relationship_ID = 'Has causative agent' AND 
	  CR.concept_id_1 = A.concept_id AND 
	  A.vocabulary_id = VA.vocabulary_id AND 
	  CR.concept_id_2 = D.concept_id AND 
	  D.concept_id =
	4248851                                             
	  AND D.vocabulary_id = VS.vocabulary_id AND 
	sysdate                                             
	  BETWEEN CR.valid_start_date AND CR.valid_end_date;

Output:

Output field list:

|  Field |  Description |
| --- | --- |
|  Condition_ID |  Condition concept Identifier |
|  Condition_Name |  Name of the standard condition concept |
|  Condition_Code |  Concept code of the standard concept in the source vocabulary |
|  Condition_Class |  Concept class of standard vocabulary concept |
|  Condition_Vocab_ID |  Vocabulary the standard concept is derived from as vocabulary ID |
|  Condition_Vocab_Name |  Name of the vocabulary the standard concept is derived from |
|  Causative_Agent_ID |  Pathogen concept ID entered as input |
|  Causative_Agent_Name |  Pathogen Name |
|  Causative_Agent_Code |  Concept Code of pathogen concept |
|  Causative_Agent_Class |  Concept Class of pathogen concept |
|  Causative_Agent_Vocab_ID |  Vocabulary the pathogen concept is derived from as vocabulary ID |
|  Causative_Agent_Vocab_Name |  Name of the vocabulary the pathogen concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Condition_ID |  4326735 |
|  Condition_Name |  Spastic spinal syphilitic paralysis |
|  Condition_Code |  75299005 |
|  Condition_Class |  Clinical finding |
|  Condition_Vocab_ID |  SNOMED |
|  Condition_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
|  Causative_Agent_ID |  4248851 |
|  Causative_Agent_Name |  Treponema pallidum |
|  Causative_Agent_Code |  72904005 |
|  Causative_Agent_Class |  Organism |
|  Causative_Agent_Vocab_ID |  SNOMED |
|  Causative_Agent_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C10: Find an anatomical site by keyword
---

This query enables a search of all anatomical sites using a keyword entered as input. The resulting concepts could be used in query  [C11](http://vocabqueries.omop.org/condition-queries/c11) to identify diseases occurring at a certain anatomical site.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Epiglottis' |  Yes | Keyword should be placed in a single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run:

The following is a sample run of the query to list all anatomical site concept IDs specified using a keyword as input. The sample parameter substitutions are highlighted in  blue.

	SELECT 
	  C.concept_id Anatomical_site_ID, 
	  C.concept_name Anatomical_site_Name, 
	  C.concept_code Anatomical_site_Code, 
	  C.concept_class_id Anatomical_site_Class, 
	  C.standard_concept Anatomical_standard_concept, 
	  C.vocabulary_id Anatomical_site_Vocab_ID, 
	  V.vocabulary_name Anatomical_site_Vocab_Name 
	FROM 
	  concept C, 
	  vocabulary V 
	WHERE 
	  LOWER(C.concept_class_id) = 'body structure' AND 
	  LOWER(C.concept_name) like
	'%epiglottis%'                                  
	AND C.vocabulary_id = V.vocabulary_id AND
	sysdate                                          
	BETWEEN C.valid_start_date AND C.valid_end_date;

Output:

|  Field |  Description |
| --- | --- |
|  Anatomical_site_ID |  Concept ID of SNOMED-CT anatomical site concept |
|  Anatomical_site_Name |  Name of SNOMED-CT anatomical site concept entered as input |
|  Anatomical_site_Code |  Concept Code of SNOMED-CT anatomical site concept |
|  Anatomical_site_Class |  Concept class of SNOMED-CT anatomical site |
|  Anatomical_standard_concept |  Indicator of standard concept for SNOMED-CT anatomical site |
|  Anatomical_site_vocab_ID |  Vocabulary ID of the vocabulary from which the anatomical site  concept is derived from |
|  Anatomical_site_vocab_name |  Name of the vocabulary from which the anatomical site concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Anatomical_site_ID |  4103720 |
|  Anatomical_site_Name |  Posterior epiglottis |
|  Anatomical_site_Code |  2894003 |
|  Anatomical_site_Class |  Body structure |
|  Anatomical_standard_concept |  S |
|  Anatomical_site_vocab_ID |  SNOMED 1 |
|  Anatomical_site_vocab_name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |

C11: Find all SNOMED-CT condition concepts that are occurring at an anatomical site
---

This query accepts a SNOMED-CT body structure ID as input and returns all conditions occurring in the anatomical site, which can be identified using query  [C10](http://vocabqueries.omop.org/condition-queries/c10). Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  4103720 |  Yes | Concept Identifier for 'Posterior epiglottis' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Sample query run: 

The following is a sample run of the query to list conditions located in the anatomical site.

	SELECT
	  A.concept_Id Condition_ID,
	  A.concept_Name Condition_name,
	  A.concept_Code Condition_code,
	  A.concept_Class_id Condition_class,
	  A.vocabulary_id Condition_vocab_ID,
	  VA.vocabulary_name Condition_vocab_name,
	  D.concept_Id Anatomical_site_ID,
	  D.concept_Name Anatomical_site_Name,
	  D.concept_Code Anatomical_site_Code,
	  D.concept_Class_id Anatomical_site_Class,
	  D.vocabulary_id Anatomical_site_vocab_ID,
	  VS.vocabulary_name Anatomical_site_vocab_name
	FROM
	  concept_relationship CR,
	  concept A,
	  concept D,
	  vocabulary VA,
	  vocabulary VS
	WHERE
	  CR.relationship_ID = 'Has finding site' AND
	  CR.concept_id_1 = A.concept_id AND
	  A.vocabulary_id = VA.vocabulary_id AND
	  CR.concept_id_2 = D.concept_id AND
	  D.concept_id =
	4103720                                             --input
	  AND D.vocabulary_id = VS.vocabulary_id AND
	sysdate                                             --input
	  BETWEEN CR.valid_start_date AND CR.valid_end_date;

 Output: 

 Output field list:

|  Field |  Description |
| --- | --- |
|  Condition_ID |  Condition concept Identifier |
|  Condition_Name |  Name of the standard condition concept |
|  Condition_Code |  Concept code of the standard concept in the source vocabulary |
|  Condition_Class |  Concept class of standard vocabulary concept |
|  Condition_Vocab_ID |  Vocabulary the standard concept is derived from as vocabulary ID |
|  Condition_Vocab_Name |  Name of the vocabulary the standard concept is derived from |
|  Anatomical_Site_ID |  Body Structure ID entered as input |
|  Anatomical_Site_Name |  Body Structure Name |
|  Anatomical_Site_Code |  Concept Code of the body structure concept |
|  Anatomical_Site_Class |  Concept Class of the body structure concept |
|  Anatomical_Site_Vocab_ID |  Vocabulary the body structure concept is derived from as vocabulary code |
|  Anatomical_Site_Vocab_Name |  Name of the vocabulary the body structure concept is derived from |

 Sample output record:

|  Field |  Value |
| --- | --- |
|  Condition_ID |  4054522 |
|  Condition_Name |  Neoplasm of laryngeal surface of epiglottis |
|  Condition_Code |  126700009 |
|  Condition_Class |  Clinical finding |
|  Condition_Vocab_ID |  SNOMED |
|  Condition_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
|  Anatomical_Site_ID |  4103720 |
|  Anatomical_Site_Name |  Posterior epiglottis |
|  Anatomical_Site_Code |  2894003 |
|  Anatomical_Site_Class |  Body structure |
|  Anatomical_Site_Vocab_ID |  SNOMED |
|  Anatomical_Site_Vocab_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
