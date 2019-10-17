Labelling power:substations using Overpass API

Labels.py will fetch coordinate data for substations using Overpass API. It needs as an input a satellite picture of size 109 800 x 109 800 pixels. Queried area is this script is 64.8214388312971, 24.8120825440702, 65.8214035188828, 27.20571148892141. Area can be changed as wanted by modifying variable values in the beginning of the script.
Script will crop pictures of size 6400 x 4000 from a source satellite picture. Each picture contains a power:substation object. A label file (gt file) will be created, label file contains coordinates and width and height for a substation in each picture. 

Steps to crop pictures and create a label coordinate file:

Save satellite picture in .jpg format into the same directory with labels.py file

Run main function in labels.py with the below parameters:
- folder: give the folder where .jpg file is located in
- srcFile: give the name of the .jpg file
- tgtFile: give name for the gt file, the labels will be stored here
- repeatCntr: how many times the process is executed, each process will produce one picture per substation object in the source picture area, area around the object is randomly different by each process in the cropped picture

E.g: main(“C:\temp”, “T35WMN_20190829T100031_TCI.jpg”, “gt.txt”, 50)
