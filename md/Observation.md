###
# O1: Find a Observation from a keyword

| This query enables the search of LOINC and UCUM descriptions that are used in the observation domain of the vocabulary by keyword.
It does not require prior knowledge of where in the logic of the vocabularies the entity is situated.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword |  'LDL' |  Yes | Keyword search is case insensitive, and spaces and dashes are excluded from the search |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to run a search of the Observation domain for keyword 'LDL'. The input parameters are highlighted in  **blue**.SELECT  T.Entity\_Concept\_Id,        T.Entity\_Name,        T.Entity\_Code,        T.Entity\_Type,        T.Entity\_concept\_class\_id,        T.Entity\_vocabulary\_id,        T.Entity\_vocabulary\_nameFROM   (       SELECT  C.concept\_id       Entity\_Concept\_Id,               C.concept\_name     Entity\_Name,               C.concept\_code     Entity\_Code,               'Concept'          Entity\_Type,               C.concept\_class\_id    Entity\_concept\_class\_id,               C.vocabulary\_id    Entity\_vocabulary\_id,               V.vocabulary\_name  Entity\_vocabulary\_name,               C.valid\_start\_date,               C.valid\_end\_date       FROM    concept         C,                vocabulary      V       WHERE  C.vocabulary\_id IN ('LOINC', 'UCUM')       AND    C.concept\_class\_id IS NOT NULL       AND    C.standard\_concept = 'S'       AND    C.vocabulary\_id = V.vocabulary\_id       ) TWHERE  REGEXP\_INSTR(LOWER(REPLACE(REPLACE(T.Entity\_Name, ' ', ''), '-', '')),              LOWER(REPLACE(REPLACE( **'LDL'** , ' ', ''), '-', ''))) > 0AND     **sysdate** BETWEEN T.valid\_start\_date AND T.valid\_end\_date   **Output:**
Output field list

| ** Field** | ** Description** |
| --- | --- |
|  Entity\_Concept\_ID | Concept ID of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Name | Concept name of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Code | Concept code of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Type | Type of entity with keyword match (consistent with other keyword search queries elsewhere). Since procedure search is restricted to standard concepts and synonyms, the entity type is always set to 'Concept' |
| --- | --- |
|  Entity\_Concept\_Class | Concept class of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Vocabulary\_ID | Vocabulary the concept with string match is derived from |
| --- | --- |
|  Entity\_Vocabulary\_Name | Name of the vocabulary the concept code is derived from |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Entity\_Concept\_ID |  3033200 |
| --- | --- |
|  Entity\_Name |  Cholesterol in LDL [Mass or Moles/volume] in Serum or Plasma |
| --- | --- |
|  Entity\_Code |  35198-1 |
| --- | --- |
|  Entity\_Type |  Concept |
| --- | --- |
|  Entity\_Concept\_Class |  LOINC Code |
| --- | --- |
|  Entity\_Vocabulary\_ID |  LOINC |
| --- | --- |
|  Entity\_Vocabulary\_Name |  Logical Observation Identifiers Names and Codes (Regenstrief Institute) |
| --- | --- |

  |
| --- |
*-*-*-*-*
