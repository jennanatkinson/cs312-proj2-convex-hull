from hull import Hull, Point
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



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
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

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
		if root == {} or root.pt == {} or root.next == {} or root.next.pt == {}:
			return polygon
		point:Point = root.next
		polygon.append(QLineF(root.pt, point.pt))
		while (point != root):
			polygon.append(QLineF(point.pt, point.next.pt))
			point = point.next
			if point == {} or point.pt == {}:
				break
		return polygon

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# Sort points by increasing x value
		points = sorted(points, key=lambda point: point.x())
		
		# Creates a Hull from each point, and builds a list
		hullList = []
		for i in points:
			point = Point(i)
			hullList.append(Hull(point, point))
		t2 = time.time()

		t3 = time.time()

		# Solves the hulls by combining them
		finalHull = self.hull_solver(hullList)
		t4 = time.time()

		self.showHull(self.generatePolygonFromHull(finalHull),RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))


	# Returns a Hull object combined from a list of hulls
	def hull_solver(self, hullList):
		if len(hullList) == 1:
			return hullList[0]
		else:
			halfLen = int(len(hullList)/2)
			leftHull = self.hull_solver(hullList[:halfLen])
			rightHull = self.hull_solver(hullList[halfLen:])
			return self.combine_hull(leftHull, rightHull)
			
	# Combines two hulls together into a single hull
	def combine_hull(self, leftHull:Hull, rightHull:Hull):
		print(f"Left {leftHull}\n")
		print(f"Right {rightHull}\n")
		
		# Find the top tangent
		topLeftTanPt, topRightTanPt = self.findTopTangent(leftHull, rightHull)

		# Find the bottom tangent
		bottomLeftTanPt, bottomRightTanPt = self.findBottomTangent(leftHull, rightHull)

		# Reset points to exclude inside points from old hull (maintaining clockwise as 'next' ordering)
		topLeftTanPt.setNext(topRightTanPt)
		topRightTanPt.setPrev(topLeftTanPt)

		bottomRightTanPt.setNext(bottomLeftTanPt)
		bottomLeftTanPt.setPrev(bottomRightTanPt)

		# Find new left and rightmost
		leftmost = self.findExtremePt(topLeftTanPt, self.isMoreLeft) # topLeftTanPt is completely arbitrary
		rightmost = self.findExtremePt(topLeftTanPt, self.isMoreRight)
		
		# Return the new hull
		return Hull(leftmost, rightmost)
	
	isMoreLeft = lambda pt, ogPt: pt.x() < ogPt.x()
	isMoreRight = lambda pt, ogPt: pt.x() > ogPt.x()
	
	def findExtremePt(self, initialPt:Point, compare):
		extremePt = initialPt
		pt = initialPt.next
		while(pt != {} and pt != initialPt):
			if compare(pt, extremePt):
				extremePt = pt
			pt = pt.next
		return extremePt

	# Returns true if testSlope is more negative
	isMoreNegativeSlope = lambda testSlope, ogSlope: testSlope < ogSlope
	
	# Returns true if testSlope is more negative
	isMorePositiveSlope = lambda testSlope, ogSlope: testSlope > ogSlope

	def findBottomTangent(self, leftHull:Hull, rightHull:Hull):
		return self.findTangent(leftHull, Point.clockwise, self.isMoreNegativeSlope, 
		rightHull,  Point.counterclockwise, self.isMoreNegativeSlope)
	
	# clockwise is always more positive
	# counterclockwise is always trying to find negative
	def findTopTangent(self, leftHull:Hull, rightHull:Hull):
		return self.findTangent(leftHull, Point.counterclockwise, self.isMoreNegativeSlope, 
		rightHull, Point.clockwise, self.isMoreNegativeSlope)
	# 	initialLeftTangentPt = leftTangentPt = leftHull.rightmostPt
	# 	initialRightTangentPt = rightTangentPt = rightHull.leftmostPt
	# 	tangentSlope = self.slope(initialLeftTangentPt, initialRightTangentPt)
	# 	self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)

	# 	# Test tangent slopes by changing points on left
	# 	leftPt = initialLeftTangentPt.counterclockwise()
	# 	leftTangentPt, tangentSlope = self.findBestPtWithSlope(leftPt, initialLeftTangentPt, rightTangentPt, tangentSlope, self.isMoreNegativeSlope, False, Point.counterclockwise)
	# 	self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)
		
	# 	# Test tangent slopes by changing points on right
	# 	rightPt = initialRightTangentPt.clockwise()
	# 	rightTangentPt, tangentSlope = self.findBestPtWithSlope(rightPt, initialRightTangentPt, leftTangentPt, tangentSlope, self.isMorePositiveSlope, False, Point.clockwise)
	# 	self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)

	# 	# Test tangent slopes on the left one more time
	# 	leftPt = leftTangentPt.counterclockwise()
	# 	leftTangentPt, tangentSlope = self.findBestPtWithSlope(leftPt, leftTangentPt, rightTangentPt, tangentSlope, self.isMoreNegativeSlope, True, Point.counterclockwise)

	# 	self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)
	# 	# Return best points on the left and the right
	# 	return leftTangentPt, rightTangentPt
	
	# Returns top or bottom tangent based on the directions given
	# Left/right direction is clockwise/counterclockwise
	def findTangent(self, leftHull:Hull, leftDirection, leftCompare, rightHull:Hull, rightDirection, rightCompare):
		initialLeftTangentPt = leftTangentPt = leftHull.rightmostPt
		initialRightTangentPt = rightTangentPt = rightHull.leftmostPt
		tangentSlope = self.slope(initialLeftTangentPt, initialRightTangentPt)
		self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)

		# Test tangent slopes by changing points on left
		leftPt = leftDirection(initialLeftTangentPt)
		leftTangentPt, tangentSlope = self.findBestPtWithSlope(leftPt, initialLeftTangentPt, rightTangentPt, tangentSlope, leftCompare, False, leftDirection)
		self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)
		
		# Test tangent slopes by changing points on right
		rightPt = rightDirection(initialRightTangentPt)
		rightTangentPt, tangentSlope = self.findBestPtWithSlope(rightPt, initialRightTangentPt, leftTangentPt, tangentSlope, rightCompare, False, rightDirection)
		self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)

		# Test tangent slopes on the left one more time
		leftPt = leftDirection(leftTangentPt)
		leftTangentPt, tangentSlope = self.findBestPtWithSlope(leftPt, leftTangentPt, rightTangentPt, tangentSlope, leftCompare, True, leftDirection)

		self.showTangent([QLineF(leftTangentPt.pt, rightTangentPt.pt)], GREEN)
		# Return best points on the left and the right
		return leftTangentPt, rightTangentPt
	

	def findBestPtWithSlope(self, pt:Point, initialPt:Point, otherHullPt:Point, tangentSlope:float, compare, stopTesting:bool, getNext):
		bestPt = None
		# Test each point until we get back to the beginning
		while (pt != {} and pt != initialPt):
			testSlope = self.slope(pt, otherHullPt)
			# Try to find a more negative/positive slope
			if compare(testSlope, tangentSlope):
				tangentSlope = testSlope
				bestPt = pt
			# If we don't need to keep testing other slopes, then stop
			elif stopTesting:
				break
			# Go clockwise/counterclockwise to test again
			pt = getNext(pt) 
		return bestPt, tangentSlope
	
	def slope(self, pt1:Point, pt2:Point):
		return (pt2.y() - pt1.y()) / (pt2.x() - pt1.x())

