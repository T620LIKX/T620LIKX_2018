
CREATE TABLE original_exams (
  id SERIAL,
  day_of_exam VARCHAR(256),
  starting VARCHAR(256),
  ending VARCHAR(256),
  timeslot int,
  course_id int,
  course_code VARCHAR(256),
  course_name VARCHAR(256),
  room_name VARCHAR(256),
  room_description VARCHAR(256),
  building VARCHAR(256),
  primary key(id)
)
