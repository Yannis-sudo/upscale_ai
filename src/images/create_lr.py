import os
import sqlite3
import cv2#type:ignore

def create_lr():
    # database connection
    conn = sqlite3.connect("/home/yannis/dev/upscale_ai/data/db/images.db")
    cursor = conn.cursor()

    scale_factor = 4    

    images_hr= os.listdir("/home/yannis/dev/upscale_ai/data/images/hr")
    images_lr = "/home/yannis/dev/upscale_ai/data/images/lr"

    for image in images_hr:
        if image.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join("/home/yannis/dev/upscale_ai/data/images/hr", image)

            # check db
            cursor.execute("SELECT * FROM images WHERE path = ? AND lr = ?", (image_path, "true", ))
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
            cursor.execute("UPDATE images SET lr = ? WHERE path = ?", ("true", image_path, ))

    conn.commit()
    conn.close()