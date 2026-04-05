# IMPORTANT!!!!!!
# The following code was scraped from the final research project. This code was an important step in future python scripts that were used for 
# dataset seperation. This code was used to create actual sub folders and sub labels for the dataset.
import os
import shutil
from collections import defaultdict, Counter

def obstructionSeperation():
    Labels = {
        "eyeGlassesFolder": 16,
        "goateeFolder": 17,
        "heavyMakeupFolder": 19,
        "mustacheFolder": 23,
        "noBeardFolder": 25
    }

    # Define paths
    image_folder = '/Users/jluke/Desktop/FacialFolder/img_align_celeba'
    label_file_path = '/Users/jluke/Desktop/FacialFolder/combinedLabels.txt'

    for label in Labels:
        output_folder = f'/Users/jluke/Desktop/FaceDisguiseDatabase/{label}'

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

     
        index = Labels[label]  # index will be updated based on label name

        # Read the label file
        with open(label_file_path, 'r') as label_file:
            maleCount = 0
            femaleCount = 0
            maleRatio = 0
            femaleRatio = 0
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts
                    
                    # Check for index label, 1 means true
                    if int(labels[index]) == 1:
                        # Check if the image exists in the image folder
                        image_path = os.path.join(image_folder, image_file)
                        if os.path.exists(image_path):
                            # Copy the image to the output folder
                            shutil.copy(image_path, output_folder)
                            if int(labels[20]) == 1:
                                maleCount += 1
                            else:
                                femaleCount += 1
                            print(f"Copied {image_file} to {output_folder}")
                        else:
                            print(f"Image file {image_file} not found.")
        
            # Calculate ratios
            total = maleCount + femaleCount
            if total > 0:
                maleRatio = (maleCount / total) * 100
                femaleRatio = (femaleCount / total) * 100
            else:
                maleRatio = 0
                femaleRatio = 0

            # Write ratios to a text file in the output folder
            ratio_file_path = os.path.join(output_folder, 'ratios.txt')
            with open(ratio_file_path, 'w') as ratio_file:
                ratio_file.write(f"Male Ratio: {maleRatio}\n")
                ratio_file.write(f"Female Ratio: {femaleRatio}\n")
            print(f"Ratios written to {ratio_file_path}")


import os
import shutil

def maleFemaleSplit():
    # Define paths
    image_folder = '/Users/jluke/Desktop/FacialFolder/img_align_celeba'
    label_file_path = '/Users/jluke/Desktop/FacialFolder/combinedLabels.txt'
    outputFolderMale = '/Users/jluke/Desktop/FaceDisguiseDatabase/Male'
    outputFolderFemale = '/Users/jluke/Desktop/FaceDisguiseDatabase/Female'

    # Create output folders if they don't exist
    os.makedirs(outputFolderMale, exist_ok=True)
    os.makedirs(outputFolderFemale, exist_ok=True)

    # Index to specify gender
    index = 21  # Assuming index 21 is the gender label (1 for male, -1 for female)

    # Paths for label files
    male_label_file_path = '/Users/jluke/Desktop/FaceDisguiseDatabase/maleLabels.txt'
    female_label_file_path = '/Users/jluke/Desktop/FaceDisguiseDatabase/femaleLabels.txt'

    # Open label files for writing
    with open(male_label_file_path, 'w') as male_label_file, open(female_label_file_path, 'w') as female_label_file:
        # Read the label file
        with open(label_file_path, 'r') as label_file:
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts

                    # Check if the image exists in the image folder
                    image_path = os.path.join(image_folder, image_file)
                    if os.path.exists(image_path):
                        if int(labels[index]) == 1:
                            # Copy the image to the male output folder
                            shutil.copy(image_path, outputFolderMale)
                            male_label_file.write(line + '\n')
                            print(f"Copied {image_file} to {outputFolderMale}")
                        else:
                            # Copy the image to the female output folder
                            shutil.copy(image_path, outputFolderFemale)
                            female_label_file.write(line + '\n')
                            print(f"Copied {image_file} to {outputFolderFemale}")

    print(f"Labels written to {male_label_file_path} and {female_label_file_path}")




def beardObstruction():
    # Define paths
    image_folder = '/Users/jluke/Desktop/FacialFolder/img_align_celeba'
    label_file_path = '/Users/jluke/Desktop/FacialFolder/combinedLabels.txt'

    outputFolder="/Users/jluke/Desktop/FaceDisguiseDatabase/BeardFolder"

    # Create output folder if it doesn't exist
    os.makedirs(outputFolder, exist_ok=True)

    # Facial hair label index based on your example (adjust if needed)
    index = 25 # Index to specify beard

    # Read the label file
    with open(label_file_path, 'r') as label_file:
        maleCount = 0
        femaleCount = 0
        for line in label_file:
            line = line.strip()
            if line:
                parts = line.split()
                image_file = parts[0]
                labels = parts
                
                # Check for facial hair (when no beard = -1)
                if int(labels[index]) == -1:
                   shutil.copy(os.path.join(image_folder, image_file), outputFolder)
                   print(f"Copied {image_file} to {outputFolder}")
                else:
                    print(f"Image file {image_file} has no facial hair.")
        
        # Calculate ratios
        total = maleCount + femaleCount
        if total > 0:
            maleRatio = (maleCount / total) * 100
            femaleRatio = (femaleCount / total) * 100
        else:
            maleRatio = 0
            femaleRatio = 0

        # Write ratios to a text file in the output folder
        ratio_file_path = os.path.join(outputFolder, 'ratios.txt')
        with open(ratio_file_path, 'w') as ratio_file:
            ratio_file.write(f"Male Ratio: {maleRatio}\n")
            ratio_file.write(f"Female Ratio: {femaleRatio}\n")
        print(f"Ratios written to {ratio_file_path}")

