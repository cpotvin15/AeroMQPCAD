#Input Parameters
#   - Brake Light Switch (the switch that tells if the brake is pressed, can only be on or off)
#   - Steering angle (still need to figure out what sensor to use and how to mount it)
#   - Vehicle Speed 
#Things that we need to output
#   - Wing angle (calculated based on speed, more speed = more air braking) make this proportional to speed but also have it as a curve becuse of physics of air





#Active Aerodynamics System Code





# Necessary libraries
import math
import time

# Define Brake Light Switch status
brake_light_switch = False  # False means off, True means on

# Define the Steering Angle
steering_angle = 0.0  # in degrees

# Define the Vehicle Speed in mph
vehicle_speed = 0.0  # in miles per hour






# Function to calculate wing angle based on vehicle speed in mph
def calculate_wing_angle(speed):
    # Constants for aerodynamic calculations - these need to be tuned based on simulations
    min_angle = 0  # Minimum angle of the wing
    max_angle = 45  # Maximum angle of the wing for full air braking


    # Basic proportional control logic
    # We use a quadratic relationship to simulate increasing aerodynamic effect, adjusted for mph
    if speed < 6:  # Assuming minimal angle change at very low speeds 

        return min_angle
    else:
        # Conversion factor for mph to a scale that works with our earlier formula designed for kph
        # The conversion factor of (1.60934)^2 is used because the original speed squared formula is based on kph
        angle = ((speed / 62.137) ** 2) * max_angle  # 62.137 is the approximate equivalent of 100 kph in mph
        return min(angle, max_angle)  # Cap the angle to the maximum possible







# Function to update the wing angle based on braking and speed
def update_aero_controls(brake_switch, steering, speed):
    if brake_switch:
        # Apply full air braking if the brake is engaged
        return calculate_wing_angle(speed) + 10  # Add an offset for braking
    else:
        return calculate_wing_angle(speed)







# Main loop simulation (replace this with actual reading and writing logic in your vehicle control system)
def main_loop():
    global brake_light_switch, steering_angle, vehicle_speed

    while True:
        # Simulated sensor updates (replace with actual sensor reading logic)
        brake_light_switch = read_brake_light_switch()
        steering_angle = read_steering_angle()
        vehicle_speed = read_vehicle_speed()

        # Calculate the required wing angle
        wing_angle = update_aero_controls(brake_light_switch, steering_angle, vehicle_speed)

        # Output the wing angle to the actuator (replace with actual actuator control logic)
        set_wing_angle(wing_angle)

        # Delay for simulation purposes (remove or adjust in actual implementation)
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
