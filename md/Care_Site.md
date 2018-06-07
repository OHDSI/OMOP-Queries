CS01: Care site place of service counts

This query is used to count the care sites associated with the place of service type. This query is only available from CDM V4 and above.

Sample query:

	select cs.place_of_service_concept_id, count(1) places_of_service_count

	from care_site cs

	group by cs.place_of_service_concept_id

	order by 1;

Input:

None

Output:

| Field |  Description |
| --- | --- |
| place_of_service_concept_id | A foreign key that refers to a place of service concept identifier in the vocabulary. |
| places_of_service_count |   |

Sample output record:

| Field |  Description |
| --- | --- |
| place_of_service_concept_id |  8546 |
| places_of_service_count |  1 |

CS02: Patient count per care site place of service.

This query is used to count patients per care site place of service. This query is only available from CDM V4 and above.

Sample query:

	select cs.place_of_service_concept_id, count(1) num_patients

	from care_site cs, person p

	where p.care_site_id = cs.care_site_id

	group by cs.place_of_service_concept_id

	order by 1;

Input:

None

Output:

|  Field |  Description |
| --- | --- |
| place_of_service_concept_id | A foreign key that refers to a place of service concept identifier in the vocabulary. |
| care_site_id | A foreign key to the main care site where the provider is practicing. |
| num_patients |   |

Sample output record:

|  Field |  Description |
| --- | --- |
| place_of_service_concept_id |   |
| care_site_id |   |
| num_patients |   |



