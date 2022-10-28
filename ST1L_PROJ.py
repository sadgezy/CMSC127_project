'''
CMSC 127 - File Processing and Database Systems (Laboratory - ST1L)
Project Application:  Task Record System

Description:
A simplified version of your task listing app in your phone (e.g., Samsung Notes,
Google Calendar) where you can list tasks, provide grouping and deadline.

Authors:
    TAMARGO, Senen Zyril D.

Date: 2022-06-04 08:00
'''

# Module Imports
import sys
from xml.etree.ElementTree import TreeBuilder
import mariadb
from datetime import datetime

def connectToMariaDB (pwd):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password=pwd,                                                # INPUT HERE YOUR ROOT PASSWORD
            host="localhost",
            port=3306,
        )
        print("Successfully connected to the MariaDB Platform!")

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor(buffered = True)

    cur.execute("SHOW DATABASES LIKE 'taskdb'")
    result = cur.fetchone()

    if (result is None):
        cur.execute("CREATE DATABASE `taskdb`;")
        cur.execute("USE `taskdb`;")
        cur.execute("CREATE TABLE `category` (`categoryid` int(5) NOT NULL AUTO_INCREMENT, `categoryname` varchar(255) NOT NULL, `task_count` int(5) NOT NULL DEFAULT 0, CONSTRAINT `category_categoryid_pk` PRIMARY KEY (`categoryid`)) ENGINE = InnoDB DEFAULT CHARSET = latin1;")
        cur.execute("CREATE TABLE `task` (`taskid` int(10) NOT NULL AUTO_INCREMENT, `taskname` varchar(255) NOT NULL, `startingdate` date, `enddate` date, `content` varchar(255), `taskstatus` int(1) NOT NULL DEFAULT 0, `categoryid` int(5), CONSTRAINT `task_taskid_pk` PRIMARY KEY (`taskid`), CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category`(`categoryid`) ON DELETE SET NULL) ENGINE = InnoDB DEFAULT CHARSET = latin1;")
    else: cur.execute("USE `taskdb`;")

    return cur, conn

def titleMenu ():
     print("\n======================================")
     print("   _______             __               ")
     print("  |       .---.-.-----|  |--.-----.----.")
     print("  |.|   | |  _  |__ --|    <|  -__|   _|")
     print("  `-|.  |-|___._|_____|__|__|_____|__|  ")
     print("    |:  | ")
     print("    |::.|")
     print("    `---'")
     print("========================================")

def menu ():
    while True:
        titleMenu()
        print("[1] Show Tasks")
        print("[2] Show Categories")
        print("[0] Exit")

        try:
            choice = int(input("Choice: "))
            break
        except ValueError:
            print("Invalid input!")

    return choice

def showTasks (cur, conn):
    try:
        while True:
            statement = "SELECT * FROM task"
            cur.execute(statement)
            counter = 0

            for (taskid, taskname, startingdate, enddate, content, taskstatus, categoryid) in cur:
                if (taskstatus == 0):
                    statusName = 'Not Started'
                elif (taskstatus == 1):
                    statusName = 'Ongoing'
                elif (taskstatus == 2):
                    statusName = 'Completed'
                else:
                    statusName = 'N/A'

                if (counter%2 == 0):
                    print("\n===========================")
                    print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus} ({statusName}) \nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                    print("===========================")
                else:
                    print("\n***************************")
                    print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus} ({statusName}) \nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                    print("***************************")
                counter += 1

            if (counter == 0):
                print("\n")
                print("\tNo Tasks Available!")

            print("\n[1] Add Task")
            print("[2] Edit Task")
            print("[3] Delete Task")
            print("[0] Back")

            try:
                c = int(input("Choice: "))

                if (c == 1): addTask(cur, conn)
                elif (c == 2): 
                    taskid = int(input("\nEnter Task ID: "))
                    editTask(cur, conn, taskid)
                elif (c == 3): deleteTask(cur, conn)
                elif (c == 0): break

            except ValueError:
                print("Invalid input!")

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def getCategoryName (conn, categoryid):
    if categoryid is None:
        return
    cur2 = conn.cursor()
    statement = "SELECT categoryname FROM category WHERE categoryid=" + str(categoryid)
    cur2.execute(statement)
    result = cur2.fetchone()[0]
    if (result is not None):
        return result

