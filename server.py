# Importing the required modules #
from flask import Flask, jsonify
import re
from dbConfig import *


# Instaniating the App # 
app = Flask(__name__)



# ---------------------- Utility Functions ---------------------- #

# Function to format the result from mongoDBResultObject to python dictionary object //
def formatResult(mongoDBResultObject):

    resultObject = {}
    resultIndex = 1
    for result in mongoDBResultObject:
        resultObject[resultIndex] = result
        resultIndex += 1
    
    return resultObject


# Function to calculate number of times a specific book is issued by the specific person #
def NumberOfTimesBookIssued(bookName, personName):
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksIssued")
    return dbUtility.collectionObject.count_documents({"bookName" : bookName, "personName" : personName})


# Function to calculate number of times a specific book is returned by the specific person #
def NumberOfTimesBookReturned(bookName, personName):
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksReturned")
    return dbUtility.collectionObject.count_documents({"bookName" : bookName, "personName" : personName})


# Function to check whether a book can be issued or not #
def isBookReadyToBeIssued(bookName, personName):

    if NumberOfTimesBookIssued(bookName = bookName, personName = personName) == NumberOfTimesBookReturned(bookName = bookName, personName = personName):
        return True
    else:
        return False


# Function to check whether a book can be returned by a person or not #
def isBookReadyToBeReturned(bookName, personName):

    if NumberOfTimesBookIssued(bookName = bookName, personName = personName) == (NumberOfTimesBookReturned(bookName = bookName, personName = personName) + 1):
        return True
    else:
        return False


# Function to find and return the last issued date of a book by a specific person #
def getBookLastIssuedDate(bookName, personName):
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksIssued")
    lastIssueRecord = dbUtility.collectionObject.aggregate(
        [
            {
                "$match" : {
                    "bookName" : bookName,
                    "personName" : personName,
                }
            },
            {
                "$group":{
                    "_id" : "null",
                    "lastIssuedDate" : {
                        "$max" : "$issueDate"
                    }
                }
            }
        ]
    ).next()

    return lastIssueRecord['lastIssuedDate']


# ---------------------- Utility Functions (END) ---------------------- #




# ---------------------- Routing Functions ---------------------- #

# Searching books by their names, author names, category (strings) #
@app.route('/search/<searchKey>')
def searchBooksWithString(searchKey):
    dbUtility.setDBObject("BOOKS")
    dbUtility.setCollectionObject(collectionName = "registeredBooks")
    queryResult = dbUtility.collectionObject.find(
        {
            "$or":[
                {
                    "bookName": re.compile(searchKey, re.IGNORECASE)
                },  
                {
                    "authorName": re.compile("^"+searchKey+"$", re.IGNORECASE)
                },  
                {
                    "category": re.compile(searchKey, re.IGNORECASE)
                }  
            ] 
        },
        {
            "_id":0
        }
    )

    return jsonify(formatResult(queryResult))



# Searching books by rent #
@app.route('/search/with-rent/<int:rent>')
def searchBooksWithRent(rent):
    dbUtility.setDBObject("BOOKS")
    dbUtility.setCollectionObject(collectionName = "registeredBooks")
    queryResult = dbUtility.collectionObject.find(
        { 
            "rent": rent
        },
        {
            "_id":0
        }
    )

    return jsonify(formatResult(queryResult))



# Searching books by the range of rent #
@app.route('/search/with-rent-range/<int:low>-<int:high>')
def searchBooksWithRentRange(low, high):
    dbUtility.setDBObject("BOOKS")
    dbUtility.setCollectionObject(collectionName = "registeredBooks")
    queryResult = dbUtility.collectionObject.find(
        { 
            "rent": {
                "$gte" : low,
                "$lte" : high
            }
        },
        {
            "_id":0
        }
    )
    return jsonify(formatResult(queryResult))
    

# Issuing a book #
@app.route("/transactions/issue-book/<string:bookName>/<string:personName>/<string:issueDate>")
def issueBook(bookName, personName, issueDate):
    
    result = {}
    if isBookReadyToBeIssued(bookName = bookName, personName = personName):
        dbUtility.issueBook(bookName = bookName, personName = personName, issueDate = issueDate)
        result = {
            "isBookIssued" : "True",
            "Message" : "Book is issued successfully !!!"
        }
    else:
        result = {
            "isBookIssued" : "False",
            "Message" : "Book is already issued to you !!!"
        }
    return jsonify(result)



