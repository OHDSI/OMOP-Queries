General Queries
---

G01: Find concept by concept ID
---

This is the most generic look-up for obtaining concept details associated with a concept identifier. The query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.

Sample query:

    SELECT C.concept_id, C.concept_name, C.concept_code, C.concept_class_id, C.standard_concept, C.vocabulary_id, V.vocabulary_name

    FROM concept C, vocabulary V

    WHERE C.concept_id = 192671

    AND C.vocabulary_id = V.vocabulary_id

    AND sysdate BETWEEN valid_start_date

    AND valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | Concept Identifier for "GI - Gastrointestinal hemorrhage" |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Concept_ID |  Concept Identifier entered as input |
|  Concept_Name |  Name of the standard concept |
|  Concept_Code |  Concept code of the standard concept in the source vocabulary |
|  Concept_Class |  Concept class of standard vocabulary concept |
|  Concept_Level |  Level of the concept if defined as part of a hierarchy |
|  Vocabulary_ID |  Vocabulary the standard concept is derived from as vocabulary code |
|  Vocabulary_Name |  Name of the vocabulary the standard concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Concept_ID |  192671 |
|  Concept_Name |  GI - Gastrointestinal haemorrhage |
|  Concept_Code |  74474003 |
|  Concept_Class |  Clinical finding |
|  Concept_Level |  2 |
|  Vocabulary_ID |  1 |
|  Vocabulary_Name |  SNOMED-CT |

G04: Find synonyms for a given concept
---

This query extracts all synonyms in the vocabulary for a given Concept ID.

Sample query:

    SELECT C.concept_id, S.concept_synonym_name

    FROM concept C, concept_synonym S, vocabulary V

    WHERE C.concept_id = 192671

    AND C.concept_id = S.concept_id

    AND C.vocabulary_id = V.vocabulary_id

    AND sysdate BETWEEN C.valid_start_date AND C.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Concept_ID |  Unique identifier of the concept related to the input concept |
|  Concept_Synonym_Name |  Synonym of the concept |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Concept_ID |  192671 |
|  Concept_Synonym_Name |  GI bleeding |

G05: Translate a code from a source to a standard vocabulary.
---

This query enables search of all Standard Vocabulary concepts that are mapped to a code from a specified source vocabulary. It will return all possible concepts that are mapped to it, as well as the target vocabulary. The source code could be obtained using queries G02 or G03.
Note that to unambiguously identify a source code, the vocabulary id has to be provided, as source codes are not unique identifiers across different vocabularies.

Sample query:

    SELECT DISTINCT

            c1.domain_id,

            c2.concept_id         as Concept_Id,

            c2.concept_name       as Concept_Name,

            c2.concept_code       as Concept_Code,

            c2.concept_class_id      as Concept_Class,

            c2.vocabulary_id      as Concept_Vocabulary_ID,

                      c2.domain_id                  as Target_concept_Domain

    FROM concept_relationship cr

    JOIN concept c1 ON c1.concept_id = cr.concept_id_1

    JOIN concept c2 ON c2.concept_id = cr.concept_id_2

    WHERE cr.relationship_id = 'Maps to'

    AND c1.concept_code IN ('070.0')

    AND c1.vocabulary_id = 'ICD9CM'

    AND sysdate BETWEEN cr.valid_start_date AND cr.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Source Code List |  '070.0' |  Yes |  Source codes are alphanumeric |
|  Source Vocabulary ID |  2 |  Yes | The source vocabulary ID is mandatory, because the source code is not unique across different vocabularies.

The list of vocabulary codes is listed in the VOCABULARY table. Vocabulary ID of 2 represents ICD9-CM |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Mapping_Type |  Type of mapping from source code to target concept |
|  Target_Concept_Id |  Concept ID of mapped concept |
|  Target_Concept_Name |  Name of mapped concept |
|  Target_Concept_Code |  Concept code of mapped concept |
|  Target_Concept_Class |  Class of the mapped concept |
|  Target_Concept_Vocab_ID |  Vocabulary ID of the target vocabulary |
|  Target_Concept_Vocab_Name |  Name of the vocabulary the target concept is part of |
|  Target_Concept_Domain |  Vocabulary domain that includes the entity. The domains include:
DRUG, CONDITION, PROCEDURE, OBSERVATION, OBSERVATION UNIT, VISIT, DEMOGRAPHIC, DEATH, COST, PROVIDER |

