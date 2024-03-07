import cv2
import os
import sys
from random import randint

def resize_image(image):
    screen_width, screen_height = 1280, 720

    if image.shape[1] > screen_width or image.shape[0] > screen_height:
        ratio_width = screen_width / image.shape[1]
        ratio_height = screen_height / image.shape[0]
        scale_factor = min(ratio_width, ratio_height)
        new_width = int(image.shape[1] * scale_factor)
        new_height = int(image.shape[0] * scale_factor)
        image = cv2.resize(image, (new_width, new_height))

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

        cv2.rectangle(image, (x1, y1), (x2, y2), COLORS[class_id], 2)
        cv2.putText(image, f'{CLASSES[class_id]}', (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return image

def display_annotated_images(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))
    annotation_files = sorted(os.listdir(annotation_folder))
    if len(image_files) != len(annotation_files): 
        print(f"mismatch in no. of images & labels (images: {len(image_files)}, labels: {len(annotation_files)})")
        sys.exit(1)
    
    current_index = 0
    while current_index < len(annotation_files):
        counter = f'{current_index+1}/{len(annotation_files)}: '
        annotation_file = annotation_files[current_index]
        image_name = os.path.splitext(annotation_file)[0] + ".jpg"
        if image_name in image_files:
            image_path = os.path.join(image_folder, image_name)
            annotation_path = os.path.join(annotation_folder, annotation_file)

            image = cv2.imread(image_path)
            annotations = parse_annotation(annotation_path)
            annotated_image = draw_annotations(image, annotations)
            annotated_image = resize_image(annotated_image)

            if len(annotations) == 0:
                cv2.imshow(f'{counter} {image_name} (NEGATIVE)', annotated_image)
            else:
                cv2.imshow(f'{counter} {image_name}', annotated_image)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()

            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('n'):
                current_index = min(current_index + 1, len(annotation_files) - 1)
            elif key & 0xFF == ord('p'):
                current_index = max(current_index - 1, 0)

    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} </path/to/directory/containing/'images','labels','classes.txt'")
        sys.exit(1)

    directory = sys.argv[1]
    image_folder = os.path.join(directory,'images')
    annotation_folder = os.path.join(directory,'labels')
    class_file = os.path.join(directory,'classes.txt')

    if not os.path.exists(image_folder) or not os.path.exists(annotation_folder) or not os.path.isfile(class_file):
        print("make sure that the given directory contains: 'images', 'labels', 'classes.txt'")
        sys.exit(1)

    with open(class_file, 'r') as file:
        lines = file.readlines()

    CLASSES = [line.strip() for line in lines]
    COLORS = get_color()

    print("press 'q' to quit, 'n' for next image, 'p' for previous image")
    display_annotated_images(image_folder, annotation_folder)
