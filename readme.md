# Fut Calendar
Fut Calendar is a project to save all scheduled matches from a team in a Google Calendar. It runs almost entirely in Google Cloud Platform, automated to fetch matches from [soccerway website](https://soccerway.com/) via Cloud Functions and save it to Google Calendar via Calendar API.

## Website
The website containing the full team list, and the calendar links as well, is currently hosted at [fut-calendar.web.app](https://fut-calendar.web.app). Check it out!

## Google Cloud Project architecture
The project in GCP (Google Cloud Platform) is divided in 5 services:
- Cloud Scheduler
- Cloud Firestore
- Cloud Pub-Sub
- Cloud Functions
- Cloud Tasks

![project diagram](diagram.png?raw=true)

The python scripts runs in 5 Cloud Functions, which are responsible for the whole proccess from fetching matches from the internet to saving it to the calendars:

### function 1: `runAllScrapers`
The first function is triggered every day at 10 am by a **Cloud Scheduler**. This function is only responsible for triggering the second function via a database updation. It calls one instance of function for each team saved in the database.

### function 2: `runScraper`
The second function is triggered by the first function via a database updation under a team document. This function is responsible for scraping the web page from the corresponding team. It fetches the **soccerway** link and scrapes it to get a list of scheduled matches. Finally, it saves all the scheduled matches to the **Firestore Database**. Also, it deletes from the database all the postponed and cancelled matches.

### function 3: `enqueCalendarWriterTask`
The third function is triggered via a database creation, updation or deletion under a match document. Due to [Calendar API quotas](https://developers.google.com/calendar/api/guides/quota), the API access has to managed via **Cloud Tasks**. So this function is responsible for converting the match info to a calendar event and enqueuing the task to write an update to the calendar. The tasks queue will gradually dispatch the functions, ensuring it will be run as soon as possible without exceeding API quotas. In case of limit exceeded, it will use a exponential backoff in order to get into limits again.

### function 4: `insertCalendarEvent`
The fourth function is triggered via task dispatch by the task queue. This function is responsible for accessing the Calendar API to perform an upsertion to an event within the team calendar.

### function 5: `deleteCalendarEvent`
The fifth function, just like the fourth one, is triggered via task dispatch by the task queue. This function is respondible for accessing the Calendar API to delete an event from the team calendar.

## Repository
This repository is divided into 3 folders:
- [admin](#admin-folder)
- [functions](#functions-folder)
- [website](#website-folder)

### admin folder
This folder contains Python scripts to help mantaining the project. It includes services to list teams from a competition, add new teams and create calendars for new added teams. These services are only run by me and don't run in any cloud platform.

### functions folder
This folder contains the source code of the functions deployed to Google Cloud Platform, described 

### website folder
This folder contains the html files deployed to Firebase Hosting. In order to increase website speed and decrease database usage, this project uses static pages. So this folder also includes the Python scripts to access the database once and generate all the html files to be deployed.