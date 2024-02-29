import os
import sys
from collections import Counter

def main(folder):
    if not os.path.exists(folder):
        print(f"folder '{folder}' does not exist")
        return
    
    # load all .txt files
    all_files = []
    for root,directories,files in os.walk(folder):
        for file in files:
            if file.endswith('.txt') and not file.endswith('classes.txt'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    if len(all_files) == 0:
        print(f'no .txt files found in {folder}')
        return
    
    # read each .txt file
    all_ids = []
    negatives = 0     
    for file in all_files:
        with open(file, 'r') as f:
            lines = f.readlines()
        annos = [line.strip() for line in lines]
        if len(annos) == 0:
            negatives += 1
            continue
        ids = [anno.split(' ')[0] for anno in annos]
        for id in ids:
            all_ids.append(id)
    
    # print stats
    counter = Counter(sorted(all_ids))
    negatives_percent = round(negatives/len(all_files)*100,1)
    print(f'\nimages: {len(all_files)} ({len(all_files)-negatives}({100-negatives_percent}%) + {negatives}({negatives_percent}%))')
    print(f'annotations: {len(all_ids)}')
    print(f'classes: {len(counter)}\n')
    for value,count in counter.items():
        print(f'class {value}: {count} ({round(count/len(all_ids) *100,1)}%)')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} </path/to/annotations/folder>")
        sys.exit(1)

    main(sys.argv[1])