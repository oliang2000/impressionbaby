import numpy as np

def subset(a,b):
    # is b a subset of a
    num_matches = 0
    for x in b:
        x_in_a = int(x in a)
        if x_in_a == 1:
            ind = a==x
            np.delete(a,ind)
        num_matches += x_in_a
    is_subset = int(np.equal(num_matches,len(b)))
    return is_subset
