### COC01: Determines first line of therapy for a condition

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of condition\_concept\_id | 432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742, 4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366, 4292524, 4299298, 4299302, 4301157, 4307793 | Yes | Angioedema 1 |
| --- | --- | --- | --- |
| ancestor\_concept\_id | 21003378 | Yes | Angioedema |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT   ingredient\_name,   ingredient\_concept\_id,   count(\*) num\_patients FROM /\*Drugs started by people up to 30 days after Angioedema diagnosis \*/ (   SELECT     condition.person\_id,     condition\_start\_date ,     drug\_era\_start\_date ,     ingredient\_name,     ingredient\_concept\_id   FROM /\* people with Angioedema with 180 clean period and 180 day follow-up \*/ (     SELECT       era.person\_id,       condition\_era\_start\_date AS condition\_start\_date     FROM condition\_era era     JOIN observation\_period obs       ON obs.person\_id = era.person\_id AND          condition\_era\_start\_date BETWEEN observation\_period\_start\_date + 180 AND observation\_period\_end\_date - 180     WHERE       condition\_concept\_id IN -- SNOMed codes for OMOP Angioedema 1       ( **432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742,**  **        4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366,**  **        4292524, 4299298, 4299302, 4301157, 4307793** )   ) condition   JOIN drug\_era rx /\* Drug\_era has drugs at ingredient level \*/     ON rx.person\_id = condition.person\_id AND        rx.drug\_era\_start\_date BETWEEN condition\_start\_date AND condition\_start\_date + 30   JOIN /\* Ingredients for indication Angioedema \*/ (     SELECT       ingredient.concept\_id AS ingredient\_concept\_id ,       ingredient.concept\_name AS ingredient\_name     FROM concept ingredient     JOIN concept\_ancestor a ON a.descendant\_concept\_id = ingredient.concept\_id     WHERE       a.ancestor\_concept\_id = **21003378** /\* indication for angioedema \*/ AND       ingredient.vocabulary\_id = 8 AND       sysdate BETWEEN ingredient.valid\_start\_date AND ingredient.valid\_end\_date   ) ON ingredient\_concept\_id = drug\_concept\_id ) GROUP by ingredient\_name, ingredient\_concept\_id ORDER BY num\_patients DESC;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| ingredient\_name |   |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| ingredient\_name |   |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### COC02: Determines length of course of therapy for a condition

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| condition\_concept\_id | 500000201 | Yes | SNOMed codes for OMOP Aplastic Anemia 1 |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT        ingredient\_name,                ingredient\_concept\_id,                count(\*) AS num\_patients,                min( length\_of\_therapy ) AS min\_length\_of\_therapy\_count,                max( length\_of\_therapy ) AS max\_length\_of\_therapy\_count,                avg( length\_of\_therapy ) AS average\_length\_of\_therapy\_countFROM         (        SELECT        condition.person\_id,                        condition\_start\_date,                        drug\_era\_start\_date,                        drug\_era\_end\_date - drug\_era\_start\_date + 1 AS length\_of\_therapy,                        ingredient\_name,                        ingredient\_concept\_id        FROM                (                SELECT        era.person\_id,                                condition\_era\_start\_date AS condition\_start\_date                FROM        condition\_era era                                        JOIN        observation\_period AS obs                                                ON        obs.person\_id = era.person\_id                                                AND condition\_era\_start\_date BETWEEN observation\_period\_start\_date + 180                                                AND observation\_period\_end\_date - 180                WHERE                        condition\_concept\_id IN ( **137829,138723,140065,140681,4031699,4098027,4098028, 4098145,4098760,4100998,4101582,4101583,4120453,4125496, 4125497,4125498,4125499,4146086,4146087,4146088,4148471, 4177177,4184200,4184758,4186108,4187773,4188208,4211348, 4211695,4225810,4228194,4234973,4298690,4345236** )                ) condition                        JOIN        drug\_era rx                                ON        rx.person\_id = condition.person\_id                                AND rx.drug\_era\_start\_date BETWEEN condition\_start\_date AND condition\_start\_date + 30                        JOIN                                 (                                SELECT DISTINCT        ingredient.concept\_id as ingredient\_concept\_id,                                                                ingredient.concept\_name as ingredient\_name                                FROM        concept\_ancestor ancestor                                                        JOIN        concept indication                                                                ON        ancestor.ancestor\_concept\_id = indication.concept\_id                                                        JOIN concept ingredient                                                                ON        ingredient.concept\_id = ancestor.descendant\_concept\_id                                WHERE                                        lower( indication.concept\_name ) like( '%anemia%' )                                AND        indication.vocabulary\_id = 'Indication'                                AND ingredient.vocabulary\_id = 'RxNorm'                                AND sysdate BETWEEN indication.valid\_start\_date AND indication.valid\_end\_date                                AND sysdate BETWEEN ingredient.valid\_start\_date AND ingredient.valid\_end\_date                                 )                                        ON ingredient\_concept\_id = drug\_concept\_id         )GROUP BY        ingredient\_name,                        ingredient\_concept\_idORDER BY        num\_patients DESC; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| ingredient\_name |   |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| ingredient\_name |   |
| --- | --- |
| ingredient\_concept\_id |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### COC05: Mortality rate after initial diagnosis

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Acute Myocardial Infarction 1 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT   COUNT( DISTINCT diagnosed.person\_id ) AS all\_infarctions ,   SUM( CASE WHEN death.person\_id IS NULL THEN 0 ELSE 1 END ) AS death\_from\_infarction FROM -- Initial diagnosis of Acute Myocardial Infarction (   SELECT DISTINCT     person\_id,     condition\_era\_start\_date   FROM /\* diagnosis of Acute Myocardial Infarction, ranked by date, 6 month clean period with 1 year follow-up \*/   (     SELECT       condition.person\_id,       condition.condition\_era\_start\_date ,       sum(1) OVER(PARTITION BY condition.person\_id ORDER BY condition\_era\_start\_date ROWS UNBOUNDED PRECEDING) AS ranking     FROM       condition\_era condition     JOIN --definition of Acute Myocardial Infarction 1     (       SELECT DISTINCT descendant\_concept\_id       FROM relationship       JOIN concept\_relationship rel USING( relationship\_id )       JOIN concept concept1 ON concept1.concept\_id = concept\_id\_1       JOIN concept\_ancestor ON ancestor\_concept\_id = concept\_id\_2       WHERE         relationship\_name = 'HOI contains SNOMED (OMOP)' AND         concept1.concept\_name = **'OMOP Acute Myocardial Infarction 1'** AND         sysdate BETWEEN rel.valid\_start\_date and rel.valid\_end\_date     ) ON descendant\_concept\_id = condition\_concept\_id     JOIN observation\_period obs       ON obs.person\_id = condition.person\_id AND          condition\_era\_start\_date BETWEEN observation\_period\_start\_date + 180 AND observation\_period\_end\_date - 360   ) WHERE ranking = 1 ) diagnosed LEFT OUTER JOIN death /\* death within a year \*/   ON death.person\_id = diagnosed.person\_id AND   death.death\_date <= condition\_era\_start\_date + 360; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| all\_infarctions |   |
| --- | --- |
| death\_from\_infarction |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| all\_infarctions |   |
| --- | --- |
| death\_from\_infarction |   |
| --- | --- |

  |
