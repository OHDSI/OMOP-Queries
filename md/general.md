**G01:** Find concept by concept ID

This is the most generic look-up for obtaining concept details associated with a concept identifier. The query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.

**Sample query:**

SELECT C.concept\_id, C.concept\_name, C.concept\_code, C.concept\_class\_id, C.standard\_concept, C.vocabulary\_id, V.vocabulary\_name

FROM concept C, vocabulary V

WHERE C.concept\_id = 192671

AND C.vocabulary\_id = V.vocabulary\_id

AND sysdate BETWEEN valid\_start\_date

AND valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | Concept Identifier for "GI - Gastrointestinal hemorrhage" |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Concept\_ID |  Concept Identifier entered as input |
|  Concept\_Name |  Name of the standard concept |
|  Concept\_Code |  Concept code of the standard concept in the source vocabulary |
|  Concept\_Class |  Concept class of standard vocabulary concept |
|  Concept\_Level |  Level of the concept if defined as part of a hierarchy |
|  Vocabulary\_ID |  Vocabulary the standard concept is derived from as vocabulary code |
|  Vocabulary\_Name |  Name of the vocabulary the standard concept is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Concept\_ID |  192671 |
|  Concept\_Name |  GI - Gastrointestinal haemorrhage |
|  Concept\_Code |  74474003 |
|  Concept\_Class |  Clinical finding |
|  Concept\_Level |  2 |
|  Vocabulary\_ID |  1 |
|  Vocabulary\_Name |  SNOMED-CT |
**G04:** Find synonyms for a given concept

This query extracts all synonyms in the vocabulary for a given Concept ID.

**Sample query:**

SELECT C.concept\_id, S.concept\_synonym\_name

FROM concept C, concept\_synonym S, vocabulary V

WHERE C.concept\_id = 192671

AND C.concept\_id = S.concept\_id

AND C.vocabulary\_id = V.vocabulary\_id

AND sysdate BETWEEN C.valid\_start\_date AND C.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Concept\_ID |  Unique identifier of the concept related to the input concept |
|  Concept\_Synonym\_Name |  Synonym of the concept |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Concept\_ID |  192671 |
|  Concept\_Synonym\_Name |  GI bleeding |
**G05:** Translate a code from a source to a standard vocabulary.

This query enables search of all Standard Vocabulary concepts that are mapped to a code from a specified source vocabulary. It will return all possible concepts that are mapped to it, as well as the target vocabulary. The source code could be obtained using queries G02 or G03.
Note that to unambiguously identify a source code, the vocabulary id has to be provided, as source codes are not unique identifiers across different vocabularies.

**Sample query:**

SELECT DISTINCT

        c1.domain\_id,

        c2.concept\_id         as Concept\_Id,

        c2.concept\_name       as Concept\_Name,

        c2.concept\_code       as Concept\_Code,

        c2.concept\_class\_id      as Concept\_Class,

        c2.vocabulary\_id      as Concept\_Vocabulary\_ID,

                  c2.domain\_id                  as Target\_concept\_Domain

FROM concept\_relationship cr

JOIN concept c1 ON c1.concept\_id = cr.concept\_id\_1

JOIN concept c2 ON c2.concept\_id = cr.concept\_id\_2

WHERE cr.relationship\_id = 'Maps to'

AND c1.concept\_code IN ('070.0')

AND c1.vocabulary\_id = 'ICD9CM'

AND sysdate BETWEEN cr.valid\_start\_date AND cr.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Source Code List |  '070.0' |  Yes |  Source codes are alphanumeric |
|  Source Vocabulary ID |  2 |  Yes | The source vocabulary ID is mandatory, because the source code is not unique across different vocabularies.

The list of vocabulary codes is listed in the VOCABULARY table. Vocabulary ID of 2 represents ICD9-CM |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Mapping\_Type |  Type of mapping from source code to target concept |
|  Target\_Concept\_Id |  Concept ID of mapped concept |
|  Target\_Concept\_Name |  Name of mapped concept |
|  Target\_Concept\_Code |  Concept code of mapped concept |
|  Target\_Concept\_Class |  Class of the mapped concept |
|  Target\_Concept\_Vocab\_ID |  Vocabulary ID of the target vocabulary |
|  Target\_Concept\_Vocab\_Name |  Name of the vocabulary the target concept is part of |
|  Target\_Concept\_Domain |  Vocabulary domain that includes the entity. The domains include:
DRUG, CONDITION, PROCEDURE, OBSERVATION, OBSERVATION UNIT, VISIT, DEMOGRAPHIC, DEATH, COST, PROVIDER |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Mapping\_Type |  CONDITION-MEDDRA |
|  Target\_Concept\_Id |  35909589 |
|  Target\_Concept\_Name |  Hepatitis viral |
|  Target\_Concept\_Code |  10019799 |
|  Target\_Concept\_Class |  Preferred Term |
|  Target\_Concept\_Vocab\_ID |  15 |
|  Target\_Concept\_Vocab\_Name |  MedDRA |
|  Target\_Concept\_Domain |  CONDITION |
**G06:** Find concepts and their descendants that are covered by a given source code

This query returns all concepts that are direct maps and the descendants of these directly mapped concepts. This is useful if the target standard vocabulary is organized in a tall hierarchy, while the source vocabulary organization is flat.

Additional constraints can be added at the end of the query if only a specific target domain or target vocabulary is desired. For example, if only SNOMED-CT as the standard vocabulary for conditions needs be returned, the target vocabulary can be set to 1.

In the query only FDB indications and contraindications are returned, but not NDF-RT indications or contraindications. That is because no direct mapping between ICD-9-CM and NDF-RT exists. In order to query for drug indications please see queries D12 through D18.

**Sample query:**

WITH dm AS ( -- collect direct maps

SELECT  c1.concept\_code as source\_code,

        c1.vocabulary\_id,

        c1.domain\_id,

        c2.concept\_id        as target\_concept\_id,

        c2.concept\_name      as target\_concept\_name,

        c2.concept\_code      as target\_concept\_code,

        c2.concept\_class\_id     as target\_concept\_class,

        c2.vocabulary\_id     as target\_concept\_vocab\_id,

        'Direct map'        as target\_Type

FROM    concept\_relationship cr

                JOIN concept c1 ON cr.concept\_id\_1 = c1.concept\_id

                JOIN concept c2 ON cr.concept\_id\_2 = c2.concept\_id

WHERE   cr.relationship\_id = 'Maps to'

AND                c1.concept\_code IN ('410.0')

AND     c1.vocabulary\_id = 'ICD9CM'

AND     sysdate BETWEEN cr.valid\_start\_date AND cr.valid\_end\_date )

SELECT dm.source\_code,

        dm.vocabulary\_id,

        dm.domain\_id,

        dc.concept\_id        AS        target\_concept\_id,

        dc.concept\_name        AS target\_concept\_name,

        dc.concept\_code AS target\_concept\_code,

        dc.concept\_class\_id AS target\_concept\_class,

        dc.vocabulary\_id AS target\_concept\_vocab\_id,

    'Descendant of direct map' as target\_Type

FROM concept\_ancestor ca -- collect descendants which includes ancestor itself

JOIN dm ON ca.ancestor\_concept\_id = dm.target\_concept\_id

JOIN concept dc ON ca.descendant\_concept\_id = dc.concept\_id

WHERE dc.standard\_concept = 'S';

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Source Code List |  '410.0' |  Yes | Source codes are alphanumeric. |
|  Source Vocabulary ID |  2 |  Yes | 2 represents ICD9-CM.

The list of vocabulary codes can be found in the VOCABULARY table. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Mapping\_Type |  Type of mapping from source code to target concept |
|  Target\_Concept\_ID |  Concept ID of mapped concept |
|  Target\_Concept\_Name |  Concept name of mapped concept |
|  Target\_Concept\_Code |  Concept Code of mapped concept |
|  Target\_Concept\_Class |  Concept class of mapped concept |
|  Target\_Concept\_Vocab\_ID |  ID of the target vocabulary |
|  Target\_Concept\_Vocab\_Name |  Name of the vocabulary the target concept is part of |
|  Target\_Type |   Type of result, indicates how the target concepts was extracted. Includes:
- Concepts that are direct maps
- Concepts that are descendants of direct maps
 |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Mapping\_Type |  CONDITION |
