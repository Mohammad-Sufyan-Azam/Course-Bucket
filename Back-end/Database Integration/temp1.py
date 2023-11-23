import pickle

# Read the data from the pickle file
def readData():
    with open('metadata_mapping.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

result = readData()
print(result.keys())

# Write the data to the pickle file
# with open('metadata_mapping.pkl', 'wb') as f:
#     pickle.dump(result, f)
