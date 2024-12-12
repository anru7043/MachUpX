"""
The purpose of this script is to demonstrate the functionality of MachUpX for modelling
a traditional (straight main wing, simple empennage) airplane. Run this script using:

$ python AMD_Plane.py

The input file is also written such that the same analyses will be performed if run using
the `python -m` command. This is done using:

$ python -m machupX AMD_Plane_input.json
"""

## Import necessary modules
import machupX as MX
import csv

if __name__ == "__main__":
    # Define the input file
    input_file = "AMD_Plane_input.json"

    # Initialize Scene object
    my_scene = MX.Scene(input_file)

    # Solve for forces
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True)

    # Retrieve spanwise force distribution
    spanwise_data = my_scene.distributions(aircraft="AMD_Plane", non_dimensional=False)

    # Access data for the main wing
    wing_forces = spanwise_data["AMD_Plane"]["main_wing"]
    span_locations = wing_forces["span_locations"]
    sectional_lift = wing_forces["sectional_lift"]
    sectional_drag = wing_forces["sectional_drag"]

    # Export to CSV
    csv_file = "spanwise_force_distribution.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Span Location (ft)", "Sectional Lift (lb)", "Sectional Drag (lb)"])
        # Write data
        for i in range(len(span_locations)):
            writer.writerow([span_locations[i], sectional_lift[i], sectional_drag[i]])

    print(f"Spanwise force distribution exported to {csv_file}.")
