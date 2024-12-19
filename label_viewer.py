import cv2
import os
import sys
from random import randint
from PIL import Image
from screeninfo import get_monitors


def png_to_jpg(file):

    img = Image.open(file)
    if img.mode in ('RGBA', 'LA'):
        # convert RGBA to RGB if necessary
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background

    jpg_filename = os.path.splitext(file)[0] + ".jpg"
    img.convert('RGB').save(jpg_filename, 'JPEG', quality=95)
    img.close()
    os.remove(file)

    return jpg_filename


def get_screen_resolution():
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height
    return 1920, 1080 # fallback


def resize_image_to_screen(image):

    screen_width, screen_height = get_screen_resolution()
    original_height, original_width = image.shape[:2]
    
    if original_width > screen_width or original_height > screen_height:
        width_scale = screen_width / original_width
        height_scale = screen_height / original_height
        
        scale_factor = min(width_scale, height_scale)
        
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


def get_color():
    return [(randint(0,255),randint(0,255),randint(0,255)) for _ in range(len(CLASSES))]


def parse_annotation(annotation_file):

    with open(annotation_file, 'r') as f:
        annotations = f.readlines()

    parsed_annotations = []
    for annotation in annotations:
        class_id, x_center, y_center, width, height = map(float, annotation.split())
        parsed_annotations.append((int(class_id), x_center, y_center, width, height))
    
    return parsed_annotations


def draw_annotations(image, annotations):

    im_height, im_width, _ = image.shape
    for annotation in annotations:
        class_id, x_center, y_center, width, height = annotation
        x1 = int((x_center - width/2) * im_width)
        y1 = int((y_center - height/2) * im_height)
        x2 = int((x_center + width/2) * im_width)
        y2 = int((y_center + height/2) * im_height)

        cv2.rectangle(image, (x1, y1), (x2, y2), COLORS[class_id], 3)
        cv2.putText(image, f'{CLASSES[class_id]}', (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return image


def filter_by_class(image_folder, annotation_folder, classes):

    images = []
    annotations = []

    for file in os.listdir(image_folder):
        annos = parse_annotation(os.path.join(annotation_folder, f"{os.path.splitext(file)[0]}.txt"))
        classes_in_file = [CLASSES[anno[0]] for anno in annos]
        for c in classes_in_file:
            if c in classes:
                images.append(os.path.join(image_folder, file))
                annotations.append(os.path.join(annotation_folder, f"{os.path.splitext(file)[0]}.txt"))

    return images, annotations


def display_annotated_images(image_folder, annotation_folder, all=True):

    if all:
        # view all classes
        image_files = [os.path.join(image_folder, file) for file in sorted(os.listdir(image_folder))]
        annotation_files = [os.path.join(annotation_folder, file) for file in sorted(os.listdir(annotation_folder))]
    else:
        # view chosen class/es
        classes_to_view = ["open_damage_boxes"]
        image_files, annotation_files = filter_by_class(image_folder, annotation_folder, classes=classes_to_view)

    if len(image_files) != len(annotation_files): 
        sys.exit(f"ERROR: mismatch in no. of images & labels (images: {len(image_files)}, labels: {len(annotation_files)})")

    current_index = 0
    while current_index < len(annotation_files):

        image_file = image_files[current_index]
        if image_file.lower().endswith(".png"):
            image_file = png_to_jpg(image_file)
        annotation_file = os.path.join(annotation_folder, f"{os.path.splitext(os.path.basename(image_file))[0]}.txt")

        if annotation_file not in annotation_files:
            print(f"'{annotation_file}' does not exist for image '{image_file}'. skipping..")
            continue

        image = cv2.imread(image_file)
        annotations = parse_annotation(annotation_file)
        annotated_image = draw_annotations(image, annotations)
        annotated_image = resize_image_to_screen(annotated_image)

        counter = f'{current_index+1}/{len(annotation_files)}: '
        if len(annotations) == 0:
            cv2.imshow(f'{counter} {os.path.basename(image_file)} (NEGATIVE)', annotated_image)
        else:
            cv2.imshow(f'{counter} {os.path.basename(image_file)}', annotated_image)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('n'):
            if current_index == len(annotation_files) - 1:
                print("Reached the end of all images.")
                break
            current_index = min(current_index + 1, len(annotation_files) - 1)
        elif key & 0xFF == ord('p'):
            current_index = max(current_index - 1, 0)

    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f"USAGE: python3 {sys.argv[0]} /path/to/directory/containing/'images','labels','classes.txt'")

    directory = sys.argv[1]
    image_folder = os.path.join(directory, 'images')
    annotation_folder = os.path.join(directory, 'labels')
    class_file = os.path.join(directory, 'classes.txt')

    if not os.path.exists(image_folder) or not os.path.exists(annotation_folder) or not os.path.isfile(class_file):
        sys.exit("ERROR: make sure that the given directory contains: 'images', 'labels', 'classes.txt'")

    with open(class_file, 'r') as file:
        lines = file.readlines()

    CLASSES = [line.strip() for line in lines]
    COLORS = get_color()

    print("press 'q' to quit, 'n' for next image, 'p' for previous image")
    display_annotated_images(image_folder, annotation_folder, all=False)