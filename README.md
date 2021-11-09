# Med_Ass_Chamber_Parsers_For_Greg

**The code 'stopsigparser' is a script written to run along with the .bat file to parse stop signaling programs created by Gregory Simandl (Marquette University).**

**HOW TO USE THE CODE:**

    1) Download the .py files, .bat files, and 'Group Identifier.xlsx'
    
    2) Put all three files in the same root folder (ex. 'C:\\Users\\JoeSchmo\\Desktop\\Stop Signal')
    
    3) Run the .bat file ('Make Folders') by double-clicking. This will create the folders in the directory that are necessary for the program.
       
    4) You will be required to add your own subjects (and their group names!) to the 'Group Identifier.xlsx' spreadsheet. Add those before running any of the other .bat files. In particular, you will need to add to the 'list of acceptable MSN's' column of the spreadsheet in order for the program to recognize all the file types for analysis. Copying and pasting directly directly from the MedPC data file is typically sufficient for this process.
    
    5) Add the data to be analyzed to the 'Data' folder that you made. This is the folder where it knows to look for files.
    
    6) Once all this is setup, the stopsigparser.py script can be run by double-clicking the 'Collect Data Only.bat' file (if you only want the spreadsheet of data) or the 'Graphs and Data.bat' file (if you want the graphs* and spreadsheet). A file should be saved in your 'XL Files' folder everytime, and graphs saved to the 'Figures' folder if you choose to have the graphs made.
    
    7) That's it! Do not forget to update your spreadsheet as you add programs or as you add animals to your study!
    
    
    Notes:
    *Graphing other data type is still in dev as the root MPC program is still in dev. We will complete the graphing utility as it become possible.
          
