# Importing the required modules #
import pymongo
import dns
from datetime import date


# class to perfrom operations in database #
class dbUtilities():

    # Initializing Database Configs #
    def __init__(self, connectionString, dbName=None):
        self.collectionObject = None
        self.connectionString = connectionString 
        self.mongoDbClientObject = pymongo.MongoClient(connectionString)
        self.dbObject = None
        if dbName != None:
            self.dbObject = self.mongoDBClientObject[dbName]
    
    # Pointing to new database #
    def setDBObject(self, dbName):
        self.dbObject = self.mongoDbClientObject[dbName]

    # Pointing to new collection in the current database #
    def setCollectionObject(self, collectionName):
        self.collectionObject = self.dbObject[collectionName]

    # Adding books in the database #
    def addBooks(self, listOfBooks):
        self.collectionObject.insert_many(listOfBooks)
    
    # Issuing book for a person #
    def issueBook(self, bookName, personName, issueDate):
        self.setDBObject("TRANSACTIONS")
        self.setCollectionObject("booksIssued")
        self.collectionObject.insert_one({
            "bookName" : bookName,
            "personName" : personName,
            "issueDate" : issueDate,
        })
    
    # converting string base date to DateTime Object #
    def convertStringToDateObject(self, stringDate):
        [y, m, d] = map(int, stringDate.split('-'))
        return date(y, m, d)


    # Recording the transaction in the database (when the book is returned)#
    def makeTransaction(self, bookName, personName, issuedDate, returnDate, totalRent):
        self.setDBObject("TRANSACTIONS")
        self.setCollectionObject("transactionsMade")
        self.collectionObject.insert_one({
            "bookName" : bookName,
            "personName" : personName,
            "issueDate" : issuedDate,
            "returnDate" : returnDate,
            "totalRent" : totalRent,
        })


    # Making entry in the database for the book returned by a person #
    def returnBook(self, bookName, personName, returnDate, issueDate):
        self.setDBObject("TRANSACTIONS")
        self.setCollectionObject("booksReturned")
        self.collectionObject.insert_one({
            "bookName" : bookName,
            "personName" : personName,
            "returnDate" : returnDate,
        })
        self.setDBObject("BOOKS")
        self.setCollectionObject("registeredBooks")
        perDayRent = self.collectionObject.find_one({"bookName":bookName})['rent']
        end = self.convertStringToDateObject(returnDate)
        start = self.convertStringToDateObject(issueDate)
        totalRent = (perDayRent * ((end-start).days+1))
        self.makeTransaction(bookName = bookName, personName = personName, issuedDate = issueDate, returnDate = returnDate, totalRent = totalRent)
        return totalRent
    

    # Calculating the total rent generated by a particular book #
    def getTotalRentGeneratedByTheBook(self, bookName):
        self.setDBObject("TRANSACTIONS")
        self.setCollectionObject("transactionsMade")
        totalRentGenerated = 0
        queryResult = self.collectionObject.aggregate(
            [
                {
                    '$match':{
                        "bookName" : bookName
                    }
                },
                {
                    '$group':{
                        '_id' : '$_id',
                        'totalRentGenerated' : {
                            '$sum' : '$totalRent'
                        }
                    }
                }
            ]
        )

        try :
            totalRentGenerated = queryResult.next()['totalRentGenerated']
        except:
            pass
        return totalRentGenerated