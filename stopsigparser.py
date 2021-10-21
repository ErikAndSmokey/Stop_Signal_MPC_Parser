#The Art VanDeLay imports/exports... but more imports than exports... and that's his problem
import pandas as pd
import os
import re
from itertools import chain
from datetime import date
import numpy as np


main_file_branch = 'ENTER YOUR FILE PATH HERE! Ex --> C:\\Users\\JoeSchmo\\Desktop\\StopSignal'

#The directory where the data files are that you want to analyze
path_to_data = main_file_branch + '\\Data\\'


#These functions work for all file types... note the "specific" functions below
class MainInfoParser():
    
    def __init__(self,file,dates_list,start_time_list,subjects_list,msn_list,day_list):
        self.file = file
        self.dates = dates_list
        self.start = start_time_list
        self.subjects = subjects_list
        self.msns = msn_list
        self.days = day_list
        
    
    def maininfograbber(self):
        with open(self.file,"r") as f:
            datefinder = re.search(r"Start Date:" + ".+" + "\n",f.read())
            dategrabber = datefinder.group().split(":")
            self.dates.append(pd.to_datetime(dategrabber[1].strip()).date())
        with open(self.file,"r") as f:
            subjectfinder = re.search(r"Subject:" + ".+" + "\n", f.read())
            subjectgrabber = subjectfinder.group().split(":")
            self.subjects.append(subjectgrabber[1].strip())
        with open(self.file,"r") as f:
            msnfinder = re.search(r"MSN:" + ".+" + "\n", f.read())
            msngrabber = msnfinder.group().split(":")
            self.msns.append(msngrabber[1].strip())
        with open(self.file,"r") as f:
            paradigmfinder = re.search(r"Experiment:" + ".+" + "\n",f.read())
            paradigmgrabber = paradigmfinder.group().split(": ")
            self.days.append(paradigmgrabber[1].strip())
        with open(self.file,"r") as f:
            startfinder = re.search(r"Start Time:" + ".+" + "\n",f.read())
            startgrabber = startfinder.group().split(": ")
            self.start.append(pd.to_datetime(startgrabber[1].strip()).time())
            
            
    #Moved as static methods w/n class for namespace purposes- both are considered main info, but a small subset
    @staticmethod
    def msngrabber(file):
        with open(file,"r") as f:
            msnfinder = re.search(r"MSN:" + ".+" + "\n", f.read())
            msngrabber = msnfinder.group().split(":")
            return msngrabber[1].strip()
    @staticmethod
    def dayofparadigm(file):
        with open(file,"r") as f:
            paradigmfinder = re.search(r"Experiment:" + ".+" + "\n",f.read())
            paradigmgrabber = paradigmfinder.group().split(": ")
            return paradigmgrabber[1].strip()

        

class ArrayParser():
    
    def __init__(self,file,array_to_append,upper_delimiter,lower_delimiter):
        self.file = file
        self.array_to_ap = array_to_append
        self.upper = upper_delimiter
        self.lower = lower_delimiter


    def arraygrabber(self):
        with open(self.file,"r") as f:
            arrayfinder = re.search(fr"\n{self.upper}:", f.read())
            arraystart = arrayfinder.start()
        with open(self.file,"r") as f:
            arrayendfinder = re.search(fr"\n{self.lower}:", f.read())
            arrayend = arrayendfinder.start()
        with open(self.file,"r") as f:
            arrayfull = (f.read()[arraystart:arrayend + 1])
            arraystrip = arrayfull.strip(" ")
            arraysplitnewline = arraystrip.split("\n")
            arrayformat1 = (i.strip(" ") for i in arraysplitnewline)
            arrayformatcolumn = [re.split(r"\s{2,8}",i) for i in arrayformat1]
        return self.array_to_ap.append(list(chain.from_iterable(i[1:] for i in arrayformatcolumn)))


    def endarraygrabber(self):
        with open(self.file,'r') as f:
            arrayfinder = re.search(fr'\n{self.upper}:', f.read())
            arraystart = arrayfinder.start()
        with open(self.file,'r') as f:
            arrayfull = (f.read()[arraystart:])
            arraystrip = arrayfull.strip(" ")
            arraysplitnewline = arraystrip.split('\n')
            arrayformat1 = (i.strip(' ') for i in arraysplitnewline)
            arrayformat2 = [re.split(r'\s{2,8}',i) for i in arrayformat1]
            return self.array_to_ap.append(list(chain.from_iterable(i[1:] for i in arrayformat2)))

#Lists for capturing data!
dates = []
starttimes = []
subjects = []
msns = []
paradigms= []
stop_correct = []
go_trial_latencies = []
go_trial_q1 = [] 
go_trial_q2 = []
go_trial_q3 = []
go_correct = []

