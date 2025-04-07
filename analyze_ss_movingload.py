"""
Importing the libraries and functions required to 
Enter the shear force as a piece wise function and calculate its absolute maximum value.
Plot the influence line diagrams.
"""
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

#It is the primary function which would calculate the required quantities and display them on the screen.
def analyze_beam(L, t1, t2, x):
#The shear force as a piece wise function.
    def sf_01(a):
        if (a + x) <= L / 2:
            return -((t1 + t2) * a + t2 * x) / L
        elif a <= L / 2 <= (a + x):
            return t2 - ((t1 + t2) * a + t2 * x) / L
        else:
            return (t1 + t2) - ((t1 + t2) * a + t2 * x) / L
#Accounting  for the negative values as absolute values.
    def neg_abs_sf(a):
        return -abs(sf_01(a))
#Calculating the Maximum Reactions at Supports A and B.
    RA_max = t1 + t2 - (t2 * x) / L
    RB_max = t1 + t2 - (t1 * x) / L
#Calculating the Shear Force SF_01 at 0.5L when the leftmost weight is directly above A.
    SF_01 = sf_01(0) 
#Calculating the Bending Moment BM_01 at A when the leftmost weight is directly above A.
    BM_01 = -t2 * x
#Using the piece wise function for shear force generated and the functions imported, 
#Finding out the maximum value of shear force as well as the corresponding location of W1 from A by minimizing the negative of the function.
    result = minimize_scalar(neg_abs_sf, bounds=(0, L - x), method='bounded')
    a_max = result.x
    SF_max = abs(sf_01(a_max))
#The maximum bending moment at support A occurs when a is maximum, i.e. (L-x).
    BM_max = -t1 * (L - x) - t2 * L
#Printing the outputs on screen after all calculations.
    print("After analyzing the beam, here are the results:")
    print("(W1 is the first load as seen from support A)")
    print(f"Maximum Reaction at A : {RA_max:.3f} kN")
    print(f"Maximum Reaction at B : {RB_max:.3f} kN")
    print(f"Shear Force at (0.5)L (SF_01) when W1 is at A: {SF_01:.3f} kN")  
    print(f"Bending Moment at A (BM_01) when W1 is at A: {BM_01:.3f} kNm")
    print(f"Maximum Shear Force at (0.5)L (SF_max): {SF_max:.3f} kN when W1 is at {a_max:.3f} m from support A.")
    print(f"Maximum Bending Moment at A (BM_max): {BM_max:.3f} kNm when W1 is at {L - x:.3f} m from support A.")
    print("\n" + "_"*30)

#To generate the influence line plots
    a_vals = np.linspace(0, L - x, 500)
    RA_vals = t1 + t2 - (t1 * a_vals + t2 * (a_vals + x)) / L
    RB_vals = (t1 * a_vals + t2 * (a_vals + x)) / L

    def sf_func(a):
        if (a + x) <= L / 2:
            return -((t1 + t2) * a + t2 * x) / L
        elif a <= L / 2 <= (a + x):
            return t2 - ((t1 + t2) * a + t2 * x) / L
        else:
            return (t1 + t2) - ((t1 + t2) * a + t2 * x) / L

    SF01_vals = np.array([sf_func(ai) for ai in a_vals])
    BM01_vals = -t1 * a_vals - t2 * (a_vals + x)

#Plotting the influence line diagrams
    plt.figure(figsize=(12, 10))

#Reaction at Support A
    plt.subplot(2, 2, 1)
    plt.plot(a_vals, RA_vals, label="RA(a)", color='green')
    plt.title("Influence Line for Reaction at Support A (RA)")
    plt.xlabel("Position of W1 from Support A (a in m)")
    plt.ylabel("Reaction at A (kN)")
    plt.grid(True)
#Maximum Reaction at Support A    
    max_idx_RA = np.argmax(RA_vals)
    plt.scatter(a_vals[max_idx_RA], RA_vals[max_idx_RA], color='black', zorder=5)
    plt.annotate(f"RA_max: {RA_vals[max_idx_RA]:.2f}", 
                 (a_vals[max_idx_RA], RA_vals[max_idx_RA]),
                 textcoords="offset points", xytext=(0,10), ha='center')

#Reaction at Support B
    plt.subplot(2, 2, 2)
    plt.plot(a_vals, RB_vals, label="RB(a)", color='yellow')
    plt.title("Influence Line for Reaction at Support B (RB)")
    plt.xlabel("Position of W1 from Support A (a in m)")
    plt.ylabel("Reaction at B (kN)")
    plt.grid(True)
#Maximum Reaction at Support B   
    max_idx_RB = np.argmax(RB_vals)
    plt.scatter(a_vals[max_idx_RB], RB_vals[max_idx_RB], color='black', zorder=5)
    plt.annotate(f"RB_max: {RB_vals[max_idx_RB]:.2f}", 
                 (a_vals[max_idx_RB], RB_vals[max_idx_RB]),
                 textcoords="offset points", xytext=(0,10), ha='center')

#Shear Force at Midspan
    plt.subplot(2, 2, 3)
    plt.plot(a_vals, SF01_vals, label="SF01(a)", color='red')
    plt.title("Influence Line for Shear Force at Midspan (SF)")
    plt.xlabel("Position of W1 from Support A (a in m)")
    plt.ylabel("Shear Force at 0.5L (kN)")
    plt.grid(True)
