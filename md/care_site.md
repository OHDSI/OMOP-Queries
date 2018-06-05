
CS01: Care site place of service counts
----------

This query is used to count the care sites associated with the place of service type. This query is only available from CDM V4 and above.

**Sample query:**

    select cs.place\_of\_service\_concept\_id, count(1) places\_of\_service\_count

    from care\_site cs

    group by cs.place\_of\_service\_concept\_id

    order by 1;

**Input:**

None

**Output:**

| **Field** | ** Description** |
| --- | --- |
| place\_of\_service\_concept\_id | A foreign key that refers to a place of service concept identifier in the vocabulary. |
| places\_of\_service\_count |   |

**Sample output record:**

| **Field** | ** Description** |
| --- | --- |
| place\_of\_service\_concept\_id |  8546 |
| places\_of\_service\_count |  1 |

CS02: Patient count per care site place of service.
---------------

This query is used to count patients per care site place of service. This query is only available from CDM V4 and above.

**Sample query:**

    select cs.place\_of\_service\_concept\_id, count(1) num\_patients

    from care\_site cs, person p

    where p.care\_site\_id = cs.care\_site\_id

    group by cs.place\_of\_service\_concept\_id

    order by 1;

**Input:**

None

**Output:**

| ** Field** | ** Description** |
| --- | --- |
| place\_of\_service\_concept\_id | A foreign key that refers to a place of service concept identifier in the vocabulary. |
| care\_site\_id | A foreign key to the main care site where the provider is practicing. |
| num\_patients |   |

**Sample output record:**

| ** Field** | ** Description** |
| --- | --- |
| place\_of\_service\_concept\_id |   |
| care\_site\_id |   |
| num\_patients |   |
