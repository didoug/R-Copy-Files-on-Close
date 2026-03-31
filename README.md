# R-Copy-Files-on-Close
This is a small solution I created to keep an R workspace locally while automatically copying the files to your Google Drive folder when R is closed.

How to use:

1) Set the paths desired in the copyFilesToGDrive.py
2) Check if your R is installed at C:\Program Files\RStudio\ or change it in openR.bat
3) Open properties from "R Studio.Ink" and set your local path to hideBat_openR.vbs (Ex: "C:\Users\...\hideBat_openR.vbs)

Required:
+ Python
+ tkinter python library
+ shutil python library
+ Windows OS