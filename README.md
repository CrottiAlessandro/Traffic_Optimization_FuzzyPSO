# Traffic_Optimization_FuzzyPSO

In this project done in 2022 during my Engineering Physics degree, I've tried to implement a traffic simulation where I've studied the ripple effect of traffic congestion. This occurs when a vehicle brakes sharply or slows significantly in a congested roadway, causing a chain reaction of sudden slowdowns or stops behind it.

The code is written in Python, and this simulation was conducted using the 'pygame' library. This library allowed me to create a virtual environment where I could create a one-dimensional road where each rectangle represents a car.
I set parameters such as the maximum speed and the safety distance between vehicles, calculated as '(speed/10)^2'.

I implemented some controls:

Pressing the 'D' button allows a tagged car to brake.
Using the arrow keys, you can increase or decrease the safety distance by pressing 'UP' or 'DOWN'.

I included some alerts:
'CODA' appears when a car decreases its speed.
'ALERT' when the distance is less than the set safety distance.

Furthermore, I used the 'Fuzzy PSO' optimization method to optimize the model and find an efficient safety distance.
