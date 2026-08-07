import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle

# Load the dataset
data = pd.read_csv('Crop_recommendation.csv')

# Features and labels
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Create label mapping (crop name to number)
unique_labels = y.unique()
label_to_num = {label: idx for idx, label in enumerate(unique_labels)}
num_to_label = {idx: label for label, idx in label_to_num.items()}

# Save mapping to CSV
mapping_df = pd.DataFrame(list(label_to_num.items()), columns=['label', 'number'])
mapping_df.to_csv('label_name_number.csv', index=False)

# Encode labels
y_encoded = y.map(label_to_num)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and calculate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Model saved as model.pkl')
print('Label mapping saved as label_name_number.csv')

# Confusion Matrix
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Metrics
print("Precision: {:.2f}%".format(precision_score(y_test, y_pred, average='weighted') * 100))
print("Recall: {:.2f}%".format(recall_score(y_test, y_pred, average='weighted') * 100))
print("F1 Score: {:.2f}%".format(f1_score(y_test, y_pred, average='weighted') * 100))