#Maximum Shear Force SF_max
    max_idx_SF = np.argmax(np.abs(SF01_vals))
    plt.scatter(a_vals[max_idx_SF], SF01_vals[max_idx_SF], color='black', zorder=5)
    plt.annotate(f"SF_max: {SF01_vals[max_idx_SF]:.2f}", 
                 (a_vals[max_idx_SF], SF01_vals[max_idx_SF]),
                 textcoords="offset points", xytext=(0,10), ha='center')
#Shear Force SF_01(When W1 is at A)
    plt.scatter(0, SF01_vals[0], color='orange', label='SF01 at a=0')
    plt.annotate(f"SF_01: {SF01_vals[0]:.2f}", (0, SF01_vals[0]),
                 textcoords="offset points", xytext=(0,10), ha='center')

#Bending Moment at Support A
    plt.subplot(2, 2, 4)
    plt.plot(a_vals, BM01_vals, label="BM01(a)", color='blue')
    plt.title("Influence Line for Bending Moment at Support A (BM)")
    plt.xlabel("Position of W1 from Support A (a in m)")
    plt.ylabel("Bending Moment at A (kNm)")
    plt.grid(True)
#Maximum Bending Moment BM_max
    max_idx_BM = np.argmax(np.abs(BM01_vals))
    plt.scatter(a_vals[max_idx_BM], BM01_vals[max_idx_BM], color='black', zorder=5)
    plt.annotate(f"BM_max: {BM01_vals[max_idx_BM]:.2f}", 
                 (a_vals[max_idx_BM], BM01_vals[max_idx_BM]),
                 textcoords="offset points", xytext=(0,10), ha='center')
#Bending Moment BM_01(When W1 is at A)
    plt.scatter(0, BM01_vals[0], color='orange', label='BM01 at a=0')
    plt.annotate(f"BM_01: {BM01_vals[0]:.2f}", (0, BM01_vals[0]),
                 textcoords="offset points", xytext=(0,10), ha='center')

    plt.tight_layout()
    plt.show()

#Having test cases to visualize edge conditions
def Test_Cases():
    test_cases = [
        {"label": "Standard Case", "L": 10, "W1": 20, "W2": 30, "X": 2},
        {"label": "Equal Loads", "L": 12, "W1": 25, "W2": 25, "X": 4},
        {"label": "Load Reversal (X negative)", "L": 10, "W1": 40, "W2": 10, "X": -3},
        {"label": "Loads Far Apart", "L": 15, "W1": 30, "W2": 20, "X": 14},
        {"label": "Loads Very Close", "L": 10, "W1": 10, "W2": 15, "X": 0.01},
        {"label": "Single Load (W1=0)", "L": 8, "W1": 0, "W2": 25, "X": 2},
        {"label": "Single Load Case 2(W2=0)", "L": 8, "W1": 25, "W2": 0, "X": 2},
        {"label": "X equals L", "L": 10, "W1": 10, "W2": 15, "X": 10},
        {"label": "X equals 0", "L": 10, "W1": 25, "W2": 25, "X": 0}
    ]

#Letting the cases get executed in a loop
    for case in test_cases:
        print(f"\nRunning Test: {case['label']}")
        print(f"Inputs Considered: L = {case['L']}, W1 = {case['W1']}, W2 = {case['W2']}, X = {case['X']}")
        print("_" * 30)

        L = case['L']
        W1 = case['W1']
        W2 = case['W2']
        X = case['X']

#Handling negative X as per the original logic
        if X >= 0:
            analyze_beam(L, W1, W2, X)
        else:
            analyze_beam(L, W2, W1, -X)

#Main function
if __name__ == "__main__":
#Prompting user if he/she wishes to see the test cases 
    choice = int(input("Enter 1 if you wish to see the test cases before proceeding to input parameters."))
    if choice == 1:
      Test_Cases()
      
#Taking inputs from the user.
    print("Enter Beam and Load Parameters:\n")
    l = float(input("Length of the beam L (in metres): "))
#Ensuring that length the beam is more than 0.
    while l <= 0:
     l = float(input(f"Length of the beam (in metres, and greater than 0): "))
     if l <= 0:
        print(f"Please enter a value greater than 0.")    
    W1 = float(input("Value of one moving load (in kN): "))
    W2 = float(input("Value of the other moving load (in kN): "))
    X = float(input("Distance x between the loads(in metres): "))
#Ensuring that both the loads are within the span of the beam.
    while X < -l or X > l:
     X = float(input(f"Distance x between W1 and W2 (in metres, between {-l} and {l}): "))
     if X < -l or X > l:
        print(f"Please enter a value between {-l} and {l}.")
    print("\n")
    print("_"*30)
    print("\n")
"""
Negative value of x suggests that the load shown as W1 is actually present after W2 when seen from support A. 
Thus for the analysis we can simply switch W1 with W2 and take the absolute value of x entered.
"""
if (X>=0):
     analyze_beam(l, W1, W2, X)
else:
     analyze_beam(l, W2, W1, -X)
