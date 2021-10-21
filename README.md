# Med_Ass_Chamber_Parsers_For_Greg

**The code 'stopsigparser' is a script written to run along with the .bat file to parse stop signaling programs created by Gregory Simandl (Marquette University).**

**HOW TO USE THE CODE:**

    1) Download the .py, .bat, and 'Group Identifier.xlsx'
    
    2) Put all three files in the same root folder (ex. 'C:\\Users\\JoeSchmo\\Desktop\\Stop Signal')
    
    3) Within the root folder, two folders need to be added with the following names:
      a) 'Data'
      
      b) 'XL Files'
      
    4) The overall file structure should look like this:
    
      a) 'Main' (Or whatever you want to call this one)
      
          |
          
          --> stopsigparser.py
          
          --> launchparser.bat
          
          --> Group Identifier.xlsx
          
          --> 'Data' (FOLDER)
          
                |
                
                --> ALL THE MPC DATA FILES YOU WANT TO PARSE GO HERE!
                
          --> 'XL FILES' (FOLDER)
          
                |
                
                --> WHERE THE EXCEL FILE WITH THE PARSED DATA WILL BE SAVED! YOU CAN FIND YOUR COMPILED DATA HERE!
                
    5) You will be required to add your own subjects (and their group names!) to the 'Group Identifier.xlsx' spreadsheet.
    
    6) You will also be required to add your program names to the 'Group Identifier.xlsx' spreadsheet. The program names are what MedPC calls 'msns'. Copying and pasting directly        directly from the MedPC data file is typically sufficient for this process.
    
    7) Once all this is setup, the stopsigparser.py script can be run by double-clicking the launchparser.bat file. A file should be saved in your 'XL Files' folder located in the same root folder as the .py and .bat scripts.
          
