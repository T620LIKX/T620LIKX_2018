/*Proftafla stofa*/

param C >= 0 integer; #fj afanga (1,2....C)
param R >= 0 integer; #fj skolastofa (1,2...R)

param F {c in 1..C}; #fj nemenda i afanga c
param S {r in 1..R}; #fj exam saeta i stofu r
param K {r in 1..R}; #fj afanga sem komast i stofu r
param P {c in 1..C}; #plass sem afangi c tekur

param alfa >= 0 integer; #fasti fyrir markfall
param beta >= 0 integer; #fasti fyrir markfall 

set NotAllowed within {c in 1..C, r in 1..R}; #prof sem mega ekki vera i akv stofu

var x{c in 1..C, r in 1..R} >=0 integer; 
var y{c in 1..C, r in 1..R} binary;
var z{r in 1..R} binary;

minimize Distribution: alfa * sum{r in 1..R} z[r] + beta * sum{c in 1..C, r in 1..R} (y[c,r]);

s.t. Stofa {c in 1..C}: sum{r in 1..R} x[c,r] = F[c];

s.t. Saeti {c in 1..C, r in 1..R}: x[c,r] <= S[r] * y[c,r];

s.t. NotAllowedConstr{ (c,r) in NotAllowed }: y[c,r] = 0;

s.t. PassaISaeti {r in 1..R}: sum{c in 1..C} x[c,r] <= S[r];

s.t. StofaNotud {c in 1..C, r in 1..R}: y[c,r] <= z[r];

s.t. Takmarka {r in 1..R}: sum{c in 1..C} P[c] * y[c,r] <= K[r];

s.t. TakmarkaAfanga {c in 1..C, r in 1..R}: x[c,r] >= 0.25 * S[r] * y[c,r];

s.t. TakmarkaNemendur {c in 1..C, r in 1..R}: x[c,r] >= 0.1 * F[c] * y[c,r];

end;
