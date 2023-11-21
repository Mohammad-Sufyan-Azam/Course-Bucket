from fuzzywuzzy import fuzz

def schema_matching(source_attributes, local_attributes, threshold=50):
    matches = {}
    for s_attr in source_attributes:
        for l_attr in local_attributes:
            # Calculate the similarity between the two attribute names
            similarity = fuzz.ratio(s_attr.lower(), l_attr.lower())
            # If the similarity is above the threshold, consider it a match
            if similarity > threshold:
                matches[s_attr] = l_attr
                break
    return matches

# Example usage:
source_attributes = ['Name', 'Age', 'Email']
local_attributes = ['User_Name', 'User_Age', 'User_Email']
print(schema_matching(source_attributes, local_attributes))