| --- |
### COC06: Time until death after initial diagnosis

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Acute Myocardial Infarction 1 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT COUNT( DISTINCT diagnosed.person\_id ) AS all\_infarction\_deaths     , ROUND( min( death\_date - condition\_era\_start\_date )/365, 1 ) AS min\_years     , ROUND( max( death\_date - condition\_era\_start\_date )/365, 1 ) AS max\_years     , ROUND( avg( death\_date - condition\_era\_start\_date )/365, 1 ) AS avg\_years  FROM -- Initial diagnosis of Acute Myocardial Infarction     ( SELECT DISTINCT person\_id, condition\_era\_start\_date         FROM  /\* diagnosis of Acute Myocardial Infarction, ranked by                  date, 6 month clean                \*/            ( SELECT condition.person\_id, condition.condition\_era\_start\_date                   , rank() OVER( PARTITION BY condition.person\_id                                      ORDER BY condition\_era\_start\_date                                ) AS ranking                FROM condition\_era condition                JOIN -- definition of Acute Myocardial Infarction 1                   ( SELECT DISTINCT descendant\_concept\_id                       FROM relationship                       JOIN concept\_relationship rel USING( relationship\_id )                        JOIN concept concept1 ON concept1.concept\_id = concept\_id\_1                       JOIN concept\_ancestor ON ancestor\_concept\_id = concept\_id\_2                      WHERE relationship\_name = 'HOI contains SNOMED (OMOP)'                        AND concept1.concept\_name = **'OMOP Acute Myocardial Infarction 1'**                         AND sysdate BETWEEN rel.valid\_start\_date and rel.valid\_end\_date                   ) ON descendant\_concept\_id = condition\_concept\_id                JOIN observation\_period obs                  ON obs.person\_id = condition.person\_id                 AND condition\_era\_start\_date >= observation\_period\_start\_date + 180            )        WHERE ranking = 1     ) diagnosed  JOIN death     ON death.person\_id = diagnosed.person\_id  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| all\_infarction\_deaths |   |
| --- | --- |
| min\_years |   |
| --- | --- |
| max\_years |   |
| --- | --- |
| avg\_years |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| all\_infarction\_deaths |   |
| --- | --- |
| min\_years |   |
| --- | --- |
| max\_years |   |
| --- | --- |
| avg\_years |   |
| --- | --- |

  |
| --- |
### COC07: Patients with condition in conjunction with a procedure some number of days prior to or after initial condition.

| Aplastic Anemia AND Occurrence of at least one diagnostic procedure code for bone marrow aspiration or biopsy within 60 days prior to the diagnostic code.
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Aplastic Anemia 1 | Yes |   |
| --- | --- | --- | --- |
| list of procedure\_concept\_id | 2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142 , 3048879, 36359239, 37586183 |   | Bone marrow aspiration or biopsy |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT DISTINCT        condition.person\_id,                                procedure\_date,                                condition\_era\_start\_dateFROM        procedure\_occurrence proc                JOIN        condition\_era condition                                        ON condition.person\_id = proc.person\_id                JOIN                                        (                                SELECT DISTINCT        descendant\_concept\_id                                FROM        relationship                                                JOIN        concept\_relationship rel USING( relationship\_id )                                                JOIN        concept concept1                                                                        ON        concept1.concept\_id = concept\_id\_1                                                JOIN        concept\_ancestor                                                                        ON        ancestor\_concept\_id = concept\_id\_2                                WHERE        relationship\_name = 'HOI contains SNOMED (OMOP)'                                AND                concept1.concept\_name = **'OMOP Aplastic Anemia 1'**                                 AND                sysdate BETWEEN rel.valid\_start\_date and rel.valid\_end\_date                                )                                         ON descendant\_concept\_id = condition\_concept\_idWHERE        proc.procedure\_concept\_id IN ( **2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142, 3048879, 36359239, 37586183** )AND procedure\_date BETWEEN condition\_era\_start\_date - 60 AND condition\_era\_start\_date;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| condition\_concept\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |
| --- | --- |
| person\_id |   |
| --- | --- |
| procedure\_date |   |
| --- | --- |
| condition\_era\_start\_date |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| person\_id |   |
| --- | --- |
| procedure\_date |   |
| --- | --- |
| condition\_era\_start\_date |   |
| --- | --- |

  |
| --- |
### COC08: Patients with condition and some observation criteria some number of days prior to or after initial condition

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_name | OMOP Aplastic Anemia 1 | Yes |   |
| --- | --- | --- | --- |
| list of observation\_concept\_id | 3000905, 3003282, 3010813 |   | Leukocytes #/volume in blood |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT DISTINCT   condition.person\_id ,   observation\_date,   condition\_era\_start\_date FROM   condition\_era condition JOIN -- definition of Aplastic Anemia (   SELECT DISTINCT descendant\_concept\_id   FROM relationship   JOIN concept\_relationship rel USING( relationship\_id )   JOIN concept concept1 ON concept1.concept\_id = concept\_id\_1   JOIN concept\_ancestor ON ancestor\_concept\_id = concept\_id\_2   WHERE     relationship\_name = 'HOI contains SNOMED (OMOP)' AND     concept1.concept\_name = **'OMOP Aplastic Anemia 1'** AND     sysdate BETWEEN rel.valid\_start\_date and rel.valid\_end\_date ) ON descendant\_concept\_id = condition\_concept\_id JOIN observation   ON observation.person\_id = condition.person\_id AND      observation\_date BETWEEN condition\_era\_start\_date - 7 AND condition\_era\_start\_date + 7 WHERE   observation\_concept\_id IN /\* leukocytes #/volume in blood \*/ ( **3000905, 3003282, 3010813 ) AND**   unit\_concept\_id = 8961 /\* Thousand per cubic millimeter \*/ AND   value\_as\_number <= 3.5;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| person\_id |   |
| --- | --- |
| observation\_date |   |
| --- | --- |
| condition\_era\_start\_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| person\_id |   |
| --- | --- |
| observation\_date |   |
| --- | --- |
| condition\_era\_start\_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |
| --- | --- |

  |
