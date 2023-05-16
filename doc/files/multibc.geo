lc = 10;
Point(1) = {0, 0, 0, lc};
Point(2) = {0, 100, 0, lc};
Point(3) = {1000, 0, 0, lc};
Point(4) = {1000, 100, 0, lc};
Point(5) = {0, 200, 0, lc};
Point(6) = {0, 300, 0, lc};
Point(7) = {1000, -100, 0, lc};
Point(8) = {1000, -200, 0, lc};
Point(9) = {350, 100, 0, lc};
Point(10) = {450, 100, 0, lc};
Point(11) = {650, 0, 0, lc};
Point(12) = {550, 0, 0, lc};
Point(13) = {200, 180, 0, lc};
Point(14) = {200, 280, 0, lc};
Point(15) = {800, -80, 0, lc};
Point(16) = {800, -180, 0, lc};
Line(1) = {1, 2};
Line(2) = {3, 4};
Line(3) = {5, 6};
Line(4) = {7, 8};
Line(5) = {1, 12};
Line(6) = {2, 9};
Line(7) = {3, 11};
Line(8) = {4, 10};
BSpline(9) = {5, 13, 9};
BSpline(10) = {6, 14, 10};
BSpline(11) = {8, 16, 12};
BSpline(12) = {7, 15, 11};
Line Loop(14) = {5, -11, -4, 12, -7, 2, 8, -10, -3, 9, -6, -1};
Plane Surface(14) = {14};
Physical Line("in1") = {1};
Physical Line("in2") = {3};
Physical Line("out1") = {2};
Physical Line("out2") = {4};
Physical Surface("surf") = {14};
