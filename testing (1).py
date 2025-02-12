import warnings
import numpy as np
import math
import random
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, det_curve, auc
import matplotlib.pyplot as plt

# The code below is a testing script for the SVM-based authentication method.
# The final version of this code can be found in FinalScoreFusion.py.

# Suppress warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn

# Load data
X = np.load("landmarks.npy")  # Landmarks (features)
y = np.load("identities.npy")  # Identities (labels)
attributes = np.load("attributes.npy")  # Attributes

# HOW TO USE:
# Uncomment one of the following blocks to filter the data by a specific attribute or combination of attributes!!

print("Accuracy overall")
attribute_index = [20, 20]
selected_indices = np.where((attributes[:, attribute_index] == 1) |
                            (attributes[:, attribute_index] == -1))[0]

'''
print("Accuracy of only male identities")
attribute_index = 20
selected_indices = np.where(attributes[:, attribute_index] == 1)[0]


print("Accuracy of only female identities")
attribute_index = 20
selected_indices = np.where(attributes[:, attribute_index] == -1)[0]


print("Accuracy of only male with facial hair identities")
attribute_indices = [20, 0, 16, 22, 24]  # Indices of the attributes to filter by
selected_indices = np.where((attributes[:, 20] == 1) & 
                            ((attributes[:, 0] == 1) | 
                            (attributes[:, 16] == 1) |
                            (attributes[:, 22] == 1) |
                            (attributes[:, 24] == -1)))[0]


print("Accuracy of only male with no facial hair identities")
attribute_indices = [20, 0, 16, 22, 24]  # Indices of the attributes to filter by
selected_indices = np.where((attributes[:, 20] == 1) & 
                            ((attributes[:, 0] == -1) & 
                            (attributes[:, 16] == -1) &
                            (attributes[:, 22] == -1) &
                            (attributes[:, 24] == 1)))[0]


print("Accuracy of only female with makeup identities")
attribute_indices = [20, 36, 18]  # Indices of the attributes to filter by
selected_indices = np.where((attributes[:, 20] == -1) & 
                            ((attributes[:, 36] == 1) | 
                            (attributes[:, 18] == 1)))[0]


print("Accuracy of only female with no makeup identities")
attribute_indices = [20, 36, 18]  # Indices of the attributes to filter by
selected_indices = np.where((attributes[:, 20] == -1) & 
                            ((attributes[:, 36] == -1) & 
                            (attributes[:, 18] == -1)))[0]
'''

# Subset the landmarks and identities based on the selected indices
X_filtered = X[selected_indices]
y_filtered = y[selected_indices]
num_identities = y_filtered.shape[0]

# Euclidean distance function
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Extract features using a distance function
def extract_features(distance_function):
    features = []
    for k in range(num_identities):  # Iterate through each filtered identity
        person_k = X_filtered[k]  # Landmarks for person k
        
        # Create all unique pairs of indices (i, j) where i <= j
        indices = np.triu_indices(person_k.shape[0])
        
        # Extract corresponding points and calculate distances
        p1 = person_k[indices[0]]
        p2 = person_k[indices[1]]
        distances = np.array([distance_function(p1[i], p2[i]) for i in range(len(p1))])
        features.append(distances)

    return np.array(features)

# SVM-based authentication for the filtered data
def SupportVectorMachineAuthentication():
    # List of distance metrics to test
    distance_metrics = {
        "Euclidean Distance": euclidean_distance
    }
    # Fixed C value to test
    C_value = 10

    # Split the filtered data into 33% query and 67% template
    query_X, template_X, query_y, template_y = train_test_split(
        extract_features(euclidean_distance),  # Extracted features
        y_filtered,  # Corresponding identities
        test_size=0.33,
        random_state=42 
    )


    num_correct = 0
    num_incorrect = 0

    for i in range(len(query_y)):
        # Query sample
        query_sample_X = query_X[i, :]
        query_sample_y = query_y[i]  # True identity

        # Randomly decide between genuine or imposter case
        if random.random() < 0.25:  # 25% chance of being genuine
            claimed_id = query_sample_y  # Genuine case
        else:
            # Imposter case: Choose a claimed identity different from the true identity
            possible_ids = template_y[template_y != query_sample_y]
            claimed_id = random.choice(possible_ids)

        # Set labels for the template data: 1 for genuine, 0 for impostor
        y_hat = np.zeros(len(template_y))
        y_hat[template_y == claimed_id] = 1  # Genuine
        y_hat[template_y != claimed_id] = 0  # Impostor

        # ** Check if we have both classes (1 and 0) **
        if len(np.unique(y_hat)) < 2:
            # Skip iteration if only one class remains
            continue

        # Train the SVM classifier on the template set
        clf = SVC(kernel='rbf', C=C_value, gamma="scale", class_weight="balanced")
        clf.fit(template_X, y_hat)

        # Predict the label of the query sample
        y_pred = clf.predict(query_sample_X.reshape(1, -1))
        
        # Check the result
        if (y_pred == 1 and query_sample_y == claimed_id) or (y_pred == 0 and query_sample_y != claimed_id):
            num_correct += 1
        else:
            num_incorrect += 1

        # Print results for this C value
    accuracy = num_correct / (num_correct + num_incorrect)
    print(f"C = {C_value}, Num correct = {num_correct}, Num incorrect = {num_incorrect}, Accuracy = {accuracy:.2f}") # this will print our c value used, the number of correct and incorrect predictions, and the accuracy of our model

    return

    


if __name__ == "__main__":
    SupportVectorMachineAuthentication()
