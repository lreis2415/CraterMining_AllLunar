0. Due to the restriction of data volume in Github, all data/results are shared with onedrive. This repository only includes codes. Shared data url: https://1drv.ms/u/s!AupLwOv5hDZGkeorY5eyMOCfw4j8dg?e=SWYUYc (password: CraterMining)

1. All relevant code and results (including intermediate results) are contained in this folder.

2. Only Step1 - MultiLE (multiscale landform elements) are calculated by PaRGO with C++, the remaining codes are implemented with Python 3.7.
   For Step1, can follow "CraterMining_upload\01_Step1_MultiLE\PaRGO-MultiScaleLE" folder's README.md to use. The input data are "CraterMining_upload\00_PreStep_BlocksDivision\output_blocks" folder's divided DEMs. The parameters are described in main text and appendix. The output data are multiLE results, which are files contained in "CraterMining_upload\01_Step1_MultiLE\LE_results" folder.

3. Two intermediate results -- multiLE results of Step1 and crcs_shp (circles shapefile) results of Step6 -- are too big to upload in figshare. Thus, they are shared with onedrive. The links are shown below:
	multiLE: https://1drv.ms/u/s!AupLwOv5hDZGkex8IurmuvGk5ig3iw?e=O0NW3c
	crcs_shp: https://1drv.ms/u/s!AupLwOv5hDZGkfkzxUuB0WEBGusEWA?e=atQVQy
   Theirs passwords are all: CraterMining
   multiLE files should be extracted in "CraterMining_upload\01_Step1_MultiLE\LE_results" folder.
   crcs_shp files should be extracted in "CraterMining_upload\03_Step6_Clusters2Objects\crcs_shp" folder.

4. The entire workflow is following each folder's head order, such as run codes in "CraterMining_upload\00_PreStep_BlocksDivision" at first, then run "CraterMining_upload\01_Step1_MultiLE", ..., finally run "CraterMining_upload\04_Step789_Craters". 

5. For each folder, such as in "CraterMining_upload\02_Step2345_CraterCandidatesGrids", only run main Python file, such as its contained "Step2345_main.py".

6. Final results are contained in "CraterMining_upload\05_Final_Result".
