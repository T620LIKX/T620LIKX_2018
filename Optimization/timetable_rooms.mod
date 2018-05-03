param C >=0 integer;
param R >=0 integer;

param N {c in 1..C};
param S {r in 1..R};

var x{c in 1..C, r in 1..R} binary;

set NotAllowed within {c in 1..C, r in 1..R};

minimize TotalRooms: sum{c in 1..C, r in 1..R} x[c,r];

s.t. MinRooms{c in 1..C}: sum{r in 1..R} x[c,r] >= 1;

s.t. TotalSeats{c in 1..C}: sum{r in 1..R} x[c,r] * S[r] >= N[c];

s.t. CoursePerRoom{r in 1..R}: sum{c in 1..C} x[c,r] <= 1;

s.t. NotA{(c,r) in NotAllowed }: x[c,r] = 0;

end;

# glpsol --math -m timetable_rooms.mod -d timetable_rooms_test1.dat --check --wlp timetable_rooms.lp
# gurobi_cl ResultFile=timetable_rooms.sol timetable_rooms.lp