|  Target\_Concept\_ID |  312327 |
|  Target\_Concept\_Name |  Acute myocardial infarction |
|  Target\_Concept\_Code |  57054005 |
|  Target\_Concept\_Class |  Clinical finding |
|  Target\_Concept\_Vocab\_ID |  1 |
|  Target\_Concept\_Vocab\_Name |  SNOMED-CT |
|  Target\_Type |  Direct map |
**G07:** Find concepts that have a relationship with a given concept

For a concept identifier entered as the input parameter, the query lists all existing relationships with other concepts. The resulting output includes:

- Type of relationship (including both relationship ID and description)
- Details of the other concept to which the relationship has been defined
- Polarity of the relationship

o    Polarity of "Relates to" implies the input concept is the first concept or CONCEPT\_ID\_1 of the relationship

o    Polarity of "Is Related by" implies the input concept is the second concept or CONCEPT\_ID\_2 of the relationship

In vocabulary Version 4.0 and above all relationships are bi-directional, ie. all relationships are repeated as a mirrored version, where CONCEPT\_ID\_1 and CONCEPT\_ID\_2 are swapped and the inverse relationship ID is provided.

**Sample query:**

SELECT 'Relates to' relationship\_polarity, CR.relationship\_ID, RT.relationship\_name, D.concept\_Id concept\_id, D.concept\_Name concept\_name, D.concept\_Code concept\_code, D.concept\_class\_id concept\_class\_id, D.vocabulary\_id concept\_vocab\_ID, VS.vocabulary\_name concept\_vocab\_name

FROM concept\_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

WHERE CR.concept\_id\_1 = A.concept\_id

AND A.vocabulary\_id = VA.vocabulary\_id

AND CR.concept\_id\_2 = D.concept\_id

AND D.vocabulary\_id = VS.vocabulary\_id

AND CR.relationship\_id = RT.relationship\_ID

AND A.concept\_id = 192671

AND sysdate BETWEEN CR.valid\_start\_date

AND CR.valid\_end\_date

UNION ALL SELECT 'Is related by' relationship\_polarity, CR.relationship\_ID, RT.relationship\_name, A.concept\_Id concept\_id, A.concept\_name concept\_name, A.concept\_code concept\_code, A.concept\_class\_id concept\_class\_id, A.vocabulary\_id concept\_vocab\_ID, VA.Vocabulary\_Name concept\_vocab\_name

FROM concept\_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

WHERE CR.concept\_id\_1 = A.concept\_id

AND A.vocabulary\_id = VA.vocabulary\_id

AND CR.concept\_id\_2 = D.concept\_id

AND D.vocabulary\_id = VS.vocabulary\_id

AND CR.relationship\_id = RT.relationship\_ID

AND D.concept\_id = 192671

AND sysdate BETWEEN CR.valid\_start\_date

AND CR.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Relationship\_Polarity |  Polarity of the relationship with the input concept as a reference:
- "Relates to": Indicates input concept is CONCEPT\_ID\_1 or the first concept of the relationship
- "Is Related by": Indicates input concept
 |
|  Relationship\_ID |  Identifier for the type of relationship |
|  Relationship\_Name |  Name of the type of relationship |
|  Concept\_ID |  Unique identifier of the concept related to the input concept |
|  Concept\_Name |  Name of the concept related to the input concept |
|  Concept\_Code |  Concept code of concept related to the input concept |
|  Concept\_Class |  Concept Class of concept related to the input concept |
|  Concept\_Vocab\_ID |  ID of the vocabulary the related concept is derived from |
|  Concept\_Vocab\_Name |  Name of the vocabulary the related concept is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Relationship\_Polarity |  Is Related to |
|  Relationship\_ID |  125 |
|  Relationship\_Name |  MedDRA to SNOMED-CT equivalent (OMOP) |
|  Concept\_ID |  35707864 |
|  Concept\_Name |  Gastrointestinal haemorrhage |
|  Concept\_Code |  10017955 |
|  Concept\_Class |  Preferred Term |
|  Concept\_Vocab\_ID |  15 |
|  Concept\_Vocab\_Name |  MedDRA |
**G08:** Find ancestors for a given concept

For a concept identifier entered as the input parameter, this query lists all ancestors in the hierarchy of the domain. Ancestors are concepts that have a relationship to the given concept and is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going up in the hierarchy. The resulting output provides the ancestor concept details and the minimum and maximum level of separation.

**Sample query:**

SELECT C.concept\_id as ancestor\_concept\_id, C.concept\_name as ancestor\_concept\_name, C.concept\_code as ancestor\_concept\_code, C.concept\_class\_id as ancestor\_concept\_class\_id, C.vocabulary\_id, VA.vocabulary\_name, A.min\_levels\_of\_separation, A.max\_levels\_of\_separation

FROM concept\_ancestor A, concept C, vocabulary VA

WHERE A.ancestor\_concept\_id = C.concept\_id

AND C.vocabulary\_id = VA.vocabulary\_id

AND A.ancestor\_concept\_id<>A.descendant\_concept\_id

AND A.descendant\_concept\_id = 192671

AND sysdate BETWEEN valid\_start\_date

AND valid\_end\_date

ORDER BY 5,7;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Ancestor\_Concept\_ID |  Unique identifier of the concept related to the ancestor concept |
|  Ancestor\_Concept\_Name |  Name of the concept related to the ancestor concept |
|  Ancestor\_Concept\_Code |  Concept code of concept related to the ancestor concept |
|  Ancestor\_Concept\_>Class |  Concept Class of concept related to the ancestor concept |
|  Vocabulary\_ID |  ID of the vocabulary the ancestor concept is derived from |
|  Vocabulary\_Name |  Name of the vocabulary the ancestor concept is derived from |
|  Min\_Levels\_of\_Separation |  The length of the shortest path between the concept and the ancestor |
|  Max\_Levels\_of\_Separation |  The length of the longest path between the concept and the ancestor |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Ancestor\_Concept\_ID |  4000610 |
|  Ancestor\_Concept\_Name |  Disease of gastrointestinal tract |
|  Ancestor\_Concept\_Code |  119292006 |
|  Ancestor\_Concept\_Class |  Clinical finding |
|  Vocabulary\_ID |  1 |
|  Vocabulary\_Name |  SNOMED-CT |
|  Min\_Levels\_of\_Separation |  1 |
|  Max\_Levels\_of\_Separation |  1 |
**G09:** Find descendants for a given concept

For a concept identifier entered as the input parameter, this query lists all descendants in the hierarchy of the domain. Descendant are concepts have a relationship to the given concept that is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going down in the hierarchy. The resulting output provides the descendant concept details and the minimum and maximum level of separation.

**Sample query:**

SELECT C.concept\_id as descendant\_concept\_id, C.concept\_name as descendant\_concept\_name, C.concept\_code as descendant\_concept\_code, C.concept\_class\_id as descendant\_concept\_class\_id, C.vocabulary\_id, VA.vocabulary\_name, A.min\_levels\_of\_separation, A.max\_levels\_of\_separation

FROM concept\_ancestor A, concept C, vocabulary VA

WHERE A.descendant\_concept\_id = C.concept\_id

AND C.vocabulary\_id = VA.vocabulary\_id

AND A.ancestor\_concept\_id <> A.descendant\_concept\_id

AND A.ancestor\_concept\_id = 192671

AND sysdate BETWEEN valid\_start\_date

AND valid\_end\_date

ORDER BY 5,7;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Descendant\_Concept\_ID |  Unique identifier of the concept related to the descendant concept |
|  Descendant\_Concept\_Name |  Name of the concept related to the descendant concept |
|  Descendant\_Concept\_Code |  Concept code of concept related to the descendant concept |
|  Descendant\_Concept\_Class |  Concept Class of concept related to the descendant concept |
|  Vocabulary\_ID |  ID of the vocabulary the descendant concept is derived from |
|  Vocabulary\_Name; |  Name of the vocabulary the descendant concept is derived from |
|  Min\_Levels\_of\_Separation |  The length of the shortest path between the concept and the descendant |
|  Max\_Levels\_of\_Separation |  The length of the longest path between the concept and the descendant |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Descendant\_Concept\_ID |  4318535 |
|  Descendant\_Concept\_Name |  Duodenal haemorrhage |
|  Descendant\_Concept\_Code |  95533003 |
|  Descendant\_Concept\_Class |  Clinical finding |
|  Vocabulary\_ID |  1 |
|  Vocabulary\_Name |  SNOMED-CT |
|  Min\_Levels\_of\_Separation |  1 |
|  Max\_Levels\_of\_Separation |  1 |
**G10:** Find parents for a given concept

