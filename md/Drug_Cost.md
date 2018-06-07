**DRC01:** What is the average/max/min cost per pill (total cost / quantity) per drug concept?

**Sample query:**

SELECT avg(t.cost\_per\_pill) avg\_val\_num, max(t.cost\_per\_pill) max\_val\_num, min(t.cost\_per\_pill) min\_val\_num, t.drug\_concept\_id

from (

select c.total\_paid/d.quantity as cost\_per\_pill, d.drug\_concept\_id

FROM cost c

JOIN drug\_exposure d

ON d.drug\_exposure\_id = c.cost\_event\_id

WHERE d.quantity > 0

AND d.drug\_concept\_id

IN (906805, 1517070, 19010522) ) t

GROUP BY t.drug\_concept\_id

ORDER BY t.drug\_concept\_id;

**Input:**

| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| --- | --- | --- | --- |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |
 |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | Drug concept id |
| avg\_val\_num | Average cost per pill |
| max\_val\_num | Max cost per pill |
| min\_val\_num | Min cost per pill |



**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | 19010522 |
| avg\_val\_num | 2.6983903185925794872997154 |
| max\_val\_num | 3197.50 |
| min\_val\_num | 0 |
*-*-*-*-*
**DRC03:** What is out-of-pocket cost for a given drug?

**Sample query:**

SELECT avg(c.paid\_by\_patient - c.paid\_patient\_copay) AS avg\_out\_pocket\_cost, d.drug\_concept\_id

FROM cost c, drug\_exposure d

WHERE d.drug\_exposure\_id = c.cost\_event\_id

AND (c.paid\_by\_patient - c.paid\_patient\_copay) > 0

AND d.drug\_concept\_id

IN (906805, 1517070, 19010522)

GROUP BY d.drug\_concept\_id;

**Input:**

|   |
| --- |
| ** Parameter** | ** Example** | ** Mandatory** | ** Notes** |
| list of drug\_concept\_id | 906805, 1517070, 19010522 | Yes |   |

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| drug\_concept\_id | A foreign key that refers to a standard concept identifier in the vocabulary for the drug concept. |
| total\_out\_of\_pocket | The total amount paid by the person as a share of the expenses, excluding the copay. |
| avg\_out\_pocket\_cost | The average amount paid by the person as a share of the expenses, excluding the copay. |

**Sample output record:**

|   |
| --- |
| **Field** | ** Description** |
| avg\_out\_pocket\_cost |   |
| drug\_concept\_id |   |
| total\_out\_of\_pocket |   |
*-*-*-*-*
### DRC07:Distribution of costs paid by payer.

This query is used to to provide summary statistics for costs paid by coinsurance (paid\_coinsurance) across all drug cost records: the mean, the standard deviation, the minimum, the 25th percentile, the median, the 75th percentile, the maximum and the number of missing values. No input is required for this query.

**Sample query:**

with tt as (

  SELECT t.paid\_patient\_coinsurance AS stat\_value

  FROM cost t

  where t.paid\_patient\_coinsurance > 0

)

SELECT

  min(tt.stat\_value) AS min\_value,

  max(tt.stat\_value) AS max\_value,

  avg(tt.stat\_value) AS avg\_value,

  (round(stdDev(tt.stat\_value)) ) AS stdDev\_value ,

  (select distinct PERCENTILE\_DISC(0.25) WITHIN GROUP(ORDER BY tt.stat\_value) OVER() from tt) AS percentile\_25,

  (select distinct PERCENTILE\_DISC(0.5) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS median\_value,

  (select distinct PERCENTILE\_DISC(0.75) WITHIN GROUP (ORDER BY tt.stat\_value) OVER() from tt) AS percential\_75

FROM

 tt;

**Input:**

None

**Output:**

|   |
| --- |
| ** Field** | ** Description** |
| min\_value | The portion of the drug expenses due to the cost charged by the manufacturer for the drug, typically a percentage of the Average Wholesale Price. |
| max\_value |   |
| avg\_value |   |
| stdDev\_value |   |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| min\_value |   |
| max\_value |   |
| avg\_value |   |
| stdDev\_value |   |
*-*-*-*-*
