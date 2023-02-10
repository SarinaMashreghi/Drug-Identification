import os, shutil

root_dir = "packaging_images/bjy2svvmn8-1/"

classes = os.listdir(root_dir)
# print(root_dir)

train_root_dir = 'package_img/train/'
test_root_dir = 'package_img/test/'

# for dirpath, dirnames, filenames in os.walk(root_dir):
#     if len(filenames)!=0:
#         all_dirs.append(dirpath)

# print(all_dirs)

split_factor = 0.3
for c in classes:
    train_dest = train_root_dir +c

    all_files = os.listdir(root_dir+c)

    os.makedirs(train_dest)

    new_dir = root_dir + c + '/'
    # print('dir: ', train_dest)
    # print('filenames: ', all_files)
    for i in range(int(len(all_files)*(1-split_factor))):
        img_path = os.path.join(new_dir, all_files[i])
        move_im = shutil.copy(img_path, train_dest)

    test_dest = test_root_dir + '/' + c
    os.makedirs(test_dest)
    # print('dir: ', train_dest)
    # print('filenames: ', all_files)
    for i in range(int(len(all_files) * split_factor)):
        img_path = os.path.join(new_dir, all_files[i])
        move_im = shutil.copy(img_path, test_dest)

