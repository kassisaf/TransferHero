# TransferHero

TransferHero is a tool I wrote to help me find community colleges offering Data Structures courses over Summer 2021.  Without it (and my awesome counselor that provided the csv file that inspired the project) I would have most likely had to wait another semester to transfer.

### How it works
1. Reads in a .csv file containing a list of classes with a specific C-ID.  Classes with the same C-ID are considered equivalent among California Community Colleges (CCC's).  Since my counselor provided this file, usefulness of this project will be limited unless you have access to one of these.
1. Downloads articulation agreements between every school in the list and your specified transfer school and checks the agreement for the course you need
1. Creates a new spreadsheet showing all classes recognized by your transfer school for the specified course, including links to each school's class schedule page.  (Would love to automate class schedule searching but there's no standard search mechanism shared by CCC's, making this non-trivial to implement.)

### What I learned

- How to use Selenium to automate actions for a dynamic webpage that can't easily be parsed (particularly when everything is just a div instead of a more traditional/sensible tag, i.e. bootstrap)
- How to use Python's built-in `csv` library to create a dictionary with key names based on a csv file's first row.  Much cleaner than manually parsing csv and matching values to column indices.
- How to extract text from a PDF file in Python. I'm a little surprised to find that there's not a single ubiquitous library for this that's still maintained, but `PyMuPDF` seems to do alright.  Finding meaningful relationships to the data on the page is a challenge since the PDF format doesn't inherently structure data in natural reading order.  Would like to revisit this problem and find a better solution.
- How to find and process Google search results in Python.  I tried a couple different methods for this.  The obvious `google` package threw exceptions all over the place so I started writing my own solution using `requests` and `beautifulsoup4` until I realized that was against Google's TOS.  Finally I landed on Google's official API package, `google-api-python-client`.  While this requires more setup (registering an API key and a custom search engine), it ensures we can do up to 100 queries per day without having to worry about getting IP banned by Google.
- How to create a local spreadsheet programmatically using `openpyxl`, including some basic font styling and conditional formatting.
