from hull import Hull, Point
# from which_pyqt import PYQT_VER
# if PYQT_VER == 'PYQT5':
from PyQt5.QtCore import QLineF, QPointF, QObject
# elif PYQT_VER == 'PYQT4':
# 	from PyQt4.QtCore import QLineF, QPointF, QObject
# else:
# 	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# Class to solve the hull
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__(self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def clearAllLines(self):
		self.view.clearLines()

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
	# object can be created with two QPointF objects corresponding to the endpoints
	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)

	def generatePolygonFromHull(self, hull:Hull):
		return self.generatePolygon(hull.rightmostPt)

	def generatePolygon(self, root:Point):
		polygon = []
		if root == {} or root.pt == {}:
			return polygon
		point = root.next
		if point != {} and point.pt != {}:
			polygon.append(QLineF(root.pt, point.pt))
		while (point != {} and point.pt != {} and point != root):
			polygon.append(QLineF(point.pt, point.next.pt))
			point = point.next
		return polygon

# This is the method that gets called by the GUI and actually executes the finding of the hull
	# Time: O(nlogn) Space: O(n**2)
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# Sort points by increasing x value
		points = sorted(points, key=lambda point: point.x()) # Time: O(nlogn) Space: O(n)
		
		# Creates a Hull from each point, and builds a list
		hullList = []
		for i in points: # Time: O(n) Space: O(n)
			point = Point(i)
			hullList.append(Hull(point, point, 1))
		t2 = time.time()
		# print(f"\n\n*************************\nCOMPUTING NEW HULL (Points:{len(hullList)})\n")
		t3 = time.time()

		# Solves the hulls by combining them
		finalHull = self.hull_solver(hullList) # Time: O(nlogn) Space: O(n**2)
		# print("SUCCESS_________")
		# print(f"Final {finalHull}")
		# self.printHullValues(finalHull)
		# print("\n")
		t4 = time.time()

		self.clearAllLines()
		self.showHull(self.generatePolygonFromHull(finalHull),RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	# Prints all the Hull values starting from the leftmost pt
	def printHullValues(self, hull:Hull):
		print("Hull Values:")
		print(hull.leftmostPt)
		pt = hull.leftmostPt.next
		while (pt != {} and pt != hull.leftmostPt):
			print(pt)
			pt = pt.next
		
	# HULL_DRAW = 2
	# Returns a Hull object combined from a list of hulls
	# Time: O(nlogn) Space: O(n**2)
	def hull_solver(self, hullList):
		if len(hullList) == 1:
			return hullList[0]
		else:
			halfLen = int(len(hullList)/2)
			
			leftHull = self.hull_solver(hullList[:halfLen])
			# if (leftHull.hullLen >= self.HULL_DRAW):
			# 	self.showHull(self.generatePolygonFromHull(leftHull),BLUE)
			# 	self.clearAllLines()
			
			rightHull = self.hull_solver(hullList[halfLen:])
			# if (rightHull.hullLen >= self.HULL_DRAW):
			# 	self.showHull(self.generatePolygonFromHull(rightHull),BLUE)
			# 	self.clearAllLines()
			
			return self.combine_hull(leftHull, rightHull) # Time: O(n) Space: O(1)
			
	# Combines two hulls together into a single hull
	# Time: O(n) Space: O(1)
	def combine_hull(self, leftHull:Hull, rightHull:Hull):
		# print("COMBINING HULLS_________")
		# print(f"Left {leftHull}")
		# print(f"Right {rightHull}")
		# self.showHull(self.generatePolygonFromHull(leftHull),BLUE)
		# self.showHull(self.generatePolygonFromHull(rightHull),BLUE)
		
		# Find the top tangent
		# Time: O(n) Space: O(1)
		topLeftTanPt, topRightTanPt = self.findTopTangent(leftHull, rightHull)

		# Find the bottom tangent
		# Time: O(n) Space: O(1)
		bottomLeftTanPt, bottomRightTanPt = self.findBottomTangent(leftHull, rightHull)

		# Reset points to exclude inside points from old hull (maintaining clockwise as 'next' ordering)
		topLeftTanPt.setNext(topRightTanPt)
		topRightTanPt.setPrev(topLeftTanPt)

		bottomRightTanPt.setNext(bottomLeftTanPt)
		bottomLeftTanPt.setPrev(bottomRightTanPt)

		# Find new left and rightmost of the new hull
		# Time: O(n) Space: O(1)
		leftmost, rightmost, hullLen = self.findExtremePts(topLeftTanPt) # choosing topLeftTanPt is arbitrary

		# Return the new hull
		newHull = Hull(leftmost, rightmost, hullLen) # Time: O(1) Space: O(1)
		# print(f"Combined {newHull}\n")
		# self.showHull(self.generatePolygonFromHull(newHull),BLUE)
		return newHull
	
	# Returns the leftmost, rightmost and number of points in hull's edge after going around the linked list
	# Time: O(n) Space: O(1)
	def findExtremePts(self, initialPt:Point):
		hullLen = 1
		leftmost = initialPt
		rightmost = initialPt
		pt = initialPt.next
		while(pt != {} and pt != initialPt): # Time: O(n) Space: O(1)
			hullLen += 1
			if pt.x() < leftmost.x():
				leftmost = pt
			if pt.x() > rightmost.x():
				rightmost = pt
			pt = pt.next
		return leftmost, rightmost, hullLen

	# Returns true if testSlope is more negative
	isMoreNegativeSlope = lambda self, testSlope, ogSlope: testSlope < ogSlope
	
	# Returns true if testSlope is more negative
	isMorePositiveSlope = lambda self, testSlope, ogSlope: testSlope > ogSlope

	# NOTE: clockwise is always trying to find a more positive sloped tangent, counterclockwise is always trying to find negative
	# Time: O(n) Space: O(1)
	def findBottomTangent(self, leftHull:Hull, rightHull:Hull):
		return self.findTangent(leftHull, Point.clockwise, self.isMorePositiveSlope, 
		rightHull,  Point.counterclockwise, self.isMoreNegativeSlope)
	
	# Time: O(n) Space: O(1)
	def findTopTangent(self, leftHull:Hull, rightHull:Hull):
		return self.findTangent(leftHull, Point.counterclockwise, self.isMoreNegativeSlope, 
		rightHull, Point.clockwise, self.isMorePositiveSlope)
	
	# Returns top or bottom tangent based on the directions given
	# Left/right direction is clockwise/counterclockwise
	# Time: O(n) Space: O(1)
	def findTangent(self, leftHull:Hull, leftDirection, leftCompare, rightHull:Hull, rightDirection, rightCompare):
		leftTangentPt = leftHull.rightmostPt
		rightTangentPt = rightHull.leftmostPt
		# self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)],GREEN)
		# self.eraseTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)])

		# Test tangent slopes by changing points on left # Time: O(n/2) Space: O(1)
		leftTangentPt = self.findBestPtWithSlope(leftTangentPt, rightTangentPt, leftCompare, False, leftDirection)
		# self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)],GREEN)
		# self.eraseTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)])

		# Test tangent slopes by changing points on right # Time: O(n/2) Space: O(1)
		rightTangentPt = self.findBestPtWithSlope(rightTangentPt, leftTangentPt, rightCompare, False, rightDirection)
		# self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)],GREEN)
		# self.eraseTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)])

		oldLeftPt = None
		oldRightPt = None
		# Continue testing right or left tangents until neither change
		while (oldLeftPt != leftTangentPt or oldRightPt != rightTangentPt):  # Time: O(n/2) Space: O(1) because we will run this loop at most 4 times
			oldLeftPt = leftTangentPt
			oldRightPt = rightTangentPt
			# Test tangent slopes on the left again # Time: O(n/2) Space: O(1)
			leftTangentPt = self.findBestPtWithSlope(leftTangentPt, rightTangentPt, leftCompare, True, leftDirection)
			# self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)],GREEN)
			# self.eraseTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)])

			# Test tangent slopes on the right again # Time: O(n/2) Space: O(1)
			rightTangentPt = self.findBestPtWithSlope(rightTangentPt, leftTangentPt, rightCompare, True, rightDirection)
			# self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)],GREEN)
			# self.eraseTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)])

		# Return best points on the left and the right
		return leftTangentPt, rightTangentPt
	
	# Traverse the linked list in search of a more positive or negative slope
	# Time: O(n/2) Space: O(1)
	def findBestPtWithSlope(self, initialPt:Point, otherHullPt:Point, compare, stopTesting:bool, getNext):
		pt = getNext(initialPt) # Time: O(1)
		tangentSlope = self.slope(initialPt, otherHullPt)
		bestPt = initialPt
		# Test each point until we get back to the beginning
		while (pt != {} and pt != initialPt): # Time: O(n/2) Space: O(1)
			testSlope = self.slope(pt, otherHullPt) # Time: O(1) Space: O(1)
			# Try to find a more negative/positive slope
			if compare(testSlope, tangentSlope):  # Time: O(1) Space: O(1)
				tangentSlope = testSlope
				bestPt = pt
			# If we don't need to keep testing other slopes, then stop
			elif stopTesting:
				break
			# Go clockwise/counterclockwise to test again
			pt = getNext(pt) # Time: O(1)
		return bestPt
	
	# Returns slope of two points
	# Time: O(1) Space: O(1)
	def slope(self, pt1:Point, pt2:Point): 
		return (pt2.y() - pt1.y()) / (pt2.x() - pt1.x())

