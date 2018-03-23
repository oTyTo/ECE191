Sample images are stored in samples folder. Images are sampled from four videos: PV, CV in no light, CV in low light, and CV in middel light. There are five samples images at frame number 1,10,50,100,150 for each video.
CalculateTranform.py: Read in CV image and PV image. Calculate tranfer matrix that maps CV to PV and ouput the matrix as Geo_Transfer.mat
DetectImage.py      : Read in CV image, PV image, and transfer matrix. Apply transfer matrix on CV to align with the PV and compare the transferd CV with PV to detect oscar. Output the tranfered CV and a mask of detect Oscar on CV.
Geo_Transfer.mat    : Transfer matrix calculated by CalculateTranform.py
TransferedCV.jpg    : Aligned CV