def maleFemaleObstructionNoObstruction():
    # Define paths
    imageFolderMale = '/Users/jluke/Desktop/FaceDisguiseDatabase/Male'
    label_file_path = '/Users/jluke/Desktop/FacialFolder/list_attr_celeba.txt'
    imageFolderFemale = '/Users/jluke/Desktop/FaceDisguiseDatabase/Female'

    outputFolderMale = f'/Users/jluke/Desktop/FaceDisguiseDatabase/MaleImagesWithObstruction'
    outputFolderFemale = f'/Users/jluke/Desktop/FaceDisguiseDatabase/FemaleImagesWithObstruction'
    outputFolderMale2 = f'/Users/jluke/Desktop/FaceDisguiseDatabase/MaleImagesNoObstruction'
    outputFolderFemale2 = f'/Users/jluke/Desktop/FaceDisguiseDatabase/FemaleImagesNoObstruction'

    # Open label files for writing
    male_label_file_path = '/Users/jluke/Desktop/FaceDisguiseDatabase/maleLabels.txt'
    female_label_file_path = '/Users/jluke/Desktop/FaceDisguiseDatabase/femaleLabels.txt'

    # Create new label files for each obstruction/no obstruction seperation
    maleObstructionLabelFile = '/Users/jluke/Desktop/FaceDisguiseDatabase/maleObstructionLabels.txt'
    maleNoObstructionLabelFile = '/Users/jluke/Desktop/FaceDisguiseDatabase/maleNoObstructionLabels.txt'
    femaleObstructionLabelFile = '/Users/jluke/Desktop/FaceDisguiseDatabase/femaleObstructionLabels.txt'
    femaleNoObstructionLabelFile = '/Users/jluke/Desktop/FaceDisguiseDatabase/femaleNoObstructionLabels.txt'

    # Create output folder if it doesn't exist
    os.makedirs(outputFolderMale, exist_ok=True)
    os.makedirs(outputFolderFemale, exist_ok=True)
    os.makedirs(outputFolderMale2, exist_ok=True)
    os.makedirs(outputFolderFemale2, exist_ok=True)


    def maleObstruction():
        with open(maleObstructionLabelFile, 'w') as maleObstruction, open(male_label_file_path, 'r') as label_file:
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts
                    if 1 == int(labels[1]) or 1 == int(labels[17]) or 1 == int(labels[23]) or -1 == int(labels[25]):
                        shutil.copy(os.path.join(imageFolderMale, image_file), outputFolderMale)
                        maleObstruction.write(line + '\n')
                        print(f"Copied {image_file} to {outputFolderMale}")
                    else:
                        print(f"Image file {image_file} has no obstruction.")
    def maleNoObstruction():
        with open(maleNoObstructionLabelFile, 'w') as maleNoObstruction, open(male_label_file_path, 'r') as label_file:
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts
                    if -1 == int(labels[1]) and -1 == int(labels[17]) and -1 == int(labels[23]) and 1 == int(labels[25]): # and -1 == labels[31]: for sideburns
                        shutil.copy(os.path.join(imageFolderMale, image_file), outputFolderMale2)
                        maleNoObstruction.write(line + '\n')
                        print(f"Copied {image_file} to {outputFolderMale2}")
                    else:
                        print(f"Image file {image_file} has obstructions.")
    def femaleObstruction():
        with open(femaleObstructionLabelFile, 'w') as femaleObstruction, open(female_label_file_path, 'r') as label_file:
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts
                    if 1 == int(labels[19]) or 1 == int(labels[37]):
                        shutil.copy(os.path.join(imageFolderFemale, image_file), outputFolderFemale)
                        femaleObstruction.write(line + '\n')
                        print(f"Copied {image_file} to {outputFolderFemale}")
                    else:
                        print(f"Image file {image_file} has no obstruction.")
    def femaleNoObstruction():
        with open(femaleNoObstructionLabelFile, 'w') as femaleNoObstruction, open(female_label_file_path, 'r') as label_file:
            for line in label_file:
                line = line.strip()
                if line:
                    parts = line.split()
                    image_file = parts[0]
                    labels = parts
                    if -1 == int(labels[19]) and -1 == int(labels[37]):
                        shutil.copy(os.path.join(imageFolderFemale, image_file), outputFolderFemale2)
                        femaleNoObstruction.write(line + '\n')
                        print(f"Copied {image_file} to {outputFolderFemale2}")
                    else:
                        print(f"Image file {image_file} has obstructions.")
    maleObstruction()
    maleNoObstruction()
    femaleNoObstruction()
    femaleObstruction()


if __name__ == "__main__":
    #beardObstruction() 
    #labelConcatenation() # RUN FIRST
    # RUN ONE AT A TIME!!!
    maleFemaleSplit() # RUN SECOND
    #maleFemaleObstructionNoObstruction() # RUN THIRD
