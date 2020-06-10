import mysql.connector

from core.const import HOST_ADRESS, USER_NAME, PWD, DB_NAME


print("Creating database ...")
mydb = mysql.connector.connect(
  host=HOST_ADRESS,
  user=USER_NAME,
  passwd=PWD
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE " + DB_NAME)

from core.db import Purbeurre_db
from core.reach_api import OffAPI

print("Reaching API ...")
API = OffAPI()

print("init DB ...")
DB = Purbeurre_db(mode="install")

print("PurBeurre dependencies installed successfuly.")