def addTask (cur, conn):
    try:
        taskname = input("\nTask title: ")
        content = input("Task description: ")
        while True:
            startingdate = input("Start date (YYYY-MM-DD): ")
            if validDateFormat(startingdate) is True:
                break
        while True:
            enddate = input("End date (YYYY-MM-DD): ")
            if validDateFormat(enddate) is True:
                if validEndDate(startingdate, enddate) is True:
                    break
                else:
                    print("Invalid Entry! End Date earlier than Start Date!")
        while True:
            try:
                    taskstatus = int(input("Task status (0 - Not Started; 1 - Ongoing; 2 - Completed): "))
                    if taskstatus >= 0 and taskstatus <= 2:
                        break
                    else:
                        print('Please enter valid status!')

            except ValueError:
                    print("Provide an integer value...")
                    continue
        statement = "INSERT INTO task (taskname, startingdate, enddate, content, taskstatus) VALUES (%s, %s, %s, %s, %s)"
        data = (taskname, startingdate, enddate, content, taskstatus)
        cur.execute(statement, data)
        conn.commit()
        print("Successfully added entry to database!")
        print(cur.rowcount, "record(s) added.")

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def editTask (cur, conn, taskid):
    try:

        while True:
            statement = "SELECT taskname, startingdate, enddate, content, taskstatus, categoryid FROM task WHERE taskid=%s"
            data = (taskid,)
            cur.execute(statement, data)
            result = cur.fetchone()

            if result is not None:
                statement = "SELECT taskname, startingdate, enddate, content, taskstatus, categoryid FROM task WHERE taskid=%s"
                data = (taskid,)
                cur.execute(statement, data)
                for (taskname, startingdate, enddate, content, taskstatus, categoryid) in cur:
                    print("\n***************************")
                    print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus}\nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                    print("***************************")

                print("\nWhat data will you update?")
                print("[1] Title")
                print("[2] Content")
                print("[3] Start Date")
                print("[4] End Date")
                print("[5] Status")
                print("[6] Add Task to Category")
                print("[0] Back (Save Changes)")

                c = int(input("Enter choice: "))                                    # INT ERROR

                if (c == 1):
                    temp = input("\nEnter New Title: ")
                    statement = "UPDATE task SET taskname=%s WHERE taskid=%s"
                    data = (temp, taskid)
                    cur.execute(statement, data)
                    print("Successfully changed title!")
                elif (c == 2):
                    temp = input("\nEnter New Content: ")
                    statement = "UPDATE task SET content=%s WHERE taskid=%s"
                    data = (temp, taskid,)
                    cur.execute(statement, data)
                    print("Successfully changed content!")
                elif (c == 3):
                    while True:
                        temp = input("Enter New Starting Date (YYYY-MM-DD): ")
                        if validDateFormat(temp) is True:
                            break
                    statement = "UPDATE task SET startingdate=%s WHERE taskid=%s"
                    data = (temp, taskid,)
                    cur.execute(statement, data)
                    print("Successfully changed starting date!")
                elif (c == 4):
                    while True:
                        temp = input("Enter New End Date (YYYY-MM-DD): ")
                        if validDateFormat(temp) is True:
                            print (result[1])
                            if validEndDate(str(result[1]),temp) is True:
                                break
                            else:
                                print("Invalid Entry! End Date earlier than Start Date!")
                    statement = "UPDATE task SET enddate=%s WHERE taskid=%s"
                    data = (temp, taskid,)
                    cur.execute(statement, data)
                    print("Successfully changed end date!")
                elif (c == 5):
                    while True:
                        try:
                            temp = int(input("Enter New Status (0 - Not Started; 1 - Ongoing; 2 - Completed): "))           # INT VALIDATION
                            if temp >= 0 and temp <= 2:
                                statement = "UPDATE task SET taskstatus=%s WHERE taskid=%s"
                                data = (temp, taskid,)
                                cur.execute(statement, data)
                                print("Successfully changed status!")
                                break
                            else:
                                print('Please enter valid status!')

                        except ValueError:
                            print("Provide an integer value...")
                            continue
                elif (c == 6):
                    addTaskToCategory(cur, conn, taskid)
                elif (c == 0):              # Let the changes be permanent
                    conn.commit()
                    print("Successfully modified entry from the database!")
                    break
                else:
                    print("Invalid choice!")
            else:
                print('Task ID not found!')
                break

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def deleteTask (cur, conn):
    try:
        taskid = int(input("\nTask no: "))
        statement = "SELECT taskid FROM task WHERE taskid=%s"
        data = (taskid,)
        cur.execute(statement, data)
        result = cur.fetchone()
        if result is not None:
            statement = "DELETE FROM task WHERE taskid=%s"
            data = (taskid,)
            cur.execute(statement, data)
            conn.commit()
            print("Successfully deleted entry from the database!")
            print(cur.rowcount, "record(s) deleted.")
        else:
            print('Task ID not found!')

    except mariadb.Error as e:
        print('Task ID not found!')

