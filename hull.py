from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

class Hull:
  # Point leftmostPt
  # Point rightmostPt
  def __init__(self, left, right):
    if isinstance(left, Point):
      self.leftmostPt = left
    else:
      self.leftmostPt = {}
    if isinstance(right, Point):
      self.rightmostPt = right
    else:
      self.rightmostPt = {}

  def setLeftmost(self, left):
    if isinstance(next, Point):
      self.leftmostPt = left

  def setRightmost(self, right):
    if isinstance(next, Point):
      self.rightmostPt = right

  def __str__(self):
    return f"Hull\nLeftmost: {self.leftmostPt}\nRightmost: {self.rightmostPt}"

class Point:
  # QPointF pt
  # Point next #clockwise
  # Point prev #counterclockwise
  def __init__(self, point:QPointF, next=None, prev=None):
    self.pt = point
    self.next = next
    self.prev = prev
    if next is None:
      self.next = {}
    if prev is None:
      self.prev = {}

  def x(self):
    return self.pt.x()

  def y(self):
    return self.pt.y()

  # Next point
  def setNext(self, next):
    if isinstance(next, Point):
      self.next = next

  def clockwise(self):
    return self.next

  # Prev Point
  def setPrev(self, prev):
    if isinstance(prev, Point):
      self.prev = prev

  def counterclockwise(self):
    return self.prev

  def __str__(self):
    return f"Point (X: {self.pt.x()} Y: {self.pt.y()})"