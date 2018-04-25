/*Proftafla*/

param C >= 0 integer; #Courses
param T >= 0 integer; #Time periods
param S >= 0 integer; #Classrooms
param P >= 0 integer; #refsing
param N >= 0 integer; #Hámarksfjöldi nemenda fyrir hvert timabil
param FjoldiNemenda {c in 1..C};

set FixedCourses within {c in 1..C, t in 1..T};
set NotAllowed within {c in 1..C, t in 1..T};

param Courses{c in 1..C, c_hat in 1..C: c <> c_hat};

var x{c in 1..C, t in 1..T} binary; #ef áfangi c er á tímabili t

var z1{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #ef áfangar skarast sama tíma 1.
var z2{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #ef áfangar skarast sama dag 2.
var z3{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #áfangar skarast ekkert tímabil á milli 3.
var z4{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #áfangar skarast eitt tímabil á milli 4.HH
var z5{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #áfangar skarast eitt tímabil á milli 5.MM
var z6{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #áfangar skarast tvö tímabil á milli 6.
var z_hat{c in 1..C, c_hat in 1..C: c <> c_hat} binary; #ef það er ekki dagur/dagar á milli prófa


minimize TotalPunishment: sum{c in 1..C, c_hat in 1..C: c <> c_hat} (P * z1[c,c_hat] * Courses[c,c_hat] + P * z2[c,c_hat] * Courses[c,c_hat]) + sum{c in 1..C, t in 1..T} x[c,t] * P;


s.t. Exams{c in 1..C}: sum{t in 1..T} x[c,t] = 1;

s.t. Overlap1{t in 1..T, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t] <= 1 + z1[c,c_hat];

s.t. Overlap2a{t in {1,3,5,7,8,11,13,15,17,19}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t+1] <= 1 + z2[c,c_hat];
s.t. Overlap2b{t in {1,3,5,7,8,11,13,15,17,19}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c_hat,t] + x[c,t+1] <= 1 + z2[c,c_hat];

s.t. Overlap3a{t in {2,4,6,8,12,14,16,18}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t+1] <= 1 + z3[c,c_hat];
s.t. Overlap3b{t in {2,4,6,8,12,14,16,18}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c_hat,t] + x[c,t+1] <= 1 + z3[c,c_hat];

s.t. Overlap4a{t in {2,4,6,8,12,14,16,18}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t+2] <= 1 + z4[c,c_hat];
s.t. Overlap4b{t in {2,4,6,8,12,14,16,18}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c_hat,t] + x[c,t+2] <= 1 + z4[c,c_hat];

s.t. Overlap5a{t in {1,3,5,7,11,13,15,17}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t+2] <= 1 + z5[c,c_hat];
s.t. Overlap5b{t in {1,3,5,7,11,13,15,17}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c_hat,t] + x[c,t+2] <= 1 + z5[c,c_hat];

s.t. Overlap6a{t in {1,3,5,7,11,13,15,17}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c_hat,t+3] <= 1 + z6[c,c_hat];
s.t. Overlap6b{t in {1,3,5,7,11,13,15,17}, c in 1..C, c_hat in 1..C: c <> c_hat}: x[c_hat,t] + x[c,t+3] <= 1 + z6[c,c_hat];

s.t. DaysBetween{t in 1..(T-1), c in 1..C, c_hat in 1..C: c <> c_hat}: x[c,t] + x[c,t+1] + x[c_hat,t] + x[c_hat,t+1] <= 1 + z_hat[c,c_hat];

s.t. NotAllow{ (c,t) in NotAllowed }: x[c,t]=1;

s.t. FixCourse{ (c,t) in FixedCourses }: x[c,t]=1;

s.t. ClassR{t in 1..T}: sum{c in 1..C} x[c,t] <= S;

s.t. MaxNemfjoldi{t in 1..T}: sum{c in 1..C} x[c,t] * FjoldiNemenda[c] <= N;

end;