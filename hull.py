from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

class Hull:
  # Point leftmostPoint
  # Point rightmostPoint

  def setLeftmost(self, leftPt):
    self.leftmostPoint = leftPt

  def setRightmost(self, rightPt):
    self.rightmostPoint = rightPt

class Point:
  # QPointF myPoint
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