import os
import random
import sys
from PIL import Image
import imagehash


def find_similar_images(image_directory, hash_length):
    image_paths = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if len(image_paths) == 0:
        sys.exit(f'no images found in directory {image_directory}')

    similar_images = {}
    for img_path in image_paths:
        img = Image.open(img_path)
        img_hash = imagehash.phash(img, hash_size=hash_length)
        
        if img_hash in similar_images:
            similar_images[img_hash].append(img_path)
        else:
            similar_images[img_hash] = [img_path]

    return similar_images, len(image_paths)


def remove_similar_images(image_directory, hash_length):
    if not os.path.exists(image_directory):
        sys.exit(f'directory {image_directory} does not exist.')

    print(f'using hash size: {hash_length}\n.\n.\n.')
    similar_images, total_imgs = find_similar_images(image_directory, int(hash_length))
    removed = 0
    for img_paths in similar_images.values():
        if len(img_paths) > 1:
            # randomly choose one image to keep
            img_to_keep = random.choice(img_paths)
            img_paths.remove(img_to_keep)
            # remove the rest
            for img in img_paths:
                os.remove(img)
            removed += len(img_paths)

    # print info
    print(f'imgs removed: {removed}(out of {total_imgs}) - {round(removed/total_imgs *100,1)}%')
    print(f'imgs remaining: {len(os.listdir(image_directory))}')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f'usage: python3 {sys.argv[0]} </path/to/images> <hash_length>')

    remove_similar_images(*sys.argv[1:])
