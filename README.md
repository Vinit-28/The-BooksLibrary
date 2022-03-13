
This is an internship assignment given by Quixote.

Tech Stack Used:
1. Python-Flask (to create APIs).
1. MongoDB (For Database).



Let us discuss how to use this api :

1. Searching a book

    a. Searching a book by its name or a term in the book's name :
        Type in the url bar = "https://the-bookslibrary.herokuapp.com/search/<book name / term in the book's name>"
        
        Replace "<book name / term in the book's name>" with book's name or term.
    
    b. Searching a book by its author name :
        Type in the url bar = "https://the-bookslibrary.herokuapp.com/search/<author name>"
    
        Replace "<author name>" with book's author name.
    
    c. Searching a book by its category :
        Type in the url bar = "https://the-bookslibrary.herokuapp.com/search/<category / term in the category>"
    
        Replace "<category / term in the category>" with book's category.
    
    d. Searching a book by its rent :
        Type in the url bar = "https://the-bookslibrary.herokuapp.com/search/with-rent/<rent amount>"
    
        Replace "<rent amount>" with book's rent amount.
    
    e. Searching a book by a range of rent :
        Type in the url bar = "https://the-bookslibrary.herokuapp.com/search/with-rent-range/<low>-<high>"
    
        Replace "<low>" with lowest amount of range.
        Replace "<high>" with highest amount of range.
    

2. Issuing a book

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/transactions/issue-book/<bookName>/<personName>/<issueDate>"
    
    Replace "<bookName>" with book's name.
    Replace "<personName>" with your name.
    Replace "<issueDate>" with current date or with the book's issuing date (date format : YYYY-MM-DD).



3. Returning a book

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/transactions/return-book/<bookName>/<personName>/<returnDate>"
    
    Replace "<bookName>" with book's name.
    Replace "<personName>" with your name.
    Replace "<returnDate>" with current date or with the book's returning date (date format : YYYY-MM-DD).



4. To find the usage of a specifc book

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/usage/issued/<bookName>"
    
    Replace "<bookName>" with book's name.
    This will return you two things :
        a. List of people who have issued that book
        b. List of people who currently have that book issued



5. To find the total rent generated by a specifc book

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/usage/total-rent-generated/<bookName>"
    
    Replace "<bookName>" with book's name.
    This will return you the total rent generated by the specified book till date.



6. To find list of books issued to a particular person

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/person-info/<personName>"
    
    Replace "<personName>" with person's name.
    This will return you the list of the books issued by the specified person.



7. To find list of books issued to a particular person

    Type in the url bar = "https://the-bookslibrary.herokuapp.com/book-issued/date-range/<fromDate>/<toDate>"
    
    Replace "<fromDate>" with the date from which you want to find the list of books issued (date format : YYYY-MM-DD).
    Replace "<toDate>" with the date to which you want to find the list of books issued (date format : YYYY-MM-DD).

    This will return you the list of the books issued between the specified dates and the person they are issued to.
