<!-- 
    Author:
    TAMARGO, Senen Zyril D.
-->

**PRELIMINARY INSTRUCTIONS**
Check if you have the following installed in your computer

_Python_
To check:
1. Open a terminal (Command Prompt or Windows Powershell)
2. Type in 'Python' or 'Py'
    * If Python is already installed, it will show you the version you have in your computer
    * If not installed, you can go to this link https://www.python.org/downloads/ , download and install the file

_MariaDB_
To check:
1. Click start in your computer
2. Type in 'MariaDB'
    * If MariaDB is installed, it will be flashed after you type it in
    * If not, go to this link https://mariadb.com/downloads/ , select the OS your computer is running, download and install the file

_MariaDB Connector_
Do this:
1. Open a terminal (Command Prompt or Windows Powershell)
2. Type in this statement 'pip install mysql-connector-python'
3. You are done and ready to use the application

**HOW TO USE THE APPLICATION**
1. Open a terminal (Command Prompt or Windows Powershell).
2. Type in 'python ST1L_PROJ.py' and press Enter.
3. You are now using the application (task pad) and do the things you want to record just like any other task application.

**OTHER IMPORTANT NOTES**
_For the taskdb database_
1. Open your MariaDB terminal
2. Log in as root by typing in 'mysql -u root -p'
3. Enter your root password
    * Always remember your root password
4. Run the task sql dump file by typing in 'source taskdb.sql;'
5. You are now using the taskdb database, a dump file or an initial sample of the application