from src.dataset import SuperResDataset
from torch.utils.data import DataLoader
from src.model import SRCNN

def training():
    train_dataset = SuperResDataset()
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
