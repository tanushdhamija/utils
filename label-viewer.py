import cv2
import os
import sys
from random import randint


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
        cv2.putText(image, f'{CLASSES[class_id]}', (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return image


def display_annotated_images(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))
    annotation_files = sorted(os.listdir(annotation_folder))

    for annotation_file in annotation_files:
        image_name = os.path.splitext(annotation_file)[0] + ".jpg"
        if image_name in image_files:
            image_path = os.path.join(image_folder, image_name)
            annotation_path = os.path.join(annotation_folder, annotation_file)

            image = cv2.imread(image_path)
            annotations = parse_annotation(annotation_path)
            annotated_image = draw_annotations(image, annotations)

            cv2.imshow(image_name, annotated_image)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if key & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if not os.path.exists('images') or not os.path.exists('labels') or not os.path.isfile('classes.txt'):
        print("make sure that the current directory contains: 'images', 'labels', 'classes.txt'")
        sys.exit(1)

    image_folder = 'images'
    annotation_folder = 'labels'
    with open('classes.txt', 'r') as file:
        lines = file.readlines()

    CLASSES = [line.strip() for line in lines]
    COLORS = get_color()

    print("press 'q' to quit")
    display_annotated_images(image_folder, annotation_folder)