Sample output record:

| Field |  Value |
| --- | --- |
|  Mapping_Type |  CONDITION-MEDDRA |
|  Target_Concept_Id |  35909589 |
|  Target_Concept_Name |  Hepatitis viral |
|  Target_Concept_Code |  10019799 |
|  Target_Concept_Class |  Preferred Term |
|  Target_Concept_Vocab_ID |  15 |
|  Target_Concept_Vocab_Name |  MedDRA |
|  Target_Concept_Domain |  CONDITION |

G06: Find concepts and their descendants that are covered by a given source code
---

This query returns all concepts that are direct maps and the descendants of these directly mapped concepts. This is useful if the target standard vocabulary is organized in a tall hierarchy, while the source vocabulary organization is flat.

Additional constraints can be added at the end of the query if only a specific target domain or target vocabulary is desired. For example, if only SNOMED-CT as the standard vocabulary for conditions needs be returned, the target vocabulary can be set to 1.

In the query only FDB indications and contraindications are returned, but not NDF-RT indications or contraindications. That is because no direct mapping between ICD-9-CM and NDF-RT exists. In order to query for drug indications please see queries D12 through D18.

Sample query:

    WITH dm AS ( -- collect direct maps

    SELECT  c1.concept_code as source_code,

            c1.vocabulary_id,

            c1.domain_id,

            c2.concept_id        as target_concept_id,

            c2.concept_name      as target_concept_name,

            c2.concept_code      as target_concept_code,

            c2.concept_class_id     as target_concept_class,

            c2.vocabulary_id     as target_concept_vocab_id,

            'Direct map'        as target_Type

    FROM    concept_relationship cr

                    JOIN concept c1 ON cr.concept_id_1 = c1.concept_id

                    JOIN concept c2 ON cr.concept_id_2 = c2.concept_id

    WHERE   cr.relationship_id = 'Maps to'

    AND                c1.concept_code IN ('410.0')

    AND     c1.vocabulary_id = 'ICD9CM'

    AND     sysdate BETWEEN cr.valid_start_date AND cr.valid_end_date )

    SELECT dm.source_code,

            dm.vocabulary_id,

            dm.domain_id,

            dc.concept_id        AS        target_concept_id,

            dc.concept_name        AS target_concept_name,

            dc.concept_code AS target_concept_code,

            dc.concept_class_id AS target_concept_class,

            dc.vocabulary_id AS target_concept_vocab_id,

        'Descendant of direct map' as target_Type

    FROM concept_ancestor ca -- collect descendants which includes ancestor itself

    JOIN dm ON ca.ancestor_concept_id = dm.target_concept_id

    JOIN concept dc ON ca.descendant_concept_id = dc.concept_id

    WHERE dc.standard_concept = 'S';

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Source Code List |  '410.0' |  Yes | Source codes are alphanumeric. |
|  Source Vocabulary ID |  2 |  Yes | 2 represents ICD9-CM.

The list of vocabulary codes can be found in the VOCABULARY table. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Mapping_Type |  Type of mapping from source code to target concept |
|  Target_Concept_ID |  Concept ID of mapped concept |
|  Target_Concept_Name |  Concept name of mapped concept |
|  Target_Concept_Code |  Concept Code of mapped concept |
|  Target_Concept_Class |  Concept class of mapped concept |
|  Target_Concept_Vocab_ID |  ID of the target vocabulary |
|  Target_Concept_Vocab_Name |  Name of the vocabulary the target concept is part of |
|  Target_Type |   Type of result, indicates how the target concepts was extracted. Includes:
- Concepts that are direct maps
- Concepts that are descendants of direct maps
 |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Mapping_Type |  CONDITION |
|  Target_Concept_ID |  312327 |
|  Target_Concept_Name |  Acute myocardial infarction |
|  Target_Concept_Code |  57054005 |
|  Target_Concept_Class |  Clinical finding |
|  Target_Concept_Vocab_ID |  1 |
|  Target_Concept_Vocab_Name |  SNOMED-CT |
|  Target_Type |  Direct map |

G07: Find concepts that have a relationship with a given concept
---

For a concept identifier entered as the input parameter, the query lists all existing relationships with other concepts. The resulting output includes:

- Type of relationship (including both relationship ID and description)
- Details of the other concept to which the relationship has been defined
- Polarity of the relationship

