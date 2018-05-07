ALTER TABLE solutions
DROP COLUMN room_id;

CREATE TABLE solution_room_assignment (
  id serial,
  solution_id int,
  timeslot int,
  course_id int references courses(id),
  room_id int references rooms(id),
  student_count int,
  primary key(id)
);