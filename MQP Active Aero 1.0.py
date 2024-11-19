import numpy as np

# Constants for the system
MAX_BRAKE_PRESSURE = 100  # Max brake pressure in percentage
MAX_WING_ANGLE = 90  # Maximum wing angle in degrees (fully deployed at high speed)
ACTUATOR_MAX_EXTENSION = 100  # Maximum actuator extension in mm (fully extended)

#Speed threshold for air braking
MIN_AIR_BRAKING_SPEED = 50  # Air braking starts at 50 mph
MAX_SPEED = 120  # Speed in mph at which the wing fully deploys to 90 degrees

# Buffer zone for steering angle (±5 degrees)
STEERING_BUFFER_ZONE = 5  # Degrees




import numpy as np

# Constants for the system
MAX_BRAKE_PRESSURE = 100  # Max brake pressure in percentage
MAX_WING_ANGLE = 90  # Maximum wing angle in degrees (fully deployed at high speed)
ACTUATOR_MAX_EXTENSION = 100  # Maximum actuator extension in mm (fully extended)

# Speed threshold for air braking
MIN_AIR_BRAKING_SPEED = 50  # Air braking starts at 50 mph
MAX_SPEED = 120  # Speed in mph at which the wing fully deploys to 90 degrees

# Buffer zone for steering angle (±5 degrees)
STEERING_BUFFER_ZONE = 5  # Degrees

class ActiveAero:
    def __init__(self):
        self.brake_pressure = 0  # Initialize brake pressure (percentage)
        self.wing_angle = 0  # Initialize wing angle (degrees)
        self.actuator_extension = 0  # Initialize actuator extension (mm)
        self.speed = 0  # Vehicle speed in mph
        self.steering_angle = 0  # Steering angle (degrees)

    def set_brake_pressure(self, pressure):
        """Sets the brake pressure and updates the wing position based purely on brake pressure and speed."""
        if 0 <= pressure <= MAX_BRAKE_PRESSURE:
            self.brake_pressure = pressure
        else:
            print("Invalid brake pressure value. Must be between 0 and 100.")

    def set_speed(self, speed):
        """Sets the vehicle's speed in mph."""
        self.speed = speed
        print(f"Vehicle speed: {self.speed} mph")

    def set_steering_angle(self, angle):
        """Sets the steering angle. The wing will only reset if steering angle exceeds the buffer zone."""
        self.steering_angle = angle
        print(f"Steering angle: {self.steering_angle}°")
        if abs(self.steering_angle) > STEERING_BUFFER_ZONE:  # Wing resets only if steering exceeds buffer
            self.reset_wing()

    def reset_wing(self):
        """Resets the wing to its normal position (0 degrees) when steering is detected outside the buffer zone."""
        self.wing_angle = 0
        self.actuator_extension = 0
        print(f"Steering input detected! Wing reset to {self.wing_angle}° | Actuator extension: {self.actuator_extension} mm")

    def update_wing_position(self):
        """Updates the wing angle and actuator position based purely on brake pressure and speed, with air braking starting only at 50 mph or above."""
        if abs(self.steering_angle) <= STEERING_BUFFER_ZONE:  # Ensure wing only adjusts if steering is within buffer
            # Prevent air braking below 50 mph
            if self.speed < MIN_AIR_BRAKING_SPEED:
                self.wing_angle = 0
                self.actuator_extension = 0
                print(f"Speed below {MIN_AIR_BRAKING_SPEED} mph. No air braking.")
                return

            # Calculate maximum possible wing angle based on current speed
            max_speed_angle = min(MAX_WING_ANGLE, (self.speed / MAX_SPEED) * MAX_WING_ANGLE)
            
            # Calculate wing angle proportional to brake pressure, capped by speed
            self.wing_angle = (self.brake_pressure / MAX_BRAKE_PRESSURE) * max_speed_angle
            
            # Calculate actuator extension proportional to the wing angle
            self.actuator_extension = (self.wing_angle / MAX_WING_ANGLE) * ACTUATOR_MAX_EXTENSION
            
            print(f"Brake pressure: {self.brake_pressure}% | Wing angle: {self.wing_angle}° | Actuator extension: {self.actuator_extension} mm")

"""for wing angle stuff, were gonna have a potentiometer on the wing measuring the angle, redo this function at some point to make that make sense"""




