# Find My OSHI!!! by lowCortisol

## Roster:
- Jun Jie Li (PM):
    - Project manager. Make sure deliverable checkpoints are met.
    - Handle Flask routing and SQLite queries
    - Favorite VTubers button and list of them in home page

- Shafin Kazi:
    - Visualize Data with charts
    - Handle profile organization
    - Handle kaggle dataset downloading logic 
    - Handle creation + population of db
    - Create quiz 
    - Code search and filter functionalities across VTuber pages

- Lucas Zheng:
    - Help create tables for visualization
    - Store picture of tables in folders rather than constant generation
    - Decorate home page with tailwind

- Kyle Liu:
    - Handle templates and site design with Tailwind
    - Link HTML with Jinja for conditional rendering of templates


## Description:
It’s the big 26, and you don’t have a fav VTuber? Look no further! Take a quiz, find your Oshi, view their stats and make a post to share your opinion!
Every VTuber will have a page displaying a photo of their model, a link to their channel, their subscriber count, video count, total/average likes/comments, etc. If they stream, data from their YouTube streams will be displayed, including information on their chatter data (how many unique chatters, unique messages) and their superchat data (unique superchats, revenue by superchats).

#### Visit our live site at [https://oshi4.me/](https://oshi4.me/)

## Install Guide:

Click the green button on the repo, and choose the SSH clone option. Copy the link and open a terminal session. 
```
$ git clone git@github.com:brian38444/lowCortisol.git
$ cd lowCortisol
$ python -m venv ~venv
```
For Linux and Mac users

```
$ source venv/bin/activate
$ pip install -r requirements.txt
```

For Windows users

```
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Steps to Run
1. Create a Kaggle account at [https://www.kaggle.com](kaggle.com)
2. Go to account --> Settings --> Create Legacy API Key which downloads kaggle.json to your machine
3. Move kaggle.json to ~/.kaggle
4. Create a Holodex acccount at [https://holodex.net/](holodex.net)
5. Go to profile ==> Account Settings --> Create + Copy Free API Key
7. In terminal, access project root directory and run the command:

```
~$ export HOLODEX_API_KEY=paste_api_key_here
~$ cd app
~$ python download_datasets.py
~$ python update_pfp.py
~$ python __init__.py
```

## FEATURE SPOTLIGHT
* A quiz to find a matching VTuber for you
* Graphs displaying channel and livestream statistics
* Share your opinions on VTubers with the commenting feature
* Favorite VTubers to easily find and keep track of them later

## KNOWN BUGS/ISSUES
* Placeholder VTuber profile pictures because of outdated dataset
* Deleted YT channels -> Empty profile pages
* Project might not run locally with old python version ?