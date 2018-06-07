Payer Plan Queries
---

PP01: Continuous years with patient counts
---

List number of patients who have continuous payer plan of at least one year

Sample query:

	SELECT floor((p.payer_plan_period_end_date - p.payer_plan_period_start_date)/365) AS year_int, count(1) AS num_patients

	FROM payer_plan_period p

	GROUP BY floor((p.payer_plan_period_end_date - p.payer_plan_period_start_date)/365)

	ORDER BY 1;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| year_int | Years between payer plan end date and start date |
| num_patients | Number of patients |

Sample output record:

| Field |  Description |
| --- | --- |
| year_int |  1 |
| num_patients |  42458099 |


PP02:Patient distribution by plan type
---

Sample query:

	select

	  t.plan_source_value,

	  t.pat_cnt as num_patients,

	  100.00\*t.pat_cnt/ (sum(t.pat_cnt) over()) perc_of_total_count

	from (

	  select p.plan_source_value, count(1) as pat_cnt

	  from payer_plan_period p

	  group by p.plan_source_value

	) t

	order by t.plan_source_value;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| plan_source_value | The source code for the person's coverage plan as it appears in the source data. |
| num_patients | Number of patients |
| perc_of_total_count | Total count |

Sample output record:

|  Field |  Value |
| --- | --- |
| plan_source_value | Preferred Provider Organization |
| num_patients | 148348803 |
| perc_of_total_count | 68.632428630338134 |