o    Polarity of "Relates to" implies the input concept is the first concept or CONCEPT_ID_1 of the relationship

o    Polarity of "Is Related by" implies the input concept is the second concept or CONCEPT_ID_2 of the relationship

In vocabulary Version 4.0 and above all relationships are bi-directional, ie. all relationships are repeated as a mirrored version, where CONCEPT_ID_1 and CONCEPT_ID_2 are swapped and the inverse relationship ID is provided.

Sample query:

    SELECT 'Relates to' relationship_polarity, CR.relationship_ID, RT.relationship_name, D.concept_Id concept_id, D.concept_Name concept_name, D.concept_Code concept_code, D.concept_class_id concept_class_id, D.vocabulary_id concept_vocab_ID, VS.vocabulary_name concept_vocab_name

    FROM concept_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

    WHERE CR.concept_id_1 = A.concept_id

    AND A.vocabulary_id = VA.vocabulary_id

    AND CR.concept_id_2 = D.concept_id

    AND D.vocabulary_id = VS.vocabulary_id

    AND CR.relationship_id = RT.relationship_ID

    AND A.concept_id = 192671

    AND sysdate BETWEEN CR.valid_start_date

    AND CR.valid_end_date

    UNION ALL SELECT 'Is related by' relationship_polarity, CR.relationship_ID, RT.relationship_name, A.concept_Id concept_id, A.concept_name concept_name, A.concept_code concept_code, A.concept_class_id concept_class_id, A.vocabulary_id concept_vocab_ID, VA.Vocabulary_Name concept_vocab_name

    FROM concept_relationship CR, concept A, concept D, vocabulary VA, vocabulary VS, relationship RT

    WHERE CR.concept_id_1 = A.concept_id

    AND A.vocabulary_id = VA.vocabulary_id

    AND CR.concept_id_2 = D.concept_id

    AND D.vocabulary_id = VS.vocabulary_id

    AND CR.relationship_id = RT.relationship_ID

    AND D.concept_id = 192671

    AND sysdate BETWEEN CR.valid_start_date

    AND CR.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Relationship_Polarity |  Polarity of the relationship with the input concept as a reference:
- "Relates to": Indicates input concept is CONCEPT_ID_1 or the first concept of the relationship
- "Is Related by": Indicates input concept
 |
|  Relationship_ID |  Identifier for the type of relationship |
|  Relationship_Name |  Name of the type of relationship |
|  Concept_ID |  Unique identifier of the concept related to the input concept |
|  Concept_Name |  Name of the concept related to the input concept |
|  Concept_Code |  Concept code of concept related to the input concept |
|  Concept_Class |  Concept Class of concept related to the input concept |
|  Concept_Vocab_ID |  ID of the vocabulary the related concept is derived from |
|  Concept_Vocab_Name |  Name of the vocabulary the related concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Relationship_Polarity |  Is Related to |
|  Relationship_ID |  125 |
|  Relationship_Name |  MedDRA to SNOMED-CT equivalent (OMOP) |
|  Concept_ID |  35707864 |
|  Concept_Name |  Gastrointestinal haemorrhage |
|  Concept_Code |  10017955 |
|  Concept_Class |  Preferred Term |
|  Concept_Vocab_ID |  15 |
|  Concept_Vocab_Name |  MedDRA |


G08: Find ancestors for a given concept
---

For a concept identifier entered as the input parameter, this query lists all ancestors in the hierarchy of the domain. Ancestors are concepts that have a relationship to the given concept and is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going up in the hierarchy. The resulting output provides the ancestor concept details and the minimum and maximum level of separation.

Sample query:

    SELECT C.concept_id as ancestor_concept_id, C.concept_name as ancestor_concept_name, C.concept_code as ancestor_concept_code, C.concept_class_id as ancestor_concept_class_id, C.vocabulary_id, VA.vocabulary_name, A.min_levels_of_separation, A.max_levels_of_separation

    FROM concept_ancestor A, concept C, vocabulary VA

    WHERE A.ancestor_concept_id = C.concept_id

    AND C.vocabulary_id = VA.vocabulary_id

    AND A.ancestor_concept_id<>A.descendant_concept_id

    AND A.descendant_concept_id = 192671

    AND sysdate BETWEEN valid_start_date

    AND valid_end_date

    ORDER BY 5,7;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Ancestor_Concept_ID |  Unique identifier of the concept related to the ancestor concept |
