### P02: Find a procedure from a keyword.

This query enables search of procedure domain of the vocabulary by keyword. The query does a search of standard concepts names in the PROCEDURE domain (SNOMED-CT procedures, ICD9 procedures, CPT procedures and HCPCS procedures) and their synonyms to return all related concepts.

This is a comprehensive query to find relevant terms in the vocabulary. It does not require prior knowledge of where in the logic of the vocabularies the entity is situated. To constrain, additional clauses can be added to the query. However, it is recommended to do a filtering after the result set is produced to avoid syntactical mistakes.
The query only returns concepts that are part of the Standard Vocabulary, ie. they have concept level that is not 0. If all concepts are needed, including the non-standard ones, the clause in the query restricting the concept level and concept class can be commented out.

**Sample query:**

SELECT C.concept\_id         Entity\_Concept\_Id,

       C.concept\_name       Entity\_Name,

       C.concept\_code       Entity\_Code,

       'Concept'            Entity\_Type,

       C.concept\_class\_id      Entity\_concept\_class\_id,

       C.vocabulary\_id      Entity\_vocabulary\_id,

       V.vocabulary\_name    Entity\_vocabulary\_name

FROM   concept   C

   INNER JOIN vocabulary V ON C.vocabulary\_id = V.vocabulary\_id

   LEFT OUTER JOIN concept\_synonym S ON C.concept\_id = S.concept\_id

WHERE  (

              C.vocabulary\_id IN ('ICD9Proc', 'CPT4', 'HCPCS')

       OR     LOWER(C.concept\_class\_id) = 'procedure'

       )

AND    C.concept\_class\_id IS NOT NULL

AND    C.standard\_concept = 'S'

AND    (

            REGEXP\_INSTR(LOWER(C.concept\_name), LOWER('artery bypass')) > 0

       OR   REGEXP\_INSTR(LOWER(S.concept\_synonym\_name), LOWER('artery bypass')) > 0

       )

AND    sysdate BETWEEN C.valid\_start\_date AND C.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword |  'artery bypass' |  Yes | Procedure keyword search |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Entity\_Concept\_ID |  Concept ID of entity with string match on name or synonym concept |
|  Entity\_Name |  Concept name of entity with string match on name or synonym concept |
|  Entity\_Code |  Concept code of entity with string match on name or synonym concept |
|  Entity\_Type |  Type of entity with keyword match (consistent with other keyword search queries elsewhere). Since procedure search is restricted to standard concepts and synonyms, the entity type is always set to 'Concept' |
|  Entity\_Concept\_Class |  Concept class of entity with string match on name or synonym concept |
|  Entity\_Vocabulary\_ID |  Vocabulary the concept with string match is derived from as vocabulary ID |
|  Entity\_Vocabulary\_Name |  Name of the vocabulary the concept with string match is derived from as vocabulary code |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Entity\_Concept\_ID |  2107223 |
|  Entity\_Name |  Coronary artery bypass, using venous graft(s) and arterial graft(s); two venous grafts (List separately in addition to code for primary procedure) |
|  Entity\_Code |  33518 |
|  Entity\_Type |  Concept |
|  Entity\_Concept\_Class |  CPT-4 |
|  Entity\_Vocabulary\_ID |  4 |
|  Entity\_Vocabulary\_Name |  CPT-4 |
*-*-*-*-*
