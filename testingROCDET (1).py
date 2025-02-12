import warnings
import numpy as np
import math
import random
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, det_curve, auc
import matplotlib.pyplot as plt

# This code is testing the ROC and DET curves for the SVM-based authentication method.
# The final version of this code can be found in FinalScoreFusion.py.


# Suppress warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn

# Load data
X = np.load("landmarks.npy")
y = np.load("identities.npy")
attributes = np.load("attributes.npy")


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

X_filtered = X[selected_indices]
y_filtered = y[selected_indices]
num_identities = y_filtered.shape[0]

# Euclidean distance function
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Extract features using a distance function
def extract_features(distance_function):
    features = []
    for k in range(num_identities):
        person_k = X_filtered[k]
        indices = np.triu_indices(person_k.shape[0])
        p1 = person_k[indices[0]]
        p2 = person_k[indices[1]]
        distances = np.array([distance_function(p1[i], p2[i]) for i in range(len(p1))])
        features.append(distances)
    return np.array(features)

# SVM-based authentication
def SupportVectorMachineAuthentication():
    distance_function = euclidean_distance
    C_value = 10

    query_X, template_X, query_y, template_y = train_test_split(
        extract_features(distance_function),
        y_filtered,
        test_size=0.33,
        random_state=42
    )

    genuine_scores = []
    imposter_scores = []

    for i in range(len(query_y)):
        query_sample_X = query_X[i, :]
        query_sample_y = query_y[i]

        if random.random() < 0.5:
            claimed_id = query_sample_y
            genuine = True
        else:
            possible_ids = template_y[template_y != query_sample_y]
            claimed_id = random.choice(possible_ids)
            genuine = False

        y_hat = np.zeros(len(template_y))
        y_hat[template_y == claimed_id] = 1
        y_hat[template_y != claimed_id] = 0

        if len(np.unique(y_hat)) < 2:
            continue

        clf = SVC(kernel='rbf', C=C_value, gamma="scale", class_weight="balanced")
        clf.fit(template_X, y_hat)

        # Use decision_function to get continuous scores
        decision_score = clf.decision_function(query_sample_X.reshape(1, -1))[0]

        if genuine:
            genuine_scores.append(decision_score)
        else:
            imposter_scores.append(decision_score)

    plot_roc_and_det(genuine_scores, imposter_scores)
    return

# Plot ROC and DET curves
def plot_roc_and_det(genuine_scores, imposter_scores):
    y_true = [1] * len(genuine_scores) + [0] * len(imposter_scores)
    y_scores = genuine_scores + imposter_scores

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    fnr, fpr_det, _ = det_curve(y_true, y_scores)

    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(10, 5))

    # ROC Curve
    plt.subplot(1, 2, 1)
    plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()

    # DET Curve
    plt.subplot(1, 2, 2)
    plt.plot(fpr_det, fnr, label="DET curve")
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("False Negative Rate (FNR)")
    plt.title("DET Curve")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    SupportVectorMachineAuthentication()
