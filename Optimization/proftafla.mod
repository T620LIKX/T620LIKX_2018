/*Proftafla*/

param C >= 0 integer; #Courses
param T >= 0 integer; #Time periods
param S >= 0 integer; #Classrooms
param P >= 0 integer; #refsing

set FixedCourses within {c in 1..C, t in 1..T};
set NotAllowed within {c in 1..C, t in 1..T};

param Courses{c in 1..C, c_hat in 1..C: c <> c_hat};

var x{c in 1..C, t in 1..T} binary; #ef áfangi c er á tímabili t
var z{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #ef áfangar skarast
var z_hat{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #ef það er ekki dagur/dagar á milli prófa

minimize TotalPunishment: sum{c in 1..C, c_hat in 1..C: c <> c_hat} z[c,c_hat] * Courses[c,c_hat] + sum{c in 1..C, c_hat in 1..C: c <> c_hat} z_hat[c,c_hat] * Courses[c,c_hat] + sum{c in 1..C, t in 1..T} x[c,t] * P;

s.t. Exams{c in 1..C}: sum{t in 1..T} x[c,t] = 1;

s.t. Overlap{t in 1..T, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t] <= 1 + z[c,c_hat];

s.t. DaysBetween{t in 1..(T-1), c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c,t+1] + x[c_hat,t] + x[c_hat,t+1] <= 1 + z_hat[c,c_hat]; 

s.t. NotAllow{ (c,t) in NotAllowed }: x[c,t]=1;

s.t. FixCourse{ (c,t) in FixedCourses }: x[c,t]=1;

s.t. ClassR{t in 1..T}: sum{c in 1..C} x[c,t] <= S;

end;