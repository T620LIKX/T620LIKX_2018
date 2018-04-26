\ Model Giapetto
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3 C0 + 2 C1 + 5 C2
Subject To
 FinHours[0]: 2 C0 <= 100
 FinHours[1]: C1 <= 100
 FinHours[2]: 2 C2 <= 100
 CarpHours[0]: C0 <= 80
 CarpHours[1]: C1 <= 80
 CarpHours[2]: 2 C2 <= 80
 Demand[0]: C0 <= 40
 Demand[1]: C1 <= 500
 Demand[2]: C2 <= 200
Bounds
Generals
 C0 C1 C2
End
