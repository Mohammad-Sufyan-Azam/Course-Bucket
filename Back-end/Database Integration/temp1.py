import pickle

# Read the data from the pickle file
def readData():
    with open('metadata_mapping.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

print(readData())