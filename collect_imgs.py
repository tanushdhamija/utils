import os
import sys
import shutil
import random

def main(folder, label, n_files=500):

	img_folder = os.path.join(folder, 'images')
	label_folder = os.path.join(folder, 'labels')
	if not os.path.exists('temp'):
		os.makedirs('temp')

	annotations = os.listdir(label_folder)
	random.shuffle(annotations)

	count = 0
	for file in annotations:
		if count >= n_files:
			break
		with open(os.path.join(label_folder,file), 'r') as f:
			lines = f.readlines()
		annos = [line.strip() for line in lines]
		ids = [anno.split(' ')[0] for anno in annos]
		if label in ids:
			count += 1
			img = os.path.splitext(file)[0] + ".jpg"
			img = os.path.join(img_folder, img)
			shutil.copy(img, 'temp')
	print(f"collected {len(os.listdir('temp'))}/{n_files} files of class id {label} and saved at ./temp")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv[0]} </path/to/annotations/folder> <label to find>")
        sys.exit(1)

    main(*sys.argv[1:])
