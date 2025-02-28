# Cart-Pole Optimal Control Assignment

### **1. Summary** 
The cart-pole system is a classic control problem in which a pole is balanced on a moving cart using a feedback control strategy. The goal of this project was to implement and optimize a Linear Quadratic Regulator (LQR) controller to ensure that the cart remains near the center while keeping the pole upright. The initial cost matrix for the state variables [x, x_dot, theta, theta_dot] was set to [1, 1, 10, 10]. Through an iterative tuning process, the cost matrix was optimized to [100, 50, 200, 50], significantly improving stability and minimizing deviations.

###  **2. LQR Controller Tuning**

The LQR controller was tuned iteratively to achieve optimal balance between the cart’s position and the pole’s stability. The methodology involved adjusting the state cost matrix Q, which penalizes deviations in the state variables, and the control cost R, which penalizes excessive control effort. The chosen control cost R was 0.1.

State Cost Matrix (Q):

x (cart position): High penalty to keep the cart near the center

x_dot (cart velocity): Moderate penalty to prevent excessive movement

theta (pole angle): High penalty to maintain the pole upright

theta_dot (pole angular velocity): Moderate penalty to limit angular oscillations

The optimization was performed iteratively by simulating the system and adjusting the cost matrix until a satisfactory balance between cart position and pole stability was achieved.

### **3. Graph Plotting**

```Python
def plot_data(self):
        """Plot cart position, velocity, pole angle, and control force over time."""
        plt.figure(figsize=(12, 8))
        
        # Plot cart position vs. time
        plt.subplot(2, 2, 1)
        plt.plot(self.time_data, self.cart_position_data, label='Cart Position (m)')
        plt.xlabel('Time (s)')
        plt.ylabel('Cart Position (m)')
        plt.title('Cart Position vs. Time')
        plt.grid()
        plt.legend()
        
        # Plot cart velocity vs. time
        plt.subplot(2, 2, 2)
        plt.plot(self.time_data, self.cart_velocity_data, label='Cart Velocity (m/s)', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Cart Velocity (m/s)')
        plt.title('Cart Velocity vs. Time')
        plt.grid()
        plt.legend()
        
        # Plot pole angle vs. time
        plt.subplot(2, 2, 3)
        plt.plot(self.time_data, self.pole_angle_data, label='Pole Angle (rad)', color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('Pole Angle (rad)')
        plt.title('Pole Angle vs. Time')
        plt.grid()
        plt.legend()
        
        # Plot control force vs. time
        plt.subplot(2, 2, 4)
        plt.plot(self.time_data, self.control_force_data, label='Control Force (N)', color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Control Force (N)')
        plt.title('Control Force vs. Time')
        plt.grid()
        plt.legend()
        
        plt.tight_layout()
        plt.show()
```
### **4. Result**
The final LQR-tuned controller successfully maintained the pole upright and restricted the cart movement near the center. The key performance metrics observed were:

Maximum pole angle deviation: ±0.035 rad

Maximum cart position deviation: +0.04 m and -0.045 m

These results demonstrate that the LQR controller effectively stabilized the system, achieving the objective of keeping the cart near the center while preventing the pole from falling.

**Plots**

These are graphs of Cart position, Pole angle, Cart velocity and Control force plotted against time.


![image](https://github.com/muditkhandelwal16/RAS-SES-598-Space-Robotics-and-AI/blob/main/assignments/cart_pole_optimal_control/graphs.png)


The plots illustrate the system response over time, showing minimal deviations in both cart position and pole angle. The LQR controller successfully ensured stability and controlled oscillations efficiently.
This is the simulation of the cart pole.
![image](https://github.com/muditkhandelwal16/RAS-SES-598-Space-Robotics-and-AI/blob/main/assignments/cart_pole_optimal_control/cart_pole.png)
