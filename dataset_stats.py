import os
import sys
from collections import Counter

def main(folder):
    if not os.path.exists(folder):
        sys.exit(f"folder '{folder}' does not exist")
    
    # load all .txt files
    all_files = []
    for root,directories,files in os.walk(folder):
        for file in files:
            if file.endswith('.txt') and not file.endswith('classes.txt'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    if len(all_files) == 0:
        sys.exit(f'no .txt files found in {folder}')
    
    # read each .txt file
    all_ids = []
    negatives = 0     
    for file in all_files:
        with open(file, 'r') as f:
            lines = f.readlines()
        # annos = [line.strip() for line in lines]
        if len(lines) == 0:
            negatives += 1
            continue
        ids = [line.split(' ')[0] for line in lines]
        for id in ids:
            all_ids.append(id)
    
    # print stats
    counter = Counter(sorted(all_ids))
    negatives_percent = round(negatives/len(all_files)*100,1)
    print(f"{'-'*40}")
    print(f'images: {len(all_files)} [{len(all_files)-negatives}({100-negatives_percent}%) + {negatives}({negatives_percent}%)]')
    print(f'annotations: {len(all_ids)}')
    print(f'classes: {len(counter)}\n')
    for value,count in counter.items():
        print(f'class {value}: {count} ({round(count/len(all_ids) *100,1)}%)')
    print(f"{'-'*40}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: python3 {sys.argv[0]} </path/to/annotations/folder>")

    main(sys.argv[1])