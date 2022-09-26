# CS312-Convex-Hull

The convex hull of a set Q of points is the smallest convex polygon P for which each point in Q is either on the boundary of P or in its interior. To be rigorous, a polygon is a piecewise-linear, closed curve in the plane. That is, it is a curve, ending on itself that is formed by a sequence of straight-line segments, called the sides of the polygon. A point joining two consecutive sides is called a vertex of the polygon. If the polygon is simple, as we shall generally assume, it does not cross itself. The set of points in the plane enclosed by a simple polygon forms the interior of the polygon, the set of points on the polygon itself forms its boundary, and the set of points surrounding the polygon forms its exterior. A simple polygon is convex if, given any two points on its boundary or in its interior, all points on the line segment drawn between them are contained in the polygon's boundary or interior.

## Project Requirements
<ol>
<li>Write the full, unambiguous pseudo-code for your 
 divide-and-conquer algorithm for finding the convex hull of a set of points <i>Q</i>. Be sure to label the parts of your 
 algorithm. Also, label each part with its worst-case time efficiency.</li>

<li>Analyze the whole algorithm for its worst-case 
 time efficiency. State the Big-O asymptotic bound.  Discuss how this relates to the Master Theorem estimate for runtime.</li>
 

<li>Implement your divide and conquer algorithm in Python in the following method:</li>
 
<ol type="a">
 
<li><tt>ConvexHullSolver.compute_hull( self, unsorted_points )</tt></li>
 

<li>Use the divide and conquer algorithm from step #1 to find the convex hull of the points in pointList.</li>

 <li>You may use the GUI method <tt>addLines()</tt> to draw the line segments of the convex hull on the UI once you have identified them.</li>

 </ol>
 

<li> Conduct an empirical analysis of your algorithm by running several experiments as follows:</li>
 
<ol type="a">
 
<li>For each value <i>n</i> ∈ {10, 100, 1000, 10,000, 100,000, 500,000, 1,000,000}</li>
 
<ol type="i">

 <li>Generate 5 sets of <i>n</i> points (<i>x</i>,<i>y</i>) in the plane. You may use either provided point generator:
  the 2-D Gaussian (Normal) distribution or the uniform distribution. For every point, <i>x</i> and <i>y</i> are real 
  numbers (doubles). You may use the provided project scaffold code to assist you.</li>
  
<li>For each point set,
  
<ol type="1">

  <li>find the convex hull</li>

  <li>record the elapsed time</li>
  
</ol></li>
  
<li>For each size <i>n</i>, compute the mean time <i>t</i> required.</li>
  
</ol>
  
<li>Plot <i>n</i> (independent variable) versus <i>t</i> (dependent variable).  Note that if you use a logarithmic 
  graph to fit the data (preferable) then that may change the expected shape of your distribution.  Make sure you explain 
  that.</li>
  
</ol>
  

<li>Find the relation of your plot to your theoretical analysis. In other words, if your theoretical analysis says that 
  for a set of <i>n</i> points <i>Q</i>, the convex hull CH(<i>Q</i>) ∈ O(<i>g</i>(<i>n</i>)), does <i>g</i>(<i>n</i>) 
  actually fit your empirical data? If so, what is the constant of proportionality <i>k</i> so that 
  CH(<i>Q</i>) = <i>k</i>·<i>g</i>(<i>n</i>)? If not, then which function <i>g</i>(<i>n</i>) best fits your empirical data, 
  and what is the constant of proportionality? You can fit a function analytically using software or by trial and error 
  in a spreadsheet, for example.</li>


  <li>If your theoretical and empirical analyses differ, discuss the reason(s) for the difference.</li>
  
</ol>