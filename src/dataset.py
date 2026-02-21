from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
import src.utils as utils
import sqlite3

class SuperResDataset(Dataset):
    def __init__(self):
        self.lr_images = []
        self.hr_images = []
        self.load_images_to_array() # Load the images to lr_images and hr_images
        self.transform = transforms.ToTensor() # Transform images to tensor
    
    def __len__(self):
        return len(self.lr_images)

    def __getitem__(self, idx):
        lr = Image.open(self.lr_images[idx]).convert('RGB')
        hr = Image.open(self.hr_images[idx]).convert('RGB')
        return self.transform(lr), self.transform(hr)

    def load_images_to_array(self):
        # database connection
        conn = sqlite3.connect(utils.get_paths_json()["images_db_path"])
        cursor = conn.cursor()

        # load all images
        cursor.execute("SELECT * FROM images WHERE hr = ? AND lr = ? LIMIT 20000", ("true", "true", ))
        result = cursor.fetchall()

        for r in result:
            hr_path = r[1]
            lr_path = r[2]
            self.lr_images.append(lr_path)
            self.hr_images.append(hr_path)

        conn.close()