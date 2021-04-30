# TransferHero

TransferHero is a tool I wrote to help me find community colleges offering Data Structures courses over Summer 2021.  Without it (and my awesome counselor who provided the csv file that inspired the project) I would almost certainly have had to wait another semester to transfer.

## What does it actually do?
1. Reads in a .csv file containing a list of classes with a specific C-ID. *(Classes with the same C-ID are considered equivalent among California Community Colleges)*.
1. Creates a new spreadsheet with only the columns we care about, along with hyperlinks to each school's class schedule page, plus some conditional formatting to highlight courses based on their confirmed availability.
1. Downloads and parses articulation agreements and removes any courses that are not recognized by your transfer school

Unfortunately almost every school seems to use a different system for their class schedules, so I have to check course availability manually.  TransferHero just makes that process faster and less tedious.

Given enough time, I could create automation profiles for each school's schedule system to confirm course availability, but the amount of work that would require is currently outside the scope of the project.  

## What I learned

#### How to use Selenium to automate data retrieval from unparsable webpages
Assist.org is an amazing resource, but it lacks a public API, hides most of its elements behind AJAX calls, and uses ng-bootstrap which means just about everything is a div instead of a more sensible/descriptive HTML tag.  Parsing it would be difficult or impossible, but Selenium allows us to render the page in an actual browser and simulate human-like interaction to get to the data we need.

### How to create local spreadsheets programmatically using `openpyxl`
Including hyperlinks, basic styling, and conditional formatting rules.

### How to extract text from a PDF file in Python
This one's a bit of a mess.  I was surprised to find that there's not a single ubiquitous Python lib for this that's still maintained, but `PyMuPDF` seems to do alright.  Finding meaningful relationships to the data on the page is a challenge since the PDF format doesn't inherently structure data in natural reading order.  Would like to revisit this problem to find a better solution.

### How to use Python's built-in `csv` module to create a dictionary with key names based on a csv file's first row.
Much cleaner than manually parsing csv and matching values to column indices.

### How to find and process Google search results in Python
I tried several different methods for this:

- The `google` package on pypi was a mess and threw exceptions all over the place.  Didn't bother to debug.
- Instead I wrote my own solution using `requests` and `beautifulsoup4` until I realized that scripting and scraping search results is against Google's TOS
- Next I tried Google's official API package, `google-api-python-client`.  Requires some setup (registering a project with Google, generating an API key, and creating a "Custom Search Engine"). After all that, we're only allowed to make 100 queries a day for free.
- Ultimately I settled on generating "I'm Feeling Ducky" links which just take you to the first result from DuckDuckGo.  This ended up being the fastest solution and also the easiest to implement.
