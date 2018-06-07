**PP01:** Continuous years with patient counts

List number of patients who have continuous payer plan of at least one year

**Sample query:**

SELECT floor((p.payer\_plan\_period\_end\_date - p.payer\_plan\_period\_start\_date)/365) AS year\_int, count(1) AS num\_patients

FROM payer\_plan\_period p

GROUP BY floor((p.payer\_plan\_period\_end\_date - p.payer\_plan\_period\_start\_date)/365)

ORDER BY 1;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| year\_int | Years between payer plan end date and start date |
| num\_patients | Number of patients |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| year\_int |  1 |
| num\_patients |  42458099 |
*-*-*-*-*
**P**** P02:**Patient distribution by plan type

**Sample query:**

select

  t.plan\_source\_value,

  t.pat\_cnt as num\_patients,

  100.00\*t.pat\_cnt/ (sum(t.pat\_cnt) over()) perc\_of\_total\_count

from (

  select p.plan\_source\_value, count(1) as pat\_cnt

  from payer\_plan\_period p

  group by p.plan\_source\_value

) t

order by t.plan\_source\_value;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| plan\_source\_value | The source code for the person's coverage plan as it appears in the source data. |
| num\_patients | Number of patients |
| perc\_of\_total\_count | Total count |

**Sample output record:**

| ** Field** | ** Value** |
| --- | --- |
| plan\_source\_value | Preferred Provider Organization |
| num\_patients | 148348803 |
| perc\_of\_total\_count | 68.632428630338134 |
*-*-*-*-*