### This query accepts a concept ID as the input and returns all concepts that are its immediate parents of that concept. Parents are concepts that have a hierarchical relationship to the given concepts. Hierarchical relationships are defined in the relationship table.
The query returns only the immediate parent concepts that are directly linked to the input concept and not all ancestors.

**Sample query:**

SELECT A.concept\_id Parent\_concept\_id, A.concept\_name Parent\_concept\_name, A.concept\_code Parent\_concept\_code, A.concept\_class\_id Parent\_concept\_class\_id, A.vocabulary\_id Parent\_concept\_vocab\_ID, VA.vocabulary\_name Parent\_concept\_vocab\_name

FROM concept\_ancestor CA, concept A, concept D, vocabulary VA

WHERE CA.descendant\_concept\_id = 192671

AND CA.min\_levels\_of\_separation = 1

AND CA.ancestor\_concept\_id = A.concept\_id

AND A.vocabulary\_id = VA.vocabulary\_id

AND CA.descendant\_concept\_id = D.concept\_id

AND sysdate BETWEEN A.valid\_start\_date

AND A.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Parent\_Concept\_ID |  Concept ID of parent concept |
|  Parent\_Concept\_Name |  Name of parent concept |
|  Parent\_Concept\_Code |  Concept Code of parent concept |
|  Parent\_Concept\_Class |  Concept Class of parent concept |
|  Parent\_Concept\_Vocab\_ID |  Vocabulary parent concept is derived from as vocabulary code |
|  Parent\_Concept\_Vocab\_Name |  Name of the vocabulary the child concept is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Parent\_Concept\_ID |  4000610 |
|  Parent\_Concept\_Name |  Disease of gastrointestinal tract |
|  Parent\_Concept\_Code |  119292006 |
|  Parent\_Concept\_Class |  Clinical finding |
|  Parent\_Concept\_Vocab\_ID |  1 |
|  Parent\_Concept\_Vocab\_Name |  SNOMED-CT |
**G11:** Find children for a given concept

This query lists all standard vocabulary concepts that are child concepts of a given concept entered as input. The query accepts a concept ID as the input and returns all concepts that are its immediate child concepts.

The query returns only the immediate child concepts that are directly linked to the input concept and not all descendants.

**Sample query:**

SELECT D.concept\_id Child\_concept\_id, D.concept\_name Child\_concept\_name, D.concept\_code Child\_concept\_code, D.concept\_class\_id Child\_concept\_class\_id, D.vocabulary\_id Child\_concept\_vocab\_ID, VS.vocabulary\_name Child\_concept\_vocab\_name

FROM concept\_ancestor CA, concept D, vocabulary VS

WHERE CA.ancestor\_concept\_id = 192671

AND CA.min\_levels\_of\_separation = 1

AND CA.descendant\_concept\_id = D.concept\_id

AND D.vocabulary\_id = VS.vocabulary\_id

AND sysdate BETWEEN D.valid\_start\_date

AND D.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Child\_Concept\_ID |  Concept ID of child concept entered as input |
|  Child\_Concept\_Name |  Name of child concept entered as input |
|  Child\_Concept\_Code |  Concept Code of child concept entered as input |
|  Child\_Concept\_Class |  Concept Class of child concept entered as input |
|  Child\_Concept\_Vocab\_ID |  ID of the vocabulary the child concept is derived from |
|  Child\_Concept\_Vocab\_Name |  Name of the vocabulary the child concept is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Child\_Concept\_ID |  4128705 |
|  Child\_Concept\_Name |  Haemorrhagic enteritis |
|  Child\_Concept\_Code |  235224000 |
|  Child\_Concept\_Class |  Clinical finding |
|  Child\_Concept\_Vocab\_ID |  1 |
|  Child\_Concept\_Vocab\_Name |  SNOMED-CT |
**G12:** List current vocabulary release number

This query returns current vocabulary release number.

**Sample query:**

SELECT vocabulary\_name, vocabulary\_version FROM vocabulary;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  vocabulary\_name |  Version number of current OMOP vocabulary release |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  vocabulary\_name |  OMOP Vocabulary v4.3 Q2-2013 |
**G13:** List available vocabularies

This query returns list of available vocabularies.

**Sample query:**

SELECT vocabulary\_id, vocabulary\_name FROM vocabulary WHERE vocabulary\_id IS NOT NULL;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  vocabulary\_id |  OMOP Vocabulary ID |
|  vocabulary\_name |  Vocabulary name |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  vocabulary\_id |  1 |
|  vocabulary\_name |  SNOMED-CT |
**G14:** Statistics about relationships between concepts

This query produces list and frequency of all relationships between concepts (Standard and non-standard) and their class

**Sample query:**

SELECT

  R.relationship\_id,

  R.relationship\_name,

  C1.vocabulary\_id from\_vocabulary\_id,

  V1.vocabulary\_name from\_vocabulary\_name,

  C1.concept\_class\_id from\_concept\_class,

  C2.vocabulary\_id to\_vocabulary\_id,

  V2.vocabulary\_name to\_vocabulary\_name,

  C2.concept\_class\_id to\_concept\_class,

  count(\*) num\_records

FROM

  concept\_relationship CR,

  concept C1,

  concept C2,

  relationship R,

  vocabulary V1,

  vocabulary V2

WHERE

  CR.concept\_id\_1 = C1.concept\_id AND

  CR.concept\_id\_2 = C2.concept\_id AND

  R.relationship\_id = CR.relationship\_id AND

  C1.vocabulary\_id = V1.vocabulary\_id AND

  C2.vocabulary\_id = V2.vocabulary\_id

GROUP BY

  R.relationship\_id,

  relationship\_name,

  C1.vocabulary\_id,

  V1.vocabulary\_name,

  C1.concept\_class\_id,

  C2.vocabulary\_id,

  V2.vocabulary\_name,

  C2.concept\_class\_id

ORDER BY

  R.relationship\_id,

  C1.concept\_class\_id;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  relationship\_id |  Identifier for the type of relationship |
|  relationship\_name |  Name of the type of relationship |
|  from\_vocabulary\_id |  ID of the vocabulary of the input concepts |
|  from\_vocabulary\_name |  Name of the vocabulary of the input concepts |
|  from\_concept\_class |  Concept class of the input concepts |
|  to\_vocabulary\_id |  ID of the vocabulary the related concept is derived from |
|  to\_vocabulary\_name |  Name of the vocabulary the related concept is derived from |
|  to\_concept\_class |  Concept class the related concept is derived from |
|  num\_records |  Number of records  |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  relationship\_id |  1 |
|  relationship\_name |  Concept replaced by (LOINC) |
|  from\_vocabulary\_id |  6 |
|  from\_vocabulary\_name |  LOINC |
|  from\_concept\_class |  LOINC Code |
|  to\_vocabulary\_id |  6 |
|  to\_vocabulary\_name |  LOINC |
|  to\_concept\_class |  LOINC Code |
|  num\_records |  2022 |
**G15:** Statistic about Concepts, Vocabularies, Classes and Levels

### This query generates the list of all vocabularies in the CONCEPT table (Standard and non-standard), their class, level and frequency.

**Sample query:**

SELECT

  voc.vocabulary\_id,

  r.vocabulary\_name,

  voc.concept\_class\_id,

  voc.standard\_concept,

  voc.cnt

FROM (

  SELECT

    vocabulary\_id,

    concept\_class\_id,

    standard\_concept,

    COUNT(concept\_id) cnt

  FROM concept

  GROUP BY

    vocabulary\_id,

    concept\_class\_id,

    standard\_concept ) voc

