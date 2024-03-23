import os
import sys

def modify_label(folder, old_label, new_label):

    labels = [os.path.join(folder,label) for label in os.listdir(folder) if label.endswith('.txt') and label != 'classes.txt']
    if len(labels) == 0:
        sys.exit(f'no .txt files found in {folder}')

    print(f'changing class_id from {old_label} to {new_label} for {len(labels)} files...')
    for label in labels:
        # read file
        with open(label,'r') as file:
            lines = file.readlines()

        # replace labels
        newlines = []
        for line in lines:
            class_id = line.split(" ")[0]
            if class_id == old_label:
                new_line = new_label + " " + " ".join(line.split(" ")[1:])
            else:
                new_line = line
            newlines.append(new_line)

        # write back to file
        with open(label,'w') as file:
            file.writelines(newlines)

    print('\ndone.')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"usage: python3 {sys.argv[0]} </path/to/labels> <class_id to replace> <new class_id>")

    modify_label(*sys.argv[1:])