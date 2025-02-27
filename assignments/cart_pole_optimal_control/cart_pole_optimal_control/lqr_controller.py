#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import time

class CartPoleLQRController(Node):
    def __init__(self):
        super().__init__('cart_pole_lqr_controller')
        
        # System parameters
        self.M = 1.0  # Mass of cart (kg)
        self.m = 1.0  # Mass of pole (kg)
        self.L = 1.0  # Length of pole (m)
        self.g = 9.81  # Gravity (m/s^2)
        
        # State space matrices
        self.A = np.array([
            [0, 1, 0, 0],
            [0, 0, (self.m * self.g) / self.M, 0],
            [0, 0, 0, 1],
            [0, 0, ((self.M + self.m) * self.g) / (self.M * self.L), 0]
        ])
        
        self.B = np.array([
            [0],
            [1/self.M],
            [0],
            [-1/(self.M * self.L)]
        ])
        
        # LQR cost matrices
        self.Q = np.diag([5.0, 5.0, 200.0, 20.0])  # State cost
        self.R = np.array([[0.1]])  # Control cost
        
        # Compute LQR gain matrix
        self.K = self.compute_lqr_gain()
        self.get_logger().info(f'LQR Gain Matrix: {self.K}')
        
        # Initialize state estimate
        self.x = np.zeros((4, 1))
        self.state_initialized = False
        self.last_control = 0.0
        self.control_count = 0
        
        # Data for plotting
        self.time_data = []
        self.cart_position_data = []
        self.cart_velocity_data = []
        self.pole_angle_data = []
        self.start_time = time.time()
        
        # Create publishers and subscribers
        self.cart_cmd_pub = self.create_publisher(
            Float64, 
            '/model/cart_pole/joint/cart_to_base/cmd_force', 
            10
        )
        
        # Verify publisher created successfully
        if self.cart_cmd_pub:
            self.get_logger().info('Force command publisher created successfully')
        
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/world/empty/model/cart_pole/joint_state',
            self.joint_state_callback,
            10
        )
        
        # Control loop timer
        self.timer = self.create_timer(0.01, self.control_loop)
        
        self.get_logger().info('Cart-Pole LQR Controller initialized')
    
    def compute_lqr_gain(self):
        """Compute the LQR gain matrix K."""
        P = linalg.solve_continuous_are(self.A, self.B, self.Q, self.R)
        K = np.linalg.inv(self.R) @ self.B.T @ P
        return K
    
    def joint_state_callback(self, msg):
        """Update state estimate from joint states."""
        try:
            # Get indices for cart and pole joints
            cart_idx = msg.name.index('cart_to_base')  # Cart position/velocity
            pole_idx = msg.name.index('pole_joint')    # Pole angle/velocity
            
            # State vector: [x, ẋ, θ, θ̇]
            self.x = np.array([
                [msg.position[cart_idx]],     # Cart position (x)
                [msg.velocity[cart_idx]],     # Cart velocity (ẋ)
                [msg.position[pole_idx]],     # Pole angle (θ)
                [msg.velocity[pole_idx]]      # Pole angular velocity (θ̇)
            ])
            
            # Record data for plotting
            current_time = time.time() - self.start_time
            self.time_data.append(current_time)
            self.cart_position_data.append(msg.position[cart_idx])
            self.cart_velocity_data.append(msg.velocity[cart_idx])
            self.pole_angle_data.append(msg.position[pole_idx])
            
            if not self.state_initialized:
                self.get_logger().info(f'Initial state: cart_pos={msg.position[cart_idx]:.3f}, cart_vel={msg.velocity[cart_idx]:.3f}, pole_angle={msg.position[pole_idx]:.3f}, pole_vel={msg.velocity[pole_idx]:.3f}')
                self.state_initialized = True
                
        except (ValueError, IndexError) as e:
            self.get_logger().warn(f'Failed to process joint states: {e}, msg={msg.name}')
    
    def control_loop(self):
        """Compute and apply LQR control."""
        try:
            if not self.state_initialized:
                self.get_logger().warn('State not initialized yet')
                return

            # Compute control input u = -Kx
            u = -self.K @ self.x
            force = float(u[0])
            
            # Log control input periodically
            if abs(force - self.last_control) > 0.1 or self.control_count % 100 == 0:
                self.get_logger().info(f'State: {self.x.T}, Control force: {force:.3f}N')
            
            # Publish control command
            msg = Float64()
            msg.data = force
            self.cart_cmd_pub.publish(msg)
            
            self.last_control = force
            self.control_count += 1
            
        except Exception as e:
            self.get_logger().error(f'Control loop error: {e}')
    
    def plot_data(self):
        """Plot cart position, cart velocity, and pole angle against time."""
        plt.figure(figsize=(12, 8))
        
        # Plot cart position
        plt.subplot(3, 1, 1)
        plt.plot(self.time_data, self.cart_position_data, label='Cart Position (m)')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.title('Cart Position vs Time')
        plt.legend()
        plt.grid()
        
        # Plot cart velocity
        plt.subplot(3, 1, 2)
        plt.plot(self.time_data, self.cart_velocity_data, label='Cart Velocity (m/s)', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Cart Velocity vs Time')
        plt.legend()
        plt.grid()
        
        # Plot pole angle
        plt.subplot(3, 1, 3)
        plt.plot(self.time_data, self.pole_angle_data, label='Pole Angle (rad)', color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('Angle (rad)')
        plt.title('Pole Angle vs Time')
        plt.legend()
        plt.grid()
        
        plt.tight_layout()
        plt.show()

def main(args=None):
    rclpy.init(args=args)
    controller = CartPoleLQRController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        # Plot data when the node is shut down
        controller.get_logger().info('Shutting down and plotting data...')
        controller.plot_data()
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