JOIN vocabulary r ON voc.vocabulary\_id=r.vocabulary\_ID

ORDER BY 1,2,4,3;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  vocabulary\_id |  OMOP Vocabulary ID |
|  vocabulary\_name |  Vocabulary name |
|  concept\_class |  Concept Class |
|  concept\_level |  Concept Level Number |
|  cnt |  Number of concepts |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  vocabulary\_id |  1 |
|  vocabulary\_name |  SNOMED-CT |
|  concept\_class |  Procedure |
|  concept\_level |  2 |
|  cnt |  20286 |
**G16:** Statistics about Condition Mapping of Source Vocabularies

### The following query contains the coverage for mapped source vocabularies in the Condition domains to SNOMED-CT.

**Sample query:**

SELECT

  mapped.vocabulary\_id,

  mapped.vocabulary\_name,

  CASE mapped.standard\_concept

    WHEN null THEN 'Not mapped'

        ELSE mapped.standard\_concept

  END AS standard\_concept,

  mapped.mapped\_codes,

  sum(mapped.mapped\_codes) over (partition by vocabulary\_id) as total\_mapped\_codes,

  to\_char(mapped.mapped\_codes\*100/sum(mapped.mapped\_codes) over (partition by vocabulary\_id), '990.9') AS pct\_mapped\_codes,

  mapped.mapped\_concepts,

  (SELECT count(1)

   FROM concept

   WHERE

     vocabulary\_id='SNOMED' AND

        standard\_concept=mapped.standard\_concept AND

        lower(concept\_class\_id)='clinical finding' AND

        invalid\_reason is null

  ) AS standard\_concepts,

  to\_char(mapped.mapped\_concepts\*100/

         ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                  FROM concept

                  WHERE

                    vocabulary\_id='SNOMED' AND

                        standard\_concept=mapped.standard\_concept AND

                        lower(concept\_class\_id)='clinical finding' AND

                        invalid\_reason is null ), '990.9'

  ) AS pct\_mapped\_concepts

FROM (

  SELECT

    c1.vocabulary\_id AS vocabulary\_id,

        v.vocabulary\_name,

        c2.standard\_concept,

        COUNT(8) AS mapped\_codes,

        COUNT(DISTINCT c2.concept\_id) AS mapped\_concepts

  FROM concept\_relationship m

  JOIN concept c1 on m.concept\_id\_1=c1.concept\_id and

       m.relationship\_id='Maps to' and m.invalid\_reason is null

  JOIN concept c2 on c2.concept\_id=m.concept\_id\_2

  JOIN vocabulary v on v.vocabulary\_id=c1.vocabulary\_id

  WHERE c2.vocabulary\_id='SNOMED' AND lower(c2.domain\_id)='condition'

  GROUP BY c1.vocabulary\_id, v.vocabulary\_name, c2.standard\_concept

) mapped;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  vocabulary\_id |  Source Vocabulary ID |
|  vocabulary\_name |  Source Vocabulary name |
|  concept\_level |  Concept Level Number |
|  mapped\_codes |  Number of mapped codes |
|  total\_mapped\_codes |  Total number of mapped codes for source vocabulary |
|  pct\_mapped\_codes |  Percentile of mapped code  |
|  mapped\_concepts |  Number of mapped concepts  |
|  concepts\_in\_level |  Number of mapped concepts  |
|  pct\_mapped\_concepts |  Percentile of of mapped concepts |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  vocabulary\_id |  2 |
|  vocabulary\_name |  ICD9-CT |
|  concept\_level |  1 |
|  mapped\_codes |  4079 |
|  total\_mapped\_codes |  10770 |
|  pct\_mapped\_codes |  37.0 |
|  mapped\_concepts |  3733 |
|  concepts\_in\_level |  69280 |
|  pct\_mapped\_concepts |  5.0 |
**G17:** Statistics about Drugs Mapping of Source Vocabularies

The following query contains the coverage for mapped source vocabularies in the Drug domains to RxNorm.

**Sample query:**

SELECT

  mapped.vocabulary\_id,

  mapped.vocabulary\_name,

  CASE mapped.standard\_concept

    WHEN null THEN 'Not mapped'

        ELSE mapped.standard\_concept

  END AS standard\_concept,

  mapped.mapped\_codes,

  sum(mapped.mapped\_codes) over (partition by vocabulary\_id) as total\_mapped\_codes,

  to\_char(mapped.mapped\_codes\*100/sum(mapped.mapped\_codes) over (partition by vocabulary\_id), '990.9') AS pct\_mapped\_codes,

  mapped.mapped\_concepts,

  (SELECT count(1)

   FROM concept

   WHERE

     vocabulary\_id='RxNorm' AND

        standard\_concept=mapped.standard\_concept AND

        invalid\_reason is null

  ) AS standard\_concepts,

  to\_char(mapped.mapped\_concepts\*100/

         ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                  FROM concept

                  WHERE

                    vocabulary\_id='RxNorm' AND

                        standard\_concept=mapped.standard\_concept AND

                        invalid\_reason is null ), '990.9'

  ) AS pct\_mapped\_concepts

FROM (

  SELECT

    c1.vocabulary\_id AS vocabulary\_id,

        v.vocabulary\_name,

        c2.standard\_concept,

        COUNT(8) AS mapped\_codes,

        COUNT(DISTINCT c2.concept\_id) AS mapped\_concepts

  FROM concept\_relationship m

  JOIN concept c1 on m.concept\_id\_1=c1.concept\_id and

       m.relationship\_id='Maps to' and m.invalid\_reason is null

  JOIN concept c2 on c2.concept\_id=m.concept\_id\_2

  JOIN vocabulary v on v.vocabulary\_id=c1.vocabulary\_id

  WHERE c2.vocabulary\_id in ('ICD9CM','RxNorm') AND lower(c2.domain\_id)='drug'

  GROUP BY c1.vocabulary\_id, v.vocabulary\_name, c2.standard\_concept

) mapped;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  vocabulary\_id |  Source Vocabulary ID |
|  vocabulary\_name |  Source Vocabulary name |
|  concept\_level |  Concept Level Number |
|  mapped\_codes |  Number of mapped codes |
|  total\_mapped\_codes |  Total number of mapped codes for source vocabulary |
|  pct\_mapped\_codes |  Percentile of mapped code  |
|  mapped\_concepts |  Number of mapped concepts  |
|  concepts\_in\_level |  Number of mapped concepts  |
|  pct\_mapped\_concepts |  Percentile of of mapped concepts |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  vocabulary\_id |  9 |
|  vocabulary\_name |  NDC |
|  concept\_level |  1 |
|  mapped\_codes |  550959 |
|  total\_mapped\_codes |  551757 |
|  pct\_mapped\_codes |  99.0 |
|  mapped\_concepts |  33206 |
|  concepts\_in\_level |  57162 |
|  pct\_mapped\_concepts |  58.0 |
\*\*G01:\*\* Find concept by concept ID

This is the most generic look-up for obtaining concept details associated with a concept identifier. The query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.

\*\*Sample query:\*\*

SELECT C.concept\\_id, C.concept\\_name, C.concept\\_code, C.concept\\_class\\_id, C.standard\\_concept, C.vocabulary\\_id, V.vocabulary\\_name

FROM concept C, vocabulary V

WHERE C.concept\\_id = 192671

AND C.vocabulary\\_id = V.vocabulary\\_id

AND sysdate BETWEEN valid\\_start\\_date

AND valid\\_end\\_date;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | Concept Identifier for "GI - Gastrointestinal hemorrhage" |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Concept\\_ID |  Concept Identifier entered as input |

|  Concept\\_Name |  Name of the standard concept |

|  Concept\\_Code |  Concept code of the standard concept in the source vocabulary |

|  Concept\\_Class |  Concept class of standard vocabulary concept |

|  Concept\\_Level |  Level of the concept if defined as part of a hierarchy |

|  Vocabulary\\_ID |  Vocabulary the standard concept is derived from as vocabulary code |

|  Vocabulary\\_Name |  Name of the vocabulary the standard concept is derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Concept\\_ID |  192671 |

|  Concept\\_Name |  GI - Gastrointestinal haemorrhage |

