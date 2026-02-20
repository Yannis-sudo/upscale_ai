import os
import sqlite3
import cv2#type:ignore
from src.utils import get_paths_json#type:ignore

def create_lr():
    # database connection
    conn = sqlite3.connect(get_paths_json()["images_db_path"])
    cursor = conn.cursor()

    scale_factor = 4    

    images_path = get_paths_json()["images_path"]

    images_hr= os.listdir(os.path.join(images_path, "hr"))
    images_lr = os.path.join(images_path, "lr")

    for image in images_hr:
        if image.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(os.path.join(images_path, "hr"), image)

            # check db
            cursor.execute("SELECT * FROM images WHERE path_hr = ? AND lr = ?", (image_path, "true", ))
            res = cursor.fetchall()
            if len(res) != 0:
                continue

            # load hr image
            hr = cv2.imread(image_path)

            lr_h = hr.shape[0] // scale_factor
            lr_w = hr.shape[1] // scale_factor

            lr = cv2.resize(hr, (lr_w, lr_h), interpolation=cv2.INTER_CUBIC)

            lr_path = os.path.join(images_lr, image)
            cv2.imwrite(lr_path, lr)

            # update db
            cursor.execute("UPDATE images SET path_lr = ?, lr = ? WHERE path_hr = ?", (lr_path, "true", image_path, ))

    conn.commit()
    conn.close()