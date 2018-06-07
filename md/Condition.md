###
# C01: Find condition by concept ID

| Find condition by condition ID is the lookup for obtaining condition or disease concept details associated with a concept identifier. This query is a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier, either SNOMED-CT clinical finding or MedDRA.
This query is equivalent to  [G01](http://vocabqueries.omop.org/general-queries/g1), but if the concept is not in the condition domain the query still returns the concept details with the Is\_Disease\_Concept\_Flag field set to 'No'.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | Concept Identifier for 'GI - Gastrointestinal haemorrhage' |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to run a search for specific disease concept ID. The input parameters are highlighted in  **blue**.SELECT   C.concept\_id Condition\_concept\_id,   C.concept\_name Condition\_concept\_name,   C.concept\_code Condition\_concept\_code,   C.concept\_class\_id Condition\_concept\_class,  C.vocabulary\_id Condition\_concept\_vocab\_ID,   V.vocabulary\_name Condition\_concept\_vocab\_name,   CASE C.vocabulary\_id     WHEN 'SNOMED' THEN CASE lower(C.concept\_class\_id)            WHEN 'clinical finding' THEN 'Yes' ELSE 'No' END         WHEN 'MedDRA' THEN 'Yes'        ELSE 'No'   END Is\_Disease\_Concept\_flag FROM concept C, vocabulary V WHERE   C.concept\_id = **192671** AND   C.vocabulary\_id = V.vocabulary\_id AND   **sysdate** BETWEEN valid\_start\_date AND valid\_end\_date; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Condition\_Concept\_ID |  Condition concept Identifier entered as input |
| --- | --- |
|  Condition\_Concept\_Name |  Name of the standard condition concept |
| --- | --- |
|  Condition\_Concept\_Code |  Concept code of the standard concept in the source vocabulary |
| --- | --- |
|  Condition\_Concept\_Class |  Concept class of standard vocabulary concept |
| --- | --- |
|  Condition\_Concept\_Vocab\_ID  |  Vocabulary the standard concept is derived from as vocabulary code |
| --- | --- |
|  Condition\_Concept\_Vocab\_Name |  Name of the vocabulary the standard concept is derived from |
| --- | --- |
|  Is\_Disease\_Concept\_Flag |  Flag indicating whether the Concept ID belongs to a disease concept. 'Yes' if disease concept, 'No' if not a disease concept |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Condition\_Concept\_ID |  192671 |
| --- | --- |
|  Condition\_Concept\_Name |  GI - Gastrointestinal hemorrhage |
| --- | --- |
|  Condition\_Concept\_Code |  74474003 |
| --- | --- |
|  Condition\_Concept\_Class |  Clinical finding |
| --- | --- |
|  Condition\_Concept\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Condition\_Concept\_Vocab\_Name | Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |
|  Is\_Disease\_Concept\_Flag |  Yes |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C02: Find a condition by keyword

| This query enables search of vocabulary entities by keyword. The query does a search of standard concepts names in the CONDITION domain (SNOMED-CT clinical findings and MedDRA concepts) and their synonyms to return all related concepts.
It does not require prior knowledge of where in the logic of the vocabularies the entity is situated.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword |  'myocardial infarction' |  Yes | Keyword should be placed in a single quote |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to run a search of the Condition domain for keyword 'myocardial infarction'. The input parameters are highlighted in  **blue**.SELECT   T.Entity\_Concept\_Id,   T.Entity\_Name,   T.Entity\_Code,   T.Entity\_Type,   T.Entity\_concept\_class,   T.Entity\_vocabulary\_id,   T.Entity\_vocabulary\_name FROM (   SELECT     C.concept\_id Entity\_Concept\_Id,         C.concept\_name Entity\_Name,         C.CONCEPT\_CODE Entity\_Code,         'Concept' Entity\_Type,         C.concept\_class\_id Entity\_concept\_class,         C.vocabulary\_id Entity\_vocabulary\_id,         V.vocabulary\_name Entity\_vocabulary\_name,         NULL Entity\_Mapping\_Type,         C.valid\_start\_date,         C.valid\_end\_date   FROM concept C   JOIN vocabulary V ON C.vocabulary\_id = V.vocabulary\_id   LEFT JOIN concept\_synonym S ON C.concept\_id = S.concept\_id   WHERE     (C.vocabulary\_id IN ('SNOMED', 'MedDRA') OR LOWER(C.concept\_class\_id) = 'clinical finding' ) AND         C.concept\_class\_id IS NOT NULL AND         ( LOWER(C.concept\_name) like **'%myocardial infarction%'** OR          LOWER(S.concept\_synonym\_name) like **'%myocardial infarction%'** )   ) TWHERE **sysdate** BETWEEN valid\_start\_date AND valid\_end\_date ORDER BY 6,2;               **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Entity\_Concept\_ID |  Concept ID of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Name |  Concept name of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Code |  Concept code of entity with string match on name or synonym concept  |
| --- | --- |
|  Entity\_Type |  Concept type |
| --- | --- |
|  Entity\_Concept\_Class |  Concept class of entity with string match on name or synonym concept |
| --- | --- |
|  Entity\_Vocabulary\_ID |  ID of vocabulary associated with the concept |
| --- | --- |
|  Entity\_Vocabulary\_Name |  Name of the vocabulary associated with the concept |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Entity\_Concept\_ID |  35205180 |
| --- | --- |
|  Entity\_Name |  Acute myocardial infarction |
| --- | --- |
|  Entity\_Code |  10000891 |
| --- | --- |
|  Entity\_Type |  Concept |
| --- | --- |
|  Entity\_Concept\_Class |  Preferred Term |
| --- | --- |
|  Entity\_Vocabulary\_ID |  MedDRA |
| --- | --- |
|  Entity\_Vocabulary\_Name |  Medical Dictionary for Regulatory Activities (MSSO) |
| --- | --- |


This is a comprehensive query to find relevant terms in the vocabulary. To constrain, additional clauses can be added to the query. However, it is recommended to do a filtering after the result set is produced to avoid syntactical mistakes.
The query only returns concepts that are part of the Standard Vocabulary, ie. they have concept level that is not 0. If all concepts are needed, including the non-standard ones, the clause in the query restricting the concept level and concept class can be commented out. |
| --- |
*-*-*-*-*
###
# C03: Translate a SNOMED-CT concept into a MedDRA concept

| This query accepts a SNOMED-CT concept ID as input and returns details of the equivalent MedDRA concepts.

The relationships in the vocabulary associate MedDRA 'Preferred Term' to SNOMED-CT 'clinical findings'. The respective hierarchy for MedDRA and SNOMED-CT can be used to traverse up and down the hierarchy of each of these individual vocabularies.
Also, not all SNOMED-CT clinical findings are mapped to a MedDRA concept in the vocabulary.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  312327 |  Yes | Concept Identifier for 'Acute myocardial infarction' |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list MedDRA equivalents for SNOMED-CT concept whose concept ID is entered as input. Sample parameter substitution is highlighted in  **blue** :SELECT        D.concept\_id Snomed\_concept\_id,                D.concept\_name Snomed\_concept\_name,                D.concept\_code Snomed\_concept\_code,                D.concept\_class\_id Snomed\_concept\_class,                CR.relationship\_id,                RT.relationship\_name,                A.Concept\_id MedDRA\_concept\_id,                A.Concept\_name MedDRA\_concept\_name,                A.Concept\_code MedDRA\_concept\_code,                A.Concept\_class\_id MedDRA\_concept\_class FROM concept\_relationship CR, concept A, concept D, relationship RT WHERE CR.relationship\_id =  'SNOMED - MedDRA eq'AND CR.concept\_id\_2 = A.concept\_id AND CR.concept\_id\_1 = **312327** AND CR.concept\_id\_1 = D.concept\_id AND CR.relationship\_id = RT.relationship\_id AND **sysdate** BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  SNOMED-CT\_Concept\_ID |  Concept ID of SNOMED-CT concept entered as input |
| --- | --- |
|  SNOMED-CT\_Concept\_Name |  Name of SNOMED-CT concept |
| --- | --- |
|  SNOMED-CT\_Concept\_Code |  Concept code of SNOMED-CT concept |
| --- | --- |
|  SNOMED-CT\_Concept\_Class |  Concept class of SNOMED-CT concept |
| --- | --- |
|  Relationship\_ID |  Identifier for the type of relationship |
| --- | --- |
|  Relationship\_Name |  Description of the type of relationship |
| --- | --- |
|  MedDRA\_Concept\_ID |  Concept ID of matching MedDRA concept |
| --- | --- |
|  MedDRA\_Concept\_Name |  Concept name of matching MedDRA concept |
| --- | --- |
|  MedDRA\_Concept\_Code |  Concept code of matching MedDRA concept |
| --- | --- |
|  MedDRA\_Concept\_Class |  Concept class of matching MedDRA concept |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  SNOMED-CT\_Concept\_ID |  312327 |
| --- | --- |
|  SNOMED-CT\_Concept\_Name |  Acute myocardial infarction |
| --- | --- |
|  SNOMED-CT\_Concept\_Code |  57054005 |
| --- | --- |
|  SNOMED-CT\_Concept\_Class |  Clinical finding |
| --- | --- |
|  Relationship\_ID |  SNOMED - MedDRA eq |
| --- | --- |
|  Relationship\_Name |  SNOMED-CT to MedDRA equivalent (OMOP) |
| --- | --- |
|  MedDRA\_Concept\_ID |  35205180 |
| --- | --- |
|  MedDRA\_Concept\_Name |  Acute myocardial infarction |
| --- | --- |
|  MedDRA\_Concept\_Code |  10000891 |
| --- | --- |
|  MedDRA\_Concept\_Class |  Preferred Term |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C04: Translate a MedDRA concept into a SNOMED-CT concept

| This query accepts a MedDRA concept ID as input and returns details of the equivalent SNOMED-CT concepts.
The existing relationships in the vocabulary associate MedDRA 'Preferred Term' to SNOMED-CT 'clinical findings'. The respective hierarchy for MedDRA and SNOMED-CT can be used to traverse up and down the hierarchy of each of these individual vocabularies.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  MedDRA Concept ID |  35205180 |  Yes | Concept Identifier for 'Acute myocardial infarction' |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list all MedDRA concepts that have SNOMED-CT equivalents. Sample parameter substitution is highlighted in  **blue**.SELECT        D.concept\_id MedDRA\_concept\_id,                D.concept\_name MedDRA\_concept\_name,                D.concept\_code MedDRA\_concept\_code,                D.concept\_class\_id MedDRA\_concept\_class,                CR.relationship\_id,                RT.relationship\_name,                A.concept\_id Snomed\_concept\_id,                A.concept\_name Snomed\_concept\_name,                A.concept\_code Snomed\_concept\_code,                A.concept\_class\_id Snomed\_concept\_class FROM concept\_relationship CR, concept A, concept D, relationship RT WHERE CR.relationship\_id = 'MedDRA to SNOMED equivalent (OMOP)'AND CR.concept\_id\_2 = A.concept\_id AND CR.concept\_id\_1 = **35205180**  AND CR.concept\_id\_1 = D.concept\_id AND CR.relationship\_id = RT.relationship\_id AND **sysdate** BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  MedDRA\_Concept\_ID |  Concept ID of MedDRA concept entered as input |
| --- | --- |
|  MedDRA\_Concept\_Name |  Concept name of MedDRA concept |
| --- | --- |
|  MedDRA\_Concept\_Code |  Concept code of MedDRA concept |
| --- | --- |
|  MedDRA\_Concept\_Class |  Concept class of MedDRA concept |
| --- | --- |
|  Relationship\_ID |  Identifier for the type of relationship |
| --- | --- |
|  Relationship\_Name |  Description of the type of relationship |
| --- | --- |
|  SNOMED-CT\_Concept\_ID |  Concept ID of matching SNOMED-CT concept |
| --- | --- |
|  SNOMED-CT\_Concept\_Name |  Name of matching SNOMED-CT concept |
| --- | --- |
|  SNOMED-CT\_Concept\_Code |  Concept Code of matching SNOMED-CT concept |
| --- | --- |
|  SNOMED-CT\_Concept\_Class |  Concept class of matching SNOMED-CT concept |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  MedDRA\_Concept\_ID |  35205180 |
| --- | --- |
|  MedDRA\_Concept\_Name |  Acute myocardial infarction |
| --- | --- |
|  MedDRA\_Concept\_Code |  10000891 |
| --- | --- |
|  MedDRA\_Concept\_Class |  Preferred Term |
| --- | --- |
|  Relationship\_ID |  MedDRA to SNOMED equivalent (OMOP) |
| --- | --- |
|  Relationship\_Name |  MedDRA to SNOMED-CT equivalent (OMOP) |
| --- | --- |
|  SNOMED-CT\_Concept\_ID |  312327 |
| --- | --- |
|  SNOMED-CT\_Concept\_Name |  Acute myocardial infarction |
| --- | --- |
|  SNOMED-CT\_Concept\_Code |  57054005 |
| --- | --- |
|  SNOMED-CT\_Concept\_Class |  Clinical finding |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C05: Translate a source code to condition concepts

| This query enables to search all Standard SNOMED-CT concepts that are mapped to a condition (disease) source code. It can be used to translate e.g. ICD-9-CM, ICD-10-CM or Read codes to SNOMED-CT.
Source codes are not unique across different source vocabularies, therefore the source vocabulary ID must also be provided.
The following source vocabularies have condition/disease codes that map to SNOMED-CT concepts:
-  ICD-9-CM,    Vocabulary\_id=2
- Read,            Vocabulary\_id=17
- OXMIS,         Vocabulary\_id=18
- ICD-10-CM,   Vocabulary\_id=34

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Source Code List |  '070.0' |  Yes | Source codes are alphanumeric and need to be entered as a string enclosed by a single quote. If more than one source code needs to be entered an IN clause or a JOIN can be used. |
| --- | --- | --- | --- |
|  Source Vocabulary ID |  2 |  Yes | The source vocabulary is mandatory, because the source ID is not unique across different vocabularies. |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list SNOMED-CT concepts that a set of mapped codes entered as input map to. The sample parameter substitutions are highlighted in  **blue** :set search\_path to full\_201612\_omop\_v5; SELECT DISTINCT   c1.concept\_code,   c1.concept\_name,   c1.vocabulary\_id source\_vocabulary\_id,   VS.vocabulary\_name source\_vocabulary\_description,   C1.domain\_id,   C2.concept\_id target\_concept\_id,   C2.concept\_name target\_Concept\_Name,   C2.concept\_code target\_Concept\_Code,   C2.concept\_class\_id target\_Concept\_Class,   C2.vocabulary\_id target\_Concept\_Vocab\_ID,   VT.vocabulary\_name target\_Concept\_Vocab\_Name FROM   concept\_relationship cr,   concept c1,   concept c2,  vocabulary VS,   vocabulary VT WHERE   cr.concept\_id\_1 = c1.concept\_id AND  cr.relationship\_id = 'Maps to' AND  cr.concept\_id\_2 = c2.concept\_id AND  c1.vocabulary\_id = VS.vocabulary\_id AND   c1.domain\_id = 'Condition' AND   c2.vocabulary\_id = VT.vocabulary\_id AND   c1.concept\_code IN ( **'070.0'**                                           ) AND c2.vocabulary\_id = **'SNOMED'**                                          AND **sysdate**                                           BETWEEN c1.valid\_start\_date AND c1.valid\_end\_date;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Source\_Code |  Source code for the disease entered as input |
| --- | --- |
|  Source\_Code\_Description |  Description of the source code entered as input |
| --- | --- |
|  Source\_Vocabulary\_ID |  Vocabulary the disease source code is derived from as vocabulary ID |
| --- | --- |
|  Source\_Vocabulary\_Description |  Name of the vocabulary the disease source code is derived from |
| --- | --- |
|  Mapping\_Type |  Type of mapping or mapping domain, from source code to target concept. Example Condition, Procedure, Drug etc. |
| --- | --- |
|  Target\_Concept\_ID |  Concept ID of the target condition concept mapped to the disease source code |
| --- | --- |
|  Target\_Concept\_Name |  Name of the target condition concept mapped to the disease source code |
| --- | --- |
|  Target\_Concept\_Code |  Concept code of the target condition concept mapped to the disease source code |
| --- | --- |
|  Target\_Concept\_Class |  Concept class of the target condition concept mapped to the disease source code |
| --- | --- |
|  Target\_Concept\_Vocab\_ID |  Vocabulary the target condition concept is derived from as vocabulary code |
| --- | --- |
|  Target\_Concept\_Vocab\_Name |  Name of the vocabulary the condition concept is derived from |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Source\_Code |  070.0 |
| --- | --- |
|  Source\_Code\_Description |  Viral hepatitis |
| --- | --- |
|  Source\_Vocabulary\_ID |  ICD9CM |
| --- | --- |
|  Source\_Vocabulary\_Description |  International Classification of Diseases, Ninth Revision, Clinical Modification, Volume 1 and 2 (NCHS) |
| --- | --- |
|  Mapping\_Type |  CONDITION |
| --- | --- |
|  Target\_Concept\_ID |  4291005 |
| --- | --- |
|  Target\_Concept\_Name |  VH - Viral hepatitis |
| --- | --- |
|  Target\_Concept\_Code |  3738000 |
| --- | --- |
|  Target\_Concept\_Class |  Clinical finding |
| --- | --- |
|  Target\_Concept\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Target\_Concept\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C06: Translate a given condition to source codes

| This query allows to search all source codes that are mapped to a SNOMED-CT clinical finding concept. It can be used to translate SNOMED-CT to ICD-9-CM, ICD-10-CM, Read or OXMIS codes.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  312327 |  Yes | Concept IDs are numeric. If more than one concept code needs to be translated an IN clause or a JOIN can be used. |
| --- | --- | --- | --- |
|  Source Vocabulary ID |  2 |  Yes | 2 represents ICD9-CM |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:** The following is a sample run of the query to list all source codes that map to a SNOMED-CT concept entered as input. The sample parameter substitutions are highlighted in  **blue**.SELECT DISTINCT  c1.concept\_code,  c1.concept\_name,  c1.vocabulary\_id source\_vocabulary\_id,  VS.vocabulary\_name source\_vocabulary\_description,  C1.domain\_id,  C2.concept\_id target\_concept\_id,  C2.concept\_name target\_Concept\_Name,  C2.concept\_code target\_Concept\_Code,  C2.concept\_class\_id target\_Concept\_Class,  C2.vocabulary\_id target\_Concept\_Vocab\_ID,  VT.vocabulary\_name target\_Concept\_Vocab\_NameFROM  concept\_relationship cr,  concept c1,  concept c2,  vocabulary VS,  vocabulary VTWHERE  cr.concept\_id\_1 = c1.concept\_id AND  cr.relationship\_id = 'Maps to' AND  cr.concept\_id\_2 = c2.concept\_id AND  c1.vocabulary\_id = VS.vocabulary\_id AND  c1.domain\_id = 'Condition' AND  c2.vocabulary\_id = VT.vocabulary\_id AND  c1.concept\_id = **312327**                                              AND c1.vocabulary\_id = **'SNOMED'  **                                         AND **sysdate**                                           BETWEEN c2.valid\_start\_date AND c2.valid\_end\_date;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Source\_Code |  Source code for the disease entered as input |
| --- | --- |
|  Source\_Code\_Description |  Description of the source code entered as input |
| --- | --- |
|  Source\_Vocabulary\_ID |  Vocabulary the disease source code is derived from as vocabulary code |
| --- | --- |
|  Source\_Vocabulary\_Description |  Name of the vocabulary the disease source code is derived from |
| --- | --- |
|  Mapping\_Type |  Type of mapping or mapping domain, from source code to target concept. Example Condition, Procedure, Drug etc. |
| --- | --- |
|  Target\_Concept\_ID |  Concept ID of the SNOMED-CT concept entered as input |
| --- | --- |
|  Target\_Concept\_Name |  Name of the SNOMED-CT concept entered as input |
| --- | --- |
|  Target\_Concept\_Code |  Concept code of the SNOMED-CT concept entered as input |
| --- | --- |
|  Target\_Concept\_Class |  Concept class of the SNOMED-CT concept entered as input |
| --- | --- |
|  Target\_Concept\_Vocab\_ID |  Vocabulary of concept entered as input is derived from, as vocabulary ID |
| --- | --- |
|  Target\_Concept\_Vocab\_Name |  Name of vocabulary the concept entered as input is derived from |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Source\_Code |  410.92 |
| --- | --- |
|  Source\_Code\_Description |  Acute myocardial infarction, unspecified site, subsequent episode of care |
| --- | --- |
|  Source\_Vocabulary\_ID |  SNOMED |
| --- | --- |
|  Source\_Vocabulary\_Description |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |
|  Mapping\_Type |  CONDITION |
| --- | --- |
|  Target\_Concept\_ID |  312327 |
| --- | --- |
|  Target\_Concept\_Name |  Acute myocardial infarction |
| --- | --- |
|  Target\_Concept\_Code |  57054005 |
| --- | --- |
|  Target\_Concept\_Class |  Clinical finding |
| --- | --- |
|  Target\_Concept\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Target\_Concept\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C07: Find a pathogen by keyword

| This query enables a search of all pathogens using a keyword as input. The resulting concepts could be used in query  [C09](http://vocabqueries.omop.org/condition-queries/c9) to identify diseases caused by a certain pathogen.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Trypanosoma' |  Yes | Keyword should be placed in a single quote |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list all pathogens specified using a keyword as input. The sample parameter substitutions are highlighted in  **blue**.SELECT   C.concept\_id Pathogen\_Concept\_ID,   C.concept\_name Pathogen\_Concept\_Name,   C.concept\_code Pathogen\_concept\_code,   C.concept\_class\_id Pathogen\_concept\_class,   C.standard\_concept Pathogen\_Standard\_Concept,   C.vocabulary\_id Pathogen\_Concept\_Vocab\_ID,   V.vocabulary\_name Pathogen\_Concept\_Vocab\_Name FROM   concept C,   vocabulary VWHERE   LOWER(C.concept\_class\_id) = 'organism' AND   LOWER(C.concept\_name) like **'%trypanosoma%'**                                AND C.vocabulary\_id = V.vocabulary\_id AND **sysdate**                                        BETWEEN C.valid\_start\_date AND C.valid\_end\_date;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Pathogen\_Concept\_ID |  Concept ID of SNOMED-CT pathogen concept |
| --- | --- |
|  Pathogen\_Concept\_Name |  Name of SNOMED-CT pathogen concept with keyword entered as input |
| --- | --- |
|  Pathogen\_Concept\_Code |  Concept Code of SNOMED-CT pathogen concept |
| --- | --- |
|  Pathogen\_Concept\_Class |  Concept class of SNOMED-CT pathogen concept |
| --- | --- |
|  Pathogen\_Standard\_Concept |  Indicator of standard concept of SNOMED-CT pathogen concept |
| --- | --- |
|  Pathogen\_Vocab\_ID |  Vocabulary ID of the vocabulary from which the pathogen concept is derived from (1 for SNOMED-CT) |
| --- | --- |
|  Pathogen\_Vocab\_Name |  Name of the vocabulary from which the pathogen concept is derived from (SNOMED-CT) |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Pathogen\_Concept\_ID |  4085768 |
| --- | --- |
|  Pathogen\_Concept\_Name |  Trypanosoma brucei |
| --- | --- |
|  Pathogen\_Concept\_Code |  243659009 |
| --- | --- |
|  Pathogen\_Concept\_Class |  Organism |
| --- | --- |
| Pathogen\_Standard\_Concept |  S |
| --- | --- |
|  Pathogen\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Pathogen\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C08: Find a disease causing agent by keyword

| This query enables a search of various agents that can cause disease by keyword as input. Apart from pathogens (see query  [C07](http://vocabqueries.omop.org/condition-queries/c7)), these agents can be SNOMED-CT concepts of the following classes:
- Pharmaceutical / biologic product
- Physical object
- Special concept
- Event
- Physical force
- Substance
The resulting concepts could be used in query  [C09](http://vocabqueries.omop.org/condition-queries/c9) to identify diseases caused by the agent.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Radiation' |  Yes | Keyword should be placed in a single quote |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list all pathogens specified using a keyword as input. The sample parameter substitutions are highlighted in  **blue**.SELECT  C.concept\_id Agent\_Concept\_ID,  C.concept\_name Agent\_Concept\_Name,  C.concept\_code Agent\_concept\_code,  C.concept\_class\_id Agent\_concept\_class,  C.standard\_concept Agent\_Standard\_Concept,  C.vocabulary\_id Agent\_Concept\_Vocab\_ID,  V.vocabulary\_name Agent\_Concept\_Vocab\_NameFROM  concept C,  vocabulary VWHERE  LOWER(C.concept\_class\_id) in ('pharmaceutical / biologic product','physical object',                                'special concept','event', 'physical force','substance') AND  LOWER(C.concept\_name) like **'%radiation%'                                  ** AND C.vocabulary\_id = V.vocabulary\_id AND **sysdate**                                        BETWEEN C.valid\_start\_date AND C.valid\_end\_date;    **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Agent\_Concept\_ID |  Concept ID of SNOMED-CT agent concept |
| --- | --- |
|  Agent\_Concept\_Name |  Name of SNOMED-CT concept |
| --- | --- |
|  Agent\_Concept\_Code |  Concept Code of SNOMED-CT concept |
| --- | --- |
|  Agent\_Concept\_Class |  Concept class of SNOMED-CT concept |
| --- | --- |
|  Agent\_Standard\_Concept |  Indicator of standard concept for SNOMED-CT concept |
| --- | --- |
|  Agent\_Vocab\_ID |  Vocabulary ID of the vocabulary from which the agent concept is derived from (1 for SNOMED-CT) |
| --- | --- |
|  Agent\_Vocab\_Name |  Name of the vocabulary from which the agent concept is derived from (SNOMED-CT) |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Agent\_Concept\_ID |  4220084 |
| --- | --- |
|  Agent\_Concept\_Name |  Radiation |
| --- | --- |
|  Agent\_Concept\_Code |  82107009 |
| --- | --- |
|  Agent\_Concept\_Class |  Physical force |
| --- | --- |
|  Agent\_Standard\_Concept |  S |
| --- | --- |
|  Agent\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Agent\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C09: Find all SNOMED-CT condition concepts that can be caused by a given pathogen or causative agent

| This query accepts a SNOMED-CT pathogen ID as input and returns all conditions caused by the pathogen or disease causing agent identified using queries  [C07](http://vocabqueries.omop.org/condition-queries/c7) or  [C08](http://vocabqueries.omop.org/condition-queries/c8).

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  4248851 |  Yes | Concept Identifier for 'Treponema pallidum' |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list conditions caused by pathogen or causative agent. Sample parameter substitution is highlighted in  **blue**.SELECT   A.concept\_Id Condition\_ID,   A.concept\_Name Condition\_name,   A.concept\_Code Condition\_code,   A.concept\_Class\_id Condition\_class,   A.vocabulary\_id Condition\_vocab\_ID,   VA.vocabulary\_name Condition\_vocab\_name,   D.concept\_Id Causative\_agent\_ID,   D.concept\_Name Causative\_agent\_Name,   D.concept\_Code Causative\_agent\_Code,   D.concept\_Class\_id Causative\_agent\_Class,   D.vocabulary\_id Causative\_agent\_vocab\_ID,   VS.vocabulary\_name Causative\_agent\_vocab\_name FROM   concept\_relationship CR,   concept A,   concept D,   vocabulary VA,   vocabulary VSWHERE   CR.relationship\_ID = 'Has causative agent' AND   CR.concept\_id\_1 = A.concept\_id AND   A.vocabulary\_id = VA.vocabulary\_id AND   CR.concept\_id\_2 = D.concept\_id AND   D.concept\_id = **4248851**                                               AND D.vocabulary\_id = VS.vocabulary\_id AND **sysdate**                                               BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date;     **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Condition\_ID |  Condition concept Identifier |
| --- | --- |
|  Condition\_Name |  Name of the standard condition concept |
| --- | --- |
|  Condition\_Code |  Concept code of the standard concept in the source vocabulary |
| --- | --- |
|  Condition\_Class |  Concept class of standard vocabulary concept |
| --- | --- |
|  Condition\_Vocab\_ID |  Vocabulary the standard concept is derived from as vocabulary ID |
| --- | --- |
|  Condition\_Vocab\_Name |  Name of the vocabulary the standard concept is derived from |
| --- | --- |
|  Causative\_Agent\_ID |  Pathogen concept ID entered as input |
| --- | --- |
|  Causative\_Agent\_Name |  Pathogen Name |
| --- | --- |
|  Causative\_Agent\_Code |  Concept Code of pathogen concept |
| --- | --- |
|  Causative\_Agent\_Class |  Concept Class of pathogen concept |
| --- | --- |
|  Causative\_Agent\_Vocab\_ID |  Vocabulary the pathogen concept is derived from as vocabulary ID |
| --- | --- |
|  Causative\_Agent\_Vocab\_Name |  Name of the vocabulary the pathogen concept is derived from |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Condition\_ID |  4326735 |
| --- | --- |
|  Condition\_Name |  Spastic spinal syphilitic paralysis |
| --- | --- |
|  Condition\_Code |  75299005 |
| --- | --- |
|  Condition\_Class |  Clinical finding |
| --- | --- |
|  Condition\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Condition\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |
|  Causative\_Agent\_ID |  4248851 |
| --- | --- |
|  Causative\_Agent\_Name |  Treponema pallidum |
| --- | --- |
|  Causative\_Agent\_Code |  72904005 |
| --- | --- |
|  Causative\_Agent\_Class |  Organism |
| --- | --- |
|  Causative\_Agent\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Causative\_Agent\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C10: Find an anatomical site by keyword

| This query enables a search of all anatomical sites using a keyword entered as input. The resulting concepts could be used in query  [C11](http://vocabqueries.omop.org/condition-queries/c11) to identify diseases occurring at a certain anatomical site.

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword for pathogen |  'Epiglottis' |  Yes | Keyword should be placed in a single quote |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query to list all anatomical site concept IDs specified using a keyword as input. The sample parameter substitutions are highlighted in  **blue**.SELECT   C.concept\_id Anatomical\_site\_ID,   C.concept\_name Anatomical\_site\_Name,   C.concept\_code Anatomical\_site\_Code,   C.concept\_class\_id Anatomical\_site\_Class,   C.standard\_concept Anatomical\_standard\_concept,   C.vocabulary\_id Anatomical\_site\_Vocab\_ID,   V.vocabulary\_name Anatomical\_site\_Vocab\_Name FROM   concept C,   vocabulary V WHERE   LOWER(C.concept\_class\_id) = 'body structure' AND   LOWER(C.concept\_name) like **'%epiglottis%'                                  ** AND C.vocabulary\_id = V.vocabulary\_id AND **sysdate**                                          BETWEEN C.valid\_start\_date AND C.valid\_end\_date;  **Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Anatomical\_site\_ID |  Concept ID of SNOMED-CT anatomical site concept |
| --- | --- |
|  Anatomical\_site\_Name |  Name of SNOMED-CT anatomical site concept entered as input |
| --- | --- |
|  Anatomical\_site\_Code |  Concept Code of SNOMED-CT anatomical site concept |
| --- | --- |
|  Anatomical\_site\_Class |  Concept class of SNOMED-CT anatomical site |
| --- | --- |
|  Anatomical\_standard\_concept |  Indicator of standard concept for SNOMED-CT anatomical site |
| --- | --- |
|  Anatomical\_site\_vocab\_ID |  Vocabulary ID of the vocabulary from which the anatomical site  concept is derived from |
| --- | --- |
|  Anatomical\_site\_vocab\_name |  Name of the vocabulary from which the anatomical site concept is derived from |
| --- | --- |


Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Anatomical\_site\_ID |  4103720 |
| --- | --- |
|  Anatomical\_site\_Name |  Posterior epiglottis |
| --- | --- |
|  Anatomical\_site\_Code |  2894003 |
| --- | --- |
|  Anatomical\_site\_Class |  Body structure |
| --- | --- |
|  Anatomical\_standard\_concept |  S |
| --- | --- |
|  Anatomical\_site\_vocab\_ID |  SNOMED 1 |
| --- | --- |
|  Anatomical\_site\_vocab\_name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
###
# C11: Find all SNOMED-CT condition concepts that are occurring at an anatomical site

| This query accepts a SNOMED-CT body structure ID as input and returns all conditions occurring in the anatomical site, which can be identified using query  [C10](http://vocabqueries.omop.org/condition-queries/c10). **Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  SNOMED-CT Concept ID |  4103720 |  Yes | Concept Identifier for 'Posterior epiglottis' |
| --- | --- | --- | --- |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |
| --- | --- | --- | --- |

  **Sample query run:** The following is a sample run of the query to list conditions located in the anatomical site. Sample parameter substitution is highlighted in  **blue** :SELECT  A.concept\_Id Condition\_ID,  A.concept\_Name Condition\_name,  A.concept\_Code Condition\_code,  A.concept\_Class\_id Condition\_class,  A.vocabulary\_id Condition\_vocab\_ID,  VA.vocabulary\_name Condition\_vocab\_name,  D.concept\_Id Anatomical\_site\_ID,  D.concept\_Name Anatomical\_site\_Name,  D.concept\_Code Anatomical\_site\_Code,  D.concept\_Class\_id Anatomical\_site\_Class,  D.vocabulary\_id Anatomical\_site\_vocab\_ID,  VS.vocabulary\_name Anatomical\_site\_vocab\_nameFROM  concept\_relationship CR,  concept A,  concept D,  vocabulary VA,  vocabulary VSWHERE  CR.relationship\_ID = 'Has finding site' AND  CR.concept\_id\_1 = A.concept\_id AND  A.vocabulary\_id = VA.vocabulary\_id AND  CR.concept\_id\_2 = D.concept\_id AND  D.concept\_id = **4103720**                                             --input  AND D.vocabulary\_id = VS.vocabulary\_id AND **sysdate**                                             --input  BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date;   **Output:** Output field list:

| ** Field** | ** Description** |
| --- | --- |
|  Condition\_ID |  Condition concept Identifier |
| --- | --- |
|  Condition\_Name |  Name of the standard condition concept |
| --- | --- |
|  Condition\_Code |  Concept code of the standard concept in the source vocabulary |
| --- | --- |
|  Condition\_Class |  Concept class of standard vocabulary concept |
| --- | --- |
|  Condition\_Vocab\_ID |  Vocabulary the standard concept is derived from as vocabulary ID |
| --- | --- |
|  Condition\_Vocab\_Name |  Name of the vocabulary the standard concept is derived from |
| --- | --- |
|  Anatomical\_Site\_ID |  Body Structure ID entered as input |
| --- | --- |
|  Anatomical\_Site\_Name |  Body Structure Name |
| --- | --- |
|  Anatomical\_Site\_Code |  Concept Code of the body structure concept |
| --- | --- |
|  Anatomical\_Site\_Class |  Concept Class of the body structure concept |
| --- | --- |
|  Anatomical\_Site\_Vocab\_ID |  Vocabulary the body structure concept is derived from as vocabulary code |
| --- | --- |
|  Anatomical\_Site\_Vocab\_Name |  Name of the vocabulary the body structure concept is derived from |
| --- | --- |

 Sample output record:

| ** Field** | ** Value** |
| --- | --- |
|  Condition\_ID |  4054522 |
| --- | --- |
|  Condition\_Name |  Neoplasm of laryngeal surface of epiglottis |
| --- | --- |
|  Condition\_Code |  126700009 |
| --- | --- |
|  Condition\_Class |  Clinical finding |
| --- | --- |
|  Condition\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Condition\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |
|  Anatomical\_Site\_ID |  4103720 |
| --- | --- |
|  Anatomical\_Site\_Name |  Posterior epiglottis |
| --- | --- |
|  Anatomical\_Site\_Code |  2894003 |
| --- | --- |
|  Anatomical\_Site\_Class |  Body structure |
| --- | --- |
|  Anatomical\_Site\_Vocab\_ID |  SNOMED |
| --- | --- |
|  Anatomical\_Site\_Vocab\_Name |  Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO) |
| --- | --- |

  |
| --- |
*-*-*-*-*