|  Concept\\_Code |  74474003 |

|  Concept\\_Class |  Clinical finding |

|  Concept\\_Level |  2 |

|  Vocabulary\\_ID |  1 |

|  Vocabulary\\_Name |  SNOMED-CT |

\*\*G04:\*\* Find synonyms for a given concept

This query extracts all synonyms in the vocabulary for a given Concept ID.

\*\*Sample query:\*\*

SELECT C.concept\\_id, S.concept\\_synonym\\_name

FROM concept C, concept\\_synonym S, vocabulary V

WHERE C.concept\\_id = 192671

AND C.concept\\_id = S.concept\\_id

AND C.vocabulary\\_id = V.vocabulary\\_id

AND sysdate BETWEEN C.valid\\_start\\_date AND C.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Concept\\_ID |  Unique identifier of the concept related to the input concept |

|  Concept\\_Synonym\\_Name |  Synonym of the concept |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Concept\\_ID |  192671 |

|  Concept\\_Synonym\\_Name |  GI bleeding |

\*\*G05:\*\* Translate a code from a source to a standard vocabulary.

This query enables search of all Standard Vocabulary concepts that are mapped to a code from a specified source vocabulary. It will return all possible concepts that are mapped to it, as well as the target vocabulary. The source code could be obtained using queries G02 or G03.

Note that to unambiguously identify a source code, the vocabulary id has to be provided, as source codes are not unique identifiers across different vocabularies.

\*\*Sample query:\*\*

SELECT DISTINCT

        c1.domain\\_id,

        c2.concept\\_id         as Concept\\_Id,

        c2.concept\\_name       as Concept\\_Name,

        c2.concept\\_code       as Concept\\_Code,

        c2.concept\\_class\\_id      as Concept\\_Class,

        c2.vocabulary\\_id      as Concept\\_Vocabulary\\_ID,

                  c2.domain\\_id                  as Target\\_concept\\_Domain

FROM concept\\_relationship cr

JOIN concept c1 ON c1.concept\\_id = cr.concept\\_id\\_1

JOIN concept c2 ON c2.concept\\_id = cr.concept\\_id\\_2

WHERE cr.relationship\\_id = 'Maps to'

AND c1.concept\\_code IN ('070.0')

AND c1.vocabulary\\_id = 'ICD9CM'

AND sysdate BETWEEN cr.valid\\_start\\_date AND cr.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Source Code List |  '070.0' |  Yes |  Source codes are alphanumeric |

|  Source Vocabulary ID |  2 |  Yes | The source vocabulary ID is mandatory, because the source code is not unique across different vocabularies.

The list of vocabulary codes is listed in the VOCABULARY table. Vocabulary ID of 2 represents ICD9-CM |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Mapping\\_Type |  Type of mapping from source code to target concept |

|  Target\\_Concept\\_Id |  Concept ID of mapped concept |

|  Target\\_Concept\\_Name |  Name of mapped concept |

|  Target\\_Concept\\_Code |  Concept code of mapped concept |

|  Target\\_Concept\\_Class |  Class of the mapped concept |

|  Target\\_Concept\\_Vocab\\_ID |  Vocabulary ID of the target vocabulary |

|  Target\\_Concept\\_Vocab\\_Name |  Name of the vocabulary the target concept is part of |

|  Target\\_Concept\\_Domain |  Vocabulary domain that includes the entity. The domains include:

DRUG, CONDITION, PROCEDURE, OBSERVATION, OBSERVATION UNIT, VISIT, DEMOGRAPHIC, DEATH, COST, PROVIDER |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Mapping\\_Type |  CONDITION-MEDDRA |

|  Target\\_Concept\\_Id |  35909589 |

|  Target\\_Concept\\_Name |  Hepatitis viral |

|  Target\\_Concept\\_Code |  10019799 |

|  Target\\_Concept\\_Class |  Preferred Term |

|  Target\\_Concept\\_Vocab\\_ID |  15 |

|  Target\\_Concept\\_Vocab\\_Name |  MedDRA |

|  Target\\_Concept\\_Domain |  CONDITION |

\*\*G06:\*\* Find concepts and their descendants that are covered by a given source code

This query returns all concepts that are direct maps and the descendants of these directly mapped concepts. This is useful if the target standard vocabulary is organized in a tall hierarchy, while the source vocabulary organization is flat.

Additional constraints can be added at the end of the query if only a specific target domain or target vocabulary is desired. For example, if only SNOMED-CT as the standard vocabulary for conditions needs be returned, the target vocabulary can be set to 1.

In the query only FDB indications and contraindications are returned, but not NDF-RT indications or contraindications. That is because no direct mapping between ICD-9-CM and NDF-RT exists. In order to query for drug indications please see queries D12 through D18.

\*\*Sample query:\*\*

WITH dm AS ( -- collect direct maps

SELECT  c1.concept\\_code as source\\_code,

        c1.vocabulary\\_id,

        c1.domain\\_id,

        c2.concept\\_id        as target\\_concept\\_id,

        c2.concept\\_name      as target\\_concept\\_name,

        c2.concept\\_code      as target\\_concept\\_code,

        c2.concept\\_class\\_id     as target\\_concept\\_class,

        c2.vocabulary\\_id     as target\\_concept\\_vocab\\_id,

        'Direct map'        as target\\_Type

FROM    concept\\_relationship cr

                JOIN concept c1 ON cr.concept\\_id\\_1 = c1.concept\\_id

                JOIN concept c2 ON cr.concept\\_id\\_2 = c2.concept\\_id

WHERE   cr.relationship\\_id = 'Maps to'

AND                c1.concept\\_code IN ('410.0')

AND     c1.vocabulary\\_id = 'ICD9CM'

AND     sysdate BETWEEN cr.valid\\_start\\_date AND cr.valid\\_end\\_date )

SELECT dm.source\\_code,

        dm.vocabulary\\_id,

        dm.domain\\_id,

        dc.concept\\_id        AS        target\\_concept\\_id,

        dc.concept\\_name        AS target\\_concept\\_name,

        dc.concept\\_code AS target\\_concept\\_code,

        dc.concept\\_class\\_id AS target\\_concept\\_class,

        dc.vocabulary\\_id AS target\\_concept\\_vocab\\_id,

    'Descendant of direct map' as target\\_Type

FROM concept\\_ancestor ca -- collect descendants which includes ancestor itself

JOIN dm ON ca.ancestor\\_concept\\_id = dm.target\\_concept\\_id

JOIN concept dc ON ca.descendant\\_concept\\_id = dc.concept\\_id

WHERE dc.standard\\_concept = 'S';

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Source Code List |  '410.0' |  Yes | Source codes are alphanumeric. |

|  Source Vocabulary ID |  2 |  Yes | 2 represents ICD9-CM.

The list of vocabulary codes can be found in the VOCABULARY table. |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Mapping\\_Type |  Type of mapping from source code to target concept |

|  Target\\_Concept\\_ID |  Concept ID of mapped concept |

|  Target\\_Concept\\_Name |  Concept name of mapped concept |

|  Target\\_Concept\\_Code |  Concept Code of mapped concept |

|  Target\\_Concept\\_Class |  Concept class of mapped concept |

|  Target\\_Concept\\_Vocab\\_ID |  ID of the target vocabulary |

|  Target\\_Concept\\_Vocab\\_Name |  Name of the vocabulary the target concept is part of |

|  Target\\_Type |   Type of result, indicates how the target concepts was extracted. Includes:

- Concepts that are direct maps

- Concepts that are descendants of direct maps

 |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Mapping\\_Type |  CONDITION |

|  Target\\_Concept\\_ID |  312327 |

|  Target\\_Concept\\_Name |  Acute myocardial infarction |

|  Target\\_Concept\\_Code |  57054005 |

|  Target\\_Concept\\_Class |  Clinical finding |

|  Target\\_Concept\\_Vocab\\_ID |  1 |

|  Target\\_Concept\\_Vocab\\_Name |  SNOMED-CT |

|  Target\\_Type |  Direct map |

\*\*G07:\*\* Find concepts that have a relationship with a given concept

For a concept identifier entered as the input parameter, the query lists all existing relationships with other concepts. The resulting output includes:

