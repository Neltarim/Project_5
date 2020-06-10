from os import system as sc
import mysql.connector

from core.const import HOST_ADRESS, USER_NAME, PWD, DB_NAME


################# USE "retry" ALIAS TO RESTART ALL THE PROGRAM #################

MODE = "debug" #Change the mode to delete all files from the project directory

mydb = mysql.connector.connect(
  host=HOST_ADRESS,
  user=USER_NAME,
  passwd=PWD
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE " + DB_NAME)

if MODE != "debug":
  res = input("Do you really want to delete PurBeurre ? (YES/no) :")
  if res == "YES":
    sc("rm -rf ../../project_5/")
    
  print("purBeurre is fully deleted, thank you for trying !")