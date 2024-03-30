import boto3
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")
aws_access_key_id = config["aws_access_key_id"]
aws_secret_access_key = config["aws_secret_access_key"]
#Create txt file
with open("Result.txt","w") as file:
            file.write("") 
#Connect with aws s3 to get the logFiles                  
s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
#Used when write in txt file to indicates number of log file
logNumber = 0

#The function will take bucket name to retrive all the files
def number_of_lines(bucket_name):  
    #Retrive all files
    objects = s3.list_objects_v2(Bucket="threat-monitor-task")
    #Loop Throw each file to check how mant lines in each file  
    for logFile in objects['Contents']:
        #Logfile to retrive it it take bucket name and file name iwch is the key that comes from s3
        logFile = s3.get_object(Bucket=bucket_name, Key=logFile['Key'])
        #Read the data to start the process
        data = logFile['Body'].read()
        #The text that come from aws s3 is (class, byte) to converted to string we use decode('utf-8')
        string_data = data.decode('utf-8')
        global logNumber
        #Increase each time we read new file
        logNumber = logNumber + 1
        #Write the logfile number in result.txt 
        with open("Result.txt","a") as file:
            file.write("Log Number:"+ str(logNumber) + "\n")
        #This varible for count how many lines in the log file
        lineCount = 0
        #I used built in function from python wihc issplitlines() to split every line the i looped throw evrey line to cunt it
        for line in string_data.splitlines():
            lineCount = lineCount + 1
        #Write lineCount in Result.txt File    
        with open("Result.txt","a") as file:
            file.write("Number Of Lines:"+ str(lineCount) + "\n\n")   
    
    
#call number_of_lines function
number_of_lines("threat-monitor-task")