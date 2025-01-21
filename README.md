# McCabe-Thiele Diagram and Column Design

This project implements a Python-based simulation to design a distillation column using the **McCabe-Thiele method**. It calculates key parameters like reflux ratios, number of stages, column diameter, and tray spacing, and visualizes the results with a diagram.

---

## Features

1. **Equilibrium Curve with Spline Interpolation**:
   - Smooth equilibrium data transitions for accurate stage calculations.

2. **Feed Line Customization**:
   - Includes support for saturated liquid feed (q=1) and other feed conditions.

3. **Reflux Ratio Calculations**:
   - Determines the minimum reflux ratio and scales it based on user-defined operating conditions.

4. **Stage Determination**:
   - Iterative calculation of McCabe-Thiele stages using equilibrium and operating lines.

5. **Column Design Calculations**:
   - Estimates the column diameter and tray spacing based on process specifications.

6. **Visualization**:
   - Generates a high-quality McCabe-Thiele diagram with equilibrium, operating, feed lines, and detailed stage steps.

---

## Getting Started

### Prerequisites
1. **Python 3.7+**
2. Required Libraries:
   - `numpy`
   - `matplotlib`
   - `scipy`

   Install dependencies using:
   ```bash
   pip install numpy matplotlib scipy
   ```

### How to Run
1. Save the script as `mccabe_thiele.py`.
2. Execute the script:
   ```bash
   python mccabe_thiele.py
   ```

3. Outputs:
   - McCabe-Thiele Diagram
   - Design summary in the console:
     - Minimum Reflux Ratio
     - Operating Reflux Ratio
     - Number of stages
     - Feed stage location
     - Column diameter

---

## Key Components

### Constants
- **Feed Mole Fraction (`xF`)**: Benzene composition in the feed stream.
- **Distillate and Bottoms Composition (`xD`, `xW`)**: Desired product purities.
- **Reflux Multiplier (`R_multiplier`)**: Defines the operating reflux ratio as a multiple of the minimum reflux ratio.
- **Feed Condition (`q`)**: Feed phase condition (e.g., saturated liquid `q=1`).
- **Column Dimensions**: Vapor density, velocity, and tray spacing.

### Outputs
- **McCabe-Thiele Diagram**:
  - Includes equilibrium curve, feed line, rectifying line, stripping line, and stages.
- **Column Design**:
  - Minimum and operating reflux ratios.
  - Number of theoretical stages.
  - Feed stage location.
  - Estimated column diameter.

---

## Example Output

### Console Summary
```
Minimum Reflux Ratio (R_min): 0.73
Operating Reflux Ratio (R): 1.10
Number of Stages: 8
Feed Stage: 4
Column Diameter: 0.78 m
Tray Spacing: 0.60 m
```

### McCabe-Thiele Diagram
A visual representation of the distillation process with annotated stages, feed, and operating lines.

---

## Customization
Modify the following constants to simulate different scenarios:
- **Feed Composition (`xF`)**
- **Product Purities (`xD`, `xW`)**
- **Operating Conditions (`q`, `R_multiplier`)**
- **Vapor Properties (`vapor_density`, `vapor_velocity`)
- **Tray Spacing (`tray_spacing`)

---

## License
This project is open-source and can be used for educational and professional purposes.