- Type of relationship (including both relationship ID and description)

- Details of the other concept to which the relationship has been defined

- Polarity of the relationship

o    Polarity of "Relates to" implies the input concept is the first concept or CONCEPT\\_ID\\_1 of the relationship

o    Polarity of "Is Related by" implies the input concept is the second concept or CONCEPT\\_ID\\_2 of the relationship

In vocabulary Version 4.0 and above all relationships are bi-directional, ie. all relationships are repeated as a mirrored version, where CONCEPT\\_ID\\_1 and CONCEPT\\_ID\\_2 are swapped and the inverse relationship ID is provided.

\*\*Sample query:\*\*

SELECT 'Relates to' relationship\\_polarity, CR.relationship\\_ID, RT.relationship\\_name, D.concept\\_Id concept\\_id, D.concept\\_Name concept\\_name, D.concept\\_Code concept\\_code, D.concept\\_class\\_id concept\\_class\\_id, D.vocabulary\\_id concept\\_vocab\\_ID, VS.vocabulary\\_name concept\\_vocab\\_name

FROM concept\\_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

WHERE CR.concept\\_id\\_1 = A.concept\\_id

AND A.vocabulary\\_id = VA.vocabulary\\_id

AND CR.concept\\_id\\_2 = D.concept\\_id

AND D.vocabulary\\_id = VS.vocabulary\\_id

AND CR.relationship\\_id = RT.relationship\\_ID

AND A.concept\\_id = 192671

AND sysdate BETWEEN CR.valid\\_start\\_date

AND CR.valid\\_end\\_date

UNION ALL SELECT 'Is related by' relationship\\_polarity, CR.relationship\\_ID, RT.relationship\\_name, A.concept\\_Id concept\\_id, A.concept\\_name concept\\_name, A.concept\\_code concept\\_code, A.concept\\_class\\_id concept\\_class\\_id, A.vocabulary\\_id concept\\_vocab\\_ID, VA.Vocabulary\\_Name concept\\_vocab\\_name

FROM concept\\_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

WHERE CR.concept\\_id\\_1 = A.concept\\_id

AND A.vocabulary\\_id = VA.vocabulary\\_id

AND CR.concept\\_id\\_2 = D.concept\\_id

AND D.vocabulary\\_id = VS.vocabulary\\_id

AND CR.relationship\\_id = RT.relationship\\_ID

AND D.concept\\_id = 192671

AND sysdate BETWEEN CR.valid\\_start\\_date

AND CR.valid\\_end\\_date;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Relationship\\_Polarity |  Polarity of the relationship with the input concept as a reference:

- "Relates to": Indicates input concept is CONCEPT\\_ID\\_1 or the first concept of the relationship

- "Is Related by": Indicates input concept

 |

|  Relationship\\_ID |  Identifier for the type of relationship |

|  Relationship\\_Name |  Name of the type of relationship |

|  Concept\\_ID |  Unique identifier of the concept related to the input concept |

|  Concept\\_Name |  Name of the concept related to the input concept |

|  Concept\\_Code |  Concept code of concept related to the input concept |

|  Concept\\_Class |  Concept Class of concept related to the input concept |

|  Concept\\_Vocab\\_ID |  ID of the vocabulary the related concept is derived from |

|  Concept\\_Vocab\\_Name |  Name of the vocabulary the related concept is derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Relationship\\_Polarity |  Is Related to |

|  Relationship\\_ID |  125 |

|  Relationship\\_Name |  MedDRA to SNOMED-CT equivalent (OMOP) |

|  Concept\\_ID |  35707864 |

|  Concept\\_Name |  Gastrointestinal haemorrhage |

|  Concept\\_Code |  10017955 |

|  Concept\\_Class |  Preferred Term |

|  Concept\\_Vocab\\_ID |  15 |

|  Concept\\_Vocab\\_Name |  MedDRA |

\*\*G08:\*\* Find ancestors for a given concept

For a concept identifier entered as the input parameter, this query lists all ancestors in the hierarchy of the domain. Ancestors are concepts that have a relationship to the given concept and is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going up in the hierarchy. The resulting output provides the ancestor concept details and the minimum and maximum level of separation.

\*\*Sample query:\*\*

SELECT C.concept\\_id as ancestor\\_concept\\_id, C.concept\\_name as ancestor\\_concept\\_name, C.concept\\_code as ancestor\\_concept\\_code, C.concept\\_class\\_id as ancestor\\_concept\\_class\\_id, C.vocabulary\\_id, VA.vocabulary\\_name, A.min\\_levels\\_of\\_separation, A.max\\_levels\\_of\\_separation

FROM concept\\_ancestor A, concept C, vocabulary VA

WHERE A.ancestor\\_concept\\_id = C.concept\\_id

AND C.vocabulary\\_id = VA.vocabulary\\_id

AND A.ancestor\\_concept\\_id<>A.descendant\\_concept\\_id

AND A.descendant\\_concept\\_id = 192671

AND sysdate BETWEEN valid\\_start\\_date

AND valid\\_end\\_date

ORDER BY 5,7;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Ancestor\\_Concept\\_ID |  Unique identifier of the concept related to the ancestor concept |

|  Ancestor\\_Concept\\_Name |  Name of the concept related to the ancestor concept |

|  Ancestor\\_Concept\\_Code |  Concept code of concept related to the ancestor concept |

|  Ancestor\\_Concept\\_>Class |  Concept Class of concept related to the ancestor concept |

|  Vocabulary\\_ID |  ID of the vocabulary the ancestor concept is derived from |

|  Vocabulary\\_Name |  Name of the vocabulary the ancestor concept is derived from |

|  Min\\_Levels\\_of\\_Separation |  The length of the shortest path between the concept and the ancestor |

|  Max\\_Levels\\_of\\_Separation |  The length of the longest path between the concept and the ancestor |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Ancestor\\_Concept\\_ID |  4000610 |

|  Ancestor\\_Concept\\_Name |  Disease of gastrointestinal tract |

|  Ancestor\\_Concept\\_Code |  119292006 |

|  Ancestor\\_Concept\\_Class |  Clinical finding |

|  Vocabulary\\_ID |  1 |

|  Vocabulary\\_Name |  SNOMED-CT |

|  Min\\_Levels\\_of\\_Separation |  1 |

|  Max\\_Levels\\_of\\_Separation |  1 |

\*\*G09:\*\* Find descendants for a given concept

For a concept identifier entered as the input parameter, this query lists all descendants in the hierarchy of the domain. Descendant are concepts have a relationship to the given concept that is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going down in the hierarchy. The resulting output provides the descendant concept details and the minimum and maximum level of separation.

\*\*Sample query:\*\*

SELECT C.concept\\_id as descendant\\_concept\\_id, C.concept\\_name as descendant\\_concept\\_name, C.concept\\_code as descendant\\_concept\\_code, C.concept\\_class\\_id as descendant\\_concept\\_class\\_id, C.vocabulary\\_id, VA.vocabulary\\_name, A.min\\_levels\\_of\\_separation, A.max\\_levels\\_of\\_separation

FROM concept\\_ancestor A, concept C, vocabulary VA

WHERE A.descendant\\_concept\\_id = C.concept\\_id

AND C.vocabulary\\_id = VA.vocabulary\\_id

AND A.ancestor\\_concept\\_id <> A.descendant\\_concept\\_id

AND A.ancestor\\_concept\\_id = 192671

AND sysdate BETWEEN valid\\_start\\_date

AND valid\\_end\\_date

ORDER BY 5,7;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Descendant\\_Concept\\_ID |  Unique identifier of the concept related to the descendant concept |

|  Descendant\\_Concept\\_Name |  Name of the concept related to the descendant concept |

|  Descendant\\_Concept\\_Code |  Concept code of concept related to the descendant concept |

|  Descendant\\_Concept\\_Class |  Concept Class of concept related to the descendant concept |

|  Vocabulary\\_ID |  ID of the vocabulary the descendant concept is derived from |

|  Vocabulary\\_Name; |  Name of the vocabulary the descendant concept is derived from |

|  Min\\_Levels\\_of\\_Separation |  The length of the shortest path between the concept and the descendant |

