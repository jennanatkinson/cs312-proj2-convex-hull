from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


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

class Hull:
  # Point leftmostPt
  # Point rightmostPt
  # int hullLen
  def __init__(self, left:Point, right:Point, hullLen:int):
    self.leftmostPt = left
    self.rightmostPt = right
    self.hullLen = hullLen

  def setLeftmost(self, left:Point):
    self.leftmostPt = left

  def setRightmost(self, right:Point):
    self.rightmostPt = right

  def __str__(self):
    return f"Hull (EdgeLen: {self.hullLen})\nLeftmost: {self.leftmostPt}\nRightmost: {self.rightmostPt}"