| --- |
### COC09: Condition that is regionally dependent

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| source\_code | 088.81 | Yes | lyme disease |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT        state,                count(\*) AS total\_enroled,                sum( lymed ) AS lyme\_cases,                TRUNC( ( sum(lymed) /count(\*) ) \* 100, 2 ) AS percentagesFROM        (        SELECT        person\_id,                        state,                        NVL( lymed, 0 ) lymed        FROM person                JOIN location USING( location\_id )                LEFT OUTER JOIN                        (                        SELECT DISTINCT        person\_id,                                                        1 AS lymed                        FROM                                condition\_era                                        JOIN source\_to\_concept\_map                                                ON        target\_concept\_id = condition\_concept\_id                        WHERE                                source\_vocabulary\_id         = 'ICD9CM'                        AND        target\_vocabulary\_id         = 'SNOMED'                        AND        source\_code                         = **'088.81'**                         AND sysdate                                 BETWEEN valid\_start\_date and valid\_end\_date                        ) USING( person\_id )         )GROUP BY        stateORDER BY        4 DESC;  **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| state | The state field as it appears in the source data. |
| --- | --- |
| count |   |
| --- | --- |
| lyme\_cases |   |
| --- | --- |
| percent |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| state |   |
| --- | --- |
| count |   |
| --- | --- |
| lyme\_cases |   |
| --- | --- |
| percent |   |
| --- | --- |

  |
| --- |
### COC10: Lenght of condition as function of treatment

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_code | '22851','20936','22612','22523','22630','22614','22842' , '22632', '20930','22524','27130','22525' | Yes |   |
| --- | --- | --- | --- |
| concept\_code | 20610','20552','207096','20553','20550','20605' | Yes |   |
| --- | --- | --- | --- |
| drug\_concept\_id | 1125315, 778711, 115008, 1177480, 1112807, 1506270 | Yes |   |
| --- | --- | --- | --- |
| concept\_code | '97001', '97140', '97002' | Yes |   |
| --- | --- | --- | --- |
| concept\_code | G0283 | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT   treatment,   count(\*),   min( condition\_days ) AS min ,   max( condition\_days ) AS max,   avg( condition\_days ) As avg\_condition\_days FROM (   SELECT     CASE WHEN surgery = 1 THEN 'surgery'          WHEN drug = 1 AND pt = 1 THEN 'PT Rx'          WHEN drug = 1 THEN 'Rx Only'          ELSE 'No Treatment'     END AS treatment ,     condition\_days   FROM (     SELECT       person\_id,       diag\_date ,      max( drug ) AS drug,       max( surgery ) AS surgery,       max( pt ) AS PT ,       max( condition\_days ) AS condition\_days     FROM /\* back pain and treatments over following 60 days \*/ (       SELECT         era.person\_id,         condition\_era\_start\_date AS diag\_date ,         condition\_era\_end\_date - condition\_era\_start\_date AS condition\_days,         NVL( drug, 0 ) AS drug,         NVL( surgery, 0 ) AS surgery ,         NVL( pt, 0 ) AS pt       FROM condition\_era era       JOIN /\* SNOMed codes for back pain \*/ (         SELECT DISTINCT           descendant\_concept\_id -- concept\_name         FROM source\_to\_concept\_map map         JOIN concept\_ancestor ON ancestor\_concept\_id = target\_concept\_id         JOIN concept ON concept\_id = descendant\_concept\_id         WHERE           source\_code like '724%' AND           source\_vocabulary\_id = 'ICD9CM' AND           target\_vocabulary\_id = 'SNOMED' AND           sysdate BETWEEN map.valid\_start\_date AND map.valid\_end\_date       ) ON descendant\_concept\_id = condition\_concept\_id       LEFT OUTER JOIN (         SELECT           person\_id,           procedure\_date,           1 AS surgery         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 'CPT4' AND           concept\_code IN( '22851','20936','22612','22523','22630','22614\*','22842','22632','20930','22524','27130','22525' )       ) surgery         ON surgery.person\_id = era.person\_id AND            surgery.procedure\_date BETWEEN condition\_era\_start\_date AND condition\_era\_start\_date + 60       LEFT OUTER JOIN (         SELECT           person\_id,           procedure\_date AS drug\_date,           1 AS drug         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 'CPT4' AND           concept\_code IN( '20610','20552','207096','20553','20550','20605' ,'20551','20600','23350' )         UNION SELECT           person\_id,           drug\_era\_start\_date,           1         FROM drug\_era         WHERE drug\_concept\_id IN(1125315, 778711, 1115008, 1177480, 1112807,1506270 )       ) drug         ON drug.person\_id = era.person\_id AND            drug.drug\_date BETWEEN condition\_era\_start\_date AND condition\_era\_start\_date + 60       LEFT OUTER JOIN (         SELECT           person\_id,           procedure\_date AS pt\_date,           1 AS pt         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 'CPT4' AND           concept\_code IN( '97001', '97140', '97002' )         UNION SELECT           person\_id,           procedure\_date AS pt\_date,           1 AS pt         FROM procedure\_occurrence proc         JOIN concept ON concept\_id = procedure\_concept\_id         WHERE           vocabulary\_id = 'HCPCS' AND           concept\_code = 'G0283'       ) pt         ON pt.person\_id = era.person\_id AND            pt.pt\_date BETWEEN condition\_era\_start\_date AND condition\_era\_start\_date + 60     )     WHERE diag\_date > '01-jan-2011'     GROUP by       person\_id,       diag\_date     ORDER BY       person\_id,       diag\_date   ) ) GROUP BY treatment ORDER BY treatment; **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg\_condition\_days |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |
| min |   |
| --- | --- |
| max |   |
| --- | --- |
| avg\_condition\_days |   |
| --- | --- |

  |
| --- |
### COC11: Given a condition, what treatment did patient receive

|
**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| concept\_code | '22851', '20936', '22612', '22523', '22630', '22614', '22842' , '22632', '20930', '22524', '27130', '22525' | Yes |   |
| --- | --- | --- | --- |