|  Ancestor_Concept_Name |  Name of the concept related to the ancestor concept |
|  Ancestor_Concept_Code |  Concept code of concept related to the ancestor concept |
|  Ancestor_Concept_>Class |  Concept Class of concept related to the ancestor concept |
|  Vocabulary_ID |  ID of the vocabulary the ancestor concept is derived from |
|  Vocabulary_Name |  Name of the vocabulary the ancestor concept is derived from |
|  Min_Levels_of_Separation |  The length of the shortest path between the concept and the ancestor |
|  Max_Levels_of_Separation |  The length of the longest path between the concept and the ancestor |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Ancestor_Concept_ID |  4000610 |
|  Ancestor_Concept_Name |  Disease of gastrointestinal tract |
|  Ancestor_Concept_Code |  119292006 |
|  Ancestor_Concept_Class |  Clinical finding |
|  Vocabulary_ID |  1 |
|  Vocabulary_Name |  SNOMED-CT |
|  Min_Levels_of_Separation |  1 |
|  Max_Levels_of_Separation |  1 |

G09: Find descendants for a given concept
---

For a concept identifier entered as the input parameter, this query lists all descendants in the hierarchy of the domain. Descendant are concepts have a relationship to the given concept that is defined as hierarchical in the relationship table, and any secondary, tertiary etc. concepts going down in the hierarchy. The resulting output provides the descendant concept details and the minimum and maximum level of separation.

Sample query:

    SELECT C.concept_id as descendant_concept_id, C.concept_name as descendant_concept_name, C.concept_code as descendant_concept_code, C.concept_class_id as descendant_concept_class_id, C.vocabulary_id, VA.vocabulary_name, A.min_levels_of_separation, A.max_levels_of_separation

    FROM concept_ancestor A, concept C, vocabulary VA

    WHERE A.descendant_concept_id = C.concept_id

    AND C.vocabulary_id = VA.vocabulary_id

    AND A.ancestor_concept_id <> A.descendant_concept_id

    AND A.ancestor_concept_id = 192671

    AND sysdate BETWEEN valid_start_date

    AND valid_end_date

    ORDER BY 5,7;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Descendant_Concept_ID |  Unique identifier of the concept related to the descendant concept |
|  Descendant_Concept_Name |  Name of the concept related to the descendant concept |
|  Descendant_Concept_Code |  Concept code of concept related to the descendant concept |
|  Descendant_Concept_Class |  Concept Class of concept related to the descendant concept |
|  Vocabulary_ID |  ID of the vocabulary the descendant concept is derived from |
|  Vocabulary_Name; |  Name of the vocabulary the descendant concept is derived from |
|  Min_Levels_of_Separation |  The length of the shortest path between the concept and the descendant |
|  Max_Levels_of_Separation |  The length of the longest path between the concept and the descendant |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Descendant_Concept_ID |  4318535 |
|  Descendant_Concept_Name |  Duodenal haemorrhage |
|  Descendant_Concept_Code |  95533003 |
|  Descendant_Concept_Class |  Clinical finding |
|  Vocabulary_ID |  1 |
|  Vocabulary_Name |  SNOMED-CT |
|  Min_Levels_of_Separation |  1 |
|  Max_Levels_of_Separation |  1 |

G10: Find parents for a given concept
---

This query accepts a concept ID as the input and returns all concepts that are its immediate parents of that concept. Parents are concepts that have a hierarchical relationship to the given concepts. Hierarchical relationships are defined in the relationship table.
The query returns only the immediate parent concepts that are directly linked to the input concept and not all ancestors.

Sample query:

    SELECT A.concept_id Parent_concept_id, A.concept_name Parent_concept_name, A.concept_code Parent_concept_code, A.concept_class_id Parent_concept_class_id, A.vocabulary_id Parent_concept_vocab_ID, VA.vocabulary_name Parent_concept_vocab_name

    FROM concept_ancestor CA, concept A, concept D, vocabulary VA

    WHERE CA.descendant_concept_id = 192671

    AND CA.min_levels_of_separation = 1

    AND CA.ancestor_concept_id = A.concept_id

    AND A.vocabulary_id = VA.vocabulary_id

    AND CA.descendant_concept_id = D.concept_id

    AND sysdate BETWEEN A.valid_start_date

    AND A.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Parent_Concept_ID |  Concept ID of parent concept |