def showCategories (cur, conn):
    try:
        while (True):
            statement = "SELECT * FROM category"
            cur.execute(statement)
            counter = 0

            for (categoryid, categoryname, task_count) in cur:
                if (counter%2 == 0):
                    print("\n===========================")
                    print(f"ID: {categoryid}\tCategory name: {categoryname}\nTask Count: {task_count}")
                    print("===========================")
                else:
                    print("\n***************************")
                    print(f"ID: {categoryid}\tCategory name: {categoryname}\nTask Count: {task_count}")
                    print("***************************")
                counter += 1

            if (counter == 0):
                print("\n")
                print("\tNo Categories Available!")

            print("\n[1] Add Category")
            print("[2] Access/Edit Category")
            print("[3] Delete Category")
            print("[0] Back")

            c = (input("Choice: "))

            if (c == '1'): addCategory(cur, conn)
            elif (c == '2'): editCategory(cur, conn)
            elif (c == '3'): deleteCategory(cur, conn)
            elif (c == '0'): break
            else: print("Invalid choice!")

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def addCategory (cur, conn):
    try:
        categoryname = input("\nCategory name: ")

        statement = "INSERT INTO category (categoryname) VALUES (%s)"
        data = (categoryname,)
        cur.execute(statement, data)
        conn.commit()
        print("Successfully added entry to database!")
        print(cur.rowcount, "record(s) added.")

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def editCategory (cur, conn):
    try:
        categoryid = int(input("\nEnter Category ID: "))                                    # INT ERROR

        while True:
            statement = "SELECT categoryid, categoryname, task_count FROM category WHERE categoryid=%s"
            data = (categoryid,)
            cur.execute(statement, data)
            result = cur.fetchone()
            if result is not None:
                statement = "SELECT categoryid, categoryname, task_count FROM category WHERE categoryid=%s"
                data = (categoryid,)
                cur.execute(statement, data)
                for (categoryid, categoryname, task_count) in cur:
                    print("\n***************************")
                    print(f"ID: {categoryid}\tCategory name: {categoryname}\nTask Count: {task_count}")
                    print("***************************")

                statement = "SELECT * FROM task WHERE categoryid=%s"
                data = (categoryid,)
                cur.execute(statement, data)
                counter = 0

                for (taskid, taskname, startingdate, enddate, content, taskstatus, categoryid) in cur:
                    if (counter%2 == 0):
                        print("\n===========================")
                        print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus}\nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                        print("===========================")
                    else:
                        print("\n***************************")
                        print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus}\nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                        print("***************************")
                    counter += 1

                print("\nWhat data will you update?")
                print("[1] Category Name")
                print("[2] Edit Tasks")
                print("[3] Remove Task from Category")
                print("[0] Back (Save Changes)")

                c = (input("Enter choice: "))

                if (c == '1'):
                    temp = input("\nEnter New Category Name: ")
                    statement = "UPDATE category SET categoryname=%s WHERE categoryid=%s"
                    data = (temp, categoryid,)
                    cur.execute(statement, data)
                    print("Successfully changed name!")
                elif (c == '2'):
                    statement = "SELECT * FROM task WHERE categoryid=%s"
                    data = (categoryid,)
                    cur.execute(statement, data)
                    counter = 0

                    for (taskid, taskname, startingdate, enddate, content, taskstatus, categoryid) in cur:
                        if (taskstatus == 0):
                                statusName = 'Not Started'
                        elif (taskstatus == 1):
                            statusName = 'Ongoing'
                        elif (taskstatus == 2):
                            statusName = 'Completed'
                        else:
                            statusName = 'N/A'
                        if (counter%2 == 0):
                            print("\n===========================")
                            print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus} ({statusName})\nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                            print("===========================")
                        else:
                            print("\n***************************")
                            print(f"ID: {taskid}\nTitle: {taskname}\nStart Date: {startingdate}\tEnd date: {enddate}\nStatus: {taskstatus} ({statusName})\nDescription: {content}\nCategory: {getCategoryName(conn, categoryid)}")
                            print("***************************")
                        counter += 1

                    taskid = int(input("\nEnter Task ID: "))
                    statement = "SELECT categoryid FROM task WHERE taskid=%s"
                    data = (taskid,)
                    cur.execute(statement, data)
                    result = cur.fetchone()

                    if(result is not None):
                        if(result[0] == categoryid):
                            editTask(cur, conn, taskid)
                        else:
                            print("The taskid does not exist in this category!")
                    else:
                        print("The taskid does not exist!")

                elif (c == '3'):                          # EDIT ERROR FOR TASK ID NOT EXISTS
                    taskid = input("Enter Task ID: ")
                    statement = "SELECT * FROM task WHERE taskid=%s"
                    data = (taskid,)
                    cur.execute(statement, data)

                    if (cur.rowcount != 0):
                        removeTaskFromCategory(cur, conn, taskid, categoryid)
                    else:
                        print("Task ID does not exist!")
                elif (c == '0'):              # Let the changes be permanent
                    conn.commit()
                    print("Successfully modified entry from the database!")
                    break
                else:
                    print("Invalid choice!")
            else:
                print('Category ID not found!')
                break

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def deleteCategory (cur, conn):
    try:
        categoryid = (input("\nCategory ID: "))

        statement = "DELETE FROM category WHERE categoryid=(%s)"
        data = (categoryid,)
        cur.execute(statement, data)
        result = cur.fetchone()
        if result is not None:
            conn.commit()
            print("Successfully deleted entry from the database!")
            print(cur.rowcount, "record(s) deleted.")
    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")
        print('Category ID not found!')

