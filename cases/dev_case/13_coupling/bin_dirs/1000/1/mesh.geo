# mesh generated from gmsh using gen_empty_mesh_dassflow() 
18 19 0. 
#Nodes||| id node, x coord, y coord, bathymetry
 1 5613.976226993861 3751.9171779141075 0.0 
2 6459.451687116561 4388.036809815948 0.0 
3 10211.752300613494 281.44171779140834 0.0 
4 9631.997699386502 -137.2699386503091 0.0 
5 6036.713957053678 4069.9769938638747 0.0 
6 7084.835122698414 3703.6042944795854 0.0 
7 7710.2185582799775 3019.171779143539 0.0 
8 8335.60199385989 2334.739263809302 0.0 
9 8960.985429444789 1650.3067484696048 0.0 
10 9586.368865028338 965.8742331313852 0.0 
11 8962.32745398941 510.92791410879863 0.0 
12 8292.657208592105 1159.1257668681133 0.0 
13 7622.986963195268 1807.323619626976 0.0 
14 6953.316717794571 2455.5214723895747 0.0 
15 6283.646472394441 3103.7193251516223 0.0 
16 6523.53070262162 3862.905288468614 0.0 
17 9619.456231826789 408.5836967060892 0.0 
18 8986.938617733245 1076.0319953809826 0.0 
#cells||| id cell, id_node1, id_node2, id_node3, id_node4, patch_manning, bathymetry 
1 8 9 12 0 1 0.
2 2 6 16 0 1 0.
3 8 12 13 0 1 0.
4 15 5 16 0 1 0.
5 14 15 6 0 1 0.
6 14 6 7 0 1 0.
7 7 8 13 0 1 0.
8 10 3 17 0 1 0.
9 14 7 13 0 1 0.
10 4 11 17 0 1 0.
11 9 10 18 0 1 0.
12 11 12 18 0 1 0.
13 6 15 16 0 1 0.
14 11 10 17 0 1 0.
15 12 9 18 0 1 0.
16 5 2 16 0 1 0.
17 3 4 17 0 1 0.
18 10 11 18 0 1 0.
19 15 1 5 0 1 0.
# boundaries 
INLET 2 1
19 2 1  1 1
16 1 1  1 1
OUTLET 1 1 
17 1 1 -1 1