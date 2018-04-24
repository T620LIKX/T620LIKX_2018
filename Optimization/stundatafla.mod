param T >=0 integer;
param C >=0 integer;

param K {c1 in 1..C, c2 in 1..C: c1 <> c2};
param P {c in 1..C, t in 1..T} ;
param S >=0 integer;

set LargeCourse100 within {c in 1..C};
set LargeCourse80 within {c in 1..C};
set LargeCourse60 within {c in 1..C};

param Course100Limit;
param Course80Limit;
param Course60Limit;

#set FixedCourses within {c in 1..C, t in 1..T};

var x{c in 1..C, t in 1..T} binary;
var y{c1 in 1..C, c2 in 1..C} binary;

minimize TotalConflicts: sum{c1 in 1..C, c2 in 1..C: c1<>c2} K[c1, c2] * y[c1,c2]
+ sum{c in 1..C, t in 1..T} P[c,t] * x[c,t];

s.t. PlanCoursesI{c in 1..C}: sum{t in 1..T/2} x[c,t] = 1;
s.t. PlanCoursesII{c in 1..C}: sum{t in (T/2 + 1)..T} x[c,t] = 1;
s.t. NoConflicts{t in 1..T,c1 in 1..C, c2 in 1..C:c1<>c2}: x[c1,t] + x[c2,t] <= 1 + y[c1,c2];
s.t. RoomsAv{t in 1..T}: sum{c in 1..C} x[c,t] <= S;
#s.t. FixCourse{(c,t) in FixedCourses }: x[c,t] = 1;

s.t. S100{t in 1..T}: sum{c in LargeCourse100} x[c,t] <= Course100Limit;
s.t. S80{t in 1..T}: sum{c in LargeCourse80} x[c,t] <= Course80Limit;
s.t. S60{t in 1..T}: sum{c in LargeCourse60} x[c,t] <= Course60Limit;


end;

# glpsol --math -m glpkdemo.mod -d glpkdemo.dat --check --wlp glpkdemo.lp
# gurobi_cl ResultFile=glpkdemo.sol glpkdemo.lp

