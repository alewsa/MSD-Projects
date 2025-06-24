''' 
COMP 467 Project 2 The Reckoning
Alyssa Andres

Goal: Create a script that a user is able to parse and input data from a QA CSV into a database
Script will need to use Argparse
Database will be MongoDB (but can be any other DB if you prefer) Mongo is widely used in M&E for it's ease of flexible scheme, completely versatile non-relational DB
Load 2 DB dump exports to two collections in your local database
Use DB to quickly create own reports by using argparse command to flag them  (do this programmatically)
Console output of all runs (minimum 6): Databases, user=kevin chaja, repeatable, blocker, repeatable&blocker, date=2/24/2024
Database Answers (From "Database Calls" and done programmatically i.e python)
List all work done by user "Kevin Chaja"- from both collections(No duplicates)
All repeatable bugs- from both collections(No duplicates)
All Blocker bugs- from both collections(No duplicates)
All Repeatable AND Blocker bugs - from both collections(No duplicates)
All reports on build 2/24/2024- from both collections(No duplicates)
CSV export of user "Kevin Chaja" output from number 1 (I don't care how you format it)
*I also made CSV exports for the different queries (user, repeatable, blocker, repeatable&blocker, date)

'''

import argparse
import pandas as pd
import pymongo
from datetime import datetime #work with dates as date objects

#Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["alewsadatabase"]  #My database
spring_collection = db["Spring2024"]  #Spring 2024 Collection
fall_collection = db["Fall2024"]  #Fall 2024 Collection

def load_data(file_path, collection):  #Loads data from Excel file into MongoDB
    try:
        #Read Excel file into pandas DataFrame
        df = pd.read_excel(file_path)
        records = df.to_dict(orient="records")  #Convert to list of dictionaries
        
        #Insert data into MongoDB and make sure there's no duplicates
        for record in records:
            record.pop("_id", None)  #Remove _id field to prevent duplicates
            if collection.count_documents(record) == 0:  #Check if the record already exists
                collection.insert_one(record)
        
        #Print how many records were added to the collection
        print(f"Loaded {len(records)} records into {collection.name}.") 
    except Exception as e:
        print(f"Error loading {file_path}: {e}")  #Print if there's something wrong loading the file

def query_data(query):  #Query for both collections and remove duplicates
    results = []
    for collection in [spring_collection, fall_collection]:
        for record in collection.find(query):
            #Remove the _id field to check for duplicates based on content
            record.pop("_id", None)
            if record not in results:
                results.append(record)
    return results

def list_user_work(user):  #List all work done by a specific user
    query = {"Test Owner": user}
    user_work = query_data(query)
    print(f"Found {len(user_work)} work records for user '{user}'.")
    return user_work

def list_repeatable_bugs():  #List all repeatable bugs
    query = {"Repeatable?": "Yes"}
    repeatable_bugs = query_data(query)
    print(f"Found {len(repeatable_bugs)} repeatable bugs.")
    return repeatable_bugs

def list_blocker_bugs():  #List all blocker bugs
    query = {"Blocker?": "Yes"}
    blocker_bugs = query_data(query)
    print(f"Found {len(blocker_bugs)} blocker bugs.")
    return blocker_bugs

def list_repeatable_and_blocker_bugs():  #List all repeatable and blocker bugs
    query = {"$and": [{"Repeatable?": "Yes"}, {"Blocker?": "Yes"}]}
    repeatable_and_blocker_bugs = query_data(query)
    print(f"Found {len(repeatable_and_blocker_bugs)} repeatable and blocker bugs.")
    return repeatable_and_blocker_bugs

def list_reports_by_date(build_date):  #List all reports for a specific build date
    try:
        build_date_parsed = datetime.strptime(build_date, "%m/%d/%Y")
        query = {"Build #": build_date_parsed}
        reports_by_date = query_data(query)
        print(f"Found {len(reports_by_date)} reports for build date {build_date}.")
        return reports_by_date
    except ValueError:
        print("Invalid date format. Please use MM/DD/YYYY.") #Print if date format is invalid
        return []

def export_to_csv(data, filename):  #Export query result to a CSV file
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")
    else:
        print("No data to export.")  #Print if no data is found in the Excel file

def main():  #Main function that sets up the argparse and execute user commands
    parser = argparse.ArgumentParser(description="QA Database Tool")

    #Add arguments for different queries
    parser.add_argument("--load", nargs=2, metavar=('SPRING_FILE', 'FALL_FILE'), help="Load Excel data into MongoDB with file paths")
    parser.add_argument("--user", type=str, help="List all work done by a specific user")
    parser.add_argument("--repeatable", action="store_true", help="List all repeatable bugs")
    parser.add_argument("--blocker", action="store_true", help="List all blocker bugs")
    parser.add_argument("--repeatable_blocker", action="store_true", help="List all repeatable AND blocker bugs")
    parser.add_argument("--date", type=str, help="List all reports on a specific build date")
    parser.add_argument("--export", type=str, help="Export results to a CSV file")  #use this for all the other args above to see full results in CSV file
    
    args = parser.parse_args()

    #Load Spring 2024 data and Fall 2024 data when --load is used
    if args.load:
        spring_collection.delete_many({})  #Clear old data
        fall_collection.delete_many({})
        load_data(args.load[0], spring_collection)  #Load Spring data
        load_data(args.load[1], fall_collection)   #Load Fall data

    #Perform queries below based on user input
    if args.user: #--user
        print(f"Work done by {args.user}:")
        user_work = list_user_work(args.user)
        for record in user_work:
            print(record)
        if args.export:
            export_to_csv(user_work, args.export)

    if args.repeatable: #repeatable
        print("Repeatable Bugs:")
        repeatable_bugs = list_repeatable_bugs()
        for record in repeatable_bugs:
            print(record)
        if args.export:
            export_to_csv(repeatable_bugs, args.export)

    if args.blocker: #blocker
        print("Blocker Bugs:")
        blocker_bugs = list_blocker_bugs()
        for record in blocker_bugs:
            print(record)
        if args.export:
            export_to_csv(blocker_bugs, args.export)

    if args.repeatable_blocker: #--repeatable_blocker
        print("Repeatable and Blocker Bugs:")
        repeatable_and_blocker_bugs = list_repeatable_and_blocker_bugs()
        for record in repeatable_and_blocker_bugs:
            print(record)
        if args.export:
            export_to_csv(repeatable_and_blocker_bugs, args.export)

    if args.date: #--date
        print(f"Reports on {args.date}:")
        reports_by_date = list_reports_by_date(args.date)
        for record in reports_by_date:
            print(record)
        if args.export:
            export_to_csv(reports_by_date, args.export)

if __name__ == "__main__":  #Call out the main function
    main()
