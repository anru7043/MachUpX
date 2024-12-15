"""
The purpose of this script is to demonstrate the functionality of MachUpX for modelling
a traditional (straight main wing, simple empennage) airplane. Run this script using:

$ python AMD_Plane.py

The input file is also written such that the same analyses will be performed if run using
the `python -m` command. This is done using:

$ python -m machupX AMD_Plane_input.json
"""

# Import necessary modules
import machupX as MX
import csv
import matplotlib.pyplot as plt
import numpy as np
import json

# Define the input file
input_file = "AMD_Plane_input.json"

# Define the output CSV file
output_csv = "exported_airfoil_with_forces.csv"

# Initialize the MachUpX scene
my_scene = MX.Scene(input_file)

# Function to export airfoil geometry with pressure forces
def export_airfoil_geometry_with_forces(scene, output_file):
    # Retrieve spanwise distributions for all components
    spanwise_data = scene.distributions(aircraft="AMD_Plane", non_dimensional=False)

    # Open the output file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(["Component", "x", "y", "z", "Fx", "Fy", "Fz"])

        # Loop through components (e.g., wings)
        for component_name, component_data in spanwise_data["AMD_Plane"].items():
            # Extract spanwise and chordwise data
            span_fracs = component_data["span_frac"]  # Spanwise fractions
            chordwise_x = component_data["cpx"]       # Chordwise x-coordinates
            chordwise_y = component_data["cpy"]       # Chordwise y-coordinates
            chordwise_z = component_data["cpz"]       # Chordwise z-coordinates
            force_x = component_data["Fx"]            # Force in x-direction
            force_y = component_data["Fy"]            # Force in y-direction
            force_z = component_data["Fz"]            # Force in z-direction

            # Write each spanwise section's data
            for i, span_frac in enumerate(span_fracs):
                for j in range(len(chordwise_x)):  # Loop through chordwise points
                    writer.writerow([
                        component_name,
                        chordwise_x[j],
                        chordwise_y[j],
                        chordwise_z[j],
                        force_x[i],
                        force_y[i],
                        force_z[i]
                    ])

    print(f"Airfoil geometry with forces exported to {output_file}.")

# Call the export function
export_airfoil_geometry_with_forces(my_scene, output_csv)

# Display the wireframe of the aircraft
print("Displaying wireframe...")
my_scene.display_wireframe(show_legend=True)

# Solve for total forces and moments acting on the aircraft
FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True)
print(json.dumps(FM_results["AMD_Plane"]["total"], indent=4))

# Perform pitch trim and display trim state
trim_state = my_scene.pitch_trim(set_trim_state=True, verbose=True)
print(json.dumps(trim_state["AMD_Plane"], indent=4))

# Compute and display aerodynamic derivatives
derivs = my_scene.derivatives()
print(json.dumps(derivs["AMD_Plane"], indent=4))

# Export geometry to files for 3D visualization
my_scene.export_stl(filename="AMD_Plane.stl")
my_scene.export_dxf(aircraft="AMD_Plane")

import machupX as MX
import pandas as pd

# Constants (replace these with actual values)
P_infinity = 101325  # Freestream pressure in Pascals
rho = 1.225  # Air density in kg/m³
V_infinity = 30  # Freestream velocity in m/s

# Load airfoil data
file_path = "naca0010-il.csv"  # Adjust to your file name
airfoil_data = pd.read_csv(file_path, names=["x", "y", "z", "Cp"], skiprows=1)  # Update columns if needed

# Ensure Cp values vary - Placeholder linear variation for example
# Replace this with actual Cp values from simulations
airfoil_data['Cp'] = 0.5 - 0.01 * airfoil_data['y']

# Calculate Pressure
airfoil_data["Pressure"] = P_infinity + 0.5 * rho * V_infinity**2 * (1 - airfoil_data["Cp"])

# Save updated data to CSV
output_file = "airfoil_with_pressure_distribution.csv"
airfoil_data.to_csv(output_file, index=False)
print(f"Updated file saved to {output_file}")

