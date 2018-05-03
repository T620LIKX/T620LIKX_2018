param C >=0 integer; # Course index
param R >=0 integer; # Room index

param N {c in 1..C}; # Number of students in course c
param S {r in 1..R}; # Seats in room r

var x{c in 1..C, r in 1..R} binary; # Binary, 1 if course c is in room r

set NotAllowed within {c in 1..C, r in 1..R};
set FixedCourses within {c in 1..C, r in 1..R};

minimize TotalRooms: sum{c in 1..C, r in 1..R} x[c,r]; # Minimize used rooms

s.t. MinRooms{c in 1..C}: sum{r in 1..R} x[c,r] >= 1;

s.t. TotalSeats{c in 1..C}: sum{r in 1..R} x[c,r] * S[r] >= N[c];

s.t. CoursePerRoom{r in 1..R}: sum{c in 1..C} x[c,r] <= 1;

s.t. NotA{(c,r) in NotAllowed }: x[c,r] = 0;

s.t. FixedC{(c,r) in FixedCourses}: x[c,r] = 1;

end;

# glpsol --math -m timetable_rooms.mod -d timetable_rooms_test1.dat --check --wlp timetable_rooms.lp
# gurobi_cl ResultFile=timetable_rooms.sol timetable_rooms.lp
