import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Define constants
xF = 0.4        # Mole fraction of benzene in feed
xD = 0.98       # Mole fraction of benzene in distillate
xW = 0.02       # Mole fraction of benzene in bottoms
R_multiplier = 1.5  # Operating reflux multiplier
q = 1.0         # Saturated liquid feed condition
column_pressure = 1  # Column operating pressure in atm
vapor_density = 2.0   # Approximate vapor density in kg/m^3
vapor_velocity = 0.8  # Allowable vapor velocity in m/s
tray_spacing = 0.6    # Tray spacing in meters

# Equilibrium Data (with smoother transitions via interpolation)
equilibrium_data = np.array([
    [0.1, 0.22],
    [0.2, 0.39],
    [0.3, 0.52],
    [0.4, 0.63],
    [0.5, 0.72],
    [0.6, 0.80],
    [0.7, 0.86],
    [0.8, 0.92],
    [0.9, 0.96]
])
x_eq = equilibrium_data[:, 0]
y_eq = equilibrium_data[:, 1]

# Interpolate the equilibrium curve with spline for smoother transitions
spl = interpolate.InterpolatedUnivariateSpline(x_eq, y_eq, k=3)
x_eq_smooth = np.linspace(0, 1, 500)
y_eq_smooth = spl(x_eq_smooth)

# Feed Line
def feed_line(xF, q):
    if q == 1:
        # Vertical feed line for saturated liquid feed
        x_feed = [xF, xF]
        y_feed = [0, 1]
    else:
        slope = q / (q - 1)
        intercept = -xF / (q - 1)
        x_feed = np.linspace(0, 1, 100)
        y_feed = slope * x_feed + intercept
    return x_feed, y_feed

x_feed, y_feed = feed_line(xF, q)

# Minimum Reflux Ratio (R_min)
def find_intersection(x_eq, y_eq, xF, xD):
    for i in range(len(x_eq)):
        if y_eq[i] > xF:
            return x_eq[i], y_eq[i]

xiE, yiE = find_intersection(x_eq, y_eq, xF, xD)
R_min = (xD - yiE) / (yiE - xiE)

# Operating Reflux Ratio
R = R_multiplier * R_min

# Rectifying Line
def rectifying_line(xD, R):
    slope = R / (R + 1)
    intercept = xD / (R + 1)
    x_rect = np.linspace(0, xD, 100)
    y_rect = slope * x_rect + intercept
    return x_rect, y_rect

x_rect, y_rect = rectifying_line(xD, R)

# Stripping Line
def stripping_line(xW, xiF, yiF):
    slope = (yiF - xW) / (xiF - xW)
    intercept = xW - slope * xW
    x_strip = np.linspace(xW, xiF, 100)
    y_strip = slope * x_strip + intercept
    return x_strip, y_strip

xiF = (xF / (q - 1) + xD / (R + 1)) / (q / (q - 1) - R / (R + 1)) if q != 1 else xF
yiF = R / (R + 1) * xiF + xD / (R + 1)
x_strip, y_strip = stripping_line(xW, xiF, yiF)

# McCabe-Thiele Stages
def binary_search_interpolate(y_target, x_eq, y_eq):
    """
    Perform a binary search to find x corresponding to y_target on the equilibrium curve.
    Assumes y_eq is sorted in ascending order.
    """
    low, high = 0, len(y_eq) - 1
    while low <= high:
        mid = (low + high) // 2
        if y_eq[mid] < y_target:
            low = mid + 1
        elif y_eq[mid] > y_target:
            high = mid - 1
        else:
            return x_eq[mid]  # Exact match

    # Linear interpolation between neighbors
    if low == 0:
        return x_eq[0]
    elif low >= len(y_eq):
        return x_eq[-1]
    else:
        x1, y1 = x_eq[low - 1], y_eq[low - 1]
        x2, y2 = x_eq[low], y_eq[low]
        return x1 + (y_target - y1) * (x2 - x1) / (y2 - y1)

stages = []
current_x = xD
tolerance = 1e-4  # Define a small tolerance to stop the loop when near xW
max_iterations = 1000  # Avoid infinite loops by setting a maximum iteration limit
iteration_count = 0

while current_x > xW + tolerance and iteration_count < max_iterations:
    iteration_count += 1

    # Determine the current_y using the appropriate line equation
    if current_x > xiF:
        current_y = R / (R + 1) * current_x + xD / (R + 1)  # Rectifying section
    else:
        current_y = (yiF - xW) / (xiF - xW) * (current_x - xW) + xW  # Stripping section

    # Add the current stage (rectifying/stripping line)
    stages.append((current_x, current_y))

    # Find the next_x from the equilibrium curve using binary search interpolation
    next_x = binary_search_interpolate(current_y, x_eq, y_eq)

    # Add the horizontal stage (equilibrium step)
    stages.append((next_x, current_y))

    # Update current_x for the next iteration
    if abs(current_x - next_x) < tolerance:  # Convergence check
        break
    current_x = next_x

# Check if the loop reached the maximum iterations
if iteration_count >= max_iterations:
    print("Warning: Maximum iterations reached before convergence.")

# Column Diameter Calculation (more accurate flow rate assumptions)
volumetric_flow_rate = 100 / 3600  # Convert feed flow rate (100 kmol/h) to m^3/s
column_diameter = np.sqrt(4 * volumetric_flow_rate / (np.pi * vapor_velocity))

# Plotting
plt.figure(figsize=(12, 8), dpi=300)
plt.plot([0, 1], [0, 1], 'k-', label="y=x", linewidth=1.5)  # Diagonal line
plt.plot(x_eq_smooth, y_eq_smooth, 'r-', label="Equilibrium Curve", linewidth=2)  # Smooth equilibrium curve
plt.plot(x_feed, y_feed, 'k--', label="Feed Line", linewidth=2)  # Feed line (dashed)
plt.plot(x_rect, y_rect, 'g--', label="Rectifying Section", linewidth=2)  # Rectifying section
plt.plot(x_strip, y_strip, 'b--', label="Stripping Section", linewidth=2)  # Stripping section

# Add small circles at equilibrium curve points
plt.scatter(x_eq, y_eq, color='r', s=40, label="Equilibrium Points")

# Plot stages with distinct symbols at each step
for i in range(0, len(stages) - 1, 2):
    # Connect stage points (horizontal + vertical steps)
    plt.plot([stages[i][0], stages[i + 1][0]], [stages[i][1], stages[i + 1][1]], 'b-', linewidth=1.5)
    # Add small circles at stage points
    plt.scatter([stages[i][0], stages[i + 1][0]], [stages[i][1], stages[i + 1][1]], color='b', s=40)

# Annotations and settings
plt.xlabel("x (Mole Fraction of Benzene in Liquid)", fontsize=14)
plt.ylabel("y (Mole Fraction of Benzene in Vapor)", fontsize=14)
plt.title("McCabe-Thiele Diagram", fontsize=16)
plt.legend(loc="upper left", fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Output Design Summary
print(f"Minimum Reflux Ratio (R_min): {R_min:.2f}")
print(f"Operating Reflux Ratio (R): {R:.2f}")
print(f"Number of Stages: {len(stages) // 2}")
print(f"Feed Stage: {len([s for s in stages if s[0] > xiF])}")
print(f"Column Diameter: {column_diameter:.2f} m")
print(f"Tray Spacing: {tray_spacing} m")
