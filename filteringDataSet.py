import random
from collections import defaultdict, Counter


def balancedDataset():
    #Explanation of this code:
    # The purpose of this code is to create a balanced data set based on the following criterias:
    # 1. The data set should contain an n amount of images for each identity.
    # 2. The data set should contain an equal amount of men and women identities.
    # 3. The data set should contain an approximated similar amount of images with and without obstructions based on gender.
    # These criterias are met by the following steps:
    # 1. Read the combined labels file and store data by identity. (Image name, attributes, landmarks, identity)
    # Define paths
    input_file_path = '/Users/jluke/Desktop/FacialShit/combinedLabels.txt'
    output_file_path = '/Users/jluke/Desktop/FacialShit/reducedSet.txt'

    # Step 1: Read the combined labels file and store data by identity
    data_by_identity = {} # Dictionary to store data by identity
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            parts = line.strip().split()
            image_name = parts[0]                           # Image file name
            attributes = list(map(int, parts[1:41]))        # Attributes as integers
            landmarks = parts[41:51]                        # Landmarks
            identity = int(parts[-1])                       # Identity (last value)
            gender_label = int(parts[21])                   # Gender label (1 for male, -1 for female)

            if identity not in data_by_identity:
                data_by_identity[identity] = {'gender': gender_label, 'data': []}
            data_by_identity[identity]['data'].append((image_name, attributes, landmarks))

    # Step 2: Filter identities by image count
    required_image_count = 20 # This value was chosen based on anaylsis of the identityNumRange() function
    filtered_data_by_identity = {identity: info for identity, info in data_by_identity.items() if len(info['data']) == required_image_count} # Filter identities by image count

    # Step 3: Define the majority classification function
    def classify_identity(identity_data, gender, obstruction_indices):
        # Explanation of this function:
        # This function classifies an identity into one of four groups based on the presence of obstructions.
        # This function uses a majority classification approach to determine the group.
        # This function applies an approximate balancing approach using majority classification.
        total_images = len(identity_data['data'])
        obstruction_count = 0

        for _, attributes, _ in identity_data['data']:
            if gender == 1: # male identity
                if any(int(attributes[i]) == 1 for i in obstruction_indices):
                    obstruction_count += 1
                elif int(attributes[25]) == -1: # Index 25: No Beard, therfore, if it is -1, it is an obstruction
                    obstruction_count += 1
            else: # female identity
                if any(int(attributes[i]) == 1 for i in obstruction_indices):
                    obstruction_count += 1
        
        # print(f"Identity: {identity}, Gender: {gender}")
        # print(f"Obstruction Count: {obstruction_count}, Total Images: {len(info['data'])}")
        
    
        if gender == 1:  # Male
            if obstruction_count > total_images / 2:
                return 'male_with_obstructions'
            else:
                return 'male_without_obstructions'
        else:  # Female
            if obstruction_count > total_images / 2:
                return 'female_with_obstructions'
            else:
                return 'female_without_obstructions'

    # Step 4: Categorize identities into the four groups
    obstruction_indices = {
        'male': [1, 17, 23], # Index 1: 5 o'clock shadow, Index 17: Goatee, Index 23: Mustache
        'female': [19, 37] # Index 19: Heavy Makeup, Index 37: Wearing Lipstick
    }

    # dictionary that stores a list of identities for each group
    categorized_identities = {
        'male_with_obstructions': [],
        'male_without_obstructions': [],
        'female_with_obstructions': [],
        'female_without_obstructions': []
    }

    for identity, info in filtered_data_by_identity.items(): # Iterate over filtered identities
        gender = 'male' if info['gender'] == 1 else 'female' # Determine gender
        group = classify_identity(info, info['gender'], obstruction_indices[gender]) # Classify identity, how it works is explained in the function itself


        categorized_identities[group].append(identity) # Append identity to the corresponding group

    # Step 5: Approximate balance by sampling
    group_counts = {group: len(ids) for group, ids in categorized_identities.items()} # Count the number of identities in each categorized group
    min_group_count = min(group_counts.values()) # Get the minimum group count in order to normalize the other groups to this count

    balanced_identities = [] # will store the final balanced identities
    for group, identities in categorized_identities.items(): # Iterate over categorized identities, adjust their count to the minimum group count
        if len(identities) > min_group_count:
            balanced_identities.extend(random.sample(identities, min_group_count))
        else:
            balanced_identities.extend(identities)

    # Step 6: Write the balanced data to the output file
    with open(output_file_path, 'w') as output_file:
        for identity in balanced_identities: # Iterate over balanced identities, write the data to the output file
            for image_name, attributes, landmarks in data_by_identity[identity]['data']:
                line = f"{image_name} {' '.join(map(str, attributes))} {' '.join(landmarks)} {identity}"
                output_file.write(line + "\n")


    # The following code below  is to ensure that the procedures above work as expected

    # Verify group counts after balancing
    final_group_counts = {group: 0 for group in categorized_identities}
    for identity in balanced_identities:
        gender = 'male' if data_by_identity[identity]['gender'] == 1 else 'female'
        group = classify_identity(data_by_identity[identity], data_by_identity[identity]['gender'], obstruction_indices[gender])
        final_group_counts[group] += 1

    # Print the results
    print("Initial group counts:", group_counts)
    print("Final group counts:", final_group_counts)

    # Step 8: Verify the lengths of male and female identities in the output file
    output_male_identities = [identity for identity in balanced_identities if data_by_identity[identity]['gender'] == 1]
    output_female_identities = [identity for identity in balanced_identities if data_by_identity[identity]['gender'] == -1]

    print(f"Number of male identities in output: {len(output_male_identities)}")
    print(f"Number of female identities in output: {len(output_female_identities)}")




