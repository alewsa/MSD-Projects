# MSD-Projects
Projects from my Multimedia System Design Class. 

QA Script

Goal: 
1. Create a script that a user is able to parse and input data from a QA CSV into a database. Script will need to use Argparse. Database will be MongoDB (but can be any other DB if you prefer) Mongo is widely used in M&E for it's ease of flexible scheme, completely versatile non-relational DB
2. Load 2 DB dump exports to two collections in your local database
3. Use DB to quickly create own reports by using argparse command to flag them  (do this programmatically)
4. Console output of all runs (minimum 6): Databases, user=kevin chaja, repeatable, blocker, repeatable&blocker, date=2/24/2024
5. Database Answers (From "Database Calls" and done programmatically i.e python)
6. List all work done by user "Kevin Chaja"- from both collections(No duplicates)
7. All repeatable bugs- from both collections(No duplicates)
8. All Blocker bugs- from both collections(No duplicates)
9. All Repeatable AND Blocker bugs - from both collections(No duplicates)
10. All reports on build 2/24/2024- from both collections(No duplicates)
11. CSV export of user "Kevin Chaja" output from number 1 (I don't care how you format it)
**I also made CSV exports for the different queries (user, repeatable, blocker, repeatable&blocker, date)

Tools used:
1. argparse for user commands such as --user, --load, --repeatable, --blocker, --repeatable_blocker, --date, and --export.
2. MongoDB via pymongo for database to connect, store, and query QA data. 
3. pandas to read Excel files and write CSV files.
4. datetime to work with dates as date objects.

VFX Tools Script

Goal: 
1. Create the script using argparse to run via commandline. Script should be able to do each/all requests from ffmpeg:
   a. -Watermarking (WM) - name of file
   b. -Gif creation (GC)
   c. -Thumbnail creation (TC) - you choose size
   d. -Metadata export (ME)
2. Rename each new file processed per the request and version the number up or new file are created with v01
   a. Ex: Bath_VFX_v01 -> Bath_VFX_v02
   b. Ex2: gif will probably be GC_VFX_v01

Tools used: 
1. argparse for user commands such as --file, --folder, --watermark, --thumbnail, --gif, and --metadata.
2. os lets Python program interact with your computer's files and folders — like opening, creating, or listing them.
3. re lets Python program find and work with patterns in text, like spotting version numbers in filenames.
4. ffmpeg for applying watermark onto images.
5. PIL (Pillow) for opening, resizing, and saving images, thumbnails, and gifs.

Marks Automation Script

Goal: 
1. Revisit Proj 1
2. Add argparse to input baselight file (--baselight),  xytech (--xytech) from proj1
3. Populate new database with 2 collections: One for Baselight (Folder/Frames) and Xytech (Workorder/Location) 
4. Download Demo reel: https://mycsun.box.com/s/wy1sit1vne1gmg8l1psbbyetp73ls4hf
5. Run script with new argparse command --process <video file>  
6. From (5) Call the populated database from (3), find all ranges only that fall in the length of video from (4)
7. Using ffmpeg or 3rd party tool of your choice, to extract timecode from video and write your own timecode method to convert marks to timecode
8. New argparse--output parameter for XLS with flag from (5) should export same CSV export as proj 1 (matching xytech/baselight locations), 
   but in XLS with new column from files found from (6) and export their timecode ranges as well
9. Create Thumbnail (96x74) from each entry in (6), but middle most frame or closest to. Add to XLS file to it's corresponding range in new column 
10. Render out each shot from (6) using (7) and upload them using API to Vimeo (see slide 11)
11. Create CSV file and show all ranges/individual frames that were not uploaded from  (10) (so show location and frame/ranges)

Tools used:
1. argparse for user commands such as --baselight, --xytech, --process, and --output.
2. os lets Python program interact with your computer's files and folders — like opening, creating, or listing them.
3. time for pausing script during retries or file checks 
4. csv for writing unused frame data into a CSV file
5. MongoDB via pymongo for database to connect, store, and query Baselight and Xytech data.
6. ffmpeg for grabbing image frames.
7. PIL (Pillow) for opening, resizing, and saving images, thumbnails, and gifs.
8. vimeo for uploading clips to a Vimeo account via API.
9. openpyxl for creating Excel files and embedding images inside the file.
10. openpyxl.utils + openpyxl.drawing.image	for adjusting Excel column widths and adding thumbnails to cells.
