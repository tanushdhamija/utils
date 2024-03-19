import os
import sys
import shutil
import random

IMGS_TO_COLLECT = None

def main(folder, *labels):

	img_folder = os.path.join(folder, 'images')
	label_folder = os.path.join(folder, 'labels')
	save_folder = os.path.join(folder, 'temp')

	if not os.path.exists(save_folder):
		os.makedirs(save_folder)

	annotations = os.listdir(label_folder)
	random.shuffle(annotations)

	count = 0
	for file in annotations:
		if IMGS_TO_COLLECT is not None:
			if count >= IMGS_TO_COLLECT:
				break

		with open(os.path.join(label_folder,file), 'r') as f:
			lines = f.readlines()
		annos = [line.strip() for line in lines]
		ids = [anno.split(' ')[0] for anno in annos]
		
		found = [True if label in ids else False for label in labels]
		if True in found:
			count += 1
			img = os.path.splitext(file)[0] + ".jpg"
			img = os.path.join(img_folder, img)
			shutil.copy(img, save_folder)

	if IMGS_TO_COLLECT is not None:
		print(f"\ncollected {count}/{IMGS_TO_COLLECT} images containing either class id: {labels} and saved at {save_folder}")
	else:
		print(f"\ncollected {count} images containing either class id: {labels} and saved at {save_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"usage: python3 {sys.argv[0]} </path/to/annotations/folder> <labels to find separated by space>")

    main(*sys.argv[1:])