**Sample query run:**
The following is a sample run of the query. The input parameters are highlighted in  **blue**  SELECT treatment, count(\*) FROM(SELECT CASE WHEN surgery = 1            THEN 'surgery'            WHEN drug = 1 AND pt = 1             THEN 'PT Rx'            WHEN drug = 1            THEN 'Rx Only'            ELSE 'No Treatment'       END AS treatmentFROM(SELECT person\_id, diag\_date     , max( drug ) AS drug, max( surgery ) AS surgery, max( pt ) AS PT  FROM /\* back pain and treatments over following 60 days \*/     (      SELECT era.person\_id, condition\_era\_start\_date AS diag\_date          , NVL( drug, 0 ) AS drug, NVL( surgery, 0 ) AS surgery          , NVL( pt, 0 ) AS pt       FROM condition\_era era                 JOIN /\* SNOMed codes for back pain \*/                        ( SELECT DISTINCT ca.descendant\_concept\_id                        FROM concept\_ancestor ca JOIN                        ( SELECT cr.concept\_id\_2 AS target\_concept\_id                                FROM concept\_relationship cr                                JOIN concept c1 ON cr.concept\_id\_1 = c1.concept\_id                                JOIN concept c2 ON cr.concept\_id\_2 = c2.concept\_id                                JOIN vocabulary v1 ON c1.vocabulary\_id = v1.vocabulary\_id                                JOIN vocabulary v2 ON c2.vocabulary\_id = v2.vocabulary\_id                                WHERE cr.relationship\_id = 'Maps to'                                AND c1.concept\_code like '724%'                                AND c2.standard\_concept = 'S'                                AND v1.vocabulary\_id = 'ICD9CM'                                AND v2.vocabulary\_id = 'SNOMED'                                AND sysdate BETWEEN cr.valid\_start\_date AND cr.valid\_end\_date                        ) t ON ca.ancestor\_concept\_id = t.target\_concept\_id                                                          ) ON descendant\_concept\_id = condition\_concept\_id      LEFT OUTER JOIN /\* surgery \*/         ( SELECT person\_id, procedure\_date, 1 AS surgery             FROM procedure\_occurrence proc             JOIN concept ON concept\_id = procedure\_concept\_id            WHERE vocabulary\_id = 'CPT4' /\* CPT-4 \*/              AND concept\_code               IN( '22851', '20936', '22612', '22523', '22630',                   '22614', '22842', '22632', '20930', '22524',                   '27130', '22525'                 )         ) surgery        ON surgery.person\_id = era.person\_id       AND surgery.procedure\_date BETWEEN condition\_era\_start\_date                                      AND condition\_era\_start\_date + 60      LEFT OUTER JOIN /\* drugs \*/         ( SELECT person\_id, procedure\_date AS drug\_date, 1 AS drug             FROM procedure\_occurrence proc             JOIN concept ON concept\_id = procedure\_concept\_id            WHERE vocabulary\_id = 'CPT4' /\* CPT-4 \*/              AND concept\_code               IN( '20610','20552','207096','20553','20550','20605'                 ,'20551','20600','23350' )          UNION           SELECT person\_id, drug\_era\_start\_date, 1            FROM drug\_era           WHERE drug\_concept\_id              IN( 1125315, 778711, 1115008, 1177480, 1112807, 1506270 )         ) drug         ON drug.person\_id = era.person\_id       AND drug.drug\_date BETWEEN condition\_era\_start\_date                              AND condition\_era\_start\_date + 60      LEFT OUTER JOIN /\* pt \*/         ( SELECT person\_id, procedure\_date AS pt\_date, 1 AS pt             FROM procedure\_occurrence proc             JOIN concept ON concept\_id = procedure\_concept\_id            WHERE vocabulary\_id = 'CPT4' /\* CPT-4 \*/              AND concept\_code               IN( '97001', '97140', '97002' )           UNION           SELECT person\_id, procedure\_date AS pt\_date, 1 AS pt             FROM procedure\_occurrence proc             JOIN concept ON concept\_id = procedure\_concept\_id            WHERE vocabulary\_id = 'HCPCS' /\* HCPCS \*/              AND concept\_code = 'G0283'         ) pt        ON pt.person\_id = era.person\_id       AND pt.pt\_date BETWEEN condition\_era\_start\_date                          AND condition\_era\_start\_date + 60     ) WHERE diag\_date > '2011-01-01' GROUP by person\_id, diag\_date ORDER BY person\_id, diag\_date))GROUP BY treatment ORDER BY treatment;   **Output:**
Output field list:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |


Sample output record:

| ** Field** | ** Description** |
| --- | --- |
| treatment |   |
| --- | --- |
| count |   |
| --- | --- |

  |
| --- |
### COC01: Determines first line of therapy for a condition

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| list of condition\\_concept\\_id | 432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742, 4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366, 4292524, 4299298, 4299302, 4301157, 4307793 | Yes | Angioedema 1 |

| --- | --- | --- | --- |

