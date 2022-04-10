# Amazon-Braket-Challenge
Optimization of single machine scheduling problems with sequence dependent setup times using QAOA

We implemented a variant of the TSP time dependant problem in the settings of industrial machine scheduling.
Our problem formulation as a QUBO was inspired from the formulation of a classical approach to this problem adressed in this paper: https://reader.elsevier.com/reader/sd/pii/S1572528608000339?token=4190C333EE1D0417E28EF3B3CC381CCD11A0A07BFCB19BFFE5AA0A4BB4E853CE7193C38223950861C2B070FF56F70ADE&originRegion=eu-west-1&originCreation=20220410140838

>Most of the research on scheduling problems has been done under the assumption that setup times are independent of job sequence.
>In this paper, we consider single machine scheduling problems in sequence dependent setup environments and we
>exhibit how these problems present similarities with the time-dependent traveling salesman problem, a variant of the
>famous traveling salesman problem in which transition costs between two cities now depends on the time of the visit.

Input to the problem is a time dependant graph where edges cost is defined for every time sequence.
Output after QAOA optimization is a final sequence corresponding to the optimal path (post processing of output is not yet finished in this work).

Presentation + mathematical formulation of QUBO:
https://www.canva.com/design/DAE9fiL-sXY/E_vaLztpOpVHRdeRpf0Iug/view?utm_content=DAE9fiL-sXY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

