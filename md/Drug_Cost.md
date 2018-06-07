DRC01: What is the average/max/min cost per pill (total cost / quantity) per drug concept?
---

Sample query:

  SELECT avg(t.cost_per_pill) avg_val_num, max(t.cost_per_pill) max_val_num, min(t.cost_per_pill) min_val_num, t.drug_concept_id

  from (

  select c.total_paid/d.quantity as cost_per_pill, d.drug_concept_id

  FROM cost c

  JOIN drug_exposure d

  ON d.drug_exposure_id = c.cost_event_id

  WHERE d.quantity > 0

  AND d.drug_concept_id

  IN (906805, 1517070, 19010522) ) t

  GROUP BY t.drug_concept_id

  ORDER BY t.drug_concept_id;

Input:

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |
 |

Output:

|  Field |  Description |
| --- | --- |
| drug_concept_id | Drug concept id |
| avg_val_num | Average cost per pill |
| max_val_num | Max cost per pill |
| min_val_num | Min cost per pill |



Sample output record:

|  Field |  Description |
| --- | --- |
| drug_concept_id | 19010522 |
| avg_val_num | 2.6983903185925794872997154 |
| max_val_num | 3197.50 |
| min_val_num | 0 |



DRC03: What is out-of-pocket cost for a given drug?

Sample query:

  SELECT avg(c.paid_by_patient - c.paid_patient_copay) AS avg_out_pocket_cost, d.drug_concept_id

  FROM cost c, drug_exposure d

  WHERE d.drug_exposure_id = c.cost_event_id

  AND (c.paid_by_patient - c.paid_patient_copay) > 0

  AND d.drug_concept_id

  IN (906805, 1517070, 19010522)

  GROUP BY d.drug_concept_id;

Input:

|   |
| --- |
|  Parameter |  Example |  Mandatory |  Notes |
| list of drug_concept_id | 906805, 1517070, 19010522 | Yes |   |

Output:

|  Field |  Description |
| --- | --- |
| drug_concept_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| total_out_of_pocket | The total amount paid by the person as a share of the expenses, excluding the copay. |
| avg_out_pocket_cost | The average amount paid by the person as a share of the expenses, excluding the copay. |

Sample output record:

|   |
| --- |
| Field |  Description |
| avg_out_pocket_cost |   |
| drug_concept_id |   |
| total_out_of_pocket |   |



 DRC07:Distribution of costs paid by payer.
 ---

This query is used to to provide summary statistics for costs paid by coinsurance (paid_coinsurance) across all drug cost records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

Sample query:

  with tt as (

    SELECT t.paid_patient_coinsurance AS stat_value

    FROM cost t

    where t.paid_patient_coinsurance > 0

  )

  SELECT

    min(tt.stat_value) AS min_value,

    max(tt.stat_value) AS max_value,

    avg(tt.stat_value) AS avg_value,

    (round(stdDev(tt.stat_value)) ) AS stdDev_value ,

    (select distinct PERCENTILE_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat_value) OVER() from tt) AS percentile_25,

    (select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS median_value,

    (select distinct PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat_value) OVER() from tt) AS percential_75

  FROM

   tt;

Input:

None

Output:

|   |
| --- |
|  Field |  Description |
| min_value | The portion of the drug expenses due to the cost charged by the manufacturer for the drug, typically a percentage of the Average Wholesale Price. |
| max_value |   |
| avg_value |   |
| stdDev_value |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| min_value |   |
| max_value |   |
| avg_value |   |
| stdDev_value |   |