| ancestor\\_concept\\_id | 21003378 | Yes | Angioedema |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT   ingredient\\_name,   ingredient\\_concept\\_id,   count(\\*) num\\_patients FROM /\\*Drugs started by people up to 30 days after Angioedema diagnosis \\*/ (   SELECT     condition.person\\_id,     condition\\_start\\_date ,     drug\\_era\\_start\\_date ,     ingredient\\_name,     ingredient\\_concept\\_id   FROM /\\* people with Angioedema with 180 clean period and 180 day follow-up \\*/ (     SELECT       era.person\\_id,       condition\\_era\\_start\\_date AS condition\\_start\\_date     FROM condition\\_era era     JOIN observation\\_period obs       ON obs.person\\_id = era.person\\_id AND          condition\\_era\\_start\\_date BETWEEN observation\\_period\\_start\\_date + 180 AND observation\\_period\\_end\\_date - 180     WHERE       condition\\_concept\\_id IN -- SNOMed codes for OMOP Angioedema 1       ( \*\*432791, 4080130, 4081073, 4083996, 4083997, 4083998, 4084171, 4084172, 4084173, 4084174, 4086741, 4086742,\*\*  \*\*        4086744, 4120778, 4125819, 4140613, 4161207, 4224624, 4224625, 4270861, 4270862, 4270865, 4292365, 4292366,\*\*  \*\*        4292524, 4299298, 4299302, 4301157, 4307793\*\* )   ) condition   JOIN drug\\_era rx /\\* Drug\\_era has drugs at ingredient level \\*/     ON rx.person\\_id = condition.person\\_id AND        rx.drug\\_era\\_start\\_date BETWEEN condition\\_start\\_date AND condition\\_start\\_date + 30   JOIN /\\* Ingredients for indication Angioedema \\*/ (     SELECT       ingredient.concept\\_id AS ingredient\\_concept\\_id ,       ingredient.concept\\_name AS ingredient\\_name     FROM concept ingredient     JOIN concept\\_ancestor a ON a.descendant\\_concept\\_id = ingredient.concept\\_id     WHERE       a.ancestor\\_concept\\_id = \*\*21003378\*\* /\\* indication for angioedema \\*/ AND       ingredient.vocabulary\\_id = 8 AND       sysdate BETWEEN ingredient.valid\\_start\\_date AND ingredient.valid\\_end\\_date   ) ON ingredient\\_concept\\_id = drug\\_concept\\_id ) GROUP by ingredient\\_name, ingredient\\_concept\\_id ORDER BY num\\_patients DESC;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| ingredient\\_name |   |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| ingredient\\_name |   |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### COC02: Determines length of course of therapy for a condition

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| condition\\_concept\\_id | 500000201 | Yes | SNOMed codes for OMOP Aplastic Anemia 1 |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT        ingredient\\_name,                ingredient\\_concept\\_id,                count(\\*) AS num\\_patients,                min( length\\_of\\_therapy ) AS min\\_length\\_of\\_therapy\\_count,                max( length\\_of\\_therapy ) AS max\\_length\\_of\\_therapy\\_count,                avg( length\\_of\\_therapy ) AS average\\_length\\_of\\_therapy\\_countFROM         (        SELECT        condition.person\\_id,                        condition\\_start\\_date,                        drug\\_era\\_start\\_date,                        drug\\_era\\_end\\_date - drug\\_era\\_start\\_date + 1 AS length\\_of\\_therapy,                        ingredient\\_name,                        ingredient\\_concept\\_id        FROM                (                SELECT        era.person\\_id,                                condition\\_era\\_start\\_date AS condition\\_start\\_date                FROM        condition\\_era era                                        JOIN        observation\\_period AS obs                                                ON        obs.person\\_id = era.person\\_id                                                AND condition\\_era\\_start\\_date BETWEEN observation\\_period\\_start\\_date + 180                                                AND observation\\_period\\_end\\_date - 180                WHERE                        condition\\_concept\\_id IN ( \*\*137829,138723,140065,140681,4031699,4098027,4098028, 4098145,4098760,4100998,4101582,4101583,4120453,4125496, 4125497,4125498,4125499,4146086,4146087,4146088,4148471, 4177177,4184200,4184758,4186108,4187773,4188208,4211348, 4211695,4225810,4228194,4234973,4298690,4345236\*\* )                ) condition                        JOIN        drug\\_era rx                                ON        rx.person\\_id = condition.person\\_id                                AND rx.drug\\_era\\_start\\_date BETWEEN condition\\_start\\_date AND condition\\_start\\_date + 30                        JOIN                                 (                                SELECT DISTINCT        ingredient.concept\\_id as ingredient\\_concept\\_id,                                                                ingredient.concept\\_name as ingredient\\_name                                FROM        concept\\_ancestor ancestor                                                        JOIN        concept indication                                                                ON        ancestor.ancestor\\_concept\\_id = indication.concept\\_id                                                        JOIN concept ingredient                                                                ON        ingredient.concept\\_id = ancestor.descendant\\_concept\\_id                                WHERE                                        lower( indication.concept\\_name ) like( '%anemia%' )                                AND        indication.vocabulary\\_id = 'Indication'                                AND ingredient.vocabulary\\_id = 'RxNorm'                                AND sysdate BETWEEN indication.valid\\_start\\_date AND indication.valid\\_end\\_date                                AND sysdate BETWEEN ingredient.valid\\_start\\_date AND ingredient.valid\\_end\\_date                                 )                                        ON ingredient\\_concept\\_id = drug\\_concept\\_id         )GROUP BY        ingredient\\_name,                        ingredient\\_concept\\_idORDER BY        num\\_patients DESC; \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| ingredient\\_name |   |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| ingredient\\_name |   |

| --- | --- |

| ingredient\\_concept\\_id |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |

### COC05: Mortality rate after initial diagnosis

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | OMOP Acute Myocardial Infarction 1 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT   COUNT( DISTINCT diagnosed.person\\_id ) AS all\\_infarctions ,   SUM( CASE WHEN death.person\\_id IS NULL THEN 0 ELSE 1 END ) AS death\\_from\\_infarction FROM -- Initial diagnosis of Acute Myocardial Infarction (   SELECT DISTINCT     person\\_id,     condition\\_era\\_start\\_date   FROM /\\* diagnosis of Acute Myocardial Infarction, ranked by date, 6 month clean period with 1 year follow-up \\*/   (     SELECT       condition.person\\_id,       condition.condition\\_era\\_start\\_date ,       sum(1) OVER(PARTITION BY condition.person\\_id ORDER BY condition\\_era\\_start\\_date ROWS UNBOUNDED PRECEDING) AS ranking     FROM       condition\\_era condition     JOIN --definition of Acute Myocardial Infarction 1     (       SELECT DISTINCT descendant\\_concept\\_id       FROM relationship       JOIN concept\\_relationship rel USING( relationship\\_id )       JOIN concept concept1 ON concept1.concept\\_id = concept\\_id\\_1       JOIN concept\\_ancestor ON ancestor\\_concept\\_id = concept\\_id\\_2       WHERE         relationship\\_name = 'HOI contains SNOMED (OMOP)' AND         concept1.concept\\_name = \*\*'OMOP Acute Myocardial Infarction 1'\*\* AND         sysdate BETWEEN rel.valid\\_start\\_date and rel.valid\\_end\\_date     ) ON descendant\\_concept\\_id = condition\\_concept\\_id     JOIN observation\\_period obs       ON obs.person\\_id = condition.person\\_id AND          condition\\_era\\_start\\_date BETWEEN observation\\_period\\_start\\_date + 180 AND observation\\_period\\_end\\_date - 360   ) WHERE ranking = 1 ) diagnosed LEFT OUTER JOIN death /\\* death within a year \\*/   ON death.person\\_id = diagnosed.person\\_id AND   death.death\\_date <= condition\\_era\\_start\\_date + 360; \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| all\\_infarctions |   |

| --- | --- |

| death\\_from\\_infarction |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| all\\_infarctions |   |

