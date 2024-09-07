# Execute these two lines in command line before run this python script.
# eval $(cryosparcm env)
# export PYTHONPATH="${CRYOSPARC_ROOT_DIR}"

import argparse
import numpy as np
from scipy.spatial.transform import Rotation
# dataset is the main module required to interact with cryoSPARC .cs files
from cryosparc_compute import dataset

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_dataset", help="path to the particle dataset in .cs format")

parser.add_argument("-o", "--output_dataset", help="path to save the result particle dataset")

parser.add_argument("-low", "--lower_angle", type=float, help="tilt angle lower bound which particles will be kept")

parser.add_argument("-up", "--upper_angle", type=float, help="tilt angle upper bound which particles will be kept")

args = parser.parse_args()
input_dataset = args.input_dataset
output_dataset = args.output_dataset
lower_angle = args.lower_angle
upper_angle = args.upper_angle

# Load particles as cs file
particle_dataset = dataset.Dataset.load(input_dataset)
# print(particle_dataset.fields)

# Load particles as numpy array
particle_array = np.load(input_dataset)
# alignment3D/pose is stored in the 4th column 
# print(particle_array.dtype[3])

# Check tilt angles, for satisfied particles, store the line index in a list
accept_rows = []
for i in range(0,len(particle_array)-1):
# Convert Axix-angle vector to ZYZ Euler angle
    # print(particle_array[i][3])
    # Define the axis-angle vector
    axis_angle_vector = particle_array[i][3]
    # Normalize the axis vector
    axis = axis_angle_vector / np.linalg.norm(axis_angle_vector)
    # Calculate the angle magnitude (radians)
    angle = np.linalg.norm(axis_angle_vector)
    # Create a rotation object from the axis-angle representation
    rotation = Rotation.from_rotvec(angle * axis)
    # Extract the ZYZ Euler angles
    euler_angles = rotation.as_euler('ZYZ', degrees=True)
    # Print the resulting Euler angles
    # print("ZYZ Euler angles (radians):", euler_angles)

    if lower_angle < euler_angles[1] < upper_angle:
        accept_rows.append(i)

print("total removed particles")
print(i+1 - len(accept_rows))

# Delete the corresponding rows in the array based on the condition
filtered_dataset = particle_dataset.take(accept_rows)

# Save the new particle dataset
filtered_dataset.save(output_dataset)
