Chickenswell Readme
=========

Chickenswell Flask server for notes and shenanigans

Installation
-----

1. Clone project
2. Install dependencies `python -m pip install -r requirements.txt`
     * It is recommanded to setup a venv first
     * Project was made on python 3.8.3
     * Also install less dependencies, `npm install less -g`
3. Make .env file in base dir
     * File is simply named '.env' (unless specified otherwise in config.py)
     * Should contain:
         * `SECRET_KEY='somelongandrandomchainofcharacters'`
         * `LESS_BIN=C:/Users/Sanchez/AppData/Roaming/npm/lessc` (only for development, not needed if css is already compiled, find via `> which lessc` or `> where lessc`)
         * `IS_PROD=False` or `IS_PROD=False`
         * `DRIVE_FOLDER_ID = 46gdg78g23w324r` Drive ID of the folder where files create by the app will be stored.
4. Edit config.py 
     * Should mostly be fine as long as .env is set up correctly
5. Get credentials from google to allow Drive sync
     * Place `credentials.json` in chickenflask/home.
     * Follow Google instructions to allow API access.
     * If unable to add notes, try running drivesync.get_binaries_from_id() from console to force the auth process.
     * If problems persist, try deleting token.pickle to force refresh.
6. Init database by running dbsetup.py
     * Create a User. Most functionalities require the user to be logged in.
     * If desired, create base note categories.
7. Run test server or deploy to prod!

Note: Markdown menu option expects a note entry named 'Markdown'. Create one (in any category/subcategory) or edit home/routes.py to avoid 404.


Notes
---

User must be logged in to view or manage notes.

Notes are fetched from Google Drive api using their sharable links. To get the link to a specific file:

* Open in browser and copy address.
* Select 'get link' from drive interface
* On windows, right click on file and select `Google Drive > Copy link to clipboard` (Requires Backup and Sync) 

Each note entry belongs to a subcategory, and each subcatogy to a category. Names are unique for each field (e.g. two note entries cannot share the same name even if they belong to different categories).

Use Manage Notes to add or delete items.

Notes content is downloaded when first added. Click 'Force Update' on note view footer to update. Updates will be automated in a future version.

Supported file types:

* .txt and .md wil be rendered as markdown 
* MS Word (.docx) and google doc files will be converted to html


TODO
----

* less css
* Split notes in new app
* Better db models and management
* Auto-update drive file based on last_updated
* Text editor!