| --- | --- |

| death\\_from\\_infarction |   |

| --- | --- |

  |

| --- |

### COC06: Time until death after initial diagnosis

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | OMOP Acute Myocardial Infarction 1 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT COUNT( DISTINCT diagnosed.person\\_id ) AS all\\_infarction\\_deaths     , ROUND( min( death\\_date - condition\\_era\\_start\\_date )/365, 1 ) AS min\\_years     , ROUND( max( death\\_date - condition\\_era\\_start\\_date )/365, 1 ) AS max\\_years     , ROUND( avg( death\\_date - condition\\_era\\_start\\_date )/365, 1 ) AS avg\\_years  FROM -- Initial diagnosis of Acute Myocardial Infarction     ( SELECT DISTINCT person\\_id, condition\\_era\\_start\\_date         FROM  /\\* diagnosis of Acute Myocardial Infarction, ranked by                  date, 6 month clean                \\*/            ( SELECT condition.person\\_id, condition.condition\\_era\\_start\\_date                   , rank() OVER( PARTITION BY condition.person\\_id                                      ORDER BY condition\\_era\\_start\\_date                                ) AS ranking                FROM condition\\_era condition                JOIN -- definition of Acute Myocardial Infarction 1                   ( SELECT DISTINCT descendant\\_concept\\_id                       FROM relationship                       JOIN concept\\_relationship rel USING( relationship\\_id )                        JOIN concept concept1 ON concept1.concept\\_id = concept\\_id\\_1                       JOIN concept\\_ancestor ON ancestor\\_concept\\_id = concept\\_id\\_2                      WHERE relationship\\_name = 'HOI contains SNOMED (OMOP)'                        AND concept1.concept\\_name = \*\*'OMOP Acute Myocardial Infarction 1'\*\*                         AND sysdate BETWEEN rel.valid\\_start\\_date and rel.valid\\_end\\_date                   ) ON descendant\\_concept\\_id = condition\\_concept\\_id                JOIN observation\\_period obs                  ON obs.person\\_id = condition.person\\_id                 AND condition\\_era\\_start\\_date >= observation\\_period\\_start\\_date + 180            )        WHERE ranking = 1     ) diagnosed  JOIN death     ON death.person\\_id = diagnosed.person\\_id  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| all\\_infarction\\_deaths |   |

| --- | --- |

| min\\_years |   |

| --- | --- |

| max\\_years |   |

| --- | --- |

| avg\\_years |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| all\\_infarction\\_deaths |   |

| --- | --- |

| min\\_years |   |

| --- | --- |

| max\\_years |   |

| --- | --- |

| avg\\_years |   |

| --- | --- |

  |

| --- |

### COC07: Patients with condition in conjunction with a procedure some number of days prior to or after initial condition.

| Aplastic Anemia AND Occurrence of at least one diagnostic procedure code for bone marrow aspiration or biopsy within 60 days prior to the diagnostic code.

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | OMOP Aplastic Anemia 1 | Yes |   |

| --- | --- | --- | --- |

| list of procedure\\_concept\\_id | 2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142 , 3048879, 36359239, 37586183 |   | Bone marrow aspiration or biopsy |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT DISTINCT        condition.person\\_id,                                procedure\\_date,                                condition\\_era\\_start\\_dateFROM        procedure\\_occurrence proc                JOIN        condition\\_era condition                                        ON condition.person\\_id = proc.person\\_id                JOIN                                        (                                SELECT DISTINCT        descendant\\_concept\\_id                                FROM        relationship                                                JOIN        concept\\_relationship rel USING( relationship\\_id )                                                JOIN        concept concept1                                                                        ON        concept1.concept\\_id = concept\\_id\\_1                                                JOIN        concept\\_ancestor                                                                        ON        ancestor\\_concept\\_id = concept\\_id\\_2                                WHERE        relationship\\_name = 'HOI contains SNOMED (OMOP)'                                AND                concept1.concept\\_name = \*\*'OMOP Aplastic Anemia 1'\*\*                                 AND                sysdate BETWEEN rel.valid\\_start\\_date and rel.valid\\_end\\_date                                )                                         ON descendant\\_concept\\_id = condition\\_concept\\_idWHERE        proc.procedure\\_concept\\_id IN ( \*\*2002382, 2002403, 2108452, 2108453, 2212660, 2212662, 3045142, 3048879, 36359239, 37586183\*\* )AND procedure\\_date BETWEEN condition\\_era\\_start\\_date - 60 AND condition\\_era\\_start\\_date;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| condition\\_concept\\_id | A foreign key that refers to a standard condition concept identifier in the vocabulary. |

| --- | --- |

| person\\_id |   |

| --- | --- |

| procedure\\_date |   |

| --- | --- |

| condition\\_era\\_start\\_date |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id |   |

| --- | --- |

| procedure\\_date |   |

| --- | --- |

| condition\\_era\\_start\\_date |   |

| --- | --- |

  |

| --- |

### COC08: Patients with condition and some observation criteria some number of days prior to or after initial condition

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_name | OMOP Aplastic Anemia 1 | Yes |   |

| --- | --- | --- | --- |

| list of observation\\_concept\\_id | 3000905, 3003282, 3010813 |   | Leukocytes #/volume in blood |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT DISTINCT   condition.person\\_id ,   observation\\_date,   condition\\_era\\_start\\_date FROM   condition\\_era condition JOIN -- definition of Aplastic Anemia (   SELECT DISTINCT descendant\\_concept\\_id   FROM relationship   JOIN concept\\_relationship rel USING( relationship\\_id )   JOIN concept concept1 ON concept1.concept\\_id = concept\\_id\\_1   JOIN concept\\_ancestor ON ancestor\\_concept\\_id = concept\\_id\\_2   WHERE     relationship\\_name = 'HOI contains SNOMED (OMOP)' AND     concept1.concept\\_name = \*\*'OMOP Aplastic Anemia 1'\*\* AND     sysdate BETWEEN rel.valid\\_start\\_date and rel.valid\\_end\\_date ) ON descendant\\_concept\\_id = condition\\_concept\\_id JOIN observation   ON observation.person\\_id = condition.person\\_id AND      observation\\_date BETWEEN condition\\_era\\_start\\_date - 7 AND condition\\_era\\_start\\_date + 7 WHERE   observation\\_concept\\_id IN /\\* leukocytes #/volume in blood \\*/ ( \*\*3000905, 3003282, 3010813 ) AND\*\*   unit\\_concept\\_id = 8961 /\\* Thousand per cubic millimeter \\*/ AND   value\\_as\\_number <= 3.5;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id |   |

