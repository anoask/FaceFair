import numpy as np
# This code takes our reduced dataset and converts it to NumPy arrays for use in the SVM-based authentication method.


# Path to the output text file from the previous step
input_file_path = "/Users/jluke/Desktop/FacialShit/reducedSet.txt"

# Lists to store the landmarks, identities, and attributes
landmarks_list = []
identities_list = []
attributes_list = []

# Step 1: Read the input file and parse the data
with open(input_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        attributes = list(map(int, parts[1:41]))       # Convert attributes to integers
        landmarks = list(map(int, parts[41:51]))       # Convert landmarks to integers
        identity = int(parts[51])                      # Identity as integer
        
        # Convert the flat list of landmarks to a list of (x, y) coordinate pairs
        landmark_pairs = [[landmarks[i], landmarks[i + 1]] for i in range(0, len(landmarks), 2)]
        
        attributes_list.append(attributes)
        landmarks_list.append(landmark_pairs)
        identities_list.append(identity)

# Step 2: Convert lists to NumPy arrays
landmarks_array = np.array(landmarks_list)
identities_array = np.array(identities_list)
attributes_array = np.array(attributes_list)

# Step 3: Save the arrays to .npy files
np.save("/Users/jluke/Desktop/mobile biometrics/landmarks.npy", landmarks_array)
np.save("/Users/jluke/Desktop/mobile biometrics/identities.npy", identities_array)
np.save("/Users/jluke/Desktop/mobile biometrics/attributes.npy", attributes_array)

print("Landmarks saved to 'landmarks.npy'")
print("Identities saved to 'identities.npy'")
print("Attributes saved to 'attributes.npy'")
