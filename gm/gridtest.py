# 600 by 600 (-300 to 300)
# limit 

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle

np.random.seed(0)

# temporary limit
limit = 60

N = 1000


area = 1

mu, sigma = 70, 50 # mean and standard deviation
x = np.random.normal(mu, sigma, N)
y = np.random.normal(mu, sigma + 0.1, N)
coordinates = list(zip(x,y))



# store all found points
# convert to a set later to ensure uniqueness (count should be 1000)
db = []
list_of_quadrants=[]

def is_in_circle(center, radius, x, y):
	return ((x - center[0])**2 + (y - center[1])**2 <= radius**2)

def find_radius(square_length):
	return 0.5 * math.sqrt(2*(square_length)**2)

def quadrants(TL,BR,db):
	list_of_quadrants.append((TL,BR))

	# lengths of the square (should be the same, but you never know)
	horizontal = BR[0] - TL[0]
	vertical = TL[1] - BR[1]

	# determine the centers for the 4 circles
	c1 = (TL[0] + horizontal/4, BR[1] + 3*vertical/4)
	c2 = (TL[0] + 3*horizontal/4, BR[1] + 3*vertical/4)
	c3 = (TL[0] + horizontal/4, BR[1] + vertical/4)
	c4 = (TL[0] + 3 * horizontal/4, BR[1] + vertical/4)

	centers = [c1,c2,c3,c4]

	TL_2 = [
			(TL[0], TL[1]), 
			(TL[0] + horizontal/2, TL[1]),
			(TL[0], TL[1] - vertical/2),
			(TL[0] + horizontal/2, TL[1] - vertical/2)
			]
	BR_2 = [
			(BR[0] - horizontal/2, BR[1] + vertical/2),
			(BR[0], BR[1] + vertical/2),
			(BR[0] - horizontal/2, BR[1]),
			(BR[0], BR[1])
			]	


	radius = find_radius(horizontal/2)

	# four quadrants TL TR BL BR
	for x in range(0,4):
		contained_points = [y for y in coordinates if is_in_circle(centers[x], radius, y[0], y[1])]

		# subdivide if too many points in quadrant
		if len(contained_points) >= limit:
			quadrants(TL_2[x], BR_2[x], db)

		else:
			db.extend(contained_points)
			item = (TL_2[x], BR_2[x])
			list_of_quadrants.append(item)







quadrants((-300,300),(300,-300),db)
#print(db)
#print(len(db))
db_set = set(db)
#print(len(db_set))

someX, someY = 10, 20
plt.scatter(x, y, s=area, alpha=0.5)
currentAxis = plt.gca()
for square in list_of_quadrants:
	print(square)
	currentAxis.add_patch(Rectangle((square[0][0], square[1][1]), square[1][0] - square[0][0], square[0][1]-square[1][1], fill=None, alpha=1))
plt.show()

#plt.show()