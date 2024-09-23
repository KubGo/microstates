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
    30])
MICROSTATE_D = np.array([
    -30,   -30,
    -30,   -30, -30,
    30, -30, -30 , -30, -30,
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
    
def test_reorder_last_microstate_assignment():
    microstates_to_reorder = np.array([
        MICROSTATE_D,
        MICROSTATE_D,
        MICROSTATE_B,
        MICROSTATE_A
    ])
    microstates_to_compare = np.array([
        MICROSTATE_A,
        MICROSTATE_B,
        MICROSTATE_D,
        MICROSTATE_D
    ])
    reordered_microstates = reorder_microstates(microstates_to_reorder)
    assert np.all(reordered_microstates == microstates_to_compare)
