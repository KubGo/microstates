import numpy as np
from clustering.utilities import reorder_microstates

MICROSTATE_A = np.array([
    -30,   -30,
    0,   -30, -30,
    30, 0, -30 ,-30, -30,
    30,   30, 30,   30,  0,  -30, -30,  -30,  -30,
    30, 30, 30,  0,  -30,
    30,  30, 0,
    30, 0, 
    30])
MICROSTATE_B = np.array([
    -30,   -30,
    -30,   -30, 0,
    -30, -30, -30 , 0, 30,
    -30, -30, -30,   -30,  0,  30, 30,  30,  30,
    -30, 0, 30,  30,  30,
    0,  30, 30,
    0, 30, 
    30])
MICROSTATE_C = np.array([
    -30,   -30,
    -30,   -30, -30,
    -30, -30, -30 , -30, -30,
    -30, -30, -30, -30, -30, -30, -30, -30,  -30,
    30, 30, 30,  30,  30,
    30, 30, 30,
    30, 30, 
    30])def reorder_microstates(microstates: np.array, reference_microstates = None):
    reordered_microstates = np.ones(microstates.shape)
    # Get correlations between microstates and it's references
    microstates_normalized = microstates - np.mean(microstates, axis=1, keepdims=True) 
    microstates_normalized /= np.std(microstates, axis=1, keepdims=True)
    if not reference_microstates:
        reference_microstates = REFERENCE_MICROSTATES
    reference_microstates_normalized = reference_microstates - np.mean(reference_microstates, axis=1, keepdims=True)
    reference_microstates_normalized /= np.std(reference_microstates, axis=1, keepdims=True) 
    corr = np.dot(
        microstates_normalized, 
        reference_microstates_normalized.T) / len(microstates[0])
    corr = corr ** 2
    print(corr)
    print()
    # Pick the highest correlation and leave other for next iteration
    old_positions = [1,2,3,4]
    new_positions = []
    for _ in microstates:
        max_corr = np.max(corr, axis=1)
        max_positions = np.argmax(corr, axis=1)
        # Get position of microstate with maximal correlation value
        current_position = np.argmax(max_corr)
        new_position = max_positions[np.argmax(max_corr)]
        # new_positions[current_position] = new_position
        reordered_microstates[new_position] = microstates[current_position]
        # Remove this microstate correlation from next iterations
        corr[:, new_position] = -1
    print(reordered_microstates)
    return reordered_microstates
    30, 30, -30, -30, -30, -30, -30, -30,  30,
    30, -30, -30,  -30,  30,
    30, -30, 30,
    30, 30, 
    30])
REFERENCE_MICROSTATES = np.array([
    MICROSTATE_A,
    MICROSTATE_B,
    MICROSTATE_C,
    MICROSTATE_D
])

def test_reorder_microstates_the_same_order():
    microstates_to_reorder = np.array([
        MICROSTATE_A,
        MICROSTATE_B,
        MICROSTATE_C,
        MICROSTATE_D
    ])
    reordered_microstates = reorder_microstates(microstates_to_reorder)
    assert np.all(reordered_microstates == REFERENCE_MICROSTATES)
def test_reorder_microstates_reversed_order():
    microstates_to_reorder = np.array([
        MICROSTATE_D,
        MICROSTATE_C,
        MICROSTATE_B,
        MICROSTATE_A
    ])
    reordered_microstates = reorder_microstates(microstates_to_reorder)
    assert np.all(reordered_microstates == REFERENCE_MICROSTATES)

def test_reorder_microstates_random_order():
    microstates_to_reorder = np.random.permutation(REFERENCE_MICROSTATES)
    reordered_microstates = reorder_microstates(microstates_to_reorder)
    assert np.all(reordered_microstates == REFERENCE_MICROSTATES)
    