#Grab group identifiers AND grab acceptable msn names
dfgroups = pd.ExcelFile(main_file_branch+'\\Group Identifier.xlsx').parse() #FILE PATH!
control_name = dfgroups.keys()[0] #Handles group ID name changes
experimental_name = dfgroups.keys()[1] #Handles group ID name changes
listofcontrols = [str(i).upper() for i in dfgroups[control_name]] #Because df to df comparisons weren't working...
listofexps = [str(i).upper() for i in dfgroups[experimental_name]] #Because df to df comparisons weren't working...
accepted_msns = [str(i).upper() for i in dfgroups['Acceptable MSNs']]
accepted_msns.pop()


#Main loop --> operates outside of def main() so it runs without instantiating python --> stopsigparser.main()
for i in os.listdir(path_to_data):
    file = path_to_data + i
    msn_check = MainInfoParser.msngrabber(file)
    if msn_check.upper() in accepted_msns:
        main_info = MainInfoParser(file,dates,starttimes,subjects,msns,paradigms)
        main_info.maininfograbber()
        delay_lengths_pre = []
        find_delays = ArrayParser(file, delay_lengths_pre, 'T','V')
        find_delays.arraygrabber()
        delay_lengths_pre = [float(x) for i,x in enumerate(delay_lengths_pre[-1]) if i != 0 and float(x) > 0.0]
        stop_latencies = []
        find_stop_lat = ArrayParser(file, stop_latencies, 'Z', 'NONE')
        find_stop_lat.endarraygrabber()
        stop_latencies = [float(x) for i,x in enumerate(stop_latencies[-1][1:len(delay_lengths_pre)+1])]
        if stop_latencies.count(0.0) == 0:
            stop_correct.append(0)
        else:
            stop_correct.append(stop_latencies.count(0.0)/len(delay_lengths_pre)*100)
        total_go_trials = []
        find_go_total = ArrayParser(file, total_go_trials, 'G','H')
        find_go_total.arraygrabber()
        total_go_trials = int(float(total_go_trials[-1][0]))
        go_trials = []
        find_gos = ArrayParser(file, go_trials, 'X','Z')
        find_gos.arraygrabber()
        go_trials =[float(i) for i in go_trials[-1][1:total_go_trials+1]]
        go_trial_latencies.append(sum(go_trials)/len(go_trials))
        go_trial_q1.append(np.percentile(go_trials,25))
        go_trial_q2.append(np.percentile(go_trials,50))
        go_trial_q3.append(np.percentile(go_trials,75))
        correct_gos = []
        find_correct_gos = ArrayParser(file, correct_gos, 'D','E')
        find_correct_gos.arraygrabber()
        correct_gos = int(float(correct_gos[-1][0]))
        go_correct.append(correct_gos/total_go_trials*100)
    else:
        pass

    
#Create a dictionary that will be used to make the pd.DataFrame    
df_maker = {'Subject':subjects,
           'Date': dates,
           'Start Time': starttimes,
           'Program': msns,
           'Day of Stop Signal': paradigms,
            'Go Trial % Correct': go_correct,
            'Avg. Go Trial Latency (secs)': go_trial_latencies,
            'Go Trial Latency Q1 (secs)':go_trial_q1,
            'Go Trial Latency Q2 (secs)(median)': go_trial_q2,
            'Go Trial Latency Q3 (secs)': go_trial_q3,
           'Stop Sig % Correct': stop_correct}

#Create dataframe and sort the values by subject/date
df = pd.DataFrame(df_maker)
df.sort_values(['Subject', 'Date'], ascending = (True, True), inplace = True)


#Create a 'day number' column by animal (i.e., see what day of the paradigm each individual animal is on)
range_by_animal = [] #This is a list for collecting all the day numbers- needs to be after the sort
for i in df.groupby('Subject'):
    x = range(1,len(i[1])+1)
    for num in x:
        range_by_animal.append(num)
df.insert(1,'Day Number', range_by_animal)


#Code for assigning a group type to each animal --> uses dfgroup that was created before the main loop
group_column = []
for i in df['Subject']:
    if i.upper() in listofcontrols:
        group_column.append(dfgroups.columns[0]) #You can change the names of the columns to match the study!
    elif i.upper() in listofexps:
        group_column.append(dfgroups.columns[1]) #You can change the names of the columns to match the study!
    else:
        group_column.append('NaN') #Because we need to match the df lengths
        print(f'{i} is not in your Group Identifier spreadsheet!!!! Please Check!!!')
df.insert(0,'Group', group_column)


#Set the index to be the subject, elimating the autogenerated DataFrame index
df.set_index('Subject', inplace=True)


#Create a file save path and save a sheet/animal in a workbook for easy data visualization
data_save = main_file_branch+f'\\XL Files\\Stop Signal Data from {date.today()}.xlsx'
with pd.ExcelWriter(data_save) as writer:
    for i,x in df.groupby('Subject'):
        x.to_excel(writer, sheet_name = i)
    df.groupby('Group').mean().to_excel(writer, sheet_name = 'AVERAGES')