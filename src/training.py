from src.dataset import SuperResDataset, DummyDataset
from torch.utils.data import DataLoader
from src.model import SRCNN, DummySRCNN
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

def training(test_with_dummy = False):
    model = SRCNN()

    if test_with_dummy:
        model = DummySRCNN()

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    train_dataset = SuperResDataset()

    if test_with_dummy:
        train_dataset = DummyDataset()

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    num_epoch = 50

    if test_with_dummy:
        num_epoch = 2

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    for epoch in range(num_epoch):
        model.train()
        epoch_loss = 0
        for lr, hr in train_loader:
            lr = lr.to(device)
            hr = hr.to(device)

            # Upscale LR to HR
            lr_up = F.interpolate(lr, size=(hr.size(2), hr.size(3)), mode='bilinear', align_corners=False)

            optimizer.zero_grad()
            sr = model(lr_up)
            loss = criterion(sr, hr)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"Epoch: {epoch+1}/{num_epoch}, Loss: {epoch_loss/len(train_loader):.6f}")