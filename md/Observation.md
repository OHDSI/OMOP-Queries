Observation Queries
---

O1: Find a Observation from a keyword
---

This query enables the search of LOINC and UCUM descriptions that are used in the observation domain of the vocabulary by keyword.
It does not require prior knowledge of where in the logic of the vocabularies the entity is situated.

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword |  'LDL' |  Yes | Keyword search is case insensitive, and spaces and dashes are excluded from the search |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |



Sample query run:

The following is a sample run of the query to run a search of the Observation domain for keyword 'LDL'. The input parameters are highlighted in  blue.

```sql
	SELECT  T.Entity_Concept_Id,
	        T.Entity_Name,
	        T.Entity_Code,
	        T.Entity_Type,
	        T.Entity_concept_class_id,
	        T.Entity_vocabulary_id,
	        T.Entity_vocabulary_name
	FROM   (
	       SELECT  C.concept_id       Entity_Concept_Id,
	               C.concept_name     Entity_Name,
	               C.concept_code     Entity_Code,
	               'Concept'          Entity_Type,
	               C.concept_class_id    Entity_concept_class_id,
	               C.vocabulary_id    Entity_vocabulary_id,
	               V.vocabulary_name  Entity_vocabulary_name,
	               C.valid_start_date,
	               C.valid_end_date
	       FROM    concept         C, 
	               vocabulary      V
	       WHERE  C.vocabulary_id IN ('LOINC', 'UCUM')
	       AND    C.concept_class_id IS NOT NULL
	       AND    C.standard_concept = 'S'
	       AND    C.vocabulary_id = V.vocabulary_id
	       ) T
	WHERE  REGEXP_INSTR(LOWER(REPLACE(REPLACE(T.Entity_Name, ' ', ''), '-', '')), 
	             LOWER(REPLACE(REPLACE('LDL' , ' ', ''), '-', ''))) > 0
	AND     sysdate BETWEEN T.valid_start_date AND T.valid_end_date
```

Output:

Output field list

|  Field |  Description |
| --- | --- |
|  Entity_Concept_ID | Concept ID of entity with string match on name or synonym concept |
|  Entity_Name | Concept name of entity with string match on name or synonym concept |
|  Entity_Code | Concept code of entity with string match on name or synonym concept |
|  Entity_Type | Type of entity with keyword match (consistent with other keyword search queries elsewhere). Since procedure search is restricted to standard concepts and synonyms, the entity type is always set to 'Concept' |
|  Entity_Concept_Class | Concept class of entity with string match on name or synonym concept |
|  Entity_Vocabulary_ID | Vocabulary the concept with string match is derived from |
|  Entity_Vocabulary_Name | Name of the vocabulary the concept code is derived from |



Sample output record:

|  Field |  Value |
| --- | --- |
|  Entity_Concept_ID |  3033200 |
|  Entity_Name |  Cholesterol in LDL [Mass or Moles/volume] in Serum or Plasma |
|  Entity_Code |  35198-1 |
|  Entity_Type |  Concept |
|  Entity_Concept_Class |  LOINC Code |
|  Entity_Vocabulary_ID |  LOINC |
|  Entity_Vocabulary_Name |  Logical Observation Identifiers Names and Codes (Regenstrief Institute) |

