select time_term_year_ld, min(class_start_day_key) as startdate
from tableau.enroll_drop_extract_tbl 
where class_start_day_key > (select min(class_start_day_key) from tableau.enroll_drop_extract_tbl where time_term_year_ld = {term}) + 25
 and class_start_day_key <= {date}
group by time_term_year_ld
order by min(class_start_day_key)