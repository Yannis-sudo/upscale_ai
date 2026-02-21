from src.dataset import SuperResDataset
from torch.utils.data import DataLoader
from src.model import SRCNN
import torch
import torch.optim as optim
import torch.nn as nn

def training():
    model = SRCNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    train_dataset = SuperResDataset()
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    num_epoch = 50
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    for epoch in range(num_epoch):
        model.train()
        epoch_loss = 0
        for lr, hr in train_loader:
            lr = lr.to(device)
            hr = hr.to(device)

            optimizer.zero_grad()
            sr = model(lr)
            loss = criterion(sr, hr)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"Epoch: {epoch+1}/{num_epoch}, Loss: {epoch_loss/len(train_loader):.6f}")