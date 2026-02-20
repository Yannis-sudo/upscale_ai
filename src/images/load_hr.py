import os
import sqlite3
from src.utils import get_paths_json#type:ignore
import shutil

def load_images(path):
    if not os.path.exists(path):
        return

    # create connection
    conn = sqlite3.connect(get_paths_json()["images_db_path"])
    cursor = conn.cursor()

    files = os.listdir(path)
    for file in files:
        print(file)
        if not file.endswith((".png", ".jpg", ".jpeg")):
            continue

        # check db
        global new_filename
        new_filename = file

        cursor.execute("SELECT * FROM images WHERE filename = ?", (file, ))
        result = cursor.fetchall()
        if len(result) != 0:
            name, ext = os.path.splitext(file)
            new_file_name = 1
            while True:
                # check db
                filename_with_new = name + str(new_file_name) + ext
                cursor.execute("SELECT * FROM images WHERE filename = ?", (filename_with_new, ))
                result = cursor.fetchall()
                if len(result) == 0:
                    new_filename = filename_with_new
                    break
                else:
                    new_file_name = new_file_name + 1

        # add file to db
        # get images folder
        images_path = get_paths_json()["images_path"]
        new_path = os.path.join(images_path, "hr", new_filename)
        cursor.execute("INSERT INTO images (path, hr, lr, filename) VALUES (?, ?, ?, ?)", (new_path, "true", "false", new_filename, ))

        # copy file into hr folder
        old_path = os.path.join(path, file)
        shutil.copy(old_path, new_path)

    # close connection and save database
    conn.commit()
    conn.close()   