|  Parent_Concept_Name |  Name of parent concept |
|  Parent_Concept_Code |  Concept Code of parent concept |
|  Parent_Concept_Class |  Concept Class of parent concept |
|  Parent_Concept_Vocab_ID |  Vocabulary parent concept is derived from as vocabulary code |
|  Parent_Concept_Vocab_Name |  Name of the vocabulary the child concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Parent_Concept_ID |  4000610 |
|  Parent_Concept_Name |  Disease of gastrointestinal tract |
|  Parent_Concept_Code |  119292006 |
|  Parent_Concept_Class |  Clinical finding |
|  Parent_Concept_Vocab_ID |  1 |
|  Parent_Concept_Vocab_Name |  SNOMED-CT |

G11: Find children for a given concept
---

This query lists all standard vocabulary concepts that are child concepts of a given concept entered as input. The query accepts a concept ID as the input and returns all concepts that are its immediate child concepts.

The query returns only the immediate child concepts that are directly linked to the input concept and not all descendants.

Sample query:

    SELECT D.concept_id Child_concept_id, D.concept_name Child_concept_name, D.concept_code Child_concept_code, D.concept_class_id Child_concept_class_id, D.vocabulary_id Child_concept_vocab_ID, VS.vocabulary_name Child_concept_vocab_name

    FROM concept_ancestor CA, concept D, vocabulary VS

    WHERE CA.ancestor_concept_id = 192671

    AND CA.min_levels_of_separation = 1

    AND CA.descendant_concept_id = D.concept_id

    AND D.vocabulary_id = VS.vocabulary_id

    AND sysdate BETWEEN D.valid_start_date

    AND D.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  192671 |  Yes | GI - Gastrointestinal hemorrhage |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Child_Concept_ID |  Concept ID of child concept entered as input |
|  Child_Concept_Name |  Name of child concept entered as input |
|  Child_Concept_Code |  Concept Code of child concept entered as input |
|  Child_Concept_Class |  Concept Class of child concept entered as input |
|  Child_Concept_Vocab_ID |  ID of the vocabulary the child concept is derived from |
|  Child_Concept_Vocab_Name |  Name of the vocabulary the child concept is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Child_Concept_ID |  4128705 |
|  Child_Concept_Name |  Haemorrhagic enteritis |
|  Child_Concept_Code |  235224000 |
|  Child_Concept_Class |  Clinical finding |
|  Child_Concept_Vocab_ID |  1 |
|  Child_Concept_Vocab_Name |  SNOMED-CT |

G12: List current vocabulary release number
---

This query returns current vocabulary release number.

Sample query:

    SELECT vocabulary_name, vocabulary_version FROM vocabulary;

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  vocabulary_name |  Version number of current OMOP vocabulary release |

Sample output record:

| Field |  Value |
| --- | --- |
|  vocabulary_name |  OMOP Vocabulary v4.3 Q2-2013 |


G13: List available vocabularies
---

This query returns list of available vocabularies.

Sample query:

    SELECT vocabulary_id, vocabulary_name FROM vocabulary WHERE vocabulary_id IS NOT NULL;

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  vocabulary_id |  OMOP Vocabulary ID |
|  vocabulary_name |  Vocabulary name |

Sample output record:

| Field |  Value |
| --- | --- |
|  vocabulary_id |  1 |
|  vocabulary_name |  SNOMED-CT |

G14: Statistics about relationships between concepts
---

This query produces list and frequency of all relationships between concepts (Standard and non-standard) and their class

Sample query:

    SELECT

      R.relationship_id,

      R.relationship_name,

      C1.vocabulary_id from_vocabulary_id,

      V1.vocabulary_name from_vocabulary_name,

      C1.concept_class_id from_concept_class,

      C2.vocabulary_id to_vocabulary_id,

      V2.vocabulary_name to_vocabulary_name,

      C2.concept_class_id to_concept_class,

      count(\*) num_records

    FROM

      concept_relationship CR,

      concept C1,

      concept C2,

      relationship R,

      vocabulary V1,

      vocabulary V2

    WHERE

      CR.concept_id_1 = C1.concept_id AND

      CR.concept_id_2 = C2.concept_id AND

      R.relationship_id = CR.relationship_id AND

      C1.vocabulary_id = V1.vocabulary_id AND

      C2.vocabulary_id = V2.vocabulary_id

    GROUP BY

      R.relationship_id,

      relationship_name,

      C1.vocabulary_id,

      V1.vocabulary_name,

      C1.concept_class_id,

      C2.vocabulary_id,

      V2.vocabulary_name,

      C2.concept_class_id

    ORDER BY

      R.relationship_id,

      C1.concept_class_id;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  relationship_id |  Identifier for the type of relationship |
