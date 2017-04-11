*******************************************
Automating Catalog Tasks : Daily Site Count
*******************************************

This program automates the "daily_site_count" task performed manually by catalog.


gtronel@sheetmusicplus.com
---------------------------------------------------------------------------------

In order to set up the dev environment to run this program, you need:

- python 2.7.x (type "python" in the terminal to see which interpreter is called by default)
- pip 
- virtualenv (to install: $ pip install virtualenv)


Next steps: to clone the project from github and install the dependencies within a virtualenv:

-> Clone "daily_site_count" from the Git repo:
$ cd <path/to/my/project/folder/>
$ git clone <https or ssh clone link on github>

-> Set up a clean virtualenv in a dedicated directory:
1) If one doesn't exist, create a parent directory for all virtualenvs:
$ mkdir ~/venvs
2) Create a clean "daily_site_count" virtualenv in the parent directory:
$ virtualenv --no-site-packages ~/venvs/venv_daily_count

-> Start the virtualenv
$ source ~/venvs/venv_daily_count/bin/activate

-> Install the dependencies
$ pip install -r requirements.txt

-> Run the program:
$ python main.py


----------------------------------------------------------------------------------------------------------
NOTES about setting up and running the program on OPS Server:

This program is schedule to run on the OPS server (Ubuntu) once a day via cron job.
Note that the default python interpreter on OPS is in usr/bin/ (2.6).

Therefore when creating a virtualenv on OPS, we need to point to the correct interpreter in usr/local/bin/ (2.7):
$ virtualenv -p /usr/local/bin/python2.7 --no-site-packages ~/venvs/venv_daily_count


Assuming the project is already cloned locally from Github, and the "venv_daily_count" virtualenv is already 
created in ~/venvs, the last steps needed to run the program are to 1) activate the virtualenv and 2) install the requirements:
$ source ~/venvs/venv_daily_count/bin/activate
$ cd ~/catalog/daily_site_count/
$ pip install -r requirements.txt

To run:
$ python main.py
----------------------------------------------------------------------------------------------------------