# Returning a book #
@app.route("/transactions/return-book/<string:bookName>/<string:personName>/<string:returnDate>")
def returnBook(bookName, personName, returnDate):
    
    result = {}
    if isBookReadyToBeReturned(bookName = bookName, personName = personName):
        issueDate = getBookLastIssuedDate(bookName = bookName, personName = personName)
        totalRent = dbUtility.returnBook(bookName = bookName, personName = personName, returnDate = returnDate, issueDate = issueDate)
        result = {
            "isBookReturned" : "True",
            "message" : "Book is Returned successfully !!!",
            "totalRentToBePaid" : totalRent
        }
    else:
        result = {
            "isBookIssued" : "False",
            "Message" : "Book is not issued to you !!!"
        }
    return jsonify(result)


# Book Usage (Total Issuing)#
@app.route("/usage/issued/<string:bookName>")
def bookUsageTotalIssuing(bookName):
    
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksIssued")
    result = {'Total Issuing of this Book' : {}, 'Current Issuing of this Book' : {}}
    totalIssuing = dbUtility.collectionObject.find({ "bookName":bookName }, {"_id":0})
    totalIssuingCopy = totalIssuing.__copy__()
    
    bookIndex = 1
    for book in totalIssuing:
        result['Total Issuing of this Book'][bookIndex] = book
        bookIndex += 1
    

    dbUtility.setCollectionObject("transactionsMade")
    bookIndex = 1
    for book in totalIssuingCopy:

        if dbUtility.collectionObject.count_documents({"bookName" : book['bookName'], "issueDate" : book['issueDate'], "personName" : book['personName']}) == 0:
            result['Current Issuing of this Book'][bookIndex] = book
            bookIndex += 1
    
    return jsonify(result)


# Book Usage (Total Rent Generated)#
@app.route("/usage/total-rent-generated/<string:bookName>")
def bookUsageTotalRentGenerated(bookName):
    
    result = {
        "bookName" : bookName,
        "totalRentGenerated" : dbUtility.getTotalRentGeneratedByTheBook(bookName = bookName)
    }    
    return jsonify(result)


# Person Info #
@app.route("/person-info/<string:personName>")
def personInfo(personName):
    
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksIssued")
    totalIssuing = dbUtility.collectionObject.find({ "personName":personName }, {"_id":0})
    result = {
        "List of books issued and returned" : {},
        "List of books issued but not returned yet" : {}
    }    
    issuedAndReturned, issuedButNotReturned = 1,1
    dbUtility.setCollectionObject('transactionsMade')

    for book in totalIssuing:

        if dbUtility.collectionObject.count_documents({"bookName" : book['bookName'], "issueDate" : book['issueDate'], "personName" : personName}) == 0:
            result['List of books issued but not returned yet'][issuedButNotReturned] = book
            issuedButNotReturned += 1
        else:
            result['List of books issued and returned'][issuedAndReturned] = book
            issuedAndReturned += 1

    return jsonify(result)



# List of books issued between range of dates #
@app.route("/book-issued/date-range/<string:fromDate>/<string:toDate>")
def bookIssuedInDateRange(fromDate, toDate):
    
    dbUtility.setDBObject("TRANSACTIONS")
    dbUtility.setCollectionObject("booksIssued")
    queryResult = dbUtility.collectionObject.find(
        { 
            "issueDate": {
                "$gte" : fromDate,
                "$lte" : toDate
            }
        },
        {
            "_id":0
        }
    )
    result = {}    
    bookIndex = 1
    for book in queryResult:
        result[bookIndex] = book
        bookIndex += 1

    print("n\n\n", fromDate, "\t\t", toDate, "\n\n\n")
    return jsonify(result)


# Root Endpoint #
@app.route('/')
def home():
    
    result = {
        "Opening Greeting" : "Welcome to the-bookslibrary API",
        "Motive" : "This is to Manage a library",
        "How to use" : "https://github.com/Vinit-28/The-BooksLibrary#readme",
        "Ending Greeting" : "Have a good day !"
    }
    return jsonify(result)


# ---------------------- Routing Functions (END) ---------------------- #


if __name__ == "__main__":
    app.run(debug=False)
