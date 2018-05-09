Update courses set final_exam = FALSE
where course_name like '%fjarnám%'
and semester_type = 20184;

Update enrollment set course_id  = 469 where course_id = 468;
Update enrollment set course_id  = 463 where course_id = 462;
Update enrollment set course_id  = 487 where course_id = 488
and student_id not in (620, 3379);