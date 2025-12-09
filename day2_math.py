import numpy as np


#1. Define 3 words as vectors which are coordinates of 3D space
king = np.array([0.9, 0.8, 0.1])
man  = np.array([0.1, 0.9, 0.1])
apple = np.array([0.1, 0.1, 0.9])

#2.Calculate similarities(Dot Product)
similarity_king_man=np.dot(king,man)
similarity_king_apple=np.dot(king,apple)

print(f"Similarity (King vs Man):{similarity_king_man:.2f}")
print(f"Similarity (King vs Apple):{similarity_king_apple:.2f}")