class BrakeSystem:
    def __init__(self):
        # Initialize temperature sensors for four brakes (all in Celsius)
        self.brake_temperatures = {
            'front_left': 0,
            'front_right': 0,
            'rear_left': 0,
            'rear_right': 0
        }

    def set_brake_temperature(self, location, temperature):
        """Updates the brake temperature for a specific brake."""
        if location in self.brake_temperatures:
            self.brake_temperatures[location] = temperature
        else:
            print(f"Invalid brake location: {location}")

    def calculate_friction(self, temperature):
        """Calculates the brake friction based on the temperature using piecewise linear interpolation."""
        # Updated friction points based on the graph provided
        temperature_points = [100, 150, 200, 250, 300, 350]
        friction_points = [0.3, 0.6, 0.5, 0.4, 0.3, 0.2]
        
        # Use numpy interpolation to calculate friction at the given temperature
        if temperature < 100:
            return 0.3  # Set minimum friction for temperatures below 100°C
        elif temperature > 350:
            return 0.2  # Set minimum friction for temperatures above 350°C
        else:
            return np.interp(temperature, temperature_points, friction_points)

    def calculate_brake_efficiency(self):
        """Calculates the brake efficiency based on the highest brake temperature."""
        max_temp = max(self.brake_temperatures.values())  # Find the highest brake temperature
        friction = self.calculate_friction(max_temp)  # Calculate the corresponding friction
        return friction / 0.6  # Return efficiency scaled based on max friction (0.6 is 100% efficiency)

    def calculate_brake_power_remaining(self):
        """Calculates the braking power remaining as a percentage for each wheel."""
        remaining_power = {}
        for location, temperature in self.brake_temperatures.items():
            # Calculate friction for each wheel based on temperature
            friction = self.calculate_friction(temperature)
            # Max friction (0.6) is considered 100% braking power, so scale remaining power by this
            power_remaining = (friction / 0.6) * 100
            remaining_power[location] = power_remaining
        return remaining_power

    def display_brake_power_remaining(self):
        """Displays the remaining braking power for all wheels as a percentage."""
        remaining_power = self.calculate_brake_power_remaining()
        for location, power in remaining_power.items():
            print(f"{location.capitalize()} braking power remaining: {power:.2f}%")

        # Convert temperatures to Fahrenheit for display
        print("\nBrake Temperatures in Fahrenheit:")
        for location, temperature in self.brake_temperatures.items():
            temp_f = celsius_to_fahrenheit(temperature)
            print(f"{location.capitalize()} brake temperature: {temp_f:.2f}°F")

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32





"""""
# Example Cases for BrakeSystem
if __name__ == "__main__":
    brake_system = BrakeSystem()

    # Set temperatures for brakes in Celsius
    brake_system.set_brake_temperature('front_left', 150)  # 150°C
    brake_system.set_brake_temperature('front_right', 250)  # 250°C
    brake_system.set_brake_temperature('rear_left', 300)  # 300°C
    brake_system.set_brake_temperature('rear_right', 350)  # 350°C

    # Display braking power remaining and temperatures in Fahrenheit
    brake_system.display_brake_power_remaining()
"""""
# test cases for brake system
def test_brake_system():
    brake_system = BrakeSystem()

    print("\n--- Test Case 1: Set brake temperature for all brakes ---")
    brake_system.set_brake_temperature('front_left', 150)  # 150°C
    brake_system.set_brake_temperature('front_right', 250)  # 250°C
    brake_system.set_brake_temperature('rear_left', 300)  # 300°C
    brake_system.set_brake_temperature('rear_right', 350)  # 350°C
    brake_system.display_brake_power_remaining()
    # Expected: Brake temperatures should be updated, and brake power should be displayed for all wheels

    print("\n--- Test Case 2: Calculate friction for a specific temperature (within range) ---")
    friction = brake_system.calculate_friction(200)  # 200°C
    print(f"Friction at 200°C: {friction}")
    # Expected: Friction value should be interpolated between 0.5 and 0.4

    print("\n--- Test Case 3: Calculate friction for a temperature below minimum threshold ---")
    friction = brake_system.calculate_friction(50)  # 50°C
    print(f"Friction at 50°C: {friction}")
    # Expected: Friction should be set to 0.3 (minimum friction)

    print("\n--- Test Case 4: Calculate friction for a temperature above maximum threshold ---")
    friction = brake_system.calculate_friction(400)  # 400°C
    print(f"Friction at 400°C: {friction}")
    # Expected: Friction should be set to 0.2 (maximum friction beyond 350°C)

    print("\n--- Test Case 5: Calculate brake efficiency based on the highest temperature ---")
    brake_system.set_brake_temperature('front_left', 150)  # Reset temperatures
    brake_system.set_brake_temperature('front_right', 300)  # Highest temperature
    efficiency = brake_system.calculate_brake_efficiency()
    print(f"Brake efficiency: {efficiency}")
    # Expected: Efficiency should be calculated based on the highest brake temperature (300°C)

    print("\n--- Test Case 6: Calculate brake power remaining for all brakes ---")
    brake_system.set_brake_temperature('front_left', 100)  # Reset all temperatures to test power
    brake_system.set_brake_temperature('front_right', 150)
    brake_system.set_brake_temperature('rear_left', 200)
    brake_system.set_brake_temperature('rear_right', 250)
    remaining_power = brake_system.calculate_brake_power_remaining()
    for location, power in remaining_power.items():
        print(f"{location.capitalize()} braking power remaining: {power:.2f}%")
    # Expected: Brake power remaining should be calculated for each wheel based on their friction

    print("\n--- Test Case 7: Handle invalid brake location ---")
    brake_system.set_brake_temperature('invalid_location', 200)  # Invalid location
    # Expected: Error message indicating invalid brake location

    print("\n--- Test Case 8: Display brake temperatures in Fahrenheit ---")
    brake_system.set_brake_temperature('front_left', 100)  # 100°C
    brake_system.set_brake_temperature('front_right', 200)  # 200°C
    brake_system.set_brake_temperature('rear_left', 300)  # 300°C
    brake_system.set_brake_temperature('rear_right', 350)  # 350°C
    brake_system.display_brake_power_remaining()
    # Expected: Temperatures should be displayed in Fahrenheit

    print("\n--- Test Case 9: Minimum friction calculation (below 100°C) ---")
    brake_system.set_brake_temperature('front_left', 50)  # 50°C
    power_remaining = brake_system.calculate_brake_power_remaining()['front_left']
    print(f"Front_left power remaining at 50°C: {power_remaining}%")
    # Expected: Friction at this temperature should be 0.3, corresponding to 50% braking power remaining

    print("\n--- Test Case 10: Maximum friction calculation (at 150°C) ---")
    brake_system.set_brake_temperature('front_left', 150)  # 150°C
    power_remaining = brake_system.calculate_brake_power_remaining()['front_left']
    print(f"Front_left power remaining at 150°C: {power_remaining}%")
    # Expected: Friction at this temperature should be 0.6, corresponding to 100% braking power remaining

    print("\n--- Test Case 11: Low friction calculation (above 350°C) ---")
    brake_system.set_brake_temperature('front_left', 400)  # 400°C
    power_remaining = brake_system.calculate_brake_power_remaining()['front_left']
    print(f"Front_left power remaining at 400°C: {power_remaining}%")
    # Expected: Friction at this temperature should be 0.2, corresponding to ~33.33% braking power remaining

