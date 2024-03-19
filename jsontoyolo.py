'''
convert annotations from label-studio JSON-MIN format to YOLO .txt files per image.
Enter class names in a 'CLASSES' variable in the same order as used to label.

Usage: python3 jsontoyolo.py <filename.json>
Output:
1. Creates one .txt file per image with annotations as per YOLO format in a directory 'labels'
2. creates 'classes.txt' with the class names mentioned
'''

import os
import json
import sys
import math

#CLASSES = ['boot', 'glove', 'hard_hat', 'vest']
CLASSES = ['plate']

# https://github.com/HumanSignal/label-studio-converter/blob/master/label_studio_converter/converter.py#L901
def rotated_rectangle(label):
    if not (
        "x" in label and "y" in label and 'width' in label and 'height' in label
    ):
        return None

    label_x, label_y, label_w, label_h, label_r = (
        label["x"],
        label["y"],
        label["width"],
        label["height"],
        label["rotation"] if "rotation" in label else 0.0,
    )

    if abs(label_r) > 0:
        alpha = math.atan(label_h / label_w)
        beta = math.pi * (
            label_r / 180
        )  # Label studio defines the angle towards the vertical axis

        radius = math.sqrt((label_w / 2) ** 2 + (label_h / 2) ** 2)

        # Label studio saves the position of top left corner after rotation
        x_0 = (
            label_x
            - radius
            * (math.cos(math.pi - alpha - beta) - math.cos(math.pi - alpha))
            + label_w / 2
        )
        y_0 = (
            label_y
            + radius
            * (math.sin(math.pi - alpha - beta) - math.sin(math.pi - alpha))
            + label_h / 2
        )

        theta_1 = alpha + beta
        theta_2 = math.pi - alpha + beta
        theta_3 = math.pi + alpha + beta
        theta_4 = 2 * math.pi - alpha + beta

        x_coord = [
            x_0 + radius * math.cos(theta_1),
            x_0 + radius * math.cos(theta_2),
            x_0 + radius * math.cos(theta_3),
            x_0 + radius * math.cos(theta_4),
        ]
        y_coord = [
            y_0 + radius * math.sin(theta_1),
            y_0 + radius * math.sin(theta_2),
            y_0 + radius * math.sin(theta_3),
            y_0 + radius * math.sin(theta_4),
        ]

        label_x = min(x_coord)
        label_y = min(y_coord)
        label_w = max(x_coord) - label_x
        label_h = max(y_coord) - label_y

    return label_x, label_y, label_w, label_h



def main(filename):

    SAVE_FOLDER = "labels"
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    with open('classes.txt', 'w') as f:
        for class_name in CLASSES:
            f.write(f'{class_name}\n')
    print(f'Using class names: {CLASSES} (created classes.txt)')
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    print(f'No. of annotations found: {len(data)}')
    for anno in data:
        txt_filename = os.path.join(SAVE_FOLDER, f"{os.path.splitext(anno['image'].split('/')[-1])[0]}.txt")

        if not 'label' in anno.keys():
            # create empty .txt file for negative
            with open(txt_filename, 'w') as f:
                pass
            continue

        # collect annotations
        labels = anno['label']
        annotations = []
        for label in labels:
            x,y,w,h = rotated_rectangle(label)
            class_id = CLASSES.index(label['rectanglelabels'][0])
            annotations.append([
                 class_id, 
                 (x + w / 2) / 100, 
                 (y + h / 2) / 100,
                 w / 100,
                 h / 100
                 ])
        
        # write annotaions to file
        with open(txt_filename, 'w') as f:
            for annotation in annotations:
                for idx,l in enumerate(annotation):
                    if idx == len(annotation) - 1:
                        f.write(f"{l}\n")
                    else:
                        f.write(f"{l} ")

    print(f".\n.\n.\nsaved at '{SAVE_FOLDER}'")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("usage: python3 jsontoyolo.py <filename.json>")

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        sys.exit("File not found:", filename)

    main(filename)
    
