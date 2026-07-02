import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from dataset import test_loader
from model import FootballPredictor

#load the data
model = FootballPredictor()

checkpoint = torch.load("../models/football_model.pth")

model.load_state_dict(
    checkpoint["model_state_dict"]
)

#Dropout off
model.eval()

#predicting on the test set
predictions = []
actual = []

with torch.no_grad():

    for features, labels in test_loader:

        outputs = model(features)

        preds = torch.argmax(outputs, dim=1)

        predictions.extend(preds.numpy())

        actual.extend(labels.numpy())
    

print("Accuracy:", accuracy_score(actual, predictions))

print("\nClassification Report\n")

print(classification_report(actual, predictions))

print("\nConfusion Matrix\n")

print(confusion_matrix(actual, predictions))
