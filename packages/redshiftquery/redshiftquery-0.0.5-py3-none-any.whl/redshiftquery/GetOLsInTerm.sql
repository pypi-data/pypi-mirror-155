select distinct class_session_cd
from tableau.enroll_drop_extract_tbl
where time_term_year_ld = {term}
 and class_session_cd like 'OL_'
 and Right(class_session_cd,1) IN ('0','1','2','3','4','5','6','7','8','9')
order by class_session_cd
