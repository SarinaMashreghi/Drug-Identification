import shutil, os
import pandas as pd

dir = "pill_IMAGES/Training_set.csv"

df = pd.read_csv(dir)
labels = df['label']

class_names = list(labels.unique())
# print(class_names)

save_dir = 'pill_IMAGES/full_train/'
for c in class_names:
    dest = save_dir + c
    os.makedirs(dest)
    for i in list(df[df['label']==c]['filename'][:560]): # Image Id
        get_image = os.path.join('pill_IMAGES/train', i) # Path to Images
        move_image_to_cat = shutil.copy(get_image, dest)

    dest_test = save_dir + c
    os.makedirs(dest_test)
    for i in list(df[df['label']==c]['filename'][560:]): # Image Id
        get_image = os.path.join('pill_IMAGES/train', i) # Path to Images
        # print()
        move_image_to_cat = shutil.copy(get_image, dest_test)