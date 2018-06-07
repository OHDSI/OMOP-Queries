D01: Find drug concept by concept ID
---

This is the lookup for obtaining drug concept details associated with a concept identifier. This query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.
This query is equivalent to  [G01](http://vocabqueries.omop.org/general-queries/g1), but if the concept is not in the drug domain the query still returns the concept details with the Is_Drug_Concept_Flag field set to 'No'.

Sample query:

        SELECT

                C.concept_id Drug_concept_id,

                C.concept_name Drug_concept_name,

                C.concept_code Drug_concept_code,

                C.concept_class_id Drug_concept_class,

                C.standard_concept Drug_concept_level,

                C.vocabulary_id Drug_concept_vocab_id,

                V.vocabulary_name Drug_concept_vocab_code,

                /\*( CASE C.vocabulary_id

                        WHEN 'RxNorm' THEN

                                CASE lower(C.concept_class_id)

                                WHEN 'clinical drug' THEN 'Yes'

                                WHEN 'branded drug' THEN 'Yes'

                                WHEN 'ingredient' THEN 'Yes'

                                WHEN 'branded pack' THEN 'Yes'

                                WHEN 'clinical pack' THEN 'Yes'

                                ELSE 'No' END

                        ELSE 'No' END) Is_Drug_Concept_flag \*/

                (CASE C.domain_id WHEN 'Drug' THEN 'Yes' ELSE 'No' END) Is_Drug_Concept_flag

        FROM

                full_201706_omop_v5.concept C,

                full_201706_omop_v5.vocabulary V

        WHERE

                C.vocabulary_id = V.vocabulary_id

                AND sysdate BETWEEN C.valid_start_date AND C.valid_end_date

                AND C.concept_id = 1545999;



Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Concept ID |  1545999 |  Yes | Concept Identifier from RxNorm for 'atorvastatin 20 MG Oral Tablet [Lipitor]' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept Identifier entered as input |
|  Drug_Concept_Name |  Name of the standard drug concept |
|  Drug_Concept_Code |  Concept code of the standard drug concept in the source vocabulary |
|  Drug_Concept_Class |  Concept class of standard drug concept |
|  Drug_Concept_Level |  Level of the concept if defined as part of a hierarchy |
|  Drug_Concept_Vocab_ID |  Vocabulary the standard drug concept is derived from as vocabulary ID |
|  Drug_Concept_Vocab_Name |  Name of the vocabulary the standard drug concept is derived from |
|  Is_Drug_Concept_Flag |  Flag indicating whether the Concept ID belongs to a drug concept
'Yes' if drug concept, 'No' if not a drug concept |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  1545999 |
|  Drug_Concept_Name |  atorvastatin 20 MG Oral Tablet [Lipitor] |
|  Drug_Concept_Code |  617318 |
|  Drug_Concept_Class |  Branded Drug |
|  Drug_Concept_Level |  1 |
|  Drug_Concept_Vocab_ID |  8 |
|  Drug_Concept_Vocab_Name |  RxNorm |
|  Is_Drug_Concept_Flag |  No |




D02: Find drug or class by keyword
---

This query enables search of vocabulary entities in the drug domain by keyword. The query does a search of standard concepts names in the DRUG domain including the following:

- RxNorm standard drug concepts
- ETC, ATC therapeutic classes
- NDF-RT mechanism of action, physiological effect, chemical structure concepts
- Synonyms of drug concepts
- Mapped drug codes from NDC, GPI, Multum, Multilex

Sample query:

        SELECT c.concept_id Entity_Concept_Id, c.concept_name Entity_Name, c.concept_code Entity_Code, 'Concept' Entity_Type, c.concept_class_id Entity_concept_class_id, c.vocabulary_id Entity_vocabulary_id

        FROM concept c

        WHERE c.concept_class_id IS NOT NULL

        AND c.vocabulary_id in ('NDFRT','RxNorm','Indication','ETC','ATC','VA Class','GCN_SEQNO')

        AND REGEXP_INSTR(LOWER(REPLACE(REPLACE(c.concept_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE('Lipitor', ' ', ''), '-', ''))) > 0

        AND sysdate BETWEEN c.valid_start_date AND c.valid_end_date

        UNION ALL

        SELECT c.concept_id Entity_Concept_Id, c.concept_name Entity_Name, c.concept_code Entity_Code, 'Mapped Code' Entity_Type,

        c.concept_class_id Entity_concept_class_id, c.vocabulary_id Entity_vocabulary_id

        FROM concept_relationship cr JOIN concept c ON c.concept_id = cr.concept_id_1

        AND cr.relationship_id = 'Maps to'

        AND c.vocabulary_id IN ('NDC', 'GPI', 'Multum', 'Multilex', 'VA Product', 'MeSH', 'SPL')

        AND REGEXP_INSTR(LOWER(REPLACE(REPLACE(c.concept_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE('Lipitor', ' ', ''), '-', ''))) > 0

        AND sysdate BETWEEN c.valid_start_date AND c.valid_end_date

        UNION ALL

        SELECT c.concept_id Entity_Concept_Id, s.concept_synonym_name Entity_Name, c.concept_code Entity_Code, 'Concept Synonym' Entity_Type, c.concept_class_id Entity_concept_class_id, c.vocabulary_id Entity_vocabulary_id

        FROM concept c, concept_synonym s

        WHERE S.concept_id = c.concept_id

        AND c.vocabulary_id in ('NDFRT','RxNorm','Indication','ETC','ATC','VA Class','GCN_SEQNO')

        AND c.concept_class_id IS NOT NULL

        AND REGEXP_INSTR(LOWER(REPLACE(REPLACE(s.concept_synonym_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE(

        'Lipitor'

        , ' ', ''), '-', ''))) > 0

        AND sysdate BETWEEN c.valid_start_date AND c.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Keyword |  'Lipitor' |  Yes | Keyword should be placed in single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Entity_Concept_ID |  Concept ID of entity with string match on name or synonym concept |
|  Entity_Name |  Concept name of entity with string match on name or synonym concept |
|  Entity_Code |  Concept code of entity with string match on name or synonym concept |
|  Entity_Type |  Type of entity with keyword match, includes one of the following:
- Concept
- Concept Synonym
- Mapped Code
 |
|  Entity_Concept_Class |  Concept class of entity with string match on name or synonym concept |
|  Entity_Vocabulary_ID |  Vocabulary the concept with string match is derived from as vocabulary ID |
|  Entity_Vocabulary_Name |  Name of the vocabulary the concept with string match is derived from as vocabulary code |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Entity_Concept_ID |  1545999 |
|  Entity_Name |  atorvastatin 20 MG Oral Tablet [Lipitor] |
|  Entity_Code |  617318 |
|  Entity_Type |  Concept |
|  Entity_Concept_Class |  Branded Drug |
|  Entity_Vocabulary_ID |  8 |
|  Entity_Vocabulary_Name |  RxNorm |




D03: Find ingredients of a drug
---

This query is designed to accept a drug concept (both clinical or branded) as input and return the list of ingredients that constitute them. Drug concept IDs can be obtained using query G03 or D02.

Sample query:

        SELECT

                D.Concept_Id drug_concept_id,

                D.Concept_Name drug_name,

                D.Concept_Code drug_concept_code,

                D.Concept_Class_id drug_concept_class,

                A.Concept_Id ingredient_concept_id,

                A.Concept_Name ingredient_name,

                A.Concept_Code ingredient_concept_code,

                A.Concept_Class_id ingredient_concept_class

        FROM

                full_201706_omop_v5.concept_ancestor CA,

                full_201706_omop_v5.concept A,

                full_201706_omop_v5.concept D

        WHERE

                CA.descendant_concept_id = D.concept_id

                AND CA.ancestor_concept_id = A.concept_id

                AND LOWER(A.concept_class_id) = 'ingredient'

                AND sysdate BETWEEN A.VALID_START_DATE AND A.VALID_END_DATE

                AND sysdate BETWEEN D.VALID_START_DATE AND D.VALID_END_DATE

                AND CA.descendant_concept_id IN (939355, 19102189, 19033566)

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  List of drug Concept ID |  939355, 19102189, 19033566 |  Yes | Includes both clinical and branded drug concepts |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug_Name |  Name of drug |
|  Drug_Concept_Code |  Concept code of the drug |
|  Drug_Concept_Class |  Concept class of the drug |
|  Ingredient_Concept_ID |  Concept ID of the clinical ingredient |
|  Ingredient_Name |  Name of the clinical ingredient |
|  Ingredient_Concept_Code |  Concept code of the clinical ingredient |
|  Ingredient_Concept_Class |  Concept Class of the clinical ingredient |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19102189 |
|  Drug_Name |  Omeprazole 20 MG Enteric Coated Tablet |
|  Drug_Concept_Code |  402014 |
|  Drug_Concept_Class |  Clinical Drug |
|  Ingredient_Concept_ID |  923645 |
|  Ingredient_Name |  Omeprazole |
|  Ingredient_Concept_Code |  7646 |
|  Ingredient_Concept_Class |  Ingredient |




D04: Find drugs by ingredient
---

This query is designed to extract all drugs that contain a specified ingredient. The query accepts an ingredient concept ID as the input and returns all drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient.
The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the concept table for concept class of 'Ingredient', e.g. using query  [D02](http://vocabqueries.omop.org/drug-queries/d2).

Sample query:

        SELECT

                A.concept_id Ingredient_concept_id,

                A.concept_Name Ingredient_name,

                A.concept_Code Ingredient_concept_code,

                A.concept_Class_id Ingredient_concept_class,

                D.concept_id Drug_concept_id,

                D.concept_Name Drug_name,

                D.concept_Code Drug_concept_code,

                D.concept_Class_id Drug_concept_class

        FROM

                full_201706_omop_v5.concept_ancestor CA,

                full_201706_omop_v5.concept A,

                full_201706_omop_v5.concept D

        WHERE

                CA.ancestor_concept_id = A.concept_id

                AND CA.descendant_concept_id = D.concept_id

                AND sysdate BETWEEN A.valid_start_date AND A.valid_end_date

                AND sysdate BETWEEN D.valid_start_date AND D.valid_end_date

                AND CA.ancestor_concept_id = 966991;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  966991 |  Yes | Concept ID for 'Simethicone'.
Ingredient concepts can be extracted from CONCEPT table as records of concept class of 'Ingredient' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient entered as input |
|  Ingredient_name |  Name of the ingredient |
|  Ingredient_Concept_code |  Concept code of the ingredient |
|  Ingredient_Concept_class |  Concept Class of the ingredient |
|  Generic_Concept_ID |  Concept ID of drug with the ingredient |
|  Generic_Name |  Name of drug concept with the ingredient |
|  Generic_Concept_Code |  Concept code of the drug with the ingredient |
|  Generic_Concept_Class |  Concept class of drug with the ingredient |

Sample output record:

| Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  966991 |
|  Ingredient_name |  Simethicone |
|  Ingredient_Concept_code |  9796 |
|  Ingredient_Concept_class |  Ingredient |
|  Generic_Concept_ID |  967306 |
|  Generic_Name |  Simethicone 10 MG/ML Oral Solution |
|  Generic_Concept_Code |  251293 |
|  Generic_Concept_Class |  Clinical Drug |




D05: Find generic drugs by ingredient
---

This query is designed to extract all generic drugs that have a specified ingredient. The query accepts an ingredient concept ID as the input and returns all generic (not branded) drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient.
The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the CONCEPT table for concept class of 'Ingredient'

Sample query:

        SELECT        A.concept_id Ingredient_concept_id,

                        A.concept_Name Ingredient_name,

                        A.concept_Code Ingredient_concept_code,

                        A.concept_Class_id Ingredient_concept_class,

                        D.concept_id Generic_concept_id,

                        D.concept_Name Generic_name,

                        D.concept_Code Generic_concept_code,

                        D.concept_class_id Generic_concept_class

        FROM        concept_ancestor CA,

                        concept A,

                        concept D

        WHERE

                CA.ancestor_concept_id                 = 966991

        AND        CA.ancestor_concept_id                = A.concept_id

        AND CA.descendant_concept_id        = D.concept_id

        AND        D.concept_class_id                        = 'Clinical Drug'

        AND        sysdate                                                BETWEEN A.valid_start_date AND A.valid_end_date AND sysdate BETWEEN D.valid_start_date AND D.valid_end_date

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Ingredient Concept ID  |  966991 |  Yes | Concept ID for 'Simethicone'.
Ingredient concepts can be extracted from CONCEPT table as records of concept class of 'Ingredient' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient entered as input |
|  Ingredient_name |  Name of the Ingredient |
|  Ingredient_Concept_code |  Concept code of the ingredient |
|  Ingredient_Concept_class |  Concept Class of the ingredient |
|  Generic_Concept_ID |  Concept ID of drug with the ingredient |
|  Generic_Name |  Name of drug concept with the ingredient |
|  Generic_Concept_Code |  Concept code of the drug with the ingredient |
|  Generic_Concept_Class |  Concept class of drug with the ingredient |

Sample output record:

| Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  966991 |
|  Ingredient_name |  Simethicone |
|  Ingredient_Concept_code |  9796 |
|  Ingredient_Concept_class |  Ingredient |
|  Generic_Concept_ID |  967306 |
|  Generic_Name |  Simethicone 10 MG/ML Oral Solution |
|  Generic_Concept_Code |  251293 |
|  Generic_Concept_Class |  Clinical Drug |




D06: Find branded drugs by ingredient
---

This query is designed to extract all branded drugs that have a specified ingredient. The query accepts an ingredient concept ID as the input and returns all branded drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient. The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the CONCEPT table for concept class of 'Ingredient'.

Sample query:

        SELECT        A.concept_id Ingredient_concept_id,

                        A.concept_name Ingredient_concept_name,

                        A.concept_code Ingredient_concept_code,

                        A.concept_class_id Ingredient_concept_class,

                        D.concept_id branded_drug_id,

                        D.concept_name branded_drug_name,

                        D.concept_code branded_drug_concept_code,

                        D.concept_class_id branded_drug_concept_class

        FROM        concept_ancestor CA,

                        concept A,

                        concept D

        WHERE

                CA.ancestor_concept_id                = 966991

        AND        CA.ancestor_concept_id                = A.concept_id

        AND        CA.descendant_concept_id        = D.concept_id

        AND        D.concept_class_id                        = 'Branded Drug'

        AND        sysdate                                                BETWEEN A.valid_start_date AND A.valid_end_date AND sysdate BETWEEN D.valid_start_date AND D.valid_end_date

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  966991 |  Yes | Concept ID for 'Simethicone'. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient entered as input |
|  Ingredient_name |  Name of the Ingredient |
|  Ingredient_Concept_code |  Concept code of the ingredient |
|  Ingredient_Concept_class |  Concept Class of the ingredient |
|  Branded_Drug_ID |  Concept ID of branded drug with the ingredient |
|  Branded_Drug_Name |  Name of branded drug concept with the ingredient |
|  Branded_Drug_Concept_Code |  Concept code of the branded drug with the ingredient |
|  Branded_Drug_Concept_Class |  Concept class of branded drug with the ingredient |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  966991 |
|  Ingredient_name |  Simethicone |
|  Ingredient_Concept_code |  9796 |
|  Ingredient_Concept_class |  Ingredient |
|  Branded_Drug_ID |  19132733 |
|  Branded_Drug_Name |  Simethicone 66.7 MG/ML Oral Suspension [Mylicon] |
|  Branded_Drug_Concept_Code |  809376 |
|  Branded_Drug_Concept_Class |  Branded Drug |




D07: Find single ingredient drugs by ingredient
---

This query accepts accepts an ingredient concept ID and returns all drugs which contain only one ingredient specified in the query. This query is useful when studying drug outcomes for ingredients where the outcome or drug-drug interaction effect of other ingredients needs to be avoided. Indications have to be provided as FDB (vocabulary_id=19) or NDF-RT indications (vocabulary_id=7).

Sample query:

        SELECT

              c.concept_id     as drug_concept_id,

              c.concept_name   as drug_concept_name,

              c.concept_class_id  as drug_concept_class_id

        FROM concept c

        INNER JOIN (

          SELECT drug.cid FROM (

            SELECT a.descendant_concept_id cid, count(\*) cnt FROM concept_ancestor a

            INNER JOIN (

              SELECT c.concept_id FROM concept c, concept_ancestor a

              WHERE a.ancestor_concept_id = 1000560

              AND a.descendant_concept_id = c.concept_id AND c.vocabulary_id = 'RxNorm'

            ) cd ON cd.concept_id = a.descendant_concept_id

            INNER JOIN concept c ON c.concept_id=a.ancestor_concept_id

                WHERE c.concept_class_id = 'Ingredient'

            GROUP BY a.descendant_concept_id

          ) drug WHERE drug.cnt = 1  -- contains only 1 ingredient

        ) onesie ON onesie.cid = c.concept_id

        WHERE sysdate BETWEEN valid_start_date AND valid_end_date

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  1000560 |  Yes | Concept ID for ingredient 'Ondansetron' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of a drug |
|  Drug_Concept_Name |  Name of drug Concept |
|  Drug_Concept_Class |  Concept Code of drug |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  40227201 |
|  Drug_Concept_Name |  Ondansetron 0.16 MG/ML Injectable Solution |
|  Drug_Concept_Class |  Clinical Drug |




D08: Find drug classes for a drug or ingredient
---

This query is designed to return the therapeutic classes that associated with a drug. The query accepts a standard drug concept ID (e.g. as identified from query  [G03](http://vocabqueries.omop.org/general-queries/g3)) as the input. The drug concept can be a clinical or branded drug or pack (concept_level=1), or an ingredient (concept_level=2). The query returns one or more therapeutic classes associated with the drug based on the following classifications.).

- Enhanced Therapeutic Classification (ETC)
- Anatomical Therapeutic Chemical classification (ATC)
- NDF-RT Mechanism of Action (MoA)
- NDF-RT Physiologic effect
- NDF-RT Chemical structure
- VA Class

By default, the query returns therapeutic classes based on all the classification systems listed above. Additional clauses can be added to restrict the query to a single classification system.

Sample query:

        SELECT

         c1.concept_id                 Class_Concept_Id,

         c1.concept_name               Class_Name,

         c1.concept_code               Class_Code,

         c1.concept_class_id              Classification,

         c1.vocabulary_id              Class_vocabulary_id,

         v1.vocabulary_name            Class_vocabulary_name,

         ca.min_levels_of_separation  Levels_of_Separation

        FROM concept_ancestor   ca,

         concept                c1,

         vocabulary             v1

        WHERE

        ca.ancestor_concept_id = c1.concept_id

        AND    c1.vocabulary_id IN ('NDFRT', 'ETC', 'ATC', 'VA Class')

        AND    c1.concept_class_id IN ('ATC','VA Class','Mechanism of Action','Chemical Structure','ETC','Physiologic Effect')

        AND    c1.vocabulary_id = v1.vocabulary_id

        AND    ca.descendant_concept_id = 1545999

        AND    sysdate BETWEEN c1.valid_start_date AND c1.valid_end_date;



Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|   Drug Concept ID |  1545999 |  Yes | Concept Identifier from RxNorm for 'atorvastatin 20 MG Oral Tablet [Lipitor]' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Class_Concept_ID |  Concept ID of the therapeutic class |
|  Class_Name |  Name of the therapeutic class |
|  Class_Code |  Concept Code of therapeutic class |
|  Classification |  Concept class of therapeutic class |
|  Class_Vocabulary_ID |  Vocabulary the therapeutic class is derived from, expressed as vocabulary ID |
|  Class_Vocabulary_Name |  Name of the vocabulary the therapeutic class is derived from |
|  Levels_of_Separation |  Levels of separation between the drug concept and the therapeutic class. Important for hierarchic classification systems to identify classes and subclasses for the drug. |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Class_Concept_ID |  21500263 |
|  Class_Name |  Antihyperlipidemics |
|  Class_Code |  263 |
|  Classification |  Enhanced Therapeutic Classification |
|  Class_Vocabulary_ID |  20 |
|  Class_Vocabulary_Name |  ETC |
|  Levels_of_Separation |  2 |




D09: Find drugs by drug class
---

This query is designed to extract all drugs that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class .
Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY_ID = 20
- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY_ID = 21

– NDF-RT Mechanism of Action (MoA), Vocabulary ID = 7, Concept Class = 'Mechanism of Action'

– NDF-RT Physiologic effect (PE),        Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

– NDF-RT Chemical Structure,              Vocabulary ID = 7, Concept Class = 'Chemical Structure'

- VA Class, Vocabulary ID = 32

Sample query:

        SELECT  c.concept_id      drug_concept_id,

                c.concept_name   drug_concept_name,

                c.concept_class_id  drug_concept_class,

                c.concept_code   drug_concept_code

        FROM    concept          c,

                 concept_ancestor ca

        WHERE   ca.ancestor_concept_id = 21506108

                AND  c.concept_id            = ca.descendant_concept_id

                AND  c.vocabulary_id         = 'RxNorm'

                AND  c.domain_id = 'Drug'

                AND  c.standard_concept = 'S'

                   AND sysdate BETWEEN c.valid_start_date AND c.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug included in therapeutic class |
|  Drug_Concept_Name |  Name of drug concept included in therapeutic class |
|  Drug_Concept_Class |  Concept class of drug concept included in therapeutic class |
|  Drug_Concept_Code |  RxNorm source code of drug concept |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  1308221 |
|  Drug_Concept_Name |  Lisinopril 40 MG Oral Tablet |
|  Drug_Concept_Class |  Clinical Drug |
|  Drug_Concept_Code |  197884 |




D10: Find ingredient by drug class
---

This query is designed to extract all ingredients that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class.
Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY_ID = 20
- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY_ID = 21

– NDF-RT Mechanism of Action (MoA), Vocabulary ID = 7, Concept Class = 'Mechanism of Action'

– NDF-RT Physiologic effect (PE), Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

– NDF-RT Chemical Structure, Vocabulary ID = 7, Concept Class = 'Chemical Structure'

-  VA Class, VOCABULARY_ID = 32

Sample query:

        SELECT  c.concept_id    ingredient_concept_id,

                c.concept_name  ingredient_concept_name,

                c.concept_class_id ingredient_concept_class,

                c.concept_code  ingredient_concept_code

         FROM   concept          c,

                concept_ancestor ca

         WHERE  ca.ancestor_concept_id = 21506108

           AND  c.concept_id           = ca.descendant_concept_id

           AND  c.vocabulary_id        = 'RxNorm'

           AND c.concept_class_id = 'Ingredient'

           AND  sysdate BETWEEN c.valid_start_date AND c.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |



Output:

|  Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of ingredient included in therapeutic class |
|  Ingredient_Concept_Name |  Name of ingredient concept included in therapeutic class |
|  Ingredient_Concept_Class |  Concept class of ingredient concept included in therapeutic class |
|  Ingredient_Concept_Code |  RxNorm source code of ingredient concept |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  1308216 |
|  Ingredient_Concept_Name |  Lisinopril |
|  Ingredient_Concept_Class |  Ingredient |
|  Ingredient_Concept_Code |  29046 |




D11: Find source codes by drug class
---

This query is designed to extract codes from a non-standard drug vocabulary that belong to a therapeutic class. The query accepts a therapeutic class concept ID and the vocabualry ID of the desired source vocabulary as input and returns all codes that are included under that class and that belong to a source vocabulary. This query could be used to derive e.g. all NDC codes that belong to a certain drug class.

Sample query:

        SELECT  d.concept_code,

                d.vocabulary_id,

                v.vocabulary_name

         FROM concept_ancestor ca

                 JOIN concept d on d.concept_id = ca.descendant_concept_id

                JOIN concept a on a.concept_id = ca.ancestor_concept_id

                JOIN vocabulary v on d.vocabulary_id = v.vocabulary_id

         WHERE  ca.ancestor_concept_id = 21506108

           AND  a.vocabulary_id = 'NDC'

           AND  d.domain_id = 'Drug'

           AND sysdate BETWEEN d.valid_start_date AND d.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  Source Vocabulary ID |  9 |  Yes | One of the above drug vocabulary ID's |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Source_Code |  Source code of drug in non-standard vocabulary (e.g. NDC code, FDA SPL number etc.) |
|  Source_Vocabulary_ID |  Vocabulary ID of source vocabulary |
|  Source_Vocabulary_Name |  Vocabulary name of source vocabulary |
|  Source_Code_Description |  Description of source code |

Sample output record:

| Field |  Value |
| --- | --- |
|  Source_Code |  00003033805 |
|  Source_Vocabulary_ID |  9 |
|  Source_Vocabulary_Name |  NDC |
|  Source_Code_Description |  Captopril 25 MG / Hydrochlorothiazide 15 MG Oral Tablet |




D12: Find indications for a drug
---

This query is designed to extract indications associated with a drug. The query accepts a standard drug concept ID (e.g. as identified from query  [G03](http://vocabqueries.omop.org/general-queries/g3)) as the input and returns all available indications associated with the drug.
The vocabulary includes indications available from more than one source vocabulary:

- First Data Bank (FDB), defined mostly for clinical drug concepts
- NDF-RT defined mostly for ingredients

FDB also distinguishes indications based on their presence in the drug label (or package insert) as FDA approved or off-label. NDF-RT distinguishes between treatment or prevention indication. The segmentation is preserved in the vocabulary through separate concept relationships.

Sample query:

        SELECT

          r.relationship_name as type_of_indication,

          c.concept_id as indication_concept_id,

          c.concept_name as indication_concept_name,

          c.vocabulary_id as indication_vocabulary_id,

          vn.vocabulary_name as indication_vocabulary_name

        FROM

          concept c,

          vocabulary vn,

          relationship r,

          ( -- collect all indications from the drugs, ingredients and pharmaceutical preps and the type of relationship

            SELECT DISTINCT

              r.relationship_id rid,

              r.concept_id_2 cid

            FROM concept c

            INNER JOIN ( -- collect onesie clinical and branded drug if query is ingredient

              SELECT onesie.cid concept_id

              FROM (

                SELECT

                  a.descendant_concept_id cid,

                  count(\*) cnt

                FROM concept_ancestor a

                INNER JOIN (

                  SELECT c.concept_id

                  FROM

                    concept c,

                    concept_ancestor a

                  WHERE

                    a.ancestor_concept_id=19005968 AND

                    a.descendant_concept_id=c.concept_id AND

                    c.vocabulary_id=8

                ) cd on cd.concept_id=a.descendant_concept_id

                INNER JOIN concept c on c.concept_id=a.ancestor_concept_id

                WHERE c.concept_level=2

                GROUP BY a.descendant_concept_id

              ) onesie

              where onesie.cnt=1

              UNION -- collect ingredient if query is clinical and branded drug

              SELECT c.concept_id

              FROM

                concept c,

                concept_ancestor a

              WHERE

                a.descendant_concept_id=19005968 AND

                a.ancestor_concept_id=c.concept_id AND

                c.vocabulary_id=8

              UNION -- collect pharmaceutical preparation equivalent to which NDFRT has reltionship

              SELECT c.concept_id

              FROM

                concept c,

                concept_ancestor a

              WHERE

                a.descendant_concept_id=19005968 AND

                a.ancestor_concept_id=c.concept_id AND

                lower(c.concept_class)='pharmaceutical preparations'

              UNION -- collect itself

              SELECT 19005968

            ) drug ON drug.concept_id=c.concept_id

            INNER JOIN concept_relationship r on c.concept_id=r.concept_id_1 -- allow only indication relationships

            WHERE

              r.relationship_id IN (21,23,155,156,126,127,240,241)

          ) ind

          WHERE

            ind.cid=c.concept_id AND

            r.relationship_id=ind.rid AND

            vn.vocabulary_id=c.vocabulary_id AND

            sysdate BETWEEN c.valid_start_date AND c.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|   Drug Concept ID |   19005968 |  Yes | Drugs concepts from RxNorm with a concept class of 'Clinical drug or pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Type_of_Indication |  Type of indication, indicating one of the following:
- FDA approved/off-label indication
- Treatment/prevention indication
 |
|  Indication_Concept_ID |  Concept ID of the therapeutic class |
|  Indication_Concept_Name |  Name of the Indication concept |
|  Indication_Vocabulary_ID |  Vocabulary the indication is derived from, expressed as vocabulary ID |
|  Indication_Vocabulary_Name |  Name of the vocabulary the indication is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Type_of_Indication |  Has FDA-approved drug indication (FDB) |
|  Indication_Concept_ID |  21003511 |
|  Indication_Concept_Name |  Cancer Chemotherapy-Induced Nausea and Vomiting |
|  Indication_Vocabulary_ID |  19 |
|  Indication_Vocabulary_Name |  FDB Indication |




D13 :Find indications as condition concepts for a drug
---

This query accepts a mapped drug code instead of a standard drug concept ID as the input. The result set from the returns detailed of indications associated with the drug.

Sample query:

        SELECT

          rn.relationship_name as type_of_indication,

          c.concept_id as indication_concept_id,

          c.concept_name as indication_concept_name,

          c.vocabulary_id as indication_vocabulary_id,

          vn.vocabulary_name as indication_vocabulary_name

        FROM

          concept c,

          vocabulary vn,

          relationship rn,

          ( -- collect all indications from the drugs, ingredients and pharmaceutical preps and the type of relationship

            SELECT DISTINCT

              r.relationship_id rid,

              r.concept_id_2 cid

            FROM concept c

            INNER JOIN ( -- collect onesie clinical and branded drug if query is ingredient

              SELECT onesie.cid concept_id

              FROM (

                SELECT

                  a.descendant_concept_id cid,

                  count(\*) cnt

                FROM concept_ancestor a

                INNER JOIN (

                  SELECT c.concept_id

                  FROM

                    concept c,

                    concept_ancestor a

                  WHERE

                    a.ancestor_concept_id=19005968 AND

                    a.descendant_concept_id=c.concept_id AND

                    c.vocabulary_id=8

                ) cd on cd.concept_id=a.descendant_concept_id

                INNER JOIN concept c on c.concept_id=a.ancestor_concept_id

                WHERE c.concept_level=2

                GROUP BY a.descendant_concept_id

              ) onesie

              where onesie.cnt=1

              UNION -- collect ingredient if query is clinical and branded drug

              SELECT c.concept_id

              FROM

                concept c,

                concept_ancestor a

              WHERE

                a.descendant_concept_id=19005968 AND

                a.ancestor_concept_id=c.concept_id AND

                c.vocabulary_id=8

              UNION -- collect pharmaceutical preparation equivalent to which NDFRT has reltionship

              SELECT c.concept_id

              FROM

                concept c,

                concept_ancestor a

              WHERE

                a.descendant_concept_id=19005968 AND

                a.ancestor_concept_id=c.concept_id AND

                lower(c.concept_class)='pharmaceutical preparations'

              UNION -- collect itself

              SELECT 19005968

            ) drug ON drug.concept_id=c.concept_id

            INNER JOIN concept_relationship r on c.concept_id=r.concept_id_1 -- allow only indication relationships

            WHERE

              r.relationship_id IN (21,23,155,156,126,127,240,241)

          ) ind

          INNER JOIN concept_relationship r ON r.concept_id_1=ind.cid

          WHERE

            r.concept_id_2=c.concept_id AND

            r.relationship_id in (247, 248) AND

            ind.rid=rn.relationship_id AND

            vn.vocabulary_id=c.vocabulary_id AND

            sysdate BETWEEN c.valid_start_date AND c.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|   Drug Concept ID |   19005968 |  Yes | Drugs concepts from RxNorm with a concept class of 'Branded Drug' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Type_of_Indication |  Type of indication, indicating one of the following:
- FDA approved/off-label indication
- Treatment/prevention indication
 |
|  Indication_Concept_ID |  Concept ID of the therapeutic class |
|  Indication_Concept_Name |  Name of the Indication concept |
|  Indication_Vocabulary_ID |  Vocabulary the indication is derived from, expressed as vocabulary ID |
|  Indication_Vocabulary_Name |  Name of the vocabulary the indication is derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Type_of_Indication |  Has FDA-approved drug indication (FDB) |
|  Indication_Concept_ID |  27674 |
|  Indication_Concept_Name |  N&V - Nausea and vomiting |
|  Indication_Vocabulary_ID |  1 |
|  Indication_Vocabulary_Name |  SNOMED-CT |




D14: Find drugs for an indication
---

This query provides all clinical or branded drugs that are indicated for a certain indication. Indications have to be given as FDB indications (vocabulary_id=19) or NDF-RT indications (vocabulary_id=7). Indications can be identified using the generic query  [G03](http://vocabqueries.omop.org/general-queries/g3), or, if at least one drug is known for this indication, query  [D04](http://vocabqueries.omop.org/drug-queries/d4).

Sample query:

        SELECT

                drug.concept_id      as drug_concept_id,

                drug.concept_name    as drug_concept_name,

                drug.concept_code    as drug_concept_code

         FROM   concept drug,

                concept_ancestor a

         WHERE  a.ancestor_concept_id   = 21000039

         AND    a.descendant_concept_id = drug.concept_id

         AND         drug.standard_concept = 'S'

         AND    drug.domain_id = 'Drug'

         AND    drug.vocabulary_id = 'RxNorm'

         AND    sysdate BETWEEN drug.valid_start_date AND drug.valid_end_date

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  21000039 |  Yes | FDB indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of the drug |
|  Drug_Concept_Name |  Name of the drug |
|  Drug_Concept_Code |  Concept code of the drug |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  1710446 |
|  Drug_Concept_Name |  Cycloserine |
|  Drug_Concept_Code |  3007 |




D15: Find drugs for an indication provided as condition concepts
---

This query provides all clinical/branded drugs that are indicated for a certain indication. Indications have to be provided as SNOMED-CT concept (vocabulary_id=1).

Sample query:

        SELECT DISTINCT

          drug.concept_id as drug_concept_id,

          drug.concept_name as drug_concept_name,

          drug.concept_code as drug_concept_code

        FROM

          concept drug,

          concept_ancestor snomed,

          concept_ancestor ind,

          concept_relationship r

        WHERE

          snomed.ancestor_concept_id = 253954 AND

          snomed.descendant_concept_id = r.concept_id_1 AND

          concept_id_2 = ind.ancestor_concept_id AND

          r.relationship_id in (247, 248) AND

          ind.descendant_concept_id = drug.concept_id AND

          drug.concept_level = 1 AND

          drug.vocabulary_id = 8 AND

          sysdate BETWEEN drug.valid_start_date AND drug.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  253954 |  Yes | SNOMED-CT indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of the drug |
|  Drug_Concept_Name |  Name of the drug |
|  Drug_Concept_Code |  Concept code of the drug |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19073074 |
|  Drug_Concept_Name |  Aminosalicylic Acid 500 MG Oral Tablet |
|  Drug_Concept_Code |  308122 |




D16: Find drugs for an indication by indication type
---

This query provides all drugs that are indicated for a certain condition. In addition, it provides the type of indication: FDA-approved, off-label (both based on FDB indication classes) and may treat and may prevent (both based on NDF-RT). Indications have to be provided as FDB indications (vocabulary_id=19) or NDF-RT (vocabulary_id=7).

Sample query:

        SELECT DISTINCT

         drug.concept_id      as drug_concept_id,

         drug.concept_name    as drug_concept_name,

         drug.concept_code    as drug_concept_code,

         rn.relationship_name as indication_type,

         indication_relation.relationship_id

        FROM

          concept_relationship indication_relation

        INNER JOIN concept_ancestor a

         ON a.ancestor_concept_id=indication_relation.concept_id_2

        INNER JOIN concept drug

         ON drug.concept_id=a.descendant_concept_id

        INNER JOIN relationship rn

         ON rn.relationship_id=indication_relation.relationship_id

        WHERE indication_relation.concept_id_1 = 4345991

          AND drug.vocabulary_id = 'RxNorm'

          AND drug.standard_concept = 'S'

          AND indication_relation.relationship_id in (

                  'May treat',

                'Is off-label ind of',

                'Is FDA-appr ind of',

                'Inferred class of',

                'May be prevented by',

                'May prevent',

                'Has FDA-appr ind',

                'Has off-label ind',

                'May be treated by',

                'Has inferred class')

          AND sysdate BETWEEN drug.valid_start_date AND drug.valid_end_date;


Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of the drug |
|  Drug_Concept_Name |  Name of the drug |
|  Drug_Concept_Code |  Concept code of the drug |
|  Indication_Type |  One of the FDB, NDF-RT or OMOP inferred indication types |
|  Relationship_id |  Corresponding relationship ID to the Indication Type |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19019530 |
|  Drug_Concept_Name |  Perphenazine 4 MG Oral Tablet |
|  Drug_Concept_Code |  198077 |
|  Indication_Type |  Inferred ingredient of (OMOP) |
|  Relationship_id |  281 |




D17: Find ingredients for an indication
---

This query provides ingredients that are designated for a certain indication. Indications have to be given as FDB indications (vocabulary_id=19) or NDF-RT indications (vocabulary_id=7). Indications can be identified using the generic query  [G03](http://vocabqueries.omop.org/general-queries/g3), or, if at least one drug is known for this indication, query  [D04](http://vocabqueries.omop.org/drug-queries/d4).

Sample query:

        SELECT

          ingredient.concept_id as ingredient_concept_id,

          ingredient.concept_name as ingredient_concept_name,

          ingredient.concept_code as ingredient_concept_code

        FROM

          concept ingredient,

          concept_ancestor a

        WHERE

          a.ancestor_concept_id = 4345991 AND

          a.descendant_concept_id = ingredient.concept_id AND

          ingredient.concept_level = 2 AND

          ingredient.vocabulary_id = 8 AND

          sysdate BETWEEN ingredient.valid_start_date AND ingredient.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient |
|  Ingredient_Concept_Name |  Name of the ingredient |
|  Ingredient_Concept_Code |  Concept code of the ingredient |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  733008 |
|  Ingredient_Concept_Name |  Perphenazine |
|  Ingredient_Concept_Code |  8076 |




D18: Find ingredients for an indication provided as condition concept
---

This query provides all ingredients that are indicated for a certain indication. Indications have to be provided as SNOMED-CT concept ID (vocabulary_id=1).

Sample query:

        SELECT DISTINCT

          ingredient.concept_id as ingredient_concept_id,

          ingredient.concept_name as ingredient_concept_name,

          ingredient.concept_code as ingredient_concept_code

        FROM

          concept ingredient,

          concept_ancestor snomed,

          concept_ancestor ind,

          concept_relationship r

        WHERE

          snomed.ancestor_concept_id = 253954 AND

          snomed.descendant_concept_id = r.concept_id_1 AND

          concept_id_2 = ind.ancestor_concept_id AND

          r.relationship_id in (247, 248) AND

          ind.descendant_concept_id = ingredient.concept_id AND

          ingredient.concept_level = 2 AND

          ingredient.vocabulary_id = 8 AND

          sysdate BETWEEN ingredient.valid_start_date AND ingredient.valid_end_date;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  253954 |  Yes | SNOMED-CT indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |





Output:

|  Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient |
|  Ingredient_Concept_Name |  Name of the ingredient |
|  Ingredient_Concept_Code |  Concept code of the ingredient |

Sample output record:

| Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  1790868 |
|  Ingredient_Concept_Name |  Amikacin |
|  Ingredient_Concept_Code |  641 |




D19: Find ingredients for an indication by indication type
---

This query provides all ingredients that are indicated for a certain condition. In addition, it provides the type of indication: FDA-approved, off-label (both based on FDB indication classes) and may treat and may prevent (both based on NDF-RT). Indications have to be provided as FDB indications (vocabulary_id=19) or NDF-RT (vocabulary_id=7).

Sample query:

        SELECT DISTINCT

          ingredient.concept_id as ingredient_concept_id,

          ingredient.concept_name as ingredient_concept_name,

          ingredient.concept_code as ingredient_concept_code,

          rn.relationship_name as indication_type,

          indication_relation.relationship_id

        FROM

          concept_relationship indication_relation

        INNER JOIN

          concept_ancestor a ON a.ancestor_concept_id=indication_relation.concept_id_2

        INNER JOIN

          concept ingredient ON ingredient.concept_id=a.descendant_concept_id

        INNER JOIN

          relationship rn ON rn.relationship_id = indication_relation.relationship_id

        WHERE

          indication_relation.concept_id_1 = 4345991 AND

          ingredient.vocabulary_id = 8 AND

          ingredient.concept_level = 2 AND

          indication_relation.relationship_id in (21,23,155,157,126,127,240,241,281,282) AND

          sysdate BETWEEN ingredient.valid_start_date AND ingredient.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Ingredient_Concept_ID |  Concept ID of the ingredient |
|  Ingredient_Concept_Name |  Name of the ingredient |
|  Ingredient_Concept_Code |  Concept code of the ingredient |
|  Indication_Type |  One of the FDB, NDF-RT or OMOP inferred indication types |
|  Relationship_id |  Corresponding relationship ID to the Indication Type |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Ingredient_Concept_ID |  733008 |
|  Ingredient_Concept_Name |  Perphenazine |
|  Ingredient_Concept_Code |  8076 |
|  Indication_Type |  Inferred ingredient of (OMOP) |
|  Relationship_id |  281 |




D20: Find dose form of a drug
---

This query accepts concept IDs for a drug product (clinical or branded drug or pack) and identifies the dose form.

The query relies on RxNorm concept relationship (4 – 'Has dose form (RxNorm)') for this.

Sample query:

        SELECT

                A.concept_id drug_concept_id,

                 A.concept_name drug_name,

                 A.concept_code drug_concept_code,

                 D.concept_id dose_form_concept_id,

                 D.concept_name dose_form_concept_name,

                 D.concept_code dose_form_concept_code

        FROM

                full_201706_omop_v5.concept_relationship CR,

                 full_201706_omop_v5.concept A,

                 full_201706_omop_v5.concept D

        WHERE

                sysdate BETWEEN CR.valid_start_date AND CR.valid_end_date

                AND CR.concept_id_1 = A.concept_id

                 AND CR.concept_id_2 = D.concept_id

                AND CR.concept_id_1 = 19060647

                AND CR.relationship_id = 'RxNorm has dose form'

                --AND CR.relationship_ID = 4

                --AND A.concept_class_id ='Clinical Drug'

                --AND A.vocabulary_id = 'RxNorm'

                ;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Drug Concept ID |  19060647 |  Yes | Must be a level 1 Clinical or Branded Drug or Pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug entered with specified dose form |
|  Drug_Name |  Name of drug with specified dose form |
|  Drug_Concept_Code |  Concept ID of the dose form |
|  Dose_Form_Concept_ID |  Concept ID of the dose form |
|  Dose_Form_Concept_name |  Name of the dose form |
|  Dose_Form_Concept_code |  Concept code of dose form |

Sample output record:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  19060647 |
|  Drug_Name |  Budesonide 0.2 MG/ACTUAT Inhalant Powder |
|  Drug_Concept_Code |  247047 |
|  Dose_Form_Concept_ID |  19082259 |
|  Dose_Form_Concept_name |  Inhalant Powder |
|  Dose_Form_Concept_code |  317000 |




D21: Find route of administration of a drug
---

This query accepts concept IDs for a drug product (clinical or branded drug or pack) and identifies the route of administration of the dose form. The following routes of administration are defined:

- Inhaled
- Intrathecal
- Nasal
- Ophthalmic
- Oral
- Unknown (cannot be defined from the dose form)
- Otic
- Parenteral
- Rectal
- Topical
- Urethral
- Vaginal

Sample query:

        SELECT        A.concept_id drug_concept_id,

                        A.concept_name drug_concept_name,

                        A.concept_code drug_concept_code,

                        D.concept_name dose_form_concept_name,

                        R.Route_of_Administration

        FROM        concept_relationship CR,

                        concept A,

                        concept D,

                        route R

        WHERE        CR.concept_id_1                = 40236916

        AND         CR.relationship_ID        = 'RxNorm has dose form'

        AND         CR.concept_id_1                = A.concept_id

        AND         CR.concept_id_2                = D.concept_id

        AND                D.concept_id                = R.concept_id

        AND                sysdate                                BETWEEN CR.valid_start_date AND CR.valid_end_date



Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Drug Concept ID  |  19060647 |  Yes | Must be a level 1 Clinical or Branded Drug or Pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug entered with specified dose form |
|  Drug_Name |  Name of drug with specified dose form |
|  Drug_Concept_Code |  Concept code of the dose form |
|  Dose_Form_Concept_name |  Name of the dose form |
|  Route_Of_Administration |  Derived route of administration for the drug |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19060647 |
|  Drug_Name |  Budesonide 0.2 MG/ACTUAT Inhalant Powder |
|  Drug_Concept_Code |  247047 |
|  Dose_Form_Concept_name |  Inhalant Powder |
|  Route_Of_Administration |  Inhaled |




D22: Find drugs by class and dose form
---

This query is designed to return a list of drug concept IDs that belong to a drug class and are of a certain dose form. The query ties together:

- Concept ancestor data to link drug concepts to therapeutic class
- RxNorm concept relationship 4 - 'Has dose form (RxNorm)

The results are combined to present a list of drugs from a specific therapeutic class with a specific dose form.

Sample query:

        SELECT C.concept_id drug_concept_id,

        C.concept_name drug_concept_name,

        C.concept_code drug_concept_code

        FROM concept C,

                concept_ancestor CA,

                concept_relationship CRF,

                concept F

        WHERE CA.ancestor_concept_id = 4318008

                AND C.concept_id = CA.descendant_concept_id

                AND C.vocabulary_id = 'RxNorm'

                AND C.standard_concept = 'S'

                AND CRF.concept_id_1 = C.concept_id

                AND CRF.relationship_ID = 'RxNorm has dose form'

                AND CRF.concept_id_2 = F.concept_id

                AND POSITION(LOWER(REPLACE(REPLACE(F.concept_name, ' ', ''), '-', '')) IN

                LOWER(REPLACE(REPLACE('Nasal spray' , ' ', ''), '-', ''))) > 0

                AND sysdate BETWEEN CRF.valid_start_date AND CRF.valid_end_date

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| Therapeutic class Concept ID |  4318008 |  Yes | Concept ID for mechanism of action "Corticosteroid Hormone Receptor Agonists". Valid drug classes can be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2). |
|  Dose Form String |  'Nasal spray' |  Yes | Dose form string. Valid dose forms can be obtained using query  [D19](http://vocabqueries.omop.org/drug-queries/d19). |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug with specified therapeutic class and dose form |
|  Drug_Name |  Name of drug with specified therapeutic class and dose form |
|  Drug_Concept_Code |  Source code of drug |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  904131 |
|  Drug_Name |  Triamcinolone 0.055 MG/ACTUAT Nasal Spray |
|  Drug_Concept_Code |  245785 |




D23:  Find drugs by class and route of administration
---

This query is designed to return a list of drug concept IDs that belong to a drug class and require a certain route of administration. For example, it can be used to find all steroid drugs used intravaginally. The query ties together:

- Concept ancestor data to link drug concepts to therapeutic class
- RxNorm concept relationship 4 - 'Has dose form (RxNorm)
- Dose form to route of administration list

The results are combined to present a list of drugs from a specific therapeutic class with a specific route of administration. Permissible routes are:

- Inhaled
- Intrathecal
- Nasal
- Ophthalmic
- Oral
- Unknown (cannot be defined from the dose form)
- Otic
- Parenteral
- Rectal
- Topical
- Urethral
- Vaginal

Sample query:

        SELECT        C.concept_id drug_concept_id,

                        C.concept_name drug_concept_name,

                        C.concept_code drug_concept_code

        FROM        concept C,

                        concept_ancestor CA,

                        concept_relationship CRF,

                        concept F,

                        route

        WHERE

                CA.ancestor_concept_id        = 4318008

        AND        C.concept_id                        = CA.descendant_concept_id

        AND        C.vocabulary_id                        = 'RxNorm'

        AND        C.standard_concept                = 'S'

        AND        CRF.concept_id_1                = C.concept_id

        AND        CRF.relationship_ID                = 'RxNorm has dose form'

        AND        CRF.concept_id_2                = F.concept_id

        AND        F.concept_id                        = route.concept_id

        AND        sysdate                                        BETWEEN CRF.valid_start_date AND CRF.valid_end_date

        AND        POSITION(LOWER(REPLACE(REPLACE(route.route_of_administration, ' ', ''), '-', '')) IN LOWER(REPLACE(REPLACE('vaginal' , ' ', ''), '-', ''))) > 0

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Therapeutic class Concept ID |  4318008 |  Yes | Concept ID for mechanism of action "Corticosteroid Hormone Receptor Agonists". Valid drug classes can be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) |
|  Dose Form String |  'vaginal' |  Yes | Route of administration string. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug with specified therapeutic class and dose form |
|  Drug_Name |  Name of drug with specified therapeutic class and dose form |
|  Drug_Concept_Code |  Source code of drug |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  40230686 |
|  Drug_Name |  hydrocortisone acetate 10 MG/ML Vaginal Cream |
|  Drug_Concept_Code |  1039349 |




D24: Find the branded drugs in a list of drugs
---

This query is designed to identify branded drug concepts from a list of standard drug concept IDs. The query identifies branded drugs from the Concept table based on a concept class setting of 'Branded Drug'

Sample query:

        SELECT C.concept_id drug_concept_id,

                C.concept_name drug_name,

                C.concept_code drug_concept_code,

                C.concept_class_id drug_concept_class,

                C.vocabulary_id drug_vocabulary_id,

                V.vocabulary_name drug_vocabulary_name

        FROM concept C,

                vocabulary V

                WHERE C.vocabulary_id = 'RxNorm'

                        AND C.concept_id IN (1396833, 19060643)

                        AND C.concept_class_id = 'Clinical Drug'

                        AND C.vocabulary_id = V.vocabulary_id

                        AND sysdate BETWEEN C.valid_start_date AND C.valid_end_date

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Drug Concept ID list |  1516830, 19046168 |  Yes | List of drug concept id's |
|  As of date |  '01-Jan-2010' |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of branded drug or pack |
|  Drug_Name |  Name of branded drug or pack |
|  Drug_Concept_Code |  Concept code of branded drug or pack |
|  Drug_Concept_Class |  Concept class of branded drug or pack |
|  Drug_Vocabulary_ID |  Vocabulary the branded drug concept has been derived from, expressed as vocabulary ID |
|  Drug_Vocabulary_Name |  Name of the Vocabulary the branded drug concept has been derived from |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19046168 |
|  Drug_Name |  Triamcinolone 0.055 MG/ACTUAT Nasal Spray [Nasacort AQ] |
|  Drug_Concept_Code |  211501 |
|  Drug_Concept_Class |  Branded Drug |
|  Drug_Vocabulary_ID |  8 |
|  Drug_Vocabulary_Name |  RxNorm |




D25: Find the generic drugs in a list of drugs
---

This query is designed to identify generic drug concepts among from a list of standard drug concept IDs. The query identifies branded drugs from the CONCEPT table based on a concept class setting of 'Clinical Drug'

Sample query:

        SELECT C.concept_id drug_concept_id,

                C.concept_name drug_name,

                C.concept_code drug_concept_code,

                C.concept_class_id drug_concept_class,

                C.vocabulary_id drug_vocabulary_id,

                V.vocabulary_name drug_vocabulary_name

        FROM concept C,

                vocabulary V

                WHERE C.vocabulary_id = 'RxNorm'

                AND C.concept_id IN (1396833, 19060643)

                AND C.concept_class_id = 'Clinical Drug'

                AND C.vocabulary_id = V.vocabulary_id

                AND sysdate BETWEEN C.valid_start_date AND C.valid_end_date

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Drug Concept ID list |  1396833, 19060643 |  Yes | List of drug concept id's |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of generic drug or pack |
|  Drug_Name |  Name of generic drug or pack |
|  Drug_Concept_Code |  Concept code of generic drug or pack |
|  Drug_Concept_Class |  Concept class of generic drug or pack |
|  Drug_Vocabulary_ID |  Vocabulary the generic drug concept has been derived from, expressed as vocabulary ID |
|  Drug_Vocabulary_Name |  Name of the Vocabulary the generic drug concept has been derived from |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19060643 |
|  Drug_Name |  Budesonide 0.05 MG/ACTUAT Nasal Spray |
|  Drug_Concept_Code |  247042 |
|  Drug_Concept_Class |  Clinical Drug |
|  Drug_Vocabulary_ID |  8 |
|  Drug_Vocabulary_Name |  RxNorm |




D26: Find the brand name of a drug
---

This query is designed to accept a drug concept (both clinical and branded) as input and return a the brand name (or branded ingredient) associated with it. The query is useful to check for a brand names associated with a clinical drug. Drug concepts can be obtained using queries  [G03](http://vocabqueries.omop.org/general-queries/g3) or  [D02](http://vocabqueries.omop.org/drug-queries/d2).

Sample query:

        SELECT A.Concept_Id               drug_concept_id,

                A.Concept_Name            drug_name,

                A.Concept_Code            drug_concept_code,

                A.concept_class_id           drug_concept_class_id,

                D.Concept_Id              brand_concept_id,

                D.Concept_Name            brand_name,

                D.Concept_Code            brand_concept_code,

                D.concept_class_id           brand_concept_class_id

        FROM   concept_relationship  CR003,

               concept               A,

               concept_relationship  CR007,

               concept_relationship  CR006,

               concept                 D

        WHERE  CR003.relationship_ID  = 'Has tradename'

        AND    CR003.concept_id_1     = A.concept_id

        AND    lower(A.concept_class_id) = 'clinical drug'

        AND    CR007.concept_id_2     = CR003.concept_id_2

        AND    CR007.relationship_ID  = 'Constitutes'

        AND    CR007.concept_id_1     = CR006.concept_id_1

        AND    CR006.relationship_ID  = 'RxNorm has ing'

        AND    CR006.concept_id_2     = D.concept_id

        AND    lower(D.concept_class_id) = 'branded name'

        AND    A.concept_Id           = 939355

        AND    sysdate BETWEEN CR006.VALID_START_DATE AND CR006.VALID_END_DATE

        UNION ALL

        SELECT A.Concept_Id               drug_concept_id,

               A.Concept_Name             drug_name,

               A.Concept_Code             drug_concept_code,

               A.concept_class_id            drug_concept_class_id,

               D.Concept_Id               brand_concept_id,

               D.Concept_Name             brand_name,

               D.Concept_Code             brand_concept_code,

               D.concept_class_id            brand_concept_class_id

        FROM   concept               A,

               concept_relationship  CR007,

               concept_relationship  CR006,

               concept               D

        WHERE  lower(A.concept_class_id) = 'branded drug'

        AND    CR007.concept_id_2     = A.concept_id

        AND    CR007.relationship_ID  = 'Constitutes'

        AND    CR007.concept_id_1     = CR006.concept_id_1

        AND    CR006.relationship_ID  = 'RxNorm has ing'

        AND    CR006.concept_id_2     = D.concept_id

        AND    lower(D.concept_class_id) = 'branded name'

        AND    A.concept_Id           = 939355

        AND    sysdate BETWEEN CR006.VALID_START_DATE AND CR006.VALID_END_DATE

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Drug Concept ID |  939355 |  Yes | Can be both clinical and branded drug concepts |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

| Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug_Name |  Name of drug |
|  Drug_Concept_Code |  Concept code of the drug |
|  Drug_Concept_Class |  Concept class of drug |
|  Brand_Concept_ID |  Concept ID of the brand name (or branded ingredient) |
|  Brand_name |  Name of the brand name |
|  Brand_Concept_code |  Concept code of the brand name |
|  Brand_Concept_class |  Concept Class of the brand name |

Sample output record:

|  Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  19102189 |
|  Drug_Name |  Omeprazole 20 MG Enteric Coated Tablet |
|  Drug_Concept_Code |  402014 |
|  Drug_Concept_Class |  Clinical Drug |
|  Brand_Concept_ID |  19045785 |
|  Brand_name |  Prilosec |
|  Brand_Concept_code |  203345 |
|  Brand_Concept_class |  Brand Name |




D27: Find drugs of a brand
---

This query is designed to extract all clinical and branded drugs associated with a branded ingredient (or simply a brand name). Since the brand names are not part of the standard drug hierarchy in the OMOP vocabulary, the association between brand name and generic/branded drugs is made using a set of relationships.
The query requires a brand name concept ID as the input. Brand name concept IDs can be obtained by querying the Concept table for a concept class of 'Brand Name'.

Sample query:

        SELECT  A.Concept_Id               drug_concept_id,

                A.Concept_Name             drug_name,

                A.Concept_Code             drug_concept_code,

                A.Concept_Class_id            drug_concept_class,

                D.Concept_Id               brand_concept_id,

                D.Concept_Name             brand_name,

                D.Concept_Code             brand_concept_code,

                D.Concept_Class_id            brand_concept_class

        FROM   concept_relationship  CR003,

               concept               A,

               concept_relationship  CR007,

               concept_relationship  CR006,

               concept               D

        WHERE  CR003.relationship_ID   = 'Constitutes'

        AND    CR003.concept_id_1      = A.concept_id

        AND     lower(A.concept_class_id) = 'clinical drug'

        AND    CR007.concept_id_2      = CR003.concept_id_2

        AND    CR007.relationship_id   = 'Has tradename'

        AND    CR007.concept_id_1      = CR006.concept_id_1

        AND    CR006.relationship_id   = 'RxNorm has ing'

        AND    CR006.concept_id_2      = D.concept_id

        AND    lower(D.concept_class_id)  = 'brand name'

        AND    D.concept_id            = 19011505

        AND    sysdate BETWEEN CR006.valid_start_date AND CR006.valid_end_date

        AND    sysdate BETWEEN CR007.valid_start_date AND CR007.valid_end_date

        UNION ALL

        SELECT  A.Concept_Id               drug_concept_id,

                A.Concept_Name             drug_name,

                A.Concept_Code             drug_concept_code,

                A.Concept_Class_id            drug_concept_class,

                D.Concept_Id               brand_concept_id,

                D.Concept_Name             brand_name,

                D.Concept_Code             brand_concept_code,

                D.Concept_Class_id            brand_concept_class

        FROM   concept              A,

               concept_relationship  CR007,

               concept_relationship  CR006,

               concept               D

        WHERE  lower(A.concept_class_id) = 'branded drug'

        AND    CR007.concept_id_2     = A.concept_id

        AND    CR007.relationship_ID  = 'Has tradename'

        AND    CR007.concept_id_1     = CR006.concept_id_1

        AND    CR006.relationship_ID  = 'RxNorm has ing'

        AND    CR006.concept_id_2     = D.concept_id

        AND    lower(D.concept_class_id) = 'brand name'

        AND    D.concept_id           = 19011505

        AND    sysdate BETWEEN CR006.valid_start_date AND CR006.valid_end_date

        AND    sysdate BETWEEN CR007.valid_start_date AND CR007.valid_end_date;

Input:

| Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  Brand name Concept ID |  19011505 |  Yes | Concept ID for brand name 'Fosamax'.
Brand name concept IDs are listed in the CONCEPT table with a concept class of 'Brand name' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

Output:

|  Field |  Description |
| --- | --- |
|  Drug_Concept_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug_Name |  Name of drug |
|  Drug_Concept_Code |  Concept code of the drug |
|  Drug_Concept_Class |  Concept class of drug |
|  Brand_Concept_ID |  Concept ID of the brand name entered as ingredient |
|  Brand_name |  Name of the brand |
|  Brand_Concept_code |  Concept code of the brand name |
|  Brand_Concept_class |  Concept Class of the brand name |

Sample output record:

| Field |  Value |
| --- | --- |
|  Drug_Concept_ID |  40173591 |
|  Drug_Name |  Alendronic acid 10 MG Oral Tablet [Fosamax] |
|  Drug_Concept_Code |  904421 |
|  Drug_Concept_Class |  Branded Drug |
|  Brand_Concept_ID |  19011505 |
|  Brand_name |  Fosamax |
|  Brand_Concept_code |  114265 |
|  Brand_Concept_class |  Brand Name |