|  relationship_name |  Name of the type of relationship |
|  from_vocabulary_id |  ID of the vocabulary of the input concepts |
|  from_vocabulary_name |  Name of the vocabulary of the input concepts |
|  from_concept_class |  Concept class of the input concepts |
|  to_vocabulary_id |  ID of the vocabulary the related concept is derived from |
|  to_vocabulary_name |  Name of the vocabulary the related concept is derived from |
|  to_concept_class |  Concept class the related concept is derived from |
|  num_records |  Number of records  |

Sample output record:

|  Field |  Value |
| --- | --- |
|  relationship_id |  1 |
|  relationship_name |  Concept replaced by (LOINC) |
|  from_vocabulary_id |  6 |
|  from_vocabulary_name |  LOINC |
|  from_concept_class |  LOINC Code |
|  to_vocabulary_id |  6 |
|  to_vocabulary_name |  LOINC |
|  to_concept_class |  LOINC Code |
|  num_records |  2022 |

G15: Statistic about Concepts, Vocabularies, Classes and Levels
---

This query generates the list of all vocabularies in the CONCEPT table (Standard and non-standard), their class, level and frequency.

Sample query:

    SELECT

      voc.vocabulary_id,

      r.vocabulary_name,

      voc.concept_class_id,

      voc.standard_concept,

      voc.cnt

    FROM (

      SELECT

        vocabulary_id,

        concept_class_id,

        standard_concept,

        COUNT(concept_id) cnt

      FROM concept

      GROUP BY

        vocabulary_id,

        concept_class_id,

        standard_concept ) voc

    JOIN vocabulary r ON voc.vocabulary_id=r.vocabulary_ID

    ORDER BY 1,2,4,3;

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  vocabulary_id |  OMOP Vocabulary ID |
|  vocabulary_name |  Vocabulary name |
|  concept_class |  Concept Class |
|  concept_level |  Concept Level Number |
|  cnt |  Number of concepts |

Sample output record:

|  Field |  Value |
| --- | --- |
|  vocabulary_id |  1 |
|  vocabulary_name |  SNOMED-CT |
|  concept_class |  Procedure |
|  concept_level |  2 |
|  cnt |  20286 |

G16: Statistics about Condition Mapping of Source Vocabularies
---

The following query contains the coverage for mapped source vocabularies in the Condition domains to SNOMED-CT.

Sample query:

    SELECT

      mapped.vocabulary_id,

      mapped.vocabulary_name,

      CASE mapped.standard_concept

        WHEN null THEN 'Not mapped'

            ELSE mapped.standard_concept

      END AS standard_concept,

      mapped.mapped_codes,

      sum(mapped.mapped_codes) over (partition by vocabulary_id) as total_mapped_codes,

      to_char(mapped.mapped_codes\*100/sum(mapped.mapped_codes) over (partition by vocabulary_id), '990.9') AS pct_mapped_codes,

      mapped.mapped_concepts,

      (SELECT count(1)

       FROM concept

       WHERE

         vocabulary_id='SNOMED' AND

            standard_concept=mapped.standard_concept AND

            lower(concept_class_id)='clinical finding' AND

            invalid_reason is null

      ) AS standard_concepts,

      to_char(mapped.mapped_concepts\*100/

             ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                      FROM concept

                      WHERE

                        vocabulary_id='SNOMED' AND

                            standard_concept=mapped.standard_concept AND

                            lower(concept_class_id)='clinical finding' AND

                            invalid_reason is null ), '990.9'

      ) AS pct_mapped_concepts

    FROM (

      SELECT

        c1.vocabulary_id AS vocabulary_id,

            v.vocabulary_name,

            c2.standard_concept,

            COUNT(8) AS mapped_codes,

            COUNT(DISTINCT c2.concept_id) AS mapped_concepts

      FROM concept_relationship m

      JOIN concept c1 on m.concept_id_1=c1.concept_id and

           m.relationship_id='Maps to' and m.invalid_reason is null

      JOIN concept c2 on c2.concept_id=m.concept_id_2

      JOIN vocabulary v on v.vocabulary_id=c1.vocabulary_id

      WHERE c2.vocabulary_id='SNOMED' AND lower(c2.domain_id)='condition'

      GROUP BY c1.vocabulary_id, v.vocabulary_name, c2.standard_concept

    ) mapped;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
