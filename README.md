# wbcusa
WBC dev. 

DEV - CODE ETHIC

Clone this repository and run on your PC/MAC/Linux:
1. Make sure Python 3.6 or later is installed on your computer
2. Make sure MySQL v8 or later is installed on your computer
3. Clone the repository to your local destination and activate virtual env.
4. Install the required packages: pip3 install -r ./requirements.txt
5. Obtain .env file from adminstrator (ME!)
6. Paste .env file to the root directory (same as the manage.py)
7. Run django to test, type: python manage.py runserver
8. Type in localhost:8000/admin, if you see the django admin page, congratulation! you got it.
9. Do not forget to start a new branch before making ANY EDIT!

How to create a new APP
1. Create a new file under the wbcplatform folder. Give the new file a name for the app you want to create.
2. Register the APP in the wbcplatform/wbcplatform/settings.py, INSTALLED_APPS.
3. Add paths in the wbcplatform/wbcplatform/urls.py (if any)
4. Happy coding

DO NOT TOUCH anything in the settings.py (besides register apps), unless you know what you are doing.