| --- | --- |

| observation\\_date |   |

| --- | --- |

| condition\\_era\\_start\\_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| person\\_id |   |

| --- | --- |

| observation\\_date |   |

| --- | --- |

| condition\\_era\\_start\\_date | The start date for the condition era constructed from the individual instances of condition occurrences. It is the start date of the very first chronologically recorded instance of the condition. |

| --- | --- |

  |

| --- |

### COC09: Condition that is regionally dependent

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| source\\_code | 088.81 | Yes | lyme disease |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT        state,                count(\\*) AS total\\_enroled,                sum( lymed ) AS lyme\\_cases,                TRUNC( ( sum(lymed) /count(\\*) ) \\* 100, 2 ) AS percentagesFROM        (        SELECT        person\\_id,                        state,                        NVL( lymed, 0 ) lymed        FROM person                JOIN location USING( location\\_id )                LEFT OUTER JOIN                        (                        SELECT DISTINCT        person\\_id,                                                        1 AS lymed                        FROM                                condition\\_era                                        JOIN source\\_to\\_concept\\_map                                                ON        target\\_concept\\_id = condition\\_concept\\_id                        WHERE                                source\\_vocabulary\\_id         = 'ICD9CM'                        AND        target\\_vocabulary\\_id         = 'SNOMED'                        AND        source\\_code                         = \*\*'088.81'\*\*                         AND sysdate                                 BETWEEN valid\\_start\\_date and valid\\_end\\_date                        ) USING( person\\_id )         )GROUP BY        stateORDER BY        4 DESC;  \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| state | The state field as it appears in the source data. |

| --- | --- |

| count |   |

| --- | --- |

| lyme\\_cases |   |

| --- | --- |

| percent |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| state |   |

| --- | --- |

| count |   |

| --- | --- |

| lyme\\_cases |   |

| --- | --- |

| percent |   |

| --- | --- |

  |

| --- |

### COC10: Lenght of condition as function of treatment

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_code | '22851','20936','22612','22523','22630','22614','22842' , '22632', '20930','22524','27130','22525' | Yes |   |

| --- | --- | --- | --- |

| concept\\_code | 20610','20552','207096','20553','20550','20605' | Yes |   |

| --- | --- | --- | --- |

| drug\\_concept\\_id | 1125315, 778711, 115008, 1177480, 1112807, 1506270 | Yes |   |

| --- | --- | --- | --- |

| concept\\_code | '97001', '97140', '97002' | Yes |   |

| --- | --- | --- | --- |

| concept\\_code | G0283 | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT   treatment,   count(\\*),   min( condition\\_days ) AS min ,   max( condition\\_days ) AS max,   avg( condition\\_days ) As avg\\_condition\\_days FROM (   SELECT     CASE WHEN surgery = 1 THEN 'surgery'          WHEN drug = 1 AND pt = 1 THEN 'PT Rx'          WHEN drug = 1 THEN 'Rx Only'          ELSE 'No Treatment'     END AS treatment ,     condition\\_days   FROM (     SELECT       person\\_id,       diag\\_date ,      max( drug ) AS drug,       max( surgery ) AS surgery,       max( pt ) AS PT ,       max( condition\\_days ) AS condition\\_days     FROM /\\* back pain and treatments over following 60 days \\*/ (       SELECT         era.person\\_id,         condition\\_era\\_start\\_date AS diag\\_date ,         condition\\_era\\_end\\_date - condition\\_era\\_start\\_date AS condition\\_days,         NVL( drug, 0 ) AS drug,         NVL( surgery, 0 ) AS surgery ,         NVL( pt, 0 ) AS pt       FROM condition\\_era era       JOIN /\\* SNOMed codes for back pain \\*/ (         SELECT DISTINCT           descendant\\_concept\\_id -- concept\\_name         FROM source\\_to\\_concept\\_map map         JOIN concept\\_ancestor ON ancestor\\_concept\\_id = target\\_concept\\_id         JOIN concept ON concept\\_id = descendant\\_concept\\_id         WHERE           source\\_code like '724%' AND           source\\_vocabulary\\_id = 'ICD9CM' AND           target\\_vocabulary\\_id = 'SNOMED' AND           sysdate BETWEEN map.valid\\_start\\_date AND map.valid\\_end\\_date       ) ON descendant\\_concept\\_id = condition\\_concept\\_id       LEFT OUTER JOIN (         SELECT           person\\_id,           procedure\\_date,           1 AS surgery         FROM procedure\\_occurrence proc         JOIN concept ON concept\\_id = procedure\\_concept\\_id         WHERE           vocabulary\\_id = 'CPT4' AND           concept\\_code IN( '22851','20936','22612','22523','22630','22614\\*','22842','22632','20930','22524','27130','22525' )       ) surgery         ON surgery.person\\_id = era.person\\_id AND            surgery.procedure\\_date BETWEEN condition\\_era\\_start\\_date AND condition\\_era\\_start\\_date + 60       LEFT OUTER JOIN (         SELECT           person\\_id,           procedure\\_date AS drug\\_date,           1 AS drug         FROM procedure\\_occurrence proc         JOIN concept ON concept\\_id = procedure\\_concept\\_id         WHERE           vocabulary\\_id = 'CPT4' AND           concept\\_code IN( '20610','20552','207096','20553','20550','20605' ,'20551','20600','23350' )         UNION SELECT           person\\_id,           drug\\_era\\_start\\_date,           1         FROM drug\\_era         WHERE drug\\_concept\\_id IN(1125315, 778711, 1115008, 1177480, 1112807,1506270 )       ) drug         ON drug.person\\_id = era.person\\_id AND            drug.drug\\_date BETWEEN condition\\_era\\_start\\_date AND condition\\_era\\_start\\_date + 60       LEFT OUTER JOIN (         SELECT           person\\_id,           procedure\\_date AS pt\\_date,           1 AS pt         FROM procedure\\_occurrence proc         JOIN concept ON concept\\_id = procedure\\_concept\\_id         WHERE           vocabulary\\_id = 'CPT4' AND           concept\\_code IN( '97001', '97140', '97002' )         UNION SELECT           person\\_id,           procedure\\_date AS pt\\_date,           1 AS pt         FROM procedure\\_occurrence proc         JOIN concept ON concept\\_id = procedure\\_concept\\_id         WHERE           vocabulary\\_id = 'HCPCS' AND           concept\\_code = 'G0283'       ) pt         ON pt.person\\_id = era.person\\_id AND            pt.pt\\_date BETWEEN condition\\_era\\_start\\_date AND condition\\_era\\_start\\_date + 60     )     WHERE diag\\_date > '01-jan-2011'     GROUP by       person\\_id,       diag\\_date     ORDER BY       person\\_id,       diag\\_date   ) ) GROUP BY treatment ORDER BY treatment; \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| treatment |   |