def addTaskToCategory (cur, conn, taskid):
    try:
        printCategories(cur)
        categoryid = int(input("\nEnter Category ID: "))
        statement = "SELECT categoryid FROM task WHERE taskid=%s"
        data = (taskid,)
        cur.execute(statement, data)
        result = cur.fetchone()

        if(result[0] != categoryid):
            statement = "UPDATE category SET task_count = task_count + 1 WHERE categoryid=%s"
            data = (categoryid,)
            cur.execute(statement, data)
            conn.commit()
            statement = "UPDATE category SET task_count = task_count - 1 WHERE categoryid=%s"
            data = (result[0],)
            cur.execute(statement, data)
            conn.commit()
            statement = "UPDATE task SET categoryid=%s WHERE taskid=%s"
            data = (categoryid, taskid,)
            cur.execute(statement, data)
            conn.commit()
            print("Successfully added task to category!")
        else:
            print("Unsuccessful. New category is the same with the previous category!")

    except mariadb.Error as e:
        print("Category does not exist!")

def removeTaskFromCategory (cur, conn, taskid, categoryid):
    try:
        statement = "SELECT categoryid FROM task WHERE taskid=%s"
        data = (taskid,)
        cur.execute(statement, data)
        result = cur.fetchone()

        if(result[0] == categoryid):
            statement = "UPDATE category SET task_count = task_count - 1 WHERE categoryid=%s"
            data = (categoryid,)
            cur.execute(statement, data)
            conn.commit()

            statement = "UPDATE task SET categoryid = NULL WHERE taskid=%s"
            data = (taskid,)
            cur.execute(statement, data)
            conn.commit()

            print("Successfully removed task from category!")
        else:
            print("The taskid does not exist in this category!")   

    except mariadb.Error as e:
        print(f"Error retrieving entry from database: {e}")

def validDateFormat (str):
    format = "%Y-%m-%d"
    try:
        datetime.strptime(str, format)
        return True

    except ValueError:
        print(f"Incorrect data format, should be YYYY-MM-DD")
        return False

def validEndDate (start, end):
    try:
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        dateDiff = (end - start).days
        if dateDiff >= 0:
            return True

    except:
        return False

def printCategories (cur):
    statement = "SELECT * FROM category"
    cur.execute(statement)
    counter = 0

    for (categoryid, categoryname, task_count) in cur:
        if (counter%2 == 0):
            print("\n===========================")
            print(f"ID: {categoryid}\tCategory name: {categoryname}\nTask Count: {task_count}")
            print("===========================")
        else:
            print("\n***************************")
            print(f"ID: {categoryid}\tCategory name: {categoryname}\nTask Count: {task_count}")
            print("***************************")
        counter += 1

def main ():
    password = input("Enter root password: ")
    cur, conn = connectToMariaDB(password)

    while True:
        c = menu()

        if (c == 1): showTasks(cur, conn)
        elif (c == 2): showCategories(cur, conn)
        elif (c == 0):
            print("Thank you for using the tasks program!")
            break
        else: print("Invalid input!")

    conn.close()

main()