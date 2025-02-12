import warnings
import numpy as np
import math
import random
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, det_curve, auc, accuracy_score
import matplotlib.pyplot as plt

# This code is our final version of the Score-Level Fusion method for face recognition.
# It uses a combination of SVM and KNN classifiers to authenticate identities.


# HOW TO USE:
# Uncomment one of the following blocks to filter the data by a specific attribute or combination of attributes!!

# Suppress warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn

# Load data
X = np.load("landmarks.npy")
y = np.load("identities.npy")
attributes = np.load("attributes.npy")

'''
print("Accuracy overall")
attribute_index = [20, 20]
selected_indices = np.where((attributes[:, attribute_index] == 1) |
                            (attributes[:, attribute_index] == -1))[0]
'''

print("Accuracy of only male identities")
attribute_index = 20
selected_indices = np.where(attributes[:, attribute_index] == 1)[0]

'''
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

# Score-level fusion with SVM and KNN classifiers
def ScoreLevelFusion():
    distance_function = euclidean_distance
    C_value = 10 # Regularization parameter for SVM
    n_neighbors = 5  # Number of neighbors for KNN

    query_X, template_X, query_y, template_y = train_test_split(
        extract_features(distance_function),
        y_filtered,
        test_size=0.33,
        random_state=42
    )

    genuine_scores = []
    imposter_scores = []
    y_true = []
    y_pred = []

    for i in range(len(query_y)):
        query_sample_X = query_X[i, :]
        query_sample_y = query_y[i]

        if random.random() < 0.3:
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

        # Train SVM
        svm_clf = SVC(kernel='rbf', C=C_value, gamma="scale", class_weight="balanced", probability=True)
        svm_clf.fit(template_X, y_hat)
        svm_score = svm_clf.decision_function(query_sample_X.reshape(1, -1))[0]

        # Train KNN
        knn_clf = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn_clf.fit(template_X, y_hat)
        knn_score = knn_clf.predict_proba(query_sample_X.reshape(1, -1))[0][1]

        # Score-level fusion (weighted sum)
        fused_score = 0.5 * svm_score + 0.5 * knn_score

        if genuine:
            genuine_scores.append(fused_score)
            y_true.append(1)  # 1 for genuine
        else:
            imposter_scores.append(fused_score)
            y_true.append(0)  # 0 for imposter

        # Threshold-based prediction (0 is often used for decision boundary in SVM)
        y_pred.append(1 if fused_score > 0 else 0)

    # Calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # Plot ROC and DET curves
    plot_roc_and_det(genuine_scores, imposter_scores)


def plot_roc_and_det(genuine_scores, imposter_scores):
    y_scores = np.concatenate([genuine_scores, imposter_scores])
    y_true = np.concatenate([np.ones(len(genuine_scores)), np.zeros(len(imposter_scores))])

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    # DET Curve
    fnr, fpr_det, _ = det_curve(y_true, y_scores)

    plt.figure(figsize=(12, 6))

    # Plot ROC Curve
    plt.subplot(1, 2, 1)
    plt.plot(fpr, tpr, label='ROC curve (AUC = {:.2f})'.format(roc_auc), color='blue')
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()

    # Plot DET Curve with logarithmic scale
    plt.subplot(1, 2, 2)
    plt.plot(fpr_det, fnr, label='DET curve', color='red')
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('False Negative Rate (FNR)')
    plt.title('DET Curve')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ScoreLevelFusion()
