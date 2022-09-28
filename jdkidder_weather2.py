#Jack Kidder
#CS195 
""" This program merges data from 8 different files into 2 regional dataframes and eventually
into merged csv and text files shwoing the differences in average temperature and percipitation. """
import pandas as pd

#This function loads the regions files into a dataframe
def load_region_files_into_dframe(files, variables):
    #Reads each column into a different dataframe
    df1 = pd.read_csv(files[0], skiprows=4)
    df2 = pd.read_csv(files[1], skiprows=4)
    df3 = pd.read_csv(files[2], skiprows=4)
    df4 = pd.read_csv(files[3], skiprows=4)

    #Creates a dataframe to hold all data
    out = pd.DataFrame()
    #Loads each dataframe as a column into the new one
    out['Date'] = df1['Date']
    out[variables[0]] = df1['Value']
    out[variables[1]] = df2['Value']
    out[variables[2]] = df3['Value']
    out[variables[3]] = df4['Value']

    #Return the dataframe with all the columns
    return out


#Function compares average temperatures both regions during a specified month, and writes them to a file
def compare_monthly_avg_temps(reg1DF,reg2DF,month,file):

    #Shows all average tempuratures for the month of april across all years in region 1
    aprilDF1 = reg1DF[reg1DF.Date.astype("str").str[4:6] == month]

    #Shows all average tempuratures for the month of april across all years in region 1
    aprilDF2 = reg2DF[reg2DF.Date.astype("str").str[4:6] == month]

    #Create dataframe to hold both regions averages during the same months and the difference
    averageDF = pd.DataFrame()
    averageDF['Date'] = aprilDF1['Date']
    averageDF['r1_tavg'] = aprilDF1['tavg']
    averageDF['r2_tavg'] = aprilDF2['tavg']
    averageDF['difference'] = ((reg1DF['tavg']) - (reg2DF['tavg'])).round(2)

    averageDF.to_csv(file,index=False)

    #Find the average of the difference
    average = averageDF['difference'].mean()

    #Open the file and write the newly discovered average difference in it
    f = open(file,"a")
    f.write(f'For the month of April during years 1900-2022, on average, Region2 is {average:.1f} degrees warmer than Region1')
    f.close()


#Finds the month with the highest average rainfall and returns the total average for that month
def most_annual_precip(dataframe):

    #Find the maximum value in the pcp column
    maximum = dataframe['pcp'].max()

    #determine which month the highest datapoint occurred in
    month = str(dataframe[dataframe.pcp == maximum].iloc[0]['Date'])[4:6]

    #Puts all datapoints from that month into a dataframe
    maxMonth = dataframe[dataframe.Date.astype("str").str[4:6] == month]

    #Finds the average percipitation from that month
    average = maxMonth['pcp'].mean()

    #Returns a tuple of the month and its average percipitation
    return month, average



#Creates a csv file with all the data in an organized form
def create_merged_csv(reg1DF,reg2DF):

    #Creatd a new dataframe to merge the data
    mergeDF = pd.DataFrame()
    #Specify each column of the new data frame and fill it
    mergeDF['Date'] = reg1DF['Date']
    mergeDF['r1_tmin'] = reg1DF['tmin']
    mergeDF['r2_tmin'] = reg2DF['tmin']
    mergeDF['r1_tmax'] = reg1DF['tmax']
    mergeDF['r2_tmax'] = reg2DF['tmax']
    mergeDF['r1_tavg'] = reg1DF['tavg']
    mergeDF['r2_tavg'] = reg2DF['tavg']
    mergeDF['r1_pcp'] = reg1DF['pcp']
    mergeDF['r2_pcp'] = reg2DF['pcp']

    #to_csv function prints the database to the newly created csv
    mergeDF.to_csv("Merge.csv",index=False)


#Recognizes an integer as a reference to a specific month
def month_int_to_name(num):
    #Declare numstring as a string of the parameter
    numString = str(num)
    #Declare month as a default blank value
    month = ""
    #Check numString to see which month its number matches with
    if (numString == "01"):
        month = "January"
    if (numString == "02"):
        month = "February"
    if (numString == "03"):
        month = "March"
    if (numString == "04"):
        month = "April"
    if (numString == "05"):
        month = "May"
    if (numString == "06"):
        month = "June"
    if (numString == "07"):
        month = "July"
    if (numString == "08"):
        month = "August"
    if (numString == "09"):
        month = "September"
    if (numString == "10"):
        month = "October"
    if (numString == "11"):
        month = "November"
    if (numString == "12"):
        month = "December"
    #Return a string of the month chosen
    return month

def main():
    vermont = load_region_files_into_dframe(['10-pcp-all-6-1900-2022.csv', '10-tmax-all-6-1900-2022.csv',
        '10-tavg-all-6-1900-2022.csv','10-tmin-all-6-1900-2022.csv'],['pcp', 'tmax', 'tavg', 'tmin'])
    idaho = load_region_files_into_dframe(['43-pcp-all-6-1900-2022.csv', '43-tmax-all-6-1900-2022.csv',
        '43-tavg-all-6-1900-2022.csv','43-tmin-all-6-1900-2022.csv'],['pcp', 'tmax', 'tavg', 'tmin'])
    create_merged_csv(vermont, idaho)
    compare_monthly_avg_temps(vermont, idaho, '04','Monthly data comp.txt') 
    month, precip = most_annual_precip(vermont)
    print(f'In Vermont, historically {month_int_to_name(month)} has had the most precipitation with avg of {precip:.2f} inches')

main()