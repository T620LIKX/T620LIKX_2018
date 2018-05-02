UPDATE departments SET department_name = 'Tæknifræði' WHERE id = 3;
UPDATE departments SET department_name = 'Tölvunarfræði' WHERE id = 4;
UPDATE departments SET department_name = 'Viðskiptafræði' WHERE id = 5;

INSERT INTO departments VALUES (6, 'Verkfræði');
INSERT INTO departments VALUES (7, 'Íþróttafræði');
INSERT INTO departments VALUES (8, 'Sálfræði');

UPDATE courses SET department_id = 6 WHERE department_id = 3 AND course_id LIKE '%SE-T-%';

UPDATE courses SET department_id = 7 WHERE department_id = 3 AND course_id LIKE '%SE-E-%';

UPDATE courses SET department_id = 8 WHERE department_id = 5 AND course_id LIKE '%SB-E-%';

ALTER TABLE courses ADD graduate_course BOOLEAN;

UPDATE courses SET graduate_course = FALSE;

UPDATE courses SET graduate_course = TRUE WHERE department_id = 4 AND course_id LIKE '%SC-T-7%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 3 AND course_id LIKE '%SE-SE-%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 5 AND course_id LIKE '%SB-V-7%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 5 AND course_id LIKE '%SB-V-8%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 6 AND course_id LIKE '%SE-T-7%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 6 AND course_id LIKE '%SE-T-8%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 7 AND course_id LIKE '%SE-E-7%';

UPDATE courses SET graduate_course = TRUE WHERE department_id = 8 AND course_id LIKE '%SB-E-7%';

