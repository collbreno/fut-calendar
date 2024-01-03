# fut-calendar
This is a python project to add soccer games automatically to your calendar. I'm currently running it on my own machine and maintaining some teams up-to-date. You can view the full list here.

## Running it yourself
### Step 1: Setting up the Google Calendar API
In ordering to run this project, you must set up a google project and activate the Google Calendar API. You can follow the instructions [here](https://developers.google.com/calendar/api/quickstart/python).

### Step 2: Install python libraries required

### Step 3: Edit the settings.json
The settings.json file contains all the info needed to create and update team's matches. You have to customize it this way:
```
{
    "team": "Fluminense",
    "matches_url": "https://br.soccerway.com/teams/brazil/fluminense-football-club/312/matches/",
    "calendar_id": "primary"
}
```