|  Max\\_Levels\\_of\\_Separation |  The length of the longest path between the concept and the descendant |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Descendant\\_Concept\\_ID |  4318535 |

|  Descendant\\_Concept\\_Name |  Duodenal haemorrhage |

|  Descendant\\_Concept\\_Code |  95533003 |

|  Descendant\\_Concept\\_Class |  Clinical finding |

|  Vocabulary\\_ID |  1 |

|  Vocabulary\\_Name |  SNOMED-CT |

|  Min\\_Levels\\_of\\_Separation |  1 |

|  Max\\_Levels\\_of\\_Separation |  1 |

\*\*G10:\*\* Find parents for a given concept

### This query accepts a concept ID as the input and returns all concepts that are its immediate parents of that concept. Parents are concepts that have a hierarchical relationship to the given concepts. Hierarchical relationships are defined in the relationship table.

The query returns only the immediate parent concepts that are directly linked to the input concept and not all ancestors.

\*\*Sample query:\*\*

SELECT A.concept\\_id Parent\\_concept\\_id, A.concept\\_name Parent\\_concept\\_name, A.concept\\_code Parent\\_concept\\_code, A.concept\\_class\\_id Parent\\_concept\\_class\\_id, A.vocabulary\\_id Parent\\_concept\\_vocab\\_ID, VA.vocabulary\\_name Parent\\_concept\\_vocab\\_name

FROM concept\\_ancestor CA, concept A, concept D, vocabulary VA

WHERE CA.descendant\\_concept\\_id = 192671

AND CA.min\\_levels\\_of\\_separation = 1

AND CA.ancestor\\_concept\\_id = A.concept\\_id

AND A.vocabulary\\_id = VA.vocabulary\\_id

AND CA.descendant\\_concept\\_id = D.concept\\_id

AND sysdate BETWEEN A.valid\\_start\\_date

AND A.valid\\_end\\_date;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Parent\\_Concept\\_ID |  Concept ID of parent concept |

|  Parent\\_Concept\\_Name |  Name of parent concept |

|  Parent\\_Concept\\_Code |  Concept Code of parent concept |

|  Parent\\_Concept\\_Class |  Concept Class of parent concept |

|  Parent\\_Concept\\_Vocab\\_ID |  Vocabulary parent concept is derived from as vocabulary code |

|  Parent\\_Concept\\_Vocab\\_Name |  Name of the vocabulary the child concept is derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Parent\\_Concept\\_ID |  4000610 |

|  Parent\\_Concept\\_Name |  Disease of gastrointestinal tract |

|  Parent\\_Concept\\_Code |  119292006 |

|  Parent\\_Concept\\_Class |  Clinical finding |

|  Parent\\_Concept\\_Vocab\\_ID |  1 |

|  Parent\\_Concept\\_Vocab\\_Name |  SNOMED-CT |

\*\*G11:\*\* Find children for a given concept

This query lists all standard vocabulary concepts that are child concepts of a given concept entered as input. The query accepts a concept ID as the input and returns all concepts that are its immediate child concepts.

The query returns only the immediate child concepts that are directly linked to the input concept and not all descendants.

\*\*Sample query:\*\*

SELECT D.concept\\_id Child\\_concept\\_id, D.concept\\_name Child\\_concept\\_name, D.concept\\_code Child\\_concept\\_code, D.concept\\_class\\_id Child\\_concept\\_class\\_id, D.vocabulary\\_id Child\\_concept\\_vocab\\_ID, VS.vocabulary\\_name Child\\_concept\\_vocab\\_name

FROM concept\\_ancestor CA, concept D, vocabulary VS

WHERE CA.ancestor\\_concept\\_id = 192671

AND CA.min\\_levels\\_of\\_separation = 1

AND CA.descendant\\_concept\\_id = D.concept\\_id

AND D.vocabulary\\_id = VS.vocabulary\\_id

AND sysdate BETWEEN D.valid\\_start\\_date

AND D.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Child\\_Concept\\_ID |  Concept ID of child concept entered as input |

|  Child\\_Concept\\_Name |  Name of child concept entered as input |

|  Child\\_Concept\\_Code |  Concept Code of child concept entered as input |

|  Child\\_Concept\\_Class |  Concept Class of child concept entered as input |

|  Child\\_Concept\\_Vocab\\_ID |  ID of the vocabulary the child concept is derived from |

|  Child\\_Concept\\_Vocab\\_Name |  Name of the vocabulary the child concept is derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Child\\_Concept\\_ID |  4128705 |

|  Child\\_Concept\\_Name |  Haemorrhagic enteritis |

|  Child\\_Concept\\_Code |  235224000 |

|  Child\\_Concept\\_Class |  Clinical finding |

|  Child\\_Concept\\_Vocab\\_ID |  1 |

|  Child\\_Concept\\_Vocab\\_Name |  SNOMED-CT |

\*\*G12:\*\* List current vocabulary release number

This query returns current vocabulary release number.

\*\*Sample query:\*\*

SELECT vocabulary\\_name, vocabulary\\_version FROM vocabulary;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  vocabulary\\_name |  Version number of current OMOP vocabulary release |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  vocabulary\\_name |  OMOP Vocabulary v4.3 Q2-2013 |

\*\*G13:\*\* List available vocabularies

This query returns list of available vocabularies.

\*\*Sample query:\*\*

SELECT vocabulary\\_id, vocabulary\\_name FROM vocabulary WHERE vocabulary\\_id IS NOT NULL;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  vocabulary\\_id |  OMOP Vocabulary ID |

|  vocabulary\\_name |  Vocabulary name |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  vocabulary\\_id |  1 |

|  vocabulary\\_name |  SNOMED-CT |

\*\*G14:\*\* Statistics about relationships between concepts

This query produces list and frequency of all relationships between concepts (Standard and non-standard) and their class

\*\*Sample query:\*\*

SELECT

  R.relationship\\_id,

  R.relationship\\_name,

  C1.vocabulary\\_id from\\_vocabulary\\_id,

  V1.vocabulary\\_name from\\_vocabulary\\_name,

  C1.concept\\_class\\_id from\\_concept\\_class,

  C2.vocabulary\\_id to\\_vocabulary\\_id,

  V2.vocabulary\\_name to\\_vocabulary\\_name,

  C2.concept\\_class\\_id to\\_concept\\_class,

  count(\\*) num\\_records

FROM

  concept\\_relationship CR,

  concept C1,

  concept C2,

  relationship R,

  vocabulary V1,

  vocabulary V2

WHERE

  CR.concept\\_id\\_1 = C1.concept\\_id AND

  CR.concept\\_id\\_2 = C2.concept\\_id AND

  R.relationship\\_id = CR.relationship\\_id AND

  C1.vocabulary\\_id = V1.vocabulary\\_id AND

  C2.vocabulary\\_id = V2.vocabulary\\_id

GROUP BY

  R.relationship\\_id,

  relationship\\_name,

  C1.vocabulary\\_id,

  V1.vocabulary\\_name,

  C1.concept\\_class\\_id,

  C2.vocabulary\\_id,

  V2.vocabulary\\_name,

  C2.concept\\_class\\_id

ORDER BY

  R.relationship\\_id,

  C1.concept\\_class\\_id;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  relationship\\_id |  Identifier for the type of relationship |

|  relationship\\_name |  Name of the type of relationship |

|  from\\_vocabulary\\_id |  ID of the vocabulary of the input concepts |

|  from\\_vocabulary\\_name |  Name of the vocabulary of the input concepts |

|  from\\_concept\\_class |  Concept class of the input concepts |

|  to\\_vocabulary\\_id |  ID of the vocabulary the related concept is derived from |

|  to\\_vocabulary\\_name |  Name of the vocabulary the related concept is derived from |

|  to\\_concept\\_class |  Concept class the related concept is derived from |

|  num\\_records |  Number of records  |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  relationship\\_id |  1 |

|  relationship\\_name |  Concept replaced by (LOINC) |

|  from\\_vocabulary\\_id |  6 |

|  from\\_vocabulary\\_name |  LOINC |

|  from\\_concept\\_class |  LOINC Code |

|  to\\_vocabulary\\_id |  6 |

|  to\\_vocabulary\\_name |  LOINC |

|  to\\_concept\\_class |  LOINC Code |

|  num\\_records |  2022 |

\*\*G15:\*\* Statistic about Concepts, Vocabularies, Classes and Levels

### This query generates the list of all vocabularies in the CONCEPT table (Standard and non-standard), their class, level and frequency.

\*\*Sample query:\*\*

SELECT

  voc.vocabulary\\_id,

  r.vocabulary\\_name,

  voc.concept\\_class\\_id,

  voc.standard\\_concept,

  voc.cnt

FROM (

  SELECT

    vocabulary\\_id,

    concept\\_class\\_id,

    standard\\_concept,

    COUNT(concept\\_id) cnt

  FROM concept

  GROUP BY

    vocabulary\\_id,

    concept\\_class\\_id,

    standard\\_concept ) voc

JOIN vocabulary r ON voc.vocabulary\\_id=r.vocabulary\\_ID

ORDER BY 1,2,4,3;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  vocabulary\\_id |  OMOP Vocabulary ID |

|  vocabulary\\_name |  Vocabulary name |

|  concept\\_class |  Concept Class |

|  concept\\_level |  Concept Level Number |

|  cnt |  Number of concepts |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  vocabulary\\_id |  1 |

|  vocabulary\\_name |  SNOMED-CT |

|  concept\\_class |  Procedure |

|  concept\\_level |  2 |

|  cnt |  20286 |

\*\*G16:\*\* Statistics about Condition Mapping of Source Vocabularies

### The following query contains the coverage for mapped source vocabularies in the Condition domains to SNOMED-CT.

\*\*Sample query:\*\*

SELECT

  mapped.vocabulary\\_id,

  mapped.vocabulary\\_name,

  CASE mapped.standard\\_concept

    WHEN null THEN 'Not mapped'

        ELSE mapped.standard\\_concept

  END AS standard\\_concept,

  mapped.mapped\\_codes,

  sum(mapped.mapped\\_codes) over (partition by vocabulary\\_id) as total\\_mapped\\_codes,

  to\\_char(mapped.mapped\\_codes\\*100/sum(mapped.mapped\\_codes) over (partition by vocabulary\\_id), '990.9') AS pct\\_mapped\\_codes,

  mapped.mapped\\_concepts,

  (SELECT count(1)

   FROM concept

   WHERE

     vocabulary\\_id='SNOMED' AND

        standard\\_concept=mapped.standard\\_concept AND

        lower(concept\\_class\\_id)='clinical finding' AND

        invalid\\_reason is null

  ) AS standard\\_concepts,

  to\\_char(mapped.mapped\\_concepts\\*100/

         ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                  FROM concept

                  WHERE

                    vocabulary\\_id='SNOMED' AND

                        standard\\_concept=mapped.standard\\_concept AND

                        lower(concept\\_class\\_id)='clinical finding' AND

                        invalid\\_reason is null ), '990.9'

  ) AS pct\\_mapped\\_concepts

FROM (

  SELECT

    c1.vocabulary\\_id AS vocabulary\\_id,

        v.vocabulary\\_name,

        c2.standard\\_concept,

        COUNT(8) AS mapped\\_codes,

        COUNT(DISTINCT c2.concept\\_id) AS mapped\\_concepts

  FROM concept\\_relationship m

  JOIN concept c1 on m.concept\\_id\\_1=c1.concept\\_id and

       m.relationship\\_id='Maps to' and m.invalid\\_reason is null

  JOIN concept c2 on c2.concept\\_id=m.concept\\_id\\_2

  JOIN vocabulary v on v.vocabulary\\_id=c1.vocabulary\\_id

  WHERE c2.vocabulary\\_id='SNOMED' AND lower(c2.domain\\_id)='condition'

  GROUP BY c1.vocabulary\\_id, v.vocabulary\\_name, c2.standard\\_concept

) mapped;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  vocabulary\\_id |  Source Vocabulary ID |

|  vocabulary\\_name |  Source Vocabulary name |

|  concept\\_level |  Concept Level Number |

|  mapped\\_codes |  Number of mapped codes |

|  total\\_mapped\\_codes |  Total number of mapped codes for source vocabulary |

|  pct\\_mapped\\_codes |  Percentile of mapped code  |

|  mapped\\_concepts |  Number of mapped concepts  |

|  concepts\\_in\\_level |  Number of mapped concepts  |

|  pct\\_mapped\\_concepts |  Percentile of of mapped concepts |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  vocabulary\\_id |  2 |

|  vocabulary\\_name |  ICD9-CT |

|  concept\\_level |  1 |

|  mapped\\_codes |  4079 |

|  total\\_mapped\\_codes |  10770 |

|  pct\\_mapped\\_codes |  37.0 |

|  mapped\\_concepts |  3733 |

|  concepts\\_in\\_level |  69280 |

|  pct\\_mapped\\_concepts |  5.0 |

\*\*G17:\*\* Statistics about Drugs Mapping of Source Vocabularies

The following query contains the coverage for mapped source vocabularies in the Drug domains to RxNorm.

\*\*Sample query:\*\*

SELECT

  mapped.vocabulary\\_id,

  mapped.vocabulary\\_name,

  CASE mapped.standard\\_concept

    WHEN null THEN 'Not mapped'

        ELSE mapped.standard\\_concept

  END AS standard\\_concept,

  mapped.mapped\\_codes,

  sum(mapped.mapped\\_codes) over (partition by vocabulary\\_id) as total\\_mapped\\_codes,

  to\\_char(mapped.mapped\\_codes\\*100/sum(mapped.mapped\\_codes) over (partition by vocabulary\\_id), '990.9') AS pct\\_mapped\\_codes,

  mapped.mapped\\_concepts,

  (SELECT count(1)

   FROM concept

   WHERE

     vocabulary\\_id='RxNorm' AND

        standard\\_concept=mapped.standard\\_concept AND

        invalid\\_reason is null

  ) AS standard\\_concepts,

  to\\_char(mapped.mapped\\_concepts\\*100/

         ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                  FROM concept

                  WHERE

                    vocabulary\\_id='RxNorm' AND

                        standard\\_concept=mapped.standard\\_concept AND

                        invalid\\_reason is null ), '990.9'

  ) AS pct\\_mapped\\_concepts

FROM (

  SELECT

    c1.vocabulary\\_id AS vocabulary\\_id,

        v.vocabulary\\_name,

        c2.standard\\_concept,

        COUNT(8) AS mapped\\_codes,

        COUNT(DISTINCT c2.concept\\_id) AS mapped\\_concepts

  FROM concept\\_relationship m

  JOIN concept c1 on m.concept\\_id\\_1=c1.concept\\_id and

       m.relationship\\_id='Maps to' and m.invalid\\_reason is null

  JOIN concept c2 on c2.concept\\_id=m.concept\\_id\\_2

  JOIN vocabulary v on v.vocabulary\\_id=c1.vocabulary\\_id

  WHERE c2.vocabulary\\_id in ('ICD9CM','RxNorm') AND lower(c2.domain\\_id)='drug'

  GROUP BY c1.vocabulary\\_id, v.vocabulary\\_name, c2.standard\\_concept

) mapped;

\*\*Input:\*\*

None

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  vocabulary\\_id |  Source Vocabulary ID |

|  vocabulary\\_name |  Source Vocabulary name |

|  concept\\_level |  Concept Level Number |

|  mapped\\_codes |  Number of mapped codes |

|  total\\_mapped\\_codes |  Total number of mapped codes for source vocabulary |

|  pct\\_mapped\\_codes |  Percentile of mapped code  |

|  mapped\\_concepts |  Number of mapped concepts  |

|  concepts\\_in\\_level |  Number of mapped concepts  |

|  pct\\_mapped\\_concepts |  Percentile of of mapped concepts |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  vocabulary\\_id |  9 |

|  vocabulary\\_name |  NDC |

|  concept\\_level |  1 |

|  mapped\\_codes |  550959 |

|  total\\_mapped\\_codes |  551757 |

|  pct\\_mapped\\_codes |  99.0 |

|  mapped\\_concepts |  33206 |

|  concepts\\_in\\_level |  57162 |

|  pct\\_mapped\\_concepts |  58.0 |
