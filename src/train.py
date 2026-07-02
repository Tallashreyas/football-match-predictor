import torch
import torch.nn as nn

from dataset import train_loader
from model import FootballPredictor
from dataset import X_train

#model
model = FootballPredictor(input_size=X_train.shape[1])

#loss function
criterion = nn.CrossEntropyLoss()

#optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    weight_decay=1e-4
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=5
)

#training loop
epochs = 50
best_loss = float("inf")
for epoch in range(epochs):

    model.train()

    total_loss = 0

    for features, labels in train_loader:

        optimizer.zero_grad()

        outputs = model(features)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save(
            {
                "epoch": epoch + 1,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "loss": best_loss,
            },
            "../models/football_model.pth"
        )
        print(f"New best model! Loss: {avg_loss:.4f}")
    scheduler.step(avg_loss)
    print(
        f"Epoch {epoch+1:02d}/{epochs} | "
        f"Loss: {avg_loss:.4f} | "
        f"LR: {optimizer.param_groups[0]['lr']:.6f}"
    )


print("Model saved!")