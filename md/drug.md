**D01:** Find drug concept by concept ID

This is the lookup for obtaining drug concept details associated with a concept identifier. This query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.
This query is equivalent to  [G01](http://vocabqueries.omop.org/general-queries/g1), but if the concept is not in the drug domain the query still returns the concept details with the Is\_Drug\_Concept\_Flag field set to 'No'.

**Sample query:**

SELECT

        C.concept\_id Drug\_concept\_id,

        C.concept\_name Drug\_concept\_name,

        C.concept\_code Drug\_concept\_code,

        C.concept\_class\_id Drug\_concept\_class,

        C.standard\_concept Drug\_concept\_level,

        C.vocabulary\_id Drug\_concept\_vocab\_id,

        V.vocabulary\_name Drug\_concept\_vocab\_code,

        /\*( CASE C.vocabulary\_id

                WHEN 'RxNorm' THEN

                        CASE lower(C.concept\_class\_id)

                        WHEN 'clinical drug' THEN 'Yes'

                        WHEN 'branded drug' THEN 'Yes'

                        WHEN 'ingredient' THEN 'Yes'

                        WHEN 'branded pack' THEN 'Yes'

                        WHEN 'clinical pack' THEN 'Yes'

                        ELSE 'No' END

                ELSE 'No' END) Is\_Drug\_Concept\_flag \*/

        (CASE C.domain\_id WHEN 'Drug' THEN 'Yes' ELSE 'No' END) Is\_Drug\_Concept\_flag

FROM

        full\_201706\_omop\_v5.concept C,

        full\_201706\_omop\_v5.vocabulary V

WHERE

        C.vocabulary\_id = V.vocabulary\_id

        AND sysdate BETWEEN C.valid\_start\_date AND C.valid\_end\_date

        AND C.concept\_id = 1545999;



**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Concept ID |  1545999 |  Yes | Concept Identifier from RxNorm for 'atorvastatin 20 MG Oral Tablet [Lipitor]' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept Identifier entered as input |
|  Drug\_Concept\_Name |  Name of the standard drug concept |
|  Drug\_Concept\_Code |  Concept code of the standard drug concept in the source vocabulary |
|  Drug\_Concept\_Class |  Concept class of standard drug concept |
|  Drug\_Concept\_Level |  Level of the concept if defined as part of a hierarchy |
|  Drug\_Concept\_Vocab\_ID |  Vocabulary the standard drug concept is derived from as vocabulary ID |
|  Drug\_Concept\_Vocab\_Name |  Name of the vocabulary the standard drug concept is derived from |
|  Is\_Drug\_Concept\_Flag |  Flag indicating whether the Concept ID belongs to a drug concept
'Yes' if drug concept, 'No' if not a drug concept |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  1545999 |
|  Drug\_Concept\_Name |  atorvastatin 20 MG Oral Tablet [Lipitor] |
|  Drug\_Concept\_Code |  617318 |
|  Drug\_Concept\_Class |  Branded Drug |
|  Drug\_Concept\_Level |  1 |
|  Drug\_Concept\_Vocab\_ID |  8 |
|  Drug\_Concept\_Vocab\_Name |  RxNorm |
|  Is\_Drug\_Concept\_Flag |  No |
**D02:** Find drug or class by keyword

This query enables search of vocabulary entities in the drug domain by keyword. The query does a search of standard concepts names in the DRUG domain including the following:

- RxNorm standard drug concepts
- ETC, ATC therapeutic classes
- NDF-RT mechanism of action, physiological effect, chemical structure concepts
- Synonyms of drug concepts
- Mapped drug codes from NDC, GPI, Multum, Multilex

**Sample query:**

SELECT c.concept\_id Entity\_Concept\_Id, c.concept\_name Entity\_Name, c.concept\_code Entity\_Code, 'Concept' Entity\_Type, c.concept\_class\_id Entity\_concept\_class\_id, c.vocabulary\_id Entity\_vocabulary\_id

FROM concept c

WHERE c.concept\_class\_id IS NOT NULL

AND c.vocabulary\_id in ('NDFRT','RxNorm','Indication','ETC','ATC','VA Class','GCN\_SEQNO')

AND REGEXP\_INSTR(LOWER(REPLACE(REPLACE(c.concept\_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE('Lipitor', ' ', ''), '-', ''))) > 0

AND sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date

UNION ALL

SELECT c.concept\_id Entity\_Concept\_Id, c.concept\_name Entity\_Name, c.concept\_code Entity\_Code, 'Mapped Code' Entity\_Type,

c.concept\_class\_id Entity\_concept\_class\_id, c.vocabulary\_id Entity\_vocabulary\_id

FROM concept\_relationship cr JOIN concept c ON c.concept\_id = cr.concept\_id\_1

AND cr.relationship\_id = 'Maps to'

AND c.vocabulary\_id IN ('NDC', 'GPI', 'Multum', 'Multilex', 'VA Product', 'MeSH', 'SPL')

AND REGEXP\_INSTR(LOWER(REPLACE(REPLACE(c.concept\_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE('Lipitor', ' ', ''), '-', ''))) > 0

AND sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date

UNION ALL

SELECT c.concept\_id Entity\_Concept\_Id, s.concept\_synonym\_name Entity\_Name, c.concept\_code Entity\_Code, 'Concept Synonym' Entity\_Type, c.concept\_class\_id Entity\_concept\_class\_id, c.vocabulary\_id Entity\_vocabulary\_id

FROM concept c, concept\_synonym s

WHERE S.concept\_id = c.concept\_id

AND c.vocabulary\_id in ('NDFRT','RxNorm','Indication','ETC','ATC','VA Class','GCN\_SEQNO')

AND c.concept\_class\_id IS NOT NULL

AND REGEXP\_INSTR(LOWER(REPLACE(REPLACE(s.concept\_synonym\_name, ' ', ''), '-', '')), LOWER(REPLACE(REPLACE(

'Lipitor'

, ' ', ''), '-', ''))) > 0

AND sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Keyword |  'Lipitor' |  Yes | Keyword should be placed in single quote |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Entity\_Concept\_ID |  Concept ID of entity with string match on name or synonym concept |
|  Entity\_Name |  Concept name of entity with string match on name or synonym concept |
|  Entity\_Code |  Concept code of entity with string match on name or synonym concept |
|  Entity\_Type |  Type of entity with keyword match, includes one of the following:
- Concept
- Concept Synonym
- Mapped Code
 |
|  Entity\_Concept\_Class |  Concept class of entity with string match on name or synonym concept |
|  Entity\_Vocabulary\_ID |  Vocabulary the concept with string match is derived from as vocabulary ID |
|  Entity\_Vocabulary\_Name |  Name of the vocabulary the concept with string match is derived from as vocabulary code |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Entity\_Concept\_ID |  1545999 |
|  Entity\_Name |  atorvastatin 20 MG Oral Tablet [Lipitor] |
|  Entity\_Code |  617318 |
|  Entity\_Type |  Concept |
|  Entity\_Concept\_Class |  Branded Drug |
|  Entity\_Vocabulary\_ID |  8 |
|  Entity\_Vocabulary\_Name |  RxNorm |
**D03:** Find ingredients of a drug

This query is designed to accept a drug concept (both clinical or branded) as input and return the list of ingredients that constitute them. Drug concept IDs can be obtained using query G03 or D02.

**Sample query:**

SELECT

        D.Concept\_Id drug\_concept\_id,

        D.Concept\_Name drug\_name,

        D.Concept\_Code drug\_concept\_code,

        D.Concept\_Class\_id drug\_concept\_class,

        A.Concept\_Id ingredient\_concept\_id,

        A.Concept\_Name ingredient\_name,

        A.Concept\_Code ingredient\_concept\_code,

        A.Concept\_Class\_id ingredient\_concept\_class

FROM

        full\_201706\_omop\_v5.concept\_ancestor CA,

        full\_201706\_omop\_v5.concept A,

        full\_201706\_omop\_v5.concept D

WHERE

        CA.descendant\_concept\_id = D.concept\_id

        AND CA.ancestor\_concept\_id = A.concept\_id

        AND LOWER(A.concept\_class\_id) = 'ingredient'

        AND sysdate BETWEEN A.VALID\_START\_DATE AND A.VALID\_END\_DATE

        AND sysdate BETWEEN D.VALID\_START\_DATE AND D.VALID\_END\_DATE

        AND CA.descendant\_concept\_id IN (939355, 19102189, 19033566)

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  List of drug Concept ID |  939355, 19102189, 19033566 |  Yes | Includes both clinical and branded drug concepts |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug\_Name |  Name of drug |
|  Drug\_Concept\_Code |  Concept code of the drug |
|  Drug\_Concept\_Class |  Concept class of the drug |
|  Ingredient\_Concept\_ID |  Concept ID of the clinical ingredient |
|  Ingredient\_Name |  Name of the clinical ingredient |
|  Ingredient\_Concept\_Code |  Concept code of the clinical ingredient |
|  Ingredient\_Concept\_Class |  Concept Class of the clinical ingredient |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19102189 |
|  Drug\_Name |  Omeprazole 20 MG Enteric Coated Tablet |
|  Drug\_Concept\_Code |  402014 |
|  Drug\_Concept\_Class |  Clinical Drug |
|  Ingredient\_Concept\_ID |  923645 |
|  Ingredient\_Name |  Omeprazole |
|  Ingredient\_Concept\_Code |  7646 |
|  Ingredient\_Concept\_Class |  Ingredient |
**D04:** Find drugs by ingredient

This query is designed to extract all drugs that contain a specified ingredient. The query accepts an ingredient concept ID as the input and returns all drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient.
The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the concept table for concept class of 'Ingredient', e.g. using query  [D02](http://vocabqueries.omop.org/drug-queries/d2).

**Sample query:**

SELECT

        A.concept\_id Ingredient\_concept\_id,

        A.concept\_Name Ingredient\_name,

        A.concept\_Code Ingredient\_concept\_code,

        A.concept\_Class\_id Ingredient\_concept\_class,

        D.concept\_id Drug\_concept\_id,

        D.concept\_Name Drug\_name,

        D.concept\_Code Drug\_concept\_code,

        D.concept\_Class\_id Drug\_concept\_class

FROM

        full\_201706\_omop\_v5.concept\_ancestor CA,

        full\_201706\_omop\_v5.concept A,

        full\_201706\_omop\_v5.concept D

WHERE

        CA.ancestor\_concept\_id = A.concept\_id

        AND CA.descendant\_concept\_id = D.concept\_id

        AND sysdate BETWEEN A.valid\_start\_date AND A.valid\_end\_date

        AND sysdate BETWEEN D.valid\_start\_date AND D.valid\_end\_date

        AND CA.ancestor\_concept\_id = 966991;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  966991 |  Yes | Concept ID for 'Simethicone'.
Ingredient concepts can be extracted from CONCEPT table as records of concept class of 'Ingredient' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient entered as input |
|  Ingredient\_name |  Name of the ingredient |
|  Ingredient\_Concept\_code |  Concept code of the ingredient |
|  Ingredient\_Concept\_class |  Concept Class of the ingredient |
|  Generic\_Concept\_ID |  Concept ID of drug with the ingredient |
|  Generic\_Name |  Name of drug concept with the ingredient |
|  Generic\_Concept\_Code |  Concept code of the drug with the ingredient |
|  Generic\_Concept\_Class |  Concept class of drug with the ingredient |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  966991 |
|  Ingredient\_name |  Simethicone |
|  Ingredient\_Concept\_code |  9796 |
|  Ingredient\_Concept\_class |  Ingredient |
|  Generic\_Concept\_ID |  967306 |
|  Generic\_Name |  Simethicone 10 MG/ML Oral Solution |
|  Generic\_Concept\_Code |  251293 |
|  Generic\_Concept\_Class |  Clinical Drug |
**D05:** Find generic drugs by ingredient

This query is designed to extract all generic drugs that have a specified ingredient. The query accepts an ingredient concept ID as the input and returns all generic (not branded) drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient.
The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the CONCEPT table for concept class of 'Ingredient'

**Sample query:**

SELECT        A.concept\_id Ingredient\_concept\_id,

                A.concept\_Name Ingredient\_name,

                A.concept\_Code Ingredient\_concept\_code,

                A.concept\_Class\_id Ingredient\_concept\_class,

                D.concept\_id Generic\_concept\_id,

                D.concept\_Name Generic\_name,

                D.concept\_Code Generic\_concept\_code,

                D.concept\_class\_id Generic\_concept\_class

FROM        concept\_ancestor CA,

                concept A,

                concept D

WHERE

        CA.ancestor\_concept\_id                 = 966991

AND        CA.ancestor\_concept\_id                = A.concept\_id

AND CA.descendant\_concept\_id        = D.concept\_id

AND        D.concept\_class\_id                        = 'Clinical Drug'

AND        sysdate                                                BETWEEN A.valid\_start\_date AND A.valid\_end\_date AND sysdate BETWEEN D.valid\_start\_date AND D.valid\_end\_date

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Ingredient Concept ID  |  966991 |  Yes | Concept ID for 'Simethicone'.
Ingredient concepts can be extracted from CONCEPT table as records of concept class of 'Ingredient' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient entered as input |
|  Ingredient\_name |  Name of the Ingredient |
|  Ingredient\_Concept\_code |  Concept code of the ingredient |
|  Ingredient\_Concept\_class |  Concept Class of the ingredient |
|  Generic\_Concept\_ID |  Concept ID of drug with the ingredient |
|  Generic\_Name |  Name of drug concept with the ingredient |
|  Generic\_Concept\_Code |  Concept code of the drug with the ingredient |
|  Generic\_Concept\_Class |  Concept class of drug with the ingredient |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  966991 |
|  Ingredient\_name |  Simethicone |
|  Ingredient\_Concept\_code |  9796 |
|  Ingredient\_Concept\_class |  Ingredient |
|  Generic\_Concept\_ID |  967306 |
|  Generic\_Name |  Simethicone 10 MG/ML Oral Solution |
|  Generic\_Concept\_Code |  251293 |
|  Generic\_Concept\_Class |  Clinical Drug |
**D06:** Find branded drugs by ingredient

This query is designed to extract all branded drugs that have a specified ingredient. The query accepts an ingredient concept ID as the input and returns all branded drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient. The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the CONCEPT table for concept class of 'Ingredient'.

**Sample query:**

SELECT        A.concept\_id Ingredient\_concept\_id,

                A.concept\_name Ingredient\_concept\_name,

                A.concept\_code Ingredient\_concept\_code,

                A.concept\_class\_id Ingredient\_concept\_class,

                D.concept\_id branded\_drug\_id,

                D.concept\_name branded\_drug\_name,

                D.concept\_code branded\_drug\_concept\_code,

                D.concept\_class\_id branded\_drug\_concept\_class

FROM        concept\_ancestor CA,

                concept A,

                concept D

WHERE

        CA.ancestor\_concept\_id                = 966991

AND        CA.ancestor\_concept\_id                = A.concept\_id

AND        CA.descendant\_concept\_id        = D.concept\_id

AND        D.concept\_class\_id                        = 'Branded Drug'

AND        sysdate                                                BETWEEN A.valid\_start\_date AND A.valid\_end\_date AND sysdate BETWEEN D.valid\_start\_date AND D.valid\_end\_date

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  966991 |  Yes | Concept ID for 'Simethicone'. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient entered as input |
|  Ingredient\_name |  Name of the Ingredient |
|  Ingredient\_Concept\_code |  Concept code of the ingredient |
|  Ingredient\_Concept\_class |  Concept Class of the ingredient |
|  Branded\_Drug\_ID |  Concept ID of branded drug with the ingredient |
|  Branded\_Drug\_Name |  Name of branded drug concept with the ingredient |
|  Branded\_Drug\_Concept\_Code |  Concept code of the branded drug with the ingredient |
|  Branded\_Drug\_Concept\_Class |  Concept class of branded drug with the ingredient |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  966991 |
|  Ingredient\_name |  Simethicone |
|  Ingredient\_Concept\_code |  9796 |
|  Ingredient\_Concept\_class |  Ingredient |
|  Branded\_Drug\_ID |  19132733 |
|  Branded\_Drug\_Name |  Simethicone 66.7 MG/ML Oral Suspension [Mylicon] |
|  Branded\_Drug\_Concept\_Code |  809376 |
|  Branded\_Drug\_Concept\_Class |  Branded Drug |
**D07:** Find single ingredient drugs by ingredient

This query accepts accepts an ingredient concept ID and returns all drugs which contain only one ingredient specified in the query. This query is useful when studying drug outcomes for ingredients where the outcome or drug-drug interaction effect of other ingredients needs to be avoided. Indications have to be provided as FDB (vocabulary\_id=19) or NDF-RT indications (vocabulary\_id=7).

**Sample query:**

SELECT

      c.concept\_id     as drug\_concept\_id,

      c.concept\_name   as drug\_concept\_name,

      c.concept\_class\_id  as drug\_concept\_class\_id

FROM concept c

INNER JOIN (

  SELECT drug.cid FROM (

    SELECT a.descendant\_concept\_id cid, count(\*) cnt FROM concept\_ancestor a

    INNER JOIN (

      SELECT c.concept\_id FROM concept c, concept\_ancestor a

      WHERE a.ancestor\_concept\_id = 1000560

      AND a.descendant\_concept\_id = c.concept\_id AND c.vocabulary\_id = 'RxNorm'

    ) cd ON cd.concept\_id = a.descendant\_concept\_id

    INNER JOIN concept c ON c.concept\_id=a.ancestor\_concept\_id

        WHERE c.concept\_class\_id = 'Ingredient'

    GROUP BY a.descendant\_concept\_id

  ) drug WHERE drug.cnt = 1  -- contains only 1 ingredient

) onesie ON onesie.cid = c.concept\_id

WHERE sysdate BETWEEN valid\_start\_date AND valid\_end\_date

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Ingredient Concept ID |  1000560 |  Yes | Concept ID for ingredient 'Ondansetron' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of a drug |
|  Drug\_Concept\_Name |  Name of drug Concept |
|  Drug\_Concept\_Class |  Concept Code of drug |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  40227201 |
|  Drug\_Concept\_Name |  Ondansetron 0.16 MG/ML Injectable Solution |
|  Drug\_Concept\_Class |  Clinical Drug |
**D08:** Find drug classes for a drug or ingredient

This query is designed to return the therapeutic classes that associated with a drug. The query accepts a standard drug concept ID (e.g. as identified from query  [G03](http://vocabqueries.omop.org/general-queries/g3)) as the input. The drug concept can be a clinical or branded drug or pack (concept\_level=1), or an ingredient (concept\_level=2). The query returns one or more therapeutic classes associated with the drug based on the following classifications.).

- Enhanced Therapeutic Classification (ETC)
- Anatomical Therapeutic Chemical classification (ATC)
- NDF-RT Mechanism of Action (MoA)
- NDF-RT Physiologic effect
- NDF-RT Chemical structure
- VA Class

By default, the query returns therapeutic classes based on all the classification systems listed above. Additional clauses can be added to restrict the query to a single classification system.

**Sample query:**

SELECT

 c1.concept\_id                 Class\_Concept\_Id,

 c1.concept\_name               Class\_Name,

 c1.concept\_code               Class\_Code,

 c1.concept\_class\_id              Classification,

 c1.vocabulary\_id              Class\_vocabulary\_id,

 v1.vocabulary\_name            Class\_vocabulary\_name,

 ca.min\_levels\_of\_separation  Levels\_of\_Separation

FROM concept\_ancestor   ca,

 concept                c1,

 vocabulary             v1

WHERE

ca.ancestor\_concept\_id = c1.concept\_id

AND    c1.vocabulary\_id IN ('NDFRT', 'ETC', 'ATC', 'VA Class')

AND    c1.concept\_class\_id IN ('ATC','VA Class','Mechanism of Action','Chemical Structure','ETC','Physiologic Effect')

AND    c1.vocabulary\_id = v1.vocabulary\_id

AND    ca.descendant\_concept\_id = 1545999

AND    sysdate BETWEEN c1.valid\_start\_date AND c1.valid\_end\_date;



**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|   Drug Concept ID |  1545999 |  Yes | Concept Identifier from RxNorm for 'atorvastatin 20 MG Oral Tablet [Lipitor]' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Class\_Concept\_ID |  Concept ID of the therapeutic class |
|  Class\_Name |  Name of the therapeutic class |
|  Class\_Code |  Concept Code of therapeutic class |
|  Classification |  Concept class of therapeutic class |
|  Class\_Vocabulary\_ID |  Vocabulary the therapeutic class is derived from, expressed as vocabulary ID |
|  Class\_Vocabulary\_Name |  Name of the vocabulary the therapeutic class is derived from |
|  Levels\_of\_Separation |  Levels of separation between the drug concept and the therapeutic class. Important for hierarchic classification systems to identify classes and subclasses for the drug. |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Class\_Concept\_ID |  21500263 |
|  Class\_Name |  Antihyperlipidemics |
|  Class\_Code |  263 |
|  Classification |  Enhanced Therapeutic Classification |
|  Class\_Vocabulary\_ID |  20 |
|  Class\_Vocabulary\_Name |  ETC |
|  Levels\_of\_Separation |  2 |
**D09:** Find drugs by drug class

This query is designed to extract all drugs that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class .
Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY\_ID = 20
- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY\_ID = 21

– NDF-RT Mechanism of Action (MoA), Vocabulary ID = 7, Concept Class = 'Mechanism of Action'

– NDF-RT Physiologic effect (PE),        Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

– NDF-RT Chemical Structure,              Vocabulary ID = 7, Concept Class = 'Chemical Structure'

- VA Class, Vocabulary ID = 32

**Sample query:**

SELECT  c.concept\_id      drug\_concept\_id,

        c.concept\_name   drug\_concept\_name,

        c.concept\_class\_id  drug\_concept\_class,

        c.concept\_code   drug\_concept\_code

FROM    concept          c,

         concept\_ancestor ca

WHERE   ca.ancestor\_concept\_id = 21506108

        AND  c.concept\_id            = ca.descendant\_concept\_id

        AND  c.vocabulary\_id         = 'RxNorm'

        AND  c.domain\_id = 'Drug'

        AND  c.standard\_concept = 'S'

           AND sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug included in therapeutic class |
|  Drug\_Concept\_Name |  Name of drug concept included in therapeutic class |
|  Drug\_Concept\_Class |  Concept class of drug concept included in therapeutic class |
|  Drug\_Concept\_Code |  RxNorm source code of drug concept |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  1308221 |
|  Drug\_Concept\_Name |  Lisinopril 40 MG Oral Tablet |
|  Drug\_Concept\_Class |  Clinical Drug |
|  Drug\_Concept\_Code |  197884 |
**D10:** Find ingredient by drug class

This query is designed to extract all ingredients that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class.
Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY\_ID = 20
- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY\_ID = 21

– NDF-RT Mechanism of Action (MoA), Vocabulary ID = 7, Concept Class = 'Mechanism of Action'

– NDF-RT Physiologic effect (PE), Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

– NDF-RT Chemical Structure, Vocabulary ID = 7, Concept Class = 'Chemical Structure'

-  VA Class, VOCABULARY\_ID = 32

**Sample query:**

SELECT  c.concept\_id    ingredient\_concept\_id,

        c.concept\_name  ingredient\_concept\_name,

        c.concept\_class\_id ingredient\_concept\_class,

        c.concept\_code  ingredient\_concept\_code

 FROM   concept          c,

        concept\_ancestor ca

 WHERE  ca.ancestor\_concept\_id = 21506108

   AND  c.concept\_id           = ca.descendant\_concept\_id

   AND  c.vocabulary\_id        = 'RxNorm'

   AND c.concept\_class\_id = 'Ingredient'

   AND  sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |



**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of ingredient included in therapeutic class |
|  Ingredient\_Concept\_Name |  Name of ingredient concept included in therapeutic class |
|  Ingredient\_Concept\_Class |  Concept class of ingredient concept included in therapeutic class |
|  Ingredient\_Concept\_Code |  RxNorm source code of ingredient concept |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  1308216 |
|  Ingredient\_Concept\_Name |  Lisinopril |
|  Ingredient\_Concept\_Class |  Ingredient |
|  Ingredient\_Concept\_Code |  29046 |
**D11:** Find source codes by drug class

This query is designed to extract codes from a non-standard drug vocabulary that belong to a therapeutic class. The query accepts a therapeutic class concept ID and the vocabualry ID of the desired source vocabulary as input and returns all codes that are included under that class and that belong to a source vocabulary. This query could be used to derive e.g. all NDC codes that belong to a certain drug class.

**Sample query:**

SELECT  d.concept\_code,

        d.vocabulary\_id,

        v.vocabulary\_name

 FROM concept\_ancestor ca

         JOIN concept d on d.concept\_id = ca.descendant\_concept\_id

        JOIN concept a on a.concept\_id = ca.ancestor\_concept\_id

        JOIN vocabulary v on d.vocabulary\_id = v.vocabulary\_id

 WHERE  ca.ancestor\_concept\_id = 21506108

   AND  a.vocabulary\_id = 'NDC'

   AND  d.domain\_id = 'Drug'

   AND sysdate BETWEEN d.valid\_start\_date AND d.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |
|  Source Vocabulary ID |  9 |  Yes | One of the above drug vocabulary ID's |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Source\_Code |  Source code of drug in non-standard vocabulary (e.g. NDC code, FDA SPL number etc.) |
|  Source\_Vocabulary\_ID |  Vocabulary ID of source vocabulary |
|  Source\_Vocabulary\_Name |  Vocabulary name of source vocabulary |
|  Source\_Code\_Description |  Description of source code |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Source\_Code |  00003033805 |
|  Source\_Vocabulary\_ID |  9 |
|  Source\_Vocabulary\_Name |  NDC |
|  Source\_Code\_Description |  Captopril 25 MG / Hydrochlorothiazide 15 MG Oral Tablet |
**D12:** Find indications for a drug

This query is designed to extract indications associated with a drug. The query accepts a standard drug concept ID (e.g. as identified from query  [G03](http://vocabqueries.omop.org/general-queries/g3)) as the input and returns all available indications associated with the drug.
The vocabulary includes indications available from more than one source vocabulary:

- First Data Bank (FDB), defined mostly for clinical drug concepts
- NDF-RT defined mostly for ingredients

FDB also distinguishes indications based on their presence in the drug label (or package insert) as FDA approved or off-label. NDF-RT distinguishes between treatment or prevention indication. The segmentation is preserved in the vocabulary through separate concept relationships.

**Sample query:**

SELECT

  r.relationship\_name as type\_of\_indication,

  c.concept\_id as indication\_concept\_id,

  c.concept\_name as indication\_concept\_name,

  c.vocabulary\_id as indication\_vocabulary\_id,

  vn.vocabulary\_name as indication\_vocabulary\_name

FROM

  concept c,

  vocabulary vn,

  relationship r,

  ( -- collect all indications from the drugs, ingredients and pharmaceutical preps and the type of relationship

    SELECT DISTINCT

      r.relationship\_id rid,

      r.concept\_id\_2 cid

    FROM concept c

    INNER JOIN ( -- collect onesie clinical and branded drug if query is ingredient

      SELECT onesie.cid concept\_id

      FROM (

        SELECT

          a.descendant\_concept\_id cid,

          count(\*) cnt

        FROM concept\_ancestor a

        INNER JOIN (

          SELECT c.concept\_id

          FROM

            concept c,

            concept\_ancestor a

          WHERE

            a.ancestor\_concept\_id=19005968 AND

            a.descendant\_concept\_id=c.concept\_id AND

            c.vocabulary\_id=8

        ) cd on cd.concept\_id=a.descendant\_concept\_id

        INNER JOIN concept c on c.concept\_id=a.ancestor\_concept\_id

        WHERE c.concept\_level=2

        GROUP BY a.descendant\_concept\_id

      ) onesie

      where onesie.cnt=1

      UNION -- collect ingredient if query is clinical and branded drug

      SELECT c.concept\_id

      FROM

        concept c,

        concept\_ancestor a

      WHERE

        a.descendant\_concept\_id=19005968 AND

        a.ancestor\_concept\_id=c.concept\_id AND

        c.vocabulary\_id=8

      UNION -- collect pharmaceutical preparation equivalent to which NDFRT has reltionship

      SELECT c.concept\_id

      FROM

        concept c,

        concept\_ancestor a

      WHERE

        a.descendant\_concept\_id=19005968 AND

        a.ancestor\_concept\_id=c.concept\_id AND

        lower(c.concept\_class)='pharmaceutical preparations'

      UNION -- collect itself

      SELECT 19005968

    ) drug ON drug.concept\_id=c.concept\_id

    INNER JOIN concept\_relationship r on c.concept\_id=r.concept\_id\_1 -- allow only indication relationships

    WHERE

      r.relationship\_id IN (21,23,155,156,126,127,240,241)

  ) ind

  WHERE

    ind.cid=c.concept\_id AND

    r.relationship\_id=ind.rid AND

    vn.vocabulary\_id=c.vocabulary\_id AND

    sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|   Drug Concept ID |   19005968 |  Yes | Drugs concepts from RxNorm with a concept class of 'Clinical drug or pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Type\_of\_Indication |  Type of indication, indicating one of the following:
- FDA approved/off-label indication
- Treatment/prevention indication
 |
|  Indication\_Concept\_ID |  Concept ID of the therapeutic class |
|  Indication\_Concept\_Name |  Name of the Indication concept |
|  Indication\_Vocabulary\_ID |  Vocabulary the indication is derived from, expressed as vocabulary ID |
|  Indication\_Vocabulary\_Name |  Name of the vocabulary the indication is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Type\_of\_Indication |  Has FDA-approved drug indication (FDB) |
|  Indication\_Concept\_ID |  21003511 |
|  Indication\_Concept\_Name |  Cancer Chemotherapy-Induced Nausea and Vomiting |
|  Indication\_Vocabulary\_ID |  19 |
|  Indication\_Vocabulary\_Name |  FDB Indication |
**D13**** :**Find indications as condition concepts for a drug

This query accepts a mapped drug code instead of a standard drug concept ID as the input. The result set from the returns detailed of indications associated with the drug.

**Sample query:**

SELECT

  rn.relationship\_name as type\_of\_indication,

  c.concept\_id as indication\_concept\_id,

  c.concept\_name as indication\_concept\_name,

  c.vocabulary\_id as indication\_vocabulary\_id,

  vn.vocabulary\_name as indication\_vocabulary\_name

FROM

  concept c,

  vocabulary vn,

  relationship rn,

  ( -- collect all indications from the drugs, ingredients and pharmaceutical preps and the type of relationship

    SELECT DISTINCT

      r.relationship\_id rid,

      r.concept\_id\_2 cid

    FROM concept c

    INNER JOIN ( -- collect onesie clinical and branded drug if query is ingredient

      SELECT onesie.cid concept\_id

      FROM (

        SELECT

          a.descendant\_concept\_id cid,

          count(\*) cnt

        FROM concept\_ancestor a

        INNER JOIN (

          SELECT c.concept\_id

          FROM

            concept c,

            concept\_ancestor a

          WHERE

            a.ancestor\_concept\_id=19005968 AND

            a.descendant\_concept\_id=c.concept\_id AND

            c.vocabulary\_id=8

        ) cd on cd.concept\_id=a.descendant\_concept\_id

        INNER JOIN concept c on c.concept\_id=a.ancestor\_concept\_id

        WHERE c.concept\_level=2

        GROUP BY a.descendant\_concept\_id

      ) onesie

      where onesie.cnt=1

      UNION -- collect ingredient if query is clinical and branded drug

      SELECT c.concept\_id

      FROM

        concept c,

        concept\_ancestor a

      WHERE

        a.descendant\_concept\_id=19005968 AND

        a.ancestor\_concept\_id=c.concept\_id AND

        c.vocabulary\_id=8

      UNION -- collect pharmaceutical preparation equivalent to which NDFRT has reltionship

      SELECT c.concept\_id

      FROM

        concept c,

        concept\_ancestor a

      WHERE

        a.descendant\_concept\_id=19005968 AND

        a.ancestor\_concept\_id=c.concept\_id AND

        lower(c.concept\_class)='pharmaceutical preparations'

      UNION -- collect itself

      SELECT 19005968

    ) drug ON drug.concept\_id=c.concept\_id

    INNER JOIN concept\_relationship r on c.concept\_id=r.concept\_id\_1 -- allow only indication relationships

    WHERE

      r.relationship\_id IN (21,23,155,156,126,127,240,241)

  ) ind

  INNER JOIN concept\_relationship r ON r.concept\_id\_1=ind.cid

  WHERE

    r.concept\_id\_2=c.concept\_id AND

    r.relationship\_id in (247, 248) AND

    ind.rid=rn.relationship\_id AND

    vn.vocabulary\_id=c.vocabulary\_id AND

    sysdate BETWEEN c.valid\_start\_date AND c.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|   Drug Concept ID |   19005968 |  Yes | Drugs concepts from RxNorm with a concept class of 'Branded Drug' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Type\_of\_Indication |  Type of indication, indicating one of the following:
- FDA approved/off-label indication
- Treatment/prevention indication
 |
|  Indication\_Concept\_ID |  Concept ID of the therapeutic class |
|  Indication\_Concept\_Name |  Name of the Indication concept |
|  Indication\_Vocabulary\_ID |  Vocabulary the indication is derived from, expressed as vocabulary ID |
|  Indication\_Vocabulary\_Name |  Name of the vocabulary the indication is derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Type\_of\_Indication |  Has FDA-approved drug indication (FDB) |
|  Indication\_Concept\_ID |  27674 |
|  Indication\_Concept\_Name |  N&V - Nausea and vomiting |
|  Indication\_Vocabulary\_ID |  1 |
|  Indication\_Vocabulary\_Name |  SNOMED-CT |
**D14:** Find drugs for an indication

This query provides all clinical or branded drugs that are indicated for a certain indication. Indications have to be given as FDB indications (vocabulary\_id=19) or NDF-RT indications (vocabulary\_id=7). Indications can be identified using the generic query  [G03](http://vocabqueries.omop.org/general-queries/g3), or, if at least one drug is known for this indication, query  [D04](http://vocabqueries.omop.org/drug-queries/d4).

**Sample query:**

SELECT

        drug.concept\_id      as drug\_concept\_id,

        drug.concept\_name    as drug\_concept\_name,

        drug.concept\_code    as drug\_concept\_code

 FROM   concept drug,

        concept\_ancestor a

 WHERE  a.ancestor\_concept\_id   = 21000039

 AND    a.descendant\_concept\_id = drug.concept\_id

 AND         drug.standard\_concept = 'S'

 AND    drug.domain\_id = 'Drug'

 AND    drug.vocabulary\_id = 'RxNorm'

 AND    sysdate BETWEEN drug.valid\_start\_date AND drug.valid\_end\_date

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  21000039 |  Yes | FDB indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of the drug |
|  Drug\_Concept\_Name |  Name of the drug |
|  Drug\_Concept\_Code |  Concept code of the drug |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  1710446 |
|  Drug\_Concept\_Name |  Cycloserine |
|  Drug\_Concept\_Code |  3007 |
**D15:** Find drugs for an indication provided as condition concepts

This query provides all clinical/branded drugs that are indicated for a certain indication. Indications have to be provided as SNOMED-CT concept (vocabulary\_id=1).

**Sample query:**

SELECT DISTINCT

  drug.concept\_id as drug\_concept\_id,

  drug.concept\_name as drug\_concept\_name,

  drug.concept\_code as drug\_concept\_code

FROM

  concept drug,

  concept\_ancestor snomed,

  concept\_ancestor ind,

  concept\_relationship r

WHERE

  snomed.ancestor\_concept\_id = 253954 AND

  snomed.descendant\_concept\_id = r.concept\_id\_1 AND

  concept\_id\_2 = ind.ancestor\_concept\_id AND

  r.relationship\_id in (247, 248) AND

  ind.descendant\_concept\_id = drug.concept\_id AND

  drug.concept\_level = 1 AND

  drug.vocabulary\_id = 8 AND

  sysdate BETWEEN drug.valid\_start\_date AND drug.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  253954 |  Yes | SNOMED-CT indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of the drug |
|  Drug\_Concept\_Name |  Name of the drug |
|  Drug\_Concept\_Code |  Concept code of the drug |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19073074 |
|  Drug\_Concept\_Name |  Aminosalicylic Acid 500 MG Oral Tablet |
|  Drug\_Concept\_Code |  308122 |
**D16:** Find drugs for an indication by indication type

This query provides all drugs that are indicated for a certain condition. In addition, it provides the type of indication: FDA-approved, off-label (both based on FDB indication classes) and may treat and may prevent (both based on NDF-RT). Indications have to be provided as FDB indications (vocabulary\_id=19) or NDF-RT (vocabulary\_id=7).

**Sample query:**

SELECT DISTINCT

 drug.concept\_id      as drug\_concept\_id,

 drug.concept\_name    as drug\_concept\_name,

 drug.concept\_code    as drug\_concept\_code,

 rn.relationship\_name as indication\_type,

 indication\_relation.relationship\_id

FROM

  concept\_relationship indication\_relation

INNER JOIN concept\_ancestor a

 ON a.ancestor\_concept\_id=indication\_relation.concept\_id\_2

INNER JOIN concept drug

 ON drug.concept\_id=a.descendant\_concept\_id

INNER JOIN relationship rn

 ON rn.relationship\_id=indication\_relation.relationship\_id

WHERE indication\_relation.concept\_id\_1 = 4345991

  AND drug.vocabulary\_id = 'RxNorm'

  AND drug.standard\_concept = 'S'

  AND indication\_relation.relationship\_id in (

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

  AND sysdate BETWEEN drug.valid\_start\_date AND drug.valid\_end\_date;



**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of the drug |
|  Drug\_Concept\_Name |  Name of the drug |
|  Drug\_Concept\_Code |  Concept code of the drug |
|  Indication\_Type |  One of the FDB, NDF-RT or OMOP inferred indication types |
|  Relationship\_id |  Corresponding relationship ID to the Indication Type |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19019530 |
|  Drug\_Concept\_Name |  Perphenazine 4 MG Oral Tablet |
|  Drug\_Concept\_Code |  198077 |
|  Indication\_Type |  Inferred ingredient of (OMOP) |
|  Relationship\_id |  281 |
**D17:** Find ingredients for an indication

This query provides ingredients that are designated for a certain indication. Indications have to be given as FDB indications (vocabulary\_id=19) or NDF-RT indications (vocabulary\_id=7). Indications can be identified using the generic query  [G03](http://vocabqueries.omop.org/general-queries/g3), or, if at least one drug is known for this indication, query  [D04](http://vocabqueries.omop.org/drug-queries/d4).

**Sample query:**

SELECT

  ingredient.concept\_id as ingredient\_concept\_id,

  ingredient.concept\_name as ingredient\_concept\_name,

  ingredient.concept\_code as ingredient\_concept\_code

FROM

  concept ingredient,

  concept\_ancestor a

WHERE

  a.ancestor\_concept\_id = 4345991 AND

  a.descendant\_concept\_id = ingredient.concept\_id AND

  ingredient.concept\_level = 2 AND

  ingredient.vocabulary\_id = 8 AND

  sysdate BETWEEN ingredient.valid\_start\_date AND ingredient.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient |
|  Ingredient\_Concept\_Name |  Name of the ingredient |
|  Ingredient\_Concept\_Code |  Concept code of the ingredient |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  733008 |
|  Ingredient\_Concept\_Name |  Perphenazine |
|  Ingredient\_Concept\_Code |  8076 |
**D18:** Find ingredients for an indication provided as condition concept

This query provides all ingredients that are indicated for a certain indication. Indications have to be provided as SNOMED-CT concept ID (vocabulary\_id=1).

**Sample query:**

SELECT DISTINCT

  ingredient.concept\_id as ingredient\_concept\_id,

  ingredient.concept\_name as ingredient\_concept\_name,

  ingredient.concept\_code as ingredient\_concept\_code

FROM

  concept ingredient,

  concept\_ancestor snomed,

  concept\_ancestor ind,

  concept\_relationship r

WHERE

  snomed.ancestor\_concept\_id = 253954 AND

  snomed.descendant\_concept\_id = r.concept\_id\_1 AND

  concept\_id\_2 = ind.ancestor\_concept\_id AND

  r.relationship\_id in (247, 248) AND

  ind.descendant\_concept\_id = ingredient.concept\_id AND

  ingredient.concept\_level = 2 AND

  ingredient.vocabulary\_id = 8 AND

  sysdate BETWEEN ingredient.valid\_start\_date AND ingredient.valid\_end\_date;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  253954 |  Yes | SNOMED-CT indication concept ID |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |





**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient |
|  Ingredient\_Concept\_Name |  Name of the ingredient |
|  Ingredient\_Concept\_Code |  Concept code of the ingredient |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  1790868 |
|  Ingredient\_Concept\_Name |  Amikacin |
|  Ingredient\_Concept\_Code |  641 |
**D19:** Find ingredients for an indication by indication type

This query provides all ingredients that are indicated for a certain condition. In addition, it provides the type of indication: FDA-approved, off-label (both based on FDB indication classes) and may treat and may prevent (both based on NDF-RT). Indications have to be provided as FDB indications (vocabulary\_id=19) or NDF-RT (vocabulary\_id=7).

**Sample query:**

SELECT DISTINCT

  ingredient.concept\_id as ingredient\_concept\_id,

  ingredient.concept\_name as ingredient\_concept\_name,

  ingredient.concept\_code as ingredient\_concept\_code,

  rn.relationship\_name as indication\_type,

  indication\_relation.relationship\_id

FROM

  concept\_relationship indication\_relation

INNER JOIN

  concept\_ancestor a ON a.ancestor\_concept\_id=indication\_relation.concept\_id\_2

INNER JOIN

  concept ingredient ON ingredient.concept\_id=a.descendant\_concept\_id

INNER JOIN

  relationship rn ON rn.relationship\_id = indication\_relation.relationship\_id

WHERE

  indication\_relation.concept\_id\_1 = 4345991 AND

  ingredient.vocabulary\_id = 8 AND

  ingredient.concept\_level = 2 AND

  indication\_relation.relationship\_id in (21,23,155,157,126,127,240,241,281,282) AND

  sysdate BETWEEN ingredient.valid\_start\_date AND ingredient.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Ingredient\_Concept\_ID |  Concept ID of the ingredient |
|  Ingredient\_Concept\_Name |  Name of the ingredient |
|  Ingredient\_Concept\_Code |  Concept code of the ingredient |
|  Indication\_Type |  One of the FDB, NDF-RT or OMOP inferred indication types |
|  Relationship\_id |  Corresponding relationship ID to the Indication Type |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Ingredient\_Concept\_ID |  733008 |
|  Ingredient\_Concept\_Name |  Perphenazine |
|  Ingredient\_Concept\_Code |  8076 |
|  Indication\_Type |  Inferred ingredient of (OMOP) |
|  Relationship\_id |  281 |
**D20:** Find dose form of a drug

This query accepts concept IDs for a drug product (clinical or branded drug or pack) and identifies the dose form.

The query relies on RxNorm concept relationship (4 – 'Has dose form (RxNorm)') for this.

**Sample query:**

SELECT

        A.concept\_id drug\_concept\_id,

         A.concept\_name drug\_name,

         A.concept\_code drug\_concept\_code,

         D.concept\_id dose\_form\_concept\_id,

         D.concept\_name dose\_form\_concept\_name,

         D.concept\_code dose\_form\_concept\_code

FROM

        full\_201706\_omop\_v5.concept\_relationship CR,

         full\_201706\_omop\_v5.concept A,

         full\_201706\_omop\_v5.concept D

WHERE

        sysdate BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date

        AND CR.concept\_id\_1 = A.concept\_id

         AND CR.concept\_id\_2 = D.concept\_id

        AND CR.concept\_id\_1 = 19060647

        AND CR.relationship\_id = 'RxNorm has dose form'

        --AND CR.relationship\_ID = 4

        --AND A.concept\_class\_id ='Clinical Drug'

        --AND A.vocabulary\_id = 'RxNorm'

        ;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Drug Concept ID |  19060647 |  Yes | Must be a level 1 Clinical or Branded Drug or Pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug entered with specified dose form |
|  Drug\_Name |  Name of drug with specified dose form |
|  Drug\_Concept\_Code |  Concept ID of the dose form |
|  Dose\_Form\_Concept\_ID |  Concept ID of the dose form |
|  Dose\_Form\_Concept\_name |  Name of the dose form |
|  Dose\_Form\_Concept\_code |  Concept code of dose form |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  19060647 |
|  Drug\_Name |  Budesonide 0.2 MG/ACTUAT Inhalant Powder |
|  Drug\_Concept\_Code |  247047 |
|  Dose\_Form\_Concept\_ID |  19082259 |
|  Dose\_Form\_Concept\_name |  Inhalant Powder |
|  Dose\_Form\_Concept\_code |  317000 |
**D21:** Find route of administration of a drug

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

**Sample query:**

SELECT        A.concept\_id drug\_concept\_id,

                A.concept\_name drug\_concept\_name,

                A.concept\_code drug\_concept\_code,

                D.concept\_name dose\_form\_concept\_name,

                R.Route\_of\_Administration

FROM        concept\_relationship CR,

                concept A,

                concept D,

                route R

WHERE        CR.concept\_id\_1                = 40236916

AND         CR.relationship\_ID        = 'RxNorm has dose form'

AND         CR.concept\_id\_1                = A.concept\_id

AND         CR.concept\_id\_2                = D.concept\_id

AND                D.concept\_id                = R.concept\_id

AND                sysdate                                BETWEEN CR.valid\_start\_date AND CR.valid\_end\_date



**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Drug Concept ID  |  19060647 |  Yes | Must be a level 1 Clinical or Branded Drug or Pack |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug entered with specified dose form |
|  Drug\_Name |  Name of drug with specified dose form |
|  Drug\_Concept\_Code |  Concept code of the dose form |
|  Dose\_Form\_Concept\_name |  Name of the dose form |
|  Route\_Of\_Administration |  Derived route of administration for the drug |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19060647 |
|  Drug\_Name |  Budesonide 0.2 MG/ACTUAT Inhalant Powder |
|  Drug\_Concept\_Code |  247047 |
|  Dose\_Form\_Concept\_name |  Inhalant Powder |
|  Route\_Of\_Administration |  Inhaled |
**D22:** Find drugs by class and dose form

This query is designed to return a list of drug concept IDs that belong to a drug class and are of a certain dose form. The query ties together:

- Concept ancestor data to link drug concepts to therapeutic class
- RxNorm concept relationship 4 - 'Has dose form (RxNorm)

The results are combined to present a list of drugs from a specific therapeutic class with a specific dose form.

**Sample query:**

SELECT C.concept\_id drug\_concept\_id,

C.concept\_name drug\_concept\_name,

C.concept\_code drug\_concept\_code

FROM concept C,

        concept\_ancestor CA,

        concept\_relationship CRF,

        concept F

WHERE CA.ancestor\_concept\_id = 4318008

        AND C.concept\_id = CA.descendant\_concept\_id

        AND C.vocabulary\_id = 'RxNorm'

        AND C.standard\_concept = 'S'

        AND CRF.concept\_id\_1 = C.concept\_id

        AND CRF.relationship\_ID = 'RxNorm has dose form'

        AND CRF.concept\_id\_2 = F.concept\_id

        AND POSITION(LOWER(REPLACE(REPLACE(F.concept\_name, ' ', ''), '-', '')) IN

        LOWER(REPLACE(REPLACE('Nasal spray' , ' ', ''), '-', ''))) > 0

        AND sysdate BETWEEN CRF.valid\_start\_date AND CRF.valid\_end\_date

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| Therapeutic class Concept ID |  4318008 |  Yes | Concept ID for mechanism of action "Corticosteroid Hormone Receptor Agonists". Valid drug classes can be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2). |
|  Dose Form String |  'Nasal spray' |  Yes | Dose form string. Valid dose forms can be obtained using query  [D19](http://vocabqueries.omop.org/drug-queries/d19). |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug with specified therapeutic class and dose form |
|  Drug\_Name |  Name of drug with specified therapeutic class and dose form |
|  Drug\_Concept\_Code |  Source code of drug |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  904131 |
|  Drug\_Name |  Triamcinolone 0.055 MG/ACTUAT Nasal Spray |
|  Drug\_Concept\_Code |  245785 |
**D23:**  Find drugs by class and route of administration

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

**Sample query:**

SELECT        C.concept\_id drug\_concept\_id,

                C.concept\_name drug\_concept\_name,

                C.concept\_code drug\_concept\_code

FROM        concept C,

                concept\_ancestor CA,

                concept\_relationship CRF,

                concept F,

                route

WHERE

        CA.ancestor\_concept\_id        = 4318008

AND        C.concept\_id                        = CA.descendant\_concept\_id

AND        C.vocabulary\_id                        = 'RxNorm'

AND        C.standard\_concept                = 'S'

AND        CRF.concept\_id\_1                = C.concept\_id

AND        CRF.relationship\_ID                = 'RxNorm has dose form'

AND        CRF.concept\_id\_2                = F.concept\_id

AND        F.concept\_id                        = route.concept\_id

AND        sysdate                                        BETWEEN CRF.valid\_start\_date AND CRF.valid\_end\_date

AND        POSITION(LOWER(REPLACE(REPLACE(route.route\_of\_administration, ' ', ''), '-', '')) IN LOWER(REPLACE(REPLACE('vaginal' , ' ', ''), '-', ''))) > 0

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Therapeutic class Concept ID |  4318008 |  Yes | Concept ID for mechanism of action "Corticosteroid Hormone Receptor Agonists". Valid drug classes can be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) |
|  Dose Form String |  'vaginal' |  Yes | Route of administration string. |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug with specified therapeutic class and dose form |
|  Drug\_Name |  Name of drug with specified therapeutic class and dose form |
|  Drug\_Concept\_Code |  Source code of drug |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  40230686 |
|  Drug\_Name |  hydrocortisone acetate 10 MG/ML Vaginal Cream |
|  Drug\_Concept\_Code |  1039349 |
**D24:** Find the branded drugs in a list of drugs

This query is designed to identify branded drug concepts from a list of standard drug concept IDs. The query identifies branded drugs from the Concept table based on a concept class setting of 'Branded Drug'

**Sample query:**

SELECT C.concept\_id drug\_concept\_id,

        C.concept\_name drug\_name,

        C.concept\_code drug\_concept\_code,

        C.concept\_class\_id drug\_concept\_class,

        C.vocabulary\_id drug\_vocabulary\_id,

        V.vocabulary\_name drug\_vocabulary\_name

FROM concept C,

        vocabulary V

        WHERE C.vocabulary\_id = 'RxNorm'

                AND C.concept\_id IN (1396833, 19060643)

                AND C.concept\_class\_id = 'Clinical Drug'

                AND C.vocabulary\_id = V.vocabulary\_id

                AND sysdate BETWEEN C.valid\_start\_date AND C.valid\_end\_date

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Drug Concept ID list |  1516830, 19046168 |  Yes | List of drug concept id's |
|  As of date |  '01-Jan-2010' |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of branded drug or pack |
|  Drug\_Name |  Name of branded drug or pack |
|  Drug\_Concept\_Code |  Concept code of branded drug or pack |
|  Drug\_Concept\_Class |  Concept class of branded drug or pack |
|  Drug\_Vocabulary\_ID |  Vocabulary the branded drug concept has been derived from, expressed as vocabulary ID |
|  Drug\_Vocabulary\_Name |  Name of the Vocabulary the branded drug concept has been derived from |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19046168 |
|  Drug\_Name |  Triamcinolone 0.055 MG/ACTUAT Nasal Spray [Nasacort AQ] |
|  Drug\_Concept\_Code |  211501 |
|  Drug\_Concept\_Class |  Branded Drug |
|  Drug\_Vocabulary\_ID |  8 |
|  Drug\_Vocabulary\_Name |  RxNorm |
**D25:** Find the generic drugs in a list of drugs

This query is designed to identify generic drug concepts among from a list of standard drug concept IDs. The query identifies branded drugs from the CONCEPT table based on a concept class setting of 'Clinical Drug'

**Sample query:**

SELECT C.concept\_id drug\_concept\_id,

        C.concept\_name drug\_name,

        C.concept\_code drug\_concept\_code,

        C.concept\_class\_id drug\_concept\_class,

        C.vocabulary\_id drug\_vocabulary\_id,

        V.vocabulary\_name drug\_vocabulary\_name

FROM concept C,

        vocabulary V

        WHERE C.vocabulary\_id = 'RxNorm'

        AND C.concept\_id IN (1396833, 19060643)

        AND C.concept\_class\_id = 'Clinical Drug'

        AND C.vocabulary\_id = V.vocabulary\_id

        AND sysdate BETWEEN C.valid\_start\_date AND C.valid\_end\_date

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Drug Concept ID list |  1396833, 19060643 |  Yes | List of drug concept id's |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of generic drug or pack |
|  Drug\_Name |  Name of generic drug or pack |
|  Drug\_Concept\_Code |  Concept code of generic drug or pack |
|  Drug\_Concept\_Class |  Concept class of generic drug or pack |
|  Drug\_Vocabulary\_ID |  Vocabulary the generic drug concept has been derived from, expressed as vocabulary ID |
|  Drug\_Vocabulary\_Name |  Name of the Vocabulary the generic drug concept has been derived from |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19060643 |
|  Drug\_Name |  Budesonide 0.05 MG/ACTUAT Nasal Spray |
|  Drug\_Concept\_Code |  247042 |
|  Drug\_Concept\_Class |  Clinical Drug |
|  Drug\_Vocabulary\_ID |  8 |
|  Drug\_Vocabulary\_Name |  RxNorm |
**D26:** Find the brand name of a drug

This query is designed to accept a drug concept (both clinical and branded) as input and return a the brand name (or branded ingredient) associated with it. The query is useful to check for a brand names associated with a clinical drug. Drug concepts can be obtained using queries  [G03](http://vocabqueries.omop.org/general-queries/g3) or  [D02](http://vocabqueries.omop.org/drug-queries/d2).

**Sample query:**

SELECT A.Concept\_Id               drug\_concept\_id,

        A.Concept\_Name            drug\_name,

        A.Concept\_Code            drug\_concept\_code,

        A.concept\_class\_id           drug\_concept\_class\_id,

        D.Concept\_Id              brand\_concept\_id,

        D.Concept\_Name            brand\_name,

        D.Concept\_Code            brand\_concept\_code,

        D.concept\_class\_id           brand\_concept\_class\_id

FROM   concept\_relationship  CR003,

       concept               A,

       concept\_relationship  CR007,

       concept\_relationship  CR006,

       concept                 D

WHERE  CR003.relationship\_ID  = 'Has tradename'

AND    CR003.concept\_id\_1     = A.concept\_id

AND    lower(A.concept\_class\_id) = 'clinical drug'

AND    CR007.concept\_id\_2     = CR003.concept\_id\_2

AND    CR007.relationship\_ID  = 'Constitutes'

AND    CR007.concept\_id\_1     = CR006.concept\_id\_1

AND    CR006.relationship\_ID  = 'RxNorm has ing'

AND    CR006.concept\_id\_2     = D.concept\_id

AND    lower(D.concept\_class\_id) = 'branded name'

AND    A.concept\_Id           = 939355

AND    sysdate BETWEEN CR006.VALID\_START\_DATE AND CR006.VALID\_END\_DATE

UNION ALL

SELECT A.Concept\_Id               drug\_concept\_id,

       A.Concept\_Name             drug\_name,

       A.Concept\_Code             drug\_concept\_code,

       A.concept\_class\_id            drug\_concept\_class\_id,

       D.Concept\_Id               brand\_concept\_id,

       D.Concept\_Name             brand\_name,

       D.Concept\_Code             brand\_concept\_code,

       D.concept\_class\_id            brand\_concept\_class\_id

FROM   concept               A,

       concept\_relationship  CR007,

       concept\_relationship  CR006,

       concept               D

WHERE  lower(A.concept\_class\_id) = 'branded drug'

AND    CR007.concept\_id\_2     = A.concept\_id

AND    CR007.relationship\_ID  = 'Constitutes'

AND    CR007.concept\_id\_1     = CR006.concept\_id\_1

AND    CR006.relationship\_ID  = 'RxNorm has ing'

AND    CR006.concept\_id\_2     = D.concept\_id

AND    lower(D.concept\_class\_id) = 'branded name'

AND    A.concept\_Id           = 939355

AND    sysdate BETWEEN CR006.VALID\_START\_DATE AND CR006.VALID\_END\_DATE

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Drug Concept ID |  939355 |  Yes | Can be both clinical and branded drug concepts |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| **Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug\_Name |  Name of drug |
|  Drug\_Concept\_Code |  Concept code of the drug |
|  Drug\_Concept\_Class |  Concept class of drug |
|  Brand\_Concept\_ID |  Concept ID of the brand name (or branded ingredient) |
|  Brand\_name |  Name of the brand name |
|  Brand\_Concept\_code |  Concept code of the brand name |
|  Brand\_Concept\_class |  Concept Class of the brand name |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  19102189 |
|  Drug\_Name |  Omeprazole 20 MG Enteric Coated Tablet |
|  Drug\_Concept\_Code |  402014 |
|  Drug\_Concept\_Class |  Clinical Drug |
|  Brand\_Concept\_ID |  19045785 |
|  Brand\_name |  Prilosec |
|  Brand\_Concept\_code |  203345 |
|  Brand\_Concept\_class |  Brand Name |
**D27:** Find drugs of a brand

This query is designed to extract all clinical and branded drugs associated with a branded ingredient (or simply a brand name). Since the brand names are not part of the standard drug hierarchy in the OMOP vocabulary, the association between brand name and generic/branded drugs is made using a set of relationships.
The query requires a brand name concept ID as the input. Brand name concept IDs can be obtained by querying the Concept table for a concept class of 'Brand Name'.

**Sample query:**

SELECT  A.Concept\_Id               drug\_concept\_id,

        A.Concept\_Name             drug\_name,

        A.Concept\_Code             drug\_concept\_code,

        A.Concept\_Class\_id            drug\_concept\_class,

        D.Concept\_Id               brand\_concept\_id,

        D.Concept\_Name             brand\_name,

        D.Concept\_Code             brand\_concept\_code,

        D.Concept\_Class\_id            brand\_concept\_class

FROM   concept\_relationship  CR003,

       concept               A,

       concept\_relationship  CR007,

       concept\_relationship  CR006,

       concept               D

WHERE  CR003.relationship\_ID   = 'Constitutes'

AND    CR003.concept\_id\_1      = A.concept\_id

AND     lower(A.concept\_class\_id) = 'clinical drug'

AND    CR007.concept\_id\_2      = CR003.concept\_id\_2

AND    CR007.relationship\_id   = 'Has tradename'

AND    CR007.concept\_id\_1      = CR006.concept\_id\_1

AND    CR006.relationship\_id   = 'RxNorm has ing'

AND    CR006.concept\_id\_2      = D.concept\_id

AND    lower(D.concept\_class\_id)  = 'brand name'

AND    D.concept\_id            = 19011505

AND    sysdate BETWEEN CR006.valid\_start\_date AND CR006.valid\_end\_date

AND    sysdate BETWEEN CR007.valid\_start\_date AND CR007.valid\_end\_date

UNION ALL

SELECT  A.Concept\_Id               drug\_concept\_id,

        A.Concept\_Name             drug\_name,

        A.Concept\_Code             drug\_concept\_code,

        A.Concept\_Class\_id            drug\_concept\_class,

        D.Concept\_Id               brand\_concept\_id,

        D.Concept\_Name             brand\_name,

        D.Concept\_Code             brand\_concept\_code,

        D.Concept\_Class\_id            brand\_concept\_class

FROM   concept              A,

       concept\_relationship  CR007,

       concept\_relationship  CR006,

       concept               D

WHERE  lower(A.concept\_class\_id) = 'branded drug'

AND    CR007.concept\_id\_2     = A.concept\_id

AND    CR007.relationship\_ID  = 'Has tradename'

AND    CR007.concept\_id\_1     = CR006.concept\_id\_1

AND    CR006.relationship\_ID  = 'RxNorm has ing'

AND    CR006.concept\_id\_2     = D.concept\_id

AND    lower(D.concept\_class\_id) = 'brand name'

AND    D.concept\_id           = 19011505

AND    sysdate BETWEEN CR006.valid\_start\_date AND CR006.valid\_end\_date

AND    sysdate BETWEEN CR007.valid\_start\_date AND CR007.valid\_end\_date;

**Input:**

| **Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
|  Brand name Concept ID |  19011505 |  Yes | Concept ID for brand name 'Fosamax'.
Brand name concept IDs are listed in the CONCEPT table with a concept class of 'Brand name' |
|  As of date |  Sysdate |  No | Valid record as of specific date. Current date – sysdate is a default |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
|  Drug\_Concept\_ID |  Concept ID of drug (clinical/generic or branded) |
|  Drug\_Name |  Name of drug |
|  Drug\_Concept\_Code |  Concept code of the drug |
|  Drug\_Concept\_Class |  Concept class of drug |
|  Brand\_Concept\_ID |  Concept ID of the brand name entered as ingredient |
|  Brand\_name |  Name of the brand |
|  Brand\_Concept\_code |  Concept code of the brand name |
|  Brand\_Concept\_class |  Concept Class of the brand name |

**Sample output record:**

| **Field** | ** Value** |
| --- | --- |
|  Drug\_Concept\_ID |  40173591 |
|  Drug\_Name |  Alendronic acid 10 MG Oral Tablet [Fosamax] |
|  Drug\_Concept\_Code |  904421 |
|  Drug\_Concept\_Class |  Branded Drug |
|  Brand\_Concept\_ID |  19011505 |
|  Brand\_name |  Fosamax |
|  Brand\_Concept\_code |  114265 |
|  Brand\_Concept\_class |  Brand Name |
\*\*D01:\*\* Find drug concept by concept ID

This is the lookup for obtaining drug concept details associated with a concept identifier. This query is intended as a tool for quick reference for the name, class, level and source vocabulary details associated with a concept identifier.

This query is equivalent to  [G01](http://vocabqueries.omop.org/general-queries/g1), but if the concept is not in the drug domain the query still returns the concept details with the Is\\_Drug\\_Concept\\_Flag field set to 'No'.

\*\*Sample query:\*\*

SELECT

       C.concept\\_id Drug\\_concept\\_id,

       C.concept\\_name Drug\\_concept\\_name,

       C.concept\\_code Drug\\_concept\\_code,

       C.concept\\_class\\_id Drug\\_concept\\_class,

       C.standard\\_concept Drug\\_concept\\_level,

       C.vocabulary\\_id Drug\\_concept\\_vocab\\_id,

       V.vocabulary\\_name Drug\\_concept\\_vocab\\_code,

       /\\*( CASE C.vocabulary\\_id

               WHEN 'RxNorm' THEN

                       CASE lower(C.concept\\_class\\_id)

                       WHEN 'clinical drug' THEN 'Yes'

                       WHEN 'branded drug' THEN 'Yes'

                       WHEN 'ingredient' THEN 'Yes'

                       WHEN 'branded pack' THEN 'Yes'

                       WHEN 'clinical pack' THEN 'Yes'

                       ELSE 'No' END

               ELSE 'No' END) Is\\_Drug\\_Concept\\_flag \\*/

       (CASE C.domain\\_id WHEN 'Drug' THEN 'Yes' ELSE 'No' END) Is\\_Drug\\_Concept\\_flag

FROM

       full\\_201706\\_omop\\_v5.concept C,

       full\\_201706\\_omop\\_v5.vocabulary V

WHERE

       C.vocabulary\\_id = V.vocabulary\\_id

       AND sysdate BETWEEN C.valid\\_start\\_date AND C.valid\\_end\\_date

       AND C.concept\\_id = 1545999;



\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Concept ID |  1545999 |  Yes | Concept Identifier from RxNorm for 'atorvastatin 20 MG Oral Tablet [Lipitor]' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Entity\\_Concept\\_ID |  Concept ID of entity with string match on name or synonym concept |

|  Entity\\_Name |  Concept name of entity with string match on name or synonym concept |

|  Entity\\_Code |  Concept code of entity with string match on name or synonym concept |

|  Entity\\_Type |  Type of entity with keyword match, includes one of the following:

- Concept

- Concept Synonym

- Mapped Code

|

|  Entity\\_Concept\\_Class |  Concept class of entity with string match on name or synonym concept |

|  Entity\\_Vocabulary\\_ID |  Vocabulary the concept with string match is derived from as vocabulary ID |

|  Entity\\_Vocabulary\\_Name |  Name of the vocabulary the concept with string match is derived from as vocabulary code |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Entity\\_Concept\\_ID |  1545999 |

|  Entity\\_Name |  atorvastatin 20 MG Oral Tablet [Lipitor] |

|  Entity\\_Code |  617318 |

|  Entity\\_Type |  Concept |

|  Entity\\_Concept\\_Class |  Branded Drug |

|  Entity\\_Vocabulary\\_ID |  8 |

|  Entity\\_Vocabulary\\_Name |  RxNorm |

\*\*D03:\*\* Find ingredients of a drug

This query is designed to accept a drug concept (both clinical or branded) as input and return the list of ingredients that constitute them. Drug concept IDs can be obtained using query G03 or D02.

\*\*Sample query:\*\*

SELECT

       D.Concept\\_Id drug\\_concept\\_id,

       D.Concept\\_Name drug\\_name,

       D.Concept\\_Code drug\\_concept\\_code,

       D.Concept\\_Class\\_id drug\\_concept\\_class,

       A.Concept\\_Id ingredient\\_concept\\_id,

       A.Concept\\_Name ingredient\\_name,

       A.Concept\\_Code ingredient\\_concept\\_code,

       A.Concept\\_Class\\_id ingredient\\_concept\\_class

FROM

       full\\_201706\\_omop\\_v5.concept\\_ancestor CA,

       full\\_201706\\_omop\\_v5.concept A,

       full\\_201706\\_omop\\_v5.concept D

WHERE

       CA.descendant\\_concept\\_id = D.concept\\_id

       AND CA.ancestor\\_concept\\_id = A.concept\\_id

       AND LOWER(A.concept\\_class\\_id) = 'ingredient'

       AND sysdate BETWEEN A.VALID\\_START\\_DATE AND A.VALID\\_END\\_DATE

       AND sysdate BETWEEN D.VALID\\_START\\_DATE AND D.VALID\\_END\\_DATE

       AND CA.descendant\\_concept\\_id IN (939355, 19102189, 19033566)

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  List of drug Concept ID |  939355, 19102189, 19033566 |  Yes | Includes both clinical and branded drug concepts |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  Concept ID of the ingredient entered as input |

|  Ingredient\\_name |  Name of the ingredient |

|  Ingredient\\_Concept\\_code |  Concept code of the ingredient |

|  Ingredient\\_Concept\\_class |  Concept Class of the ingredient |

|  Generic\\_Concept\\_ID |  Concept ID of drug with the ingredient |

|  Generic\\_Name |  Name of drug concept with the ingredient |

|  Generic\\_Concept\\_Code |  Concept code of the drug with the ingredient |

|  Generic\\_Concept\\_Class |  Concept class of drug with the ingredient |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  966991 |

|  Ingredient\\_name |  Simethicone |

|  Ingredient\\_Concept\\_code |  9796 |

|  Ingredient\\_Concept\\_class |  Ingredient |

|  Generic\\_Concept\\_ID |  967306 |

|  Generic\\_Name |  Simethicone 10 MG/ML Oral Solution |

|  Generic\\_Concept\\_Code |  251293 |

|  Generic\\_Concept\\_Class |  Clinical Drug |

\*\*D05:\*\* Find generic drugs by ingredient

This query is designed to extract all generic drugs that have a specified ingredient. The query accepts an ingredient concept ID as the input and returns all generic (not branded) drugs that have the ingredient. It should be noted that the query returns both generics that have a single ingredient (i.e. the specified ingredient) and those that are combinations which include the specified ingredient.

The query requires the ingredient concept ID as the input. A list of these ingredient concepts can be extracted by querying the CONCEPT table for concept class of 'Ingredient'

\*\*Sample query:\*\*

SELECT        A.concept\\_id Ingredient\\_concept\\_id,

               A.concept\\_Name Ingredient\\_name,

               A.concept\\_Code Ingredient\\_concept\\_code,

               A.concept\\_Class\\_id Ingredient\\_concept\\_class,

               D.concept\\_id Generic\\_concept\\_id,

               D.concept\\_Name Generic\\_name,

               D.concept\\_Code Generic\\_concept\\_code,

               D.concept\\_class\\_id Generic\\_concept\\_class

FROM        concept\\_ancestor CA,

               concept A,

               concept D

WHERE

       CA.ancestor\\_concept\\_id                 = 966991

AND        CA.ancestor\\_concept\\_id                = A.concept\\_id

AND CA.descendant\\_concept\\_id        = D.concept\\_id

AND        D.concept\\_class\\_id                        = 'Clinical Drug'

AND        sysdate                                                BETWEEN A.valid\\_start\\_date AND A.valid\\_end\\_date AND sysdate BETWEEN D.valid\\_start\\_date AND D.valid\\_end\\_date

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Ingredient Concept ID  |  966991 |  Yes | Concept ID for 'Simethicone'.

Ingredient concepts can be extracted from CONCEPT table as records of concept class of 'Ingredient' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  Concept ID of the ingredient entered as input |

|  Ingredient\\_name |  Name of the Ingredient |

|  Ingredient\\_Concept\\_code |  Concept code of the ingredient |

|  Ingredient\\_Concept\\_class |  Concept Class of the ingredient |

|  Branded\\_Drug\\_ID |  Concept ID of branded drug with the ingredient |

|  Branded\\_Drug\\_Name |  Name of branded drug concept with the ingredient |

|  Branded\\_Drug\\_Concept\\_Code |  Concept code of the branded drug with the ingredient |

|  Branded\\_Drug\\_Concept\\_Class |  Concept class of branded drug with the ingredient |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  966991 |

|  Ingredient\\_name |  Simethicone |

|  Ingredient\\_Concept\\_code |  9796 |

|  Ingredient\\_Concept\\_class |  Ingredient |

|  Branded\\_Drug\\_ID |  19132733 |

|  Branded\\_Drug\\_Name |  Simethicone 66.7 MG/ML Oral Suspension [Mylicon] |

|  Branded\\_Drug\\_Concept\\_Code |  809376 |

|  Branded\\_Drug\\_Concept\\_Class |  Branded Drug |

\*\*D07:\*\* Find single ingredient drugs by ingredient

This query accepts accepts an ingredient concept ID and returns all drugs which contain only one ingredient specified in the query. This query is useful when studying drug outcomes for ingredients where the outcome or drug-drug interaction effect of other ingredients needs to be avoided. Indications have to be provided as FDB (vocabulary\\_id=19) or NDF-RT indications (vocabulary\\_id=7).

\*\*Sample query:\*\*

SELECT

     c.concept\\_id     as drug\\_concept\\_id,

     c.concept\\_name   as drug\\_concept\\_name,

     c.concept\\_class\\_id  as drug\\_concept\\_class\\_id

FROM concept c

INNER JOIN (

 SELECT drug.cid FROM (

   SELECT a.descendant\\_concept\\_id cid, count(\\*) cnt FROM concept\\_ancestor a

   INNER JOIN (

     SELECT c.concept\\_id FROM concept c, concept\\_ancestor a

     WHERE a.ancestor\\_concept\\_id = 1000560

     AND a.descendant\\_concept\\_id = c.concept\\_id AND c.vocabulary\\_id = 'RxNorm'

   ) cd ON cd.concept\\_id = a.descendant\\_concept\\_id

   INNER JOIN concept c ON c.concept\\_id=a.ancestor\\_concept\\_id

       WHERE c.concept\\_class\\_id = 'Ingredient'

   GROUP BY a.descendant\\_concept\\_id

 ) drug WHERE drug.cnt = 1  -- contains only 1 ingredient

) onesie ON onesie.cid = c.concept\\_id

WHERE sysdate BETWEEN valid\\_start\\_date AND valid\\_end\\_date

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Ingredient Concept ID |  1000560 |  Yes | Concept ID for ingredient 'Ondansetron' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Class\\_Concept\\_ID |  Concept ID of the therapeutic class |

|  Class\\_Name |  Name of the therapeutic class |

|  Class\\_Code |  Concept Code of therapeutic class |

|  Classification |  Concept class of therapeutic class |

|  Class\\_Vocabulary\\_ID |  Vocabulary the therapeutic class is derived from, expressed as vocabulary ID |

|  Class\\_Vocabulary\\_Name |  Name of the vocabulary the therapeutic class is derived from |

|  Levels\\_of\\_Separation |  Levels of separation between the drug concept and the therapeutic class. Important for hierarchic classification systems to identify classes and subclasses for the drug. |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Class\\_Concept\\_ID |  21500263 |

|  Class\\_Name |  Antihyperlipidemics |

|  Class\\_Code |  263 |

|  Classification |  Enhanced Therapeutic Classification |

|  Class\\_Vocabulary\\_ID |  20 |

|  Class\\_Vocabulary\\_Name |  ETC |

|  Levels\\_of\\_Separation |  2 |

\*\*D09:\*\* Find drugs by drug class

This query is designed to extract all drugs that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class .

Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY\\_ID = 20

- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY\\_ID = 21

NDF-RT Physiologic effect (PE),        Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of drug included in therapeutic class |

|  Drug\\_Concept\\_Name |  Name of drug concept included in therapeutic class |

|  Drug\\_Concept\\_Class |  Concept class of drug concept included in therapeutic class |

|  Drug\\_Concept\\_Code |  RxNorm source code of drug concept |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  1308221 |

|  Drug\\_Concept\\_Name |  Lisinopril 40 MG Oral Tablet |

|  Drug\\_Concept\\_Class |  Clinical Drug |

|  Drug\\_Concept\\_Code |  197884 |

\*\*D10:\*\* Find ingredient by drug class

This query is designed to extract all ingredients that belong to a therapeutic class. The query accepts a therapeutic class concept ID as the input and returns all drugs that are included under that class.

Therapeutic classes could be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2) and are derived from one of the following:

- Enhanced Therapeutic Classification (FDB ETC), VOCABULARY\\_ID = 20

- Anatomical Therapeutic Chemical classification (WHO ATC), VOCABULARY\\_ID = 21

NDF-RT Physiologic effect (PE), Vocabulary ID = 7, Concept Class = 'Physiologic Effect'

sysdate is a default |



\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  Concept ID of ingredient included in therapeutic class |

|  Ingredient\\_Concept\\_Name |  Name of ingredient concept included in therapeutic class |

|  Ingredient\\_Concept\\_Class |  Concept class of ingredient concept included in therapeutic class |

|  Ingredient\\_Concept\\_Code |  RxNorm source code of ingredient concept |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  1308216 |

|  Ingredient\\_Concept\\_Name |  Lisinopril |

|  Ingredient\\_Concept\\_Class |  Ingredient |

|  Ingredient\\_Concept\\_Code |  29046 |

\*\*D11:\*\* Find source codes by drug class

This query is designed to extract codes from a non-standard drug vocabulary that belong to a therapeutic class. The query accepts a therapeutic class concept ID and the vocabualry ID of the desired source vocabulary as input and returns all codes that are included under that class and that belong to a source vocabulary. This query could be used to derive e.g. all NDC codes that belong to a certain drug class.

\*\*Sample query:\*\*

SELECT  d.concept\\_code,

       d.vocabulary\\_id,

       v.vocabulary\\_name

FROM concept\\_ancestor ca

        JOIN concept d on d.concept\\_id = ca.descendant\\_concept\\_id

       JOIN concept a on a.concept\\_id = ca.ancestor\\_concept\\_id

       JOIN vocabulary v on d.vocabulary\\_id = v.vocabulary\\_id

WHERE  ca.ancestor\\_concept\\_id = 21506108

  AND  a.vocabulary\\_id = 'NDC'

  AND  d.domain\\_id = 'Drug'

  AND sysdate BETWEEN d.valid\\_start\\_date AND d.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Therapeutic Class Concept ID |  21506108 |  Yes | Concept ID for 'ACE Inhibitors and ACE Inhibitor Combinations' |

|  Source Vocabulary ID |  9 |  Yes | One of the above drug vocabulary ID's |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Type\\_of\\_Indication |  Type of indication, indicating one of the following:

- FDA approved/off-label indication

- Treatment/prevention indication

|

|  Indication\\_Concept\\_ID |  Concept ID of the therapeutic class |

|  Indication\\_Concept\\_Name |  Name of the Indication concept |

|  Indication\\_Vocabulary\\_ID |  Vocabulary the indication is derived from, expressed as vocabulary ID |

|  Indication\\_Vocabulary\\_Name |  Name of the vocabulary the indication is derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Type\\_of\\_Indication |  Has FDA-approved drug indication (FDB) |

|  Indication\\_Concept\\_ID |  21003511 |

|  Indication\\_Concept\\_Name |  Cancer Chemotherapy-Induced Nausea and Vomiting |

|  Indication\\_Vocabulary\\_ID |  19 |

|  Indication\\_Vocabulary\\_Name |  FDB Indication |

\*\*D13\*\*\*\* :\*\*Find indications as condition concepts for a drug

This query accepts a mapped drug code instead of a standard drug concept ID as the input. The result set from the returns detailed of indications associated with the drug.

\*\*Sample query:\*\*

SELECT

 rn.relationship\\_name as type\\_of\\_indication,

 c.concept\\_id as indication\\_concept\\_id,

 c.concept\\_name as indication\\_concept\\_name,

 c.vocabulary\\_id as indication\\_vocabulary\\_id,

 vn.vocabulary\\_name as indication\\_vocabulary\\_name

FROM

 concept c,

 vocabulary vn,

 relationship rn,

 ( -- collect all indications from the drugs, ingredients and pharmaceutical preps and the type of relationship

   SELECT DISTINCT

     r.relationship\\_id rid,

     r.concept\\_id\\_2 cid

   FROM concept c

   INNER JOIN ( -- collect onesie clinical and branded drug if query is ingredient

     SELECT onesie.cid concept\\_id

     FROM (

       SELECT

         a.descendant\\_concept\\_id cid,

         count(\\*) cnt

       FROM concept\\_ancestor a

       INNER JOIN (

         SELECT c.concept\\_id

         FROM

           concept c,

           concept\\_ancestor a

         WHERE

           a.ancestor\\_concept\\_id=19005968 AND

           a.descendant\\_concept\\_id=c.concept\\_id AND

           c.vocabulary\\_id=8

       ) cd on cd.concept\\_id=a.descendant\\_concept\\_id

       INNER JOIN concept c on c.concept\\_id=a.ancestor\\_concept\\_id

       WHERE c.concept\\_level=2

       GROUP BY a.descendant\\_concept\\_id

     ) onesie

     where onesie.cnt=1

     UNION -- collect ingredient if query is clinical and branded drug

     SELECT c.concept\\_id

     FROM

       concept c,

       concept\\_ancestor a

     WHERE

       a.descendant\\_concept\\_id=19005968 AND

       a.ancestor\\_concept\\_id=c.concept\\_id AND

       c.vocabulary\\_id=8

     UNION -- collect pharmaceutical preparation equivalent to which NDFRT has reltionship

     SELECT c.concept\\_id

     FROM

       concept c,

       concept\\_ancestor a

     WHERE

       a.descendant\\_concept\\_id=19005968 AND

       a.ancestor\\_concept\\_id=c.concept\\_id AND

       lower(c.concept\\_class)='pharmaceutical preparations'

     UNION -- collect itself

     SELECT 19005968

   ) drug ON drug.concept\\_id=c.concept\\_id

   INNER JOIN concept\\_relationship r on c.concept\\_id=r.concept\\_id\\_1 -- allow only indication relationships

   WHERE

     r.relationship\\_id IN (21,23,155,156,126,127,240,241)

 ) ind

 INNER JOIN concept\\_relationship r ON r.concept\\_id\\_1=ind.cid

 WHERE

   r.concept\\_id\\_2=c.concept\\_id AND

   r.relationship\\_id in (247, 248) AND

   ind.rid=rn.relationship\\_id AND

   vn.vocabulary\\_id=c.vocabulary\\_id AND

   sysdate BETWEEN c.valid\\_start\\_date AND c.valid\\_end\\_date;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|   Drug Concept ID |   19005968 |  Yes | Drugs concepts from RxNorm with a concept class of 'Branded Drug' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\*Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of the drug |

|  Drug\\_Concept\\_Name |  Name of the drug |

|  Drug\\_Concept\\_Code |  Concept code of the drug |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  1710446 |

|  Drug\\_Concept\\_Name |  Cycloserine |

|  Drug\\_Concept\\_Code |  3007 |

\*\*D15:\*\* Find drugs for an indication provided as condition concepts

This query provides all clinical/branded drugs that are indicated for a certain indication. Indications have to be provided as SNOMED-CT concept (vocabulary\\_id=1).

\*\*Sample query:\*\*

SELECT DISTINCT

 drug.concept\\_id as drug\\_concept\\_id,

 drug.concept\\_name as drug\\_concept\\_name,

 drug.concept\\_code as drug\\_concept\\_code

FROM

 concept drug,

 concept\\_ancestor snomed,

 concept\\_ancestor ind,

 concept\\_relationship r

WHERE

 snomed.ancestor\\_concept\\_id = 253954 AND

 snomed.descendant\\_concept\\_id = r.concept\\_id\\_1 AND

 concept\\_id\\_2 = ind.ancestor\\_concept\\_id AND

 r.relationship\\_id in (247, 248) AND

 ind.descendant\\_concept\\_id = drug.concept\\_id AND

 drug.concept\\_level = 1 AND

 drug.vocabulary\\_id = 8 AND

 sysdate BETWEEN drug.valid\\_start\\_date AND drug.valid\\_end\\_date;

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Indication Concept ID |  253954 |  Yes | SNOMED-CT indication concept ID |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of the drug |

|  Drug\\_Concept\\_Name |  Name of the drug |

|  Drug\\_Concept\\_Code |  Concept code of the drug |

|  Indication\\_Type |  One of the FDB, NDF-RT or OMOP inferred indication types |

|  Relationship\\_id |  Corresponding relationship ID to the Indication Type |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  19019530 |

|  Drug\\_Concept\\_Name |  Perphenazine 4 MG Oral Tablet |

|  Drug\\_Concept\\_Code |  198077 |

|  Indication\\_Type |  Inferred ingredient of (OMOP) |

|  Relationship\\_id |  281 |

\*\*D17:\*\* Find ingredients for an indication

This query provides ingredients that are designated for a certain indication. Indications have to be given as FDB indications (vocabulary\\_id=19) or NDF-RT indications (vocabulary\\_id=7). Indications can be identified using the generic query  [G03](http://vocabqueries.omop.org/general-queries/g3), or, if at least one drug is known for this indication, query  [D04](http://vocabqueries.omop.org/drug-queries/d4).

\*\*Sample query:\*\*

SELECT

 ingredient.concept\\_id as ingredient\\_concept\\_id,

 ingredient.concept\\_name as ingredient\\_concept\\_name,

 ingredient.concept\\_code as ingredient\\_concept\\_code

FROM

 concept ingredient,

 concept\\_ancestor a

WHERE

 a.ancestor\\_concept\\_id = 4345991 AND

 a.descendant\\_concept\\_id = ingredient.concept\\_id AND

 ingredient.concept\\_level = 2 AND

 ingredient.vocabulary\\_id = 8 AND

 sysdate BETWEEN ingredient.valid\\_start\\_date AND ingredient.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |





\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  Concept ID of the ingredient |

|  Ingredient\\_Concept\\_Name |  Name of the ingredient |

|  Ingredient\\_Concept\\_Code |  Concept code of the ingredient |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Ingredient\\_Concept\\_ID |  1790868 |

|  Ingredient\\_Concept\\_Name |  Amikacin |

|  Ingredient\\_Concept\\_Code |  641 |

\*\*D19:\*\* Find ingredients for an indication by indication type

This query provides all ingredients that are indicated for a certain condition. In addition, it provides the type of indication: FDA-approved, off-label (both based on FDB indication classes) and may treat and may prevent (both based on NDF-RT). Indications have to be provided as FDB indications (vocabulary\\_id=19) or NDF-RT (vocabulary\\_id=7).

\*\*Sample query:\*\*

SELECT DISTINCT

 ingredient.concept\\_id as ingredient\\_concept\\_id,

 ingredient.concept\\_name as ingredient\\_concept\\_name,

 ingredient.concept\\_code as ingredient\\_concept\\_code,

 rn.relationship\\_name as indication\\_type,

 indication\\_relation.relationship\\_id

FROM

 concept\\_relationship indication\\_relation

INNER JOIN

 concept\\_ancestor a ON a.ancestor\\_concept\\_id=indication\\_relation.concept\\_id\\_2

INNER JOIN

 concept ingredient ON ingredient.concept\\_id=a.descendant\\_concept\\_id

INNER JOIN

 relationship rn ON rn.relationship\\_id = indication\\_relation.relationship\\_id

WHERE

 indication\\_relation.concept\\_id\\_1 = 4345991 AND

 ingredient.vocabulary\\_id = 8 AND

 ingredient.concept\\_level = 2 AND

 indication\\_relation.relationship\\_id in (21,23,155,157,126,127,240,241,281,282) AND

 sysdate BETWEEN ingredient.valid\\_start\\_date AND ingredient.valid\\_end\\_date;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Indication Concept ID |  4345991 |  Yes | FDB indication concept for 'Vomiting' |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date 'Has dose form (RxNorm)') for this.

\*\*Sample query:\*\*

SELECT

       A.concept\\_id drug\\_concept\\_id,

        A.concept\\_name drug\\_name,

        A.concept\\_code drug\\_concept\\_code,

        D.concept\\_id dose\\_form\\_concept\\_id,

        D.concept\\_name dose\\_form\\_concept\\_name,

        D.concept\\_code dose\\_form\\_concept\\_code

FROM

       full\\_201706\\_omop\\_v5.concept\\_relationship CR,

        full\\_201706\\_omop\\_v5.concept A,

        full\\_201706\\_omop\\_v5.concept D

WHERE

       sysdate BETWEEN CR.valid\\_start\\_date AND CR.valid\\_end\\_date

       AND CR.concept\\_id\\_1 = A.concept\\_id

        AND CR.concept\\_id\\_2 = D.concept\\_id

       AND CR.concept\\_id\\_1 = 19060647

       AND CR.relationship\\_id = 'RxNorm has dose form'

       --AND CR.relationship\\_ID = 4

       --AND A.concept\\_class\\_id ='Clinical Drug'

       --AND A.vocabulary\\_id = 'RxNorm'

       ;

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Drug Concept ID |  19060647 |  Yes | Must be a level 1 Clinical or Branded Drug or Pack |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of drug entered with specified dose form |

|  Drug\\_Name |  Name of drug with specified dose form |

|  Drug\\_Concept\\_Code |  Concept code of the dose form |

|  Dose\\_Form\\_Concept\\_name |  Name of the dose form |

|  Route\\_Of\\_Administration |  Derived route of administration for the drug |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  19060647 |

|  Drug\\_Name |  Budesonide 0.2 MG/ACTUAT Inhalant Powder |

|  Drug\\_Concept\\_Code |  247047 |

|  Dose\\_Form\\_Concept\\_name |  Inhalant Powder |

|  Route\\_Of\\_Administration |  Inhaled |

\*\*D22:\*\* Find drugs by class and dose form

This query is designed to return a list of drug concept IDs that belong to a drug class and are of a certain dose form. The query ties together:

- Concept ancestor data to link drug concepts to therapeutic class

- RxNorm concept relationship 4 - 'Has dose form (RxNorm)

The results are combined to present a list of drugs from a specific therapeutic class with a specific dose form.

\*\*Sample query:\*\*

SELECT C.concept\\_id drug\\_concept\\_id,

C.concept\\_name drug\\_concept\\_name,

C.concept\\_code drug\\_concept\\_code

FROM concept C,

       concept\\_ancestor CA,

       concept\\_relationship CRF,

       concept F

WHERE CA.ancestor\\_concept\\_id = 4318008

       AND C.concept\\_id = CA.descendant\\_concept\\_id

       AND C.vocabulary\\_id = 'RxNorm'

       AND C.standard\\_concept = 'S'

       AND CRF.concept\\_id\\_1 = C.concept\\_id

       AND CRF.relationship\\_ID = 'RxNorm has dose form'

       AND CRF.concept\\_id\\_2 = F.concept\\_id

       AND POSITION(LOWER(REPLACE(REPLACE(F.concept\\_name, ' ', ''), '-', '')) IN

       LOWER(REPLACE(REPLACE('Nasal spray' , ' ', ''), '-', ''))) > 0

       AND sysdate BETWEEN CRF.valid\\_start\\_date AND CRF.valid\\_end\\_date

\*\*Input:\*\*

| \*\*Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| Therapeutic class Concept ID |  4318008 |  Yes | Concept ID for mechanism of action "Corticosteroid Hormone Receptor Agonists". Valid drug classes can be obtained using query  [D02](http://vocabqueries.omop.org/drug-queries/d2). |

|  Dose Form String |  'Nasal spray' |  Yes | Dose form string. Valid dose forms can be obtained using query  [D19](http://vocabqueries.omop.org/drug-queries/d19). |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of drug with specified therapeutic class and dose form |

|  Drug\\_Name |  Name of drug with specified therapeutic class and dose form |

|  Drug\\_Concept\\_Code |  Source code of drug |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  40230686 |

|  Drug\\_Name |  hydrocortisone acetate 10 MG/ML Vaginal Cream |

|  Drug\\_Concept\\_Code |  1039349 |

\*\*D24:\*\* Find the branded drugs in a list of drugs

This query is designed to identify branded drug concepts from a list of standard drug concept IDs. The query identifies branded drugs from the Concept table based on a concept class setting of 'Branded Drug'

\*\*Sample query:\*\*

SELECT C.concept\\_id drug\\_concept\\_id,

       C.concept\\_name drug\\_name,

       C.concept\\_code drug\\_concept\\_code,

       C.concept\\_class\\_id drug\\_concept\\_class,

       C.vocabulary\\_id drug\\_vocabulary\\_id,

       V.vocabulary\\_name drug\\_vocabulary\\_name

FROM concept C,

       vocabulary V

       WHERE C.vocabulary\\_id = 'RxNorm'

               AND C.concept\\_id IN (1396833, 19060643)

               AND C.concept\\_class\\_id = 'Clinical Drug'

               AND C.vocabulary\\_id = V.vocabulary\\_id

               AND sysdate BETWEEN C.valid\\_start\\_date AND C.valid\\_end\\_date

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Drug Concept ID list |  1516830, 19046168 |  Yes | List of drug concept id's |

|  As of date |  '01-Jan-2010' |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of generic drug or pack |

|  Drug\\_Name |  Name of generic drug or pack |

|  Drug\\_Concept\\_Code |  Concept code of generic drug or pack |

|  Drug\\_Concept\\_Class |  Concept class of generic drug or pack |

|  Drug\\_Vocabulary\\_ID |  Vocabulary the generic drug concept has been derived from, expressed as vocabulary ID |

|  Drug\\_Vocabulary\\_Name |  Name of the Vocabulary the generic drug concept has been derived from |

\*\*Sample output record:\*\*

| \*\* Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  19060643 |

|  Drug\\_Name |  Budesonide 0.05 MG/ACTUAT Nasal Spray |

|  Drug\\_Concept\\_Code |  247042 |

|  Drug\\_Concept\\_Class |  Clinical Drug |

|  Drug\\_Vocabulary\\_ID |  8 |

|  Drug\\_Vocabulary\\_Name |  RxNorm |

\*\*D26:\*\* Find the brand name of a drug

This query is designed to accept a drug concept (both clinical and branded) as input and return a the brand name (or branded ingredient) associated with it. The query is useful to check for a brand names associated with a clinical drug. Drug concepts can be obtained using queries  [G03](http://vocabqueries.omop.org/general-queries/g3) or  [D02](http://vocabqueries.omop.org/drug-queries/d2).

\*\*Sample query:\*\*

SELECT A.Concept\\_Id               drug\\_concept\\_id,

       A.Concept\\_Name            drug\\_name,

       A.Concept\\_Code            drug\\_concept\\_code,

       A.concept\\_class\\_id           drug\\_concept\\_class\\_id,

       D.Concept\\_Id              brand\\_concept\\_id,

       D.Concept\\_Name            brand\\_name,

       D.Concept\\_Code            brand\\_concept\\_code,

       D.concept\\_class\\_id           brand\\_concept\\_class\\_id

FROM   concept\\_relationship  CR003,

      concept               A,

      concept\\_relationship  CR007,

      concept\\_relationship  CR006,

      concept                 D

WHERE  CR003.relationship\\_ID  = 'Has tradename'

AND    CR003.concept\\_id\\_1     = A.concept\\_id

AND    lower(A.concept\\_class\\_id) = 'clinical drug'

AND    CR007.concept\\_id\\_2     = CR003.concept\\_id\\_2

AND    CR007.relationship\\_ID  = 'Constitutes'

AND    CR007.concept\\_id\\_1     = CR006.concept\\_id\\_1

AND    CR006.relationship\\_ID  = 'RxNorm has ing'

AND    CR006.concept\\_id\\_2     = D.concept\\_id

AND    lower(D.concept\\_class\\_id) = 'branded name'

AND    A.concept\\_Id           = 939355

AND    sysdate BETWEEN CR006.VALID\\_START\\_DATE AND CR006.VALID\\_END\\_DATE

UNION ALL

SELECT A.Concept\\_Id               drug\\_concept\\_id,

      A.Concept\\_Name             drug\\_name,

      A.Concept\\_Code             drug\\_concept\\_code,

      A.concept\\_class\\_id            drug\\_concept\\_class\\_id,

      D.Concept\\_Id               brand\\_concept\\_id,

      D.Concept\\_Name             brand\\_name,

      D.Concept\\_Code             brand\\_concept\\_code,

      D.concept\\_class\\_id            brand\\_concept\\_class\\_id

FROM   concept               A,

      concept\\_relationship  CR007,

      concept\\_relationship  CR006,

      concept               D

WHERE  lower(A.concept\\_class\\_id) = 'branded drug'

AND    CR007.concept\\_id\\_2     = A.concept\\_id

AND    CR007.relationship\\_ID  = 'Constitutes'

AND    CR007.concept\\_id\\_1     = CR006.concept\\_id\\_1

AND    CR006.relationship\\_ID  = 'RxNorm has ing'

AND    CR006.concept\\_id\\_2     = D.concept\\_id

AND    lower(D.concept\\_class\\_id) = 'branded name'

AND    A.concept\\_Id           = 939355

AND    sysdate BETWEEN CR006.VALID\\_START\\_DATE AND CR006.VALID\\_END\\_DATE

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

|  Drug Concept ID |  939355 |  Yes | Can be both clinical and branded drug concepts |

|  As of date |  Sysdate |  No | Valid record as of specific date. Current date sysdate is a default |

\*\*Output:\*\*

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  Concept ID of drug (clinical/generic or branded) |

|  Drug\\_Name |  Name of drug |

|  Drug\\_Concept\\_Code |  Concept code of the drug |

|  Drug\\_Concept\\_Class |  Concept class of drug |

|  Brand\\_Concept\\_ID |  Concept ID of the brand name entered as ingredient |

|  Brand\\_name |  Name of the brand |

|  Brand\\_Concept\\_code |  Concept code of the brand name |

|  Brand\\_Concept\\_class |  Concept Class of the brand name |

\*\*Sample output record:\*\*

| \*\*Field\*\* | \*\* Value\*\* |

| --- | --- |

|  Drug\\_Concept\\_ID |  40173591 |

|  Drug\\_Name |  Alendronic acid 10 MG Oral Tablet [Fosamax] |

|  Drug\\_Concept\\_Code |  904421 |

|  Drug\\_Concept\\_Class |  Branded Drug |

|  Brand\\_Concept\\_ID |  19011505 |

|  Brand\\_name |  Fosamax |

|  Brand\\_Concept\\_code |  114265 |

|  Brand\\_Concept\\_class |  Brand Name |