| --- | --- |

| count |   |

| --- | --- |

| min |   |

| --- | --- |

| max |   |

| --- | --- |

| avg\\_condition\\_days |   |

| --- | --- |

Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| treatment |   |

| --- | --- |

| count |   |

| --- | --- |

| min |   |

| --- | --- |

| max |   |

| --- | --- |

| avg\\_condition\\_days |   |

| --- | --- |

  |

| --- |

### COC11: Given a condition, what treatment did patient receive

|

\*\*Input:\*\*

| \*\* Parameter\*\* | \*\* Example\*\* | \*\* Mandatory\*\* | \*\* Notes\*\* |

| --- | --- | --- | --- |

| concept\\_code | '22851', '20936', '22612', '22523', '22630', '22614', '22842' , '22632', '20930', '22524', '27130', '22525' | Yes |   |

| --- | --- | --- | --- |



\*\*Sample query run:\*\*

The following is a sample run of the query. The input parameters are highlighted in  \*\*blue\*\*  SELECT treatment, count(\\*) FROM(SELECT CASE WHEN surgery = 1            THEN 'surgery'            WHEN drug = 1 AND pt = 1             THEN 'PT Rx'            WHEN drug = 1            THEN 'Rx Only'            ELSE 'No Treatment'       END AS treatmentFROM(SELECT person\\_id, diag\\_date     , max( drug ) AS drug, max( surgery ) AS surgery, max( pt ) AS PT  FROM /\\* back pain and treatments over following 60 days \\*/     (      SELECT era.person\\_id, condition\\_era\\_start\\_date AS diag\\_date          , NVL( drug, 0 ) AS drug, NVL( surgery, 0 ) AS surgery          , NVL( pt, 0 ) AS pt       FROM condition\\_era era                 JOIN /\\* SNOMed codes for back pain \\*/                        ( SELECT DISTINCT ca.descendant\\_concept\\_id                        FROM concept\\_ancestor ca JOIN                        ( SELECT cr.concept\\_id\\_2 AS target\\_concept\\_id                                FROM concept\\_relationship cr                                JOIN concept c1 ON cr.concept\\_id\\_1 = c1.concept\\_id                                JOIN concept c2 ON cr.concept\\_id\\_2 = c2.concept\\_id                                JOIN vocabulary v1 ON c1.vocabulary\\_id = v1.vocabulary\\_id                                JOIN vocabulary v2 ON c2.vocabulary\\_id = v2.vocabulary\\_id                                WHERE cr.relationship\\_id = 'Maps to'                                AND c1.concept\\_code like '724%'                                AND c2.standard\\_concept = 'S'                                AND v1.vocabulary\\_id = 'ICD9CM'                                AND v2.vocabulary\\_id = 'SNOMED'                                AND sysdate BETWEEN cr.valid\\_start\\_date AND cr.valid\\_end\\_date                        ) t ON ca.ancestor\\_concept\\_id = t.target\\_concept\\_id                                                          ) ON descendant\\_concept\\_id = condition\\_concept\\_id      LEFT OUTER JOIN /\\* surgery \\*/         ( SELECT person\\_id, procedure\\_date, 1 AS surgery             FROM procedure\\_occurrence proc             JOIN concept ON concept\\_id = procedure\\_concept\\_id            WHERE vocabulary\\_id = 'CPT4' /\\* CPT-4 \\*/              AND concept\\_code               IN( '22851', '20936', '22612', '22523', '22630',                   '22614', '22842', '22632', '20930', '22524',                   '27130', '22525'                 )         ) surgery        ON surgery.person\\_id = era.person\\_id       AND surgery.procedure\\_date BETWEEN condition\\_era\\_start\\_date                                      AND condition\\_era\\_start\\_date + 60      LEFT OUTER JOIN /\\* drugs \\*/         ( SELECT person\\_id, procedure\\_date AS drug\\_date, 1 AS drug             FROM procedure\\_occurrence proc             JOIN concept ON concept\\_id = procedure\\_concept\\_id            WHERE vocabulary\\_id = 'CPT4' /\\* CPT-4 \\*/              AND concept\\_code               IN( '20610','20552','207096','20553','20550','20605'                 ,'20551','20600','23350' )          UNION           SELECT person\\_id, drug\\_era\\_start\\_date, 1            FROM drug\\_era           WHERE drug\\_concept\\_id              IN( 1125315, 778711, 1115008, 1177480, 1112807, 1506270 )         ) drug         ON drug.person\\_id = era.person\\_id       AND drug.drug\\_date BETWEEN condition\\_era\\_start\\_date                              AND condition\\_era\\_start\\_date + 60      LEFT OUTER JOIN /\\* pt \\*/         ( SELECT person\\_id, procedure\\_date AS pt\\_date, 1 AS pt             FROM procedure\\_occurrence proc             JOIN concept ON concept\\_id = procedure\\_concept\\_id            WHERE vocabulary\\_id = 'CPT4' /\\* CPT-4 \\*/              AND concept\\_code               IN( '97001', '97140', '97002' )           UNION           SELECT person\\_id, procedure\\_date AS pt\\_date, 1 AS pt             FROM procedure\\_occurrence proc             JOIN concept ON concept\\_id = procedure\\_concept\\_id            WHERE vocabulary\\_id = 'HCPCS' /\\* HCPCS \\*/              AND concept\\_code = 'G0283'         ) pt        ON pt.person\\_id = era.person\\_id       AND pt.pt\\_date BETWEEN condition\\_era\\_start\\_date                          AND condition\\_era\\_start\\_date + 60     ) WHERE diag\\_date > '2011-01-01' GROUP by person\\_id, diag\\_date ORDER BY person\\_id, diag\\_date))GROUP BY treatment ORDER BY treatment;   \*\*Output:\*\*

Output field list:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| treatment |   |

| --- | --- |

| count |   |

| --- | --- |



Sample output record:

| \*\* Field\*\* | \*\* Description\*\* |

| --- | --- |

| treatment |   |

| --- | --- |

| count |   |

| --- | --- |

  |

| --- |
