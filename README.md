This is the OPV GUI Project README

Qt-GUI

Parameter file generator
The GUI should provide a user friendly way to generate a parameter.txt file. I have attached an example of one for your convenience. Each option is listed in the parameter file whether it is used or not. Some of the options are not allowed if other options are turned on.  
For instance, if the method keyword is set to 0 for Time of flight. Then the following options must be set to 0.0.
Tcv 0.0
Vcv 0.0
Tlag 0.0
If method is set to 1 then the following option should be set to 0
NCh 0

When applying periodic boundary conditions if the system is periodic in X and there are electrodes located on planes on the x axis the system cannot be infinitely periodic. 
PeriodicX 1
XElecOn 1
Then 
EndX cannot be equal to 0
The same is true for the y and z directions. 

Furthermore at least one set of electrodes must always be on
XElecOn 1
YElecOn 0
ZElecOn 0

Otherwise my only recommendation would be that you group similar parameters together in the GUI. I’m sure you could figure that out for yourself. It would probably be easiest if the parameter is yes or no that you used check boxes. 
3D visualization Area
.xyz files
This will be useful to visualize the .xyz files that contain the energies of the sites. These are extremely big files. One way to deal with them once the data is loaded in the memory would be to only visualize the outside edges of the system. For instance all our systems will be cuboids so we don’t need to make the graphics card try to visualize the inside of the cuboid so we can filter that data out and only visualize the edges. 
The .xyz files are normally used to hold information about atoms. Normally the first column is the atom type. I am not dealing with atoms but to get other software to load the files I have assumed all the atoms are carbons thus all the .xyz files have C in the first column. The second, third and fourth column are the x, y and z positions of the sites. The 5th , 6th and 7th columns are values that would be useful to render. 
For instance it might be useful to plot the material and then use the 5th column to determine the color, or the 6th column. Or maybe I would use the 7th column to describe the opacity, or even the brightness. 
It would be also be useful if I could trim the sites I want to visualize. For instance if I only wanted to see the sites in column 5 with value less than -1 etc. 
.path files
These files contain the trajectories of individual charges as they move through the system. The first 3 columns contain the x,y and z positions. The 4th column contains the id of the charge. The 5th column contains the time the charge was on the site. The 6th column contains the global time as the simulation progressed. 
It would be useful to visualize individual charge trajectories after they reached the end it would also be useful to create animations that output to the .avi file format showing how charges move though the system. Just have fun with it any functionality you could include would probably be useful. 
