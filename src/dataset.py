import pandas as pd
import torch
from torch.utils.data import Dataset,DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#read the dataset
df = pd.read_csv("../data/processed/features.csv")

#converting target to numbers for torch to use it
target_map = {
    "H": 0,
    "D": 1,
    "A": 2
}

df["target"] = df["target"].map(target_map)

#create fratures and labels
X = df.drop("target", axis=1)

y = df["target"]

#keeping 20% for test and staratify keeps same clas distribution
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#scaling the data
scaler = StandardScaler()

import joblib

joblib.dump(
    scaler,
    "../models/scaler.pkl"
)

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

#converting into pytorch dataset
class FootballDataset(Dataset):

    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y.values, dtype=torch.long)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
    

#creating dataset objects
train_dataset = FootballDataset(X_train, y_train)
test_dataset = FootballDataset(X_test, y_test)

#creating Data Loaders
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)


features, labels = next(iter(train_loader))