|  vocabulary_id |  Source Vocabulary ID |
|  vocabulary_name |  Source Vocabulary name |
|  concept_level |  Concept Level Number |
|  mapped_codes |  Number of mapped codes |
|  total_mapped_codes |  Total number of mapped codes for source vocabulary |
|  pct_mapped_codes |  Percentile of mapped code  |
|  mapped_concepts |  Number of mapped concepts  |
|  concepts_in_level |  Number of mapped concepts  |
|  pct_mapped_concepts |  Percentile of of mapped concepts |

Sample output record:

| Field |  Value |
| --- | --- |
|  vocabulary_id |  2 |
|  vocabulary_name |  ICD9-CT |
|  concept_level |  1 |
|  mapped_codes |  4079 |
|  total_mapped_codes |  10770 |
|  pct_mapped_codes |  37.0 |
|  mapped_concepts |  3733 |
|  concepts_in_level |  69280 |
|  pct_mapped_concepts |  5.0 |

G17: Statistics about Drugs Mapping of Source Vocabularies
---

The following query contains the coverage for mapped source vocabularies in the Drug domains to RxNorm.

Sample query:

    SELECT

      mapped.vocabulary_id,

      mapped.vocabulary_name,

      CASE mapped.standard_concept

        WHEN null THEN 'Not mapped'

            ELSE mapped.standard_concept

      END AS standard_concept,

      mapped.mapped_codes,

      sum(mapped.mapped_codes) over (partition by vocabulary_id) as total_mapped_codes,

      to_char(mapped.mapped_codes\*100/sum(mapped.mapped_codes) over (partition by vocabulary_id), '990.9') AS pct_mapped_codes,

      mapped.mapped_concepts,

      (SELECT count(1)

       FROM concept

       WHERE

         vocabulary_id='RxNorm' AND

            standard_concept=mapped.standard_concept AND

            invalid_reason is null

      ) AS standard_concepts,

      to_char(mapped.mapped_concepts\*100/

             ( SELECT CASE count(1) WHEN 0 THEN 1e16 ELSE count(1) END

                      FROM concept

                      WHERE

                        vocabulary_id='RxNorm' AND

                            standard_concept=mapped.standard_concept AND

                            invalid_reason is null ), '990.9'

      ) AS pct_mapped_concepts

    FROM (

      SELECT

        c1.vocabulary_id AS vocabulary_id,

            v.vocabulary_name,

            c2.standard_concept,

            COUNT(8) AS mapped_codes,

            COUNT(DISTINCT c2.concept_id) AS mapped_concepts

      FROM concept_relationship m

      JOIN concept c1 on m.concept_id_1=c1.concept_id and

           m.relationship_id='Maps to' and m.invalid_reason is null

      JOIN concept c2 on c2.concept_id=m.concept_id_2

      JOIN vocabulary v on v.vocabulary_id=c1.vocabulary_id

      WHERE c2.vocabulary_id in ('ICD9CM','RxNorm') AND lower(c2.domain_id)='drug'

      GROUP BY c1.vocabulary_id, v.vocabulary_name, c2.standard_concept

    ) mapped;

Input:

None

Output:

| Field |  Description |
| --- | --- |
|  vocabulary_id |  Source Vocabulary ID |
|  vocabulary_name |  Source Vocabulary name |
|  concept_level |  Concept Level Number |
|  mapped_codes |  Number of mapped codes |
|  total_mapped_codes |  Total number of mapped codes for source vocabulary |
|  pct_mapped_codes |  Percentile of mapped code  |
|  mapped_concepts |  Number of mapped concepts  |
|  concepts_in_level |  Number of mapped concepts  |
|  pct_mapped_concepts |  Percentile of of mapped concepts |

Sample output record:

| Field |  Value |
| --- | --- |
|  vocabulary_id |  9 |
|  vocabulary_name |  NDC |
|  concept_level |  1 |
|  mapped_codes |  550959 |
|  total_mapped_codes |  551757 |
|  pct_mapped_codes |  99.0 |
|  mapped_concepts |  33206 |
|  concepts_in_level |  57162 |
|  pct_mapped_concepts |  58.0 |





