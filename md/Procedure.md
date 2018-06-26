Procedure Queries
---

P02: Find a procedure from a keyword.
---

This query enables search of procedure domain of the vocabulary by keyword. The query does a search of standard concepts names in the PROCEDURE domain (SNOMED-CT procedures, ICD9 procedures, CPT procedures and HCPCS procedures) and their synonyms to return all related concepts.

This is a comprehensive query to find relevant terms in the vocabulary. It does not require prior knowledge of where in the logic of the vocabularies the entity is situated. To constrain, additional clauses can be added to the query. However, it is recommended to do a filtering after the result set is produced to avoid syntactical mistakes.
The query only returns concepts that are part of the Standard Vocabulary, ie. they have concept level that is not 0. If all concepts are needed, including the non-standard ones, the clause in the query restricting the concept level and concept class can be commented out.

Sample query:

```sql
    SELECT C.concept_id         Entity_Concept_Id,

           C.concept_name       Entity_Name,

           C.concept_code       Entity_Code,

           'Concept'            Entity_Type,

           C.concept_class_id      Entity_concept_class_id,

           C.vocabulary_id      Entity_vocabulary_id,

           V.vocabulary_name    Entity_vocabulary_name

    FROM   concept   C

       INNER JOIN vocabulary V ON C.vocabulary_id = V.vocabulary_id

       LEFT OUTER JOIN concept_synonym S ON C.concept_id = S.concept_id

    WHERE  (

                  C.vocabulary_id IN ('ICD9Proc', 'CPT4', 'HCPCS')

           OR     LOWER(C.concept_class_id) = 'procedure'

           )

    AND    C.concept_class_id IS NOT NULL

    AND    C.standard_concept = 'S'

    AND    (

                REGEXP_INSTR(LOWER(C.concept_name), LOWER('artery bypass')) > 0

           OR   REGEXP_INSTR(LOWER(S.concept_synonym_name), LOWER('artery bypass')) > 0

           )

    AND    sysdate BETWEEN C.valid_start_date AND C.valid_end_date;
```

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword |  'artery bypass' |  Yes | Procedure keyword search |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Entity_Concept_ID |  Concept ID of entity with string match on name or synonym concept |
|  Entity_Name |  Concept name of entity with string match on name or synonym concept |
|  Entity_Code |  Concept code of entity with string match on name or synonym concept |
|  Entity_Type |  Type of entity with keyword match (consistent with other keyword search queries elsewhere). Since procedure search is restricted to standard concepts and synonyms, the entity type is always set to 'Concept' |
|  Entity_Concept_Class |  Concept class of entity with string match on name or synonym concept |
|  Entity_Vocabulary_ID |  Vocabulary the concept with string match is derived from as vocabulary ID |
|  Entity_Vocabulary_Name |  Name of the vocabulary the concept with string match is derived from as vocabulary code |

Sample output record:

| Field |  Value |
| --- | --- |
|  Entity_Concept_ID |  2107223 |
|  Entity_Name |  Coronary artery bypass, using venous graft(s) and arterial graft(s); two venous grafts (List separately in addition to code for primary procedure) |
|  Entity_Code |  33518 |
|  Entity_Type |  Concept |
|  Entity_Concept_Class |  CPT-4 |
|  Entity_Vocabulary_ID |  4 |
|  Entity_Vocabulary_Name |  CPT-4 |