def labelConcatenation():
    # Explanation of this code:
    # The purpose of this code is to combine the labels (image information) from three different files into a single file.
    # The three files were provided as part of the CelebA dataset and contain the following information:
    # 1. List of landmarks for each image
    # 2. List of identities for each image
    # 3. List of attributes for each image
    # combinedLabels.txt file will contain the combined information for each image in the following format:
    # <attributes> <landmarks> <identity>
    # This helps in creating a single file that can be used for further processing or analysis.

    # Define paths to label files
    landmarkLabelFilePath = '/Users/jluke/Desktop/FacialShit/list_landmarks_align_celeba.txt'
    identityLabelFilePath = '/Users/jluke/Desktop/FacialShit/identity_CelebA.txt'
    featureLabelFilePath = '/Users/jluke/Desktop/FacialShit/list_attr_celeba.txt'
    outputFilePath = '/Users/jluke/Desktop/FacialShit/combinedLabels.txt'

    # Open the output file for writing
    with open(outputFilePath, 'w') as outputFile:
        # Open each label file for reading
        with open(landmarkLabelFilePath, 'r') as landmarkFile, \
            open(identityLabelFilePath, 'r') as identityFile, \
            open(featureLabelFilePath, 'r') as featureFile:
            
            # Read lines from each file
            landmarkLines = landmarkFile.readlines()
            identityLines = identityFile.readlines()
            featureLines = featureFile.readlines()
            
            # Ensure all files have the same number of lines
            assert len(landmarkLines) == len(identityLines) == len(featureLines), "Label files must have the same number of lines"
            
            # Combine lines from each file
            for landmarkLine, identityLine, featureLine in zip(landmarkLines, identityLines, featureLines):
                landmarkLine = landmarkLine.strip()
                identityLine = identityLine.strip()
                featureLine = featureLine.strip()

                # Remove the first string from landmarkLine and identityLine
                landmarkParts = landmarkLine.split()[1:]  # Remove the first part
                identityParts = identityLine.split()[1:]  # Remove the first part
                
                # Join the remaining parts back into a string
                landmarkLine = ' '.join(landmarkParts)
                identityLine = ' '.join(identityParts)
                
                # Combine the information from each line (customize as needed)
                combinedLine = f"{featureLine} {landmarkLine} {identityLine}\n"
                
                # Write the combined line to the output file
                outputFile.write(combinedLine)

    print(f"Combined labels written to {outputFilePath}")


def countMaleFemaleIdentities():
    # Explanation of this code:
    # The purpose of this code is to count the number of male and female identities present in the CelebA dataset.
    # This function was used to analyze any imbalances with respect to gender in the dataset.

    # Define path to the combined labels file
    combined_label_file_path = '/Users/jluke/Desktop/FacialShit/combinedLabels.txt'

    # Create a set to store unique identities
    unique_identities = set()

    # Read the combined labels file
    with open(combined_label_file_path, 'r') as combined_file:
        for line in combined_file:
            line = line.strip()
            if line:
                parts = line.split()
                identity_value = parts[-1]  # Identity value is at the last index
                gender_label = parts[21]  # Gender label is at index 21
                unique_identities.add((identity_value, gender_label))

    # Count the number of male and female identities
    male_count = sum(1 for identity in unique_identities if identity[1] == '1')
    female_count = sum(1 for identity in unique_identities if identity[1] == '-1')

    print(f"Number of male identities: {male_count}")
    print(f"Number of female identities: {female_count}")




def identityNumRange():
    # Explanation of this code:
    # The purpose of this code is to analyze the distribution of the number of images per identity in the CelebA dataset.
    # The following steps are performed:
    # 1. Read the combined labels file and count the amount of images each identity has.
    # 2. Create a Counter that counts how many identities have a specific number of images from step 1.
    # 3. Print the frequency counts in descending order.
    # This function helped us evaluate which number of image count per identity was most common in the dataset.
    # With this information, we specify the image count value in balancedDataset() to create a balanced dataset.
    # i.e., Image count of 20 has a frequency of 1044 identities, so we have a lot of identities to evaluate and balance.

    # Define path to the combined labels file
    combined_label_file_path = '/Users/jluke/Desktop/FacialShit/combinedLabels.txt'

    # Create a dictionary to store the frequency count of each identity
    identity_frequency = defaultdict(int)

    # Read the combined labels file
    with open(combined_label_file_path, 'r') as combined_file:
        for line in combined_file:
            line = line.strip()
            if line:
                parts = line.split()
                identity_value = parts[-1]  # Identity value is at the last index
                identity_frequency[identity_value] += 1

    # Create a Counter to store the frequency of image counts for each identity
    image_count_frequency = Counter(identity_frequency.values())
    totalFrequency = 0
    # Print the frequency counts in descending order
    for image_count, frequency in sorted(image_count_frequency.items(), key=lambda x: x[1], reverse=True):
        print(f"Image count: {image_count}, Frequency: {frequency}")
        totalFrequency += frequency
    print(f"Total Frequency: {totalFrequency}") # ensures that the frequency of identities were counted properly
                                                # For reference: CelebA's dataset has 10,177 identities.


def main():
    # This function will concatenate image information from the three .txt files given in the CelebA dataset
    #labelConcatenation()
    # This function will count the amount of men and women in the CelebA dataset
    #countMaleFemaleIdentities()
    # This function will count the number of images per identity in the CelebA dataset and create a frequency count
    #identityNumRange()
    # This function will create a balanced dataset based on the criteria specified in the function
   balancedDataset()
   


if __name__ == "__main__":
    main()