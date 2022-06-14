import numpy as np

def calculate(list):
  
  if len(list) < 9: #Value has to be 9 as per the project task
    raise ValueError('List must contain nine numbers.')
  else: #Reshape the list to a 3x3 matrix
#Getting the values for both axis + the flattened matrix
    
    matrix = np.array(list).reshape(3, 3)

    mean = [(matrix.mean(axis=0).tolist()), #adds the mean of the 0th axis to list
            (matrix.mean(axis=1).tolist()), #adds the mean of the 1th axis to list
            (matrix.flatten().mean())] #Flatten 'flattens' the matrix to again make it a line

    var = [(matrix.var(axis=0).tolist()), 
           (matrix.var(axis=1).tolist()),
           (matrix.flatten().var())]

    std = [(matrix.std(axis=0).tolist()), 
           (matrix.std(axis=1).tolist()),
           (matrix.flatten().std())]

    max = [(matrix.max(axis=0).tolist()), 
           (matrix.max(axis=1).tolist()),
           (matrix.flatten().max())]

    min = [(matrix.min(axis=0).tolist()), 
           (matrix.min(axis=1).tolist()),
           (matrix.flatten().min())]

    sum = [(matrix.sum(axis=0).tolist()), 
           (matrix.sum(axis=1).tolist()),
           (matrix.flatten().sum())]
    
#Create a dictionairy where we will be returning all the values to.
    calculations = {
        "mean": mean,
        "variance": var,
        "standard deviation": std,
        "max": max,
        "min": min,
        "sum": sum,
    }

    return calculations