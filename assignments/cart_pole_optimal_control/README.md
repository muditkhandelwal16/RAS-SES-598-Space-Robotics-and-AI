# Cart-Pole Optimal Control Assignment

![image](https://github.com/muditkhandelwal16/RAS-SES-598-Space-Robotics-and-AI/blob/main/assignments/cart_pole_optimal_control/cart_pole.png)
![image](https://github.com/muditkhandelwal16/RAS-SES-598-Space-Robotics-and-AI/blob/main/assignments/cart_pole_optimal_control/graph.png)

### **1. Summary** 
This report presents the implementation and evaluation of an optimal control strategy for a cart-pole system using a Linear Quadratic Regulator (LQR). The primary objective is to stabilize the inverted pendulum while maintaining the cart within allowable constraints. The controller was designed using system dynamics and tuned to achieve minimal deviations under disturbances. The system was tested in simulation, and results were analyzed using performance plots.

###  **2. LQR Controller Tuning**

The Linear Quadratic Regulator (LQR) was designed based on the state-space representation of the cart-pole system. The control input was computed as:

where K is the gain matrix obtained from solving the Riccati equation. The state vector x consists of:

Cart position

Cart velocity

Pole angle

Pole angular velocity

After multiple iterations of tuning, the final state cost matrix was selected as:

**Cost Matrices Q=[100, 50, 200, 50]**


The control effort cost  was chosen conservatively to ensure smooth actuation:



The chosen parameters provide a balance between rapid stabilization and minimal control effort, ensuring robustness against disturbances while avoiding excessive oscillations.