# Run the test cases
if __name__ == "__main__":
    test_brake_system()

















# Test Cases for ActiveAero
def test_active_aero():
    print("\n--- Test Case 1: Set brake pressure and speed, no steering input (speed > 50 mph) ---")
    aero_system = ActiveAero()

    # Set the speed and brake pressure
    aero_system.set_speed(100)   # 100 mph
    aero_system.set_brake_pressure(70)  # 70% brake pressure
    aero_system.update_wing_position()
    # Expected: Wing angle should be proportional to brake pressure and speed, actuator should extend

    print("\n--- Test Case 2: Speed below 50 mph, no air braking ---")
    aero_system.set_speed(40)    # Speed below air braking threshold (40 mph)
    aero_system.set_brake_pressure(70)  # 70% brake pressure
    aero_system.update_wing_position()
    # Expected: No air braking should occur, wing angle should remain at 0°

    print("\n--- Test Case 3: Set steering angle within buffer zone (wing still active) ---")
    aero_system.set_steering_angle(3)   # Steering angle within buffer zone (3 degrees)
    aero_system.set_speed(100)   # Speed above air braking threshold
    aero_system.set_brake_pressure(70)  # 70% brake pressure
    aero_system.update_wing_position()
    # Expected: Wing should still respond since the steering angle is within the buffer zone

    print("\n--- Test Case 4: Set steering angle outside buffer zone (wing resets) ---")
    aero_system.set_steering_angle(7)  # Steering angle outside buffer zone (7 degrees)
    aero_system.set_brake_pressure(70)  # 70% brake pressure
    aero_system.update_wing_position()
    # Expected: Wing should reset to 0 degrees and actuator should reset

    print("\n--- Test Case 5: Full brake pressure and maximum speed (speed > 50 mph) ---")
    aero_system.set_speed(120)   # Max speed (120 mph)
    aero_system.set_steering_angle(0)  # Steering angle inside buffer zone (0 degrees)
    aero_system.set_brake_pressure(100)  # Max brake pressure (100%)
    aero_system.update_wing_position()   # Ensure wing position is updated
    # Expected: Wing should fully deploy to 90 degrees and actuator should fully extend

    print("\n--- Test Case 6: Low speed, high brake pressure (speed < 50 mph) ---")
    aero_system.set_speed(30)    # Low speed (30 mph)
    aero_system.set_brake_pressure(90)  # High brake pressure (90%)
    aero_system.update_wing_position()   # Ensure wing position is updated
    # Expected: No air braking, wing angle should remain at 0°

# Run the test cases
if __name__ == "__main__":
    test_active_aero()
