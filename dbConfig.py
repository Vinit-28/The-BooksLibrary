# Importing the required modules #
from dbUtilities import dbUtilities
import urllib

# Making Connection to the Database #
username = urllib.parse.quote_plus("username")
password = urllib.parse.quote_plus("password")
connectionString = ("mongodb+srv://%s:%s@thebookslibrary.elqki.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" % (username, password))
dbUtility = dbUtilities(connectionString = connectionString)
dbUtility.setDBObject("BOOKS")
