Chickenswell
=========

Chickenswell Flask server for notes and shenanigans

Installation
-----

1. Pull / Merge whatever
2. Install dependencies `python -m pip install -r requirements.txt`
3. Make .env file in base dir
     * File is simply named '.env' (unless specified otherwise in config.py)
     * Should contain `SECRET_KEY='somelongandrandomchainofcharacters'`
4. Edit config.py
     * Set IS_PRODUCITON to True if prod
     * Rest should be fine
5. Get credentials from google to allow Drive sync
     * Place `credentials.json` in chickenflask/home
     * Follow Google instructions to allow API access
     * If unable to add notes, try running drivesync.get_binaries_from_id() from console to force the auth process.
6. Init database by running dbsetup.py
     * Create a User.
     * If desired, create base note categories.
7. Run test server or deploy to prod!

Note: Markdown menu option expects a note entry named 'Markdown'. Create one (in any category/subcategory) or edit home/routes.py to avoid 404.
