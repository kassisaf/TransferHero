# TransferHero

TransferHero is a tool I wrote to help me find a community college that was offering Data Structures over the Summer.  Without it I may have had to wait another semester to transfer.

### How it works
It doesn't (yet)!

### What I learned

- How to use Selenium to automate actions for a website that can't easily be parsed using simple requests due to literally everything being a div instead of a more sensible tag (thanks bootstrap!)
- How to use the built-in csv library to handle parsing csv into a dictionary with key names based on what's in the header row
- How to extract text from a PDF file in Python. I'm a little surprised to find that there's not a single ubiquitous library for this that's still maintained, but `PyMuPDF` seems to do alright.  Finding meaningful relationships to the data on the page is a challenge since the PDF format doesn't inherently structure data in natural reading order.  Would like to learn more about solving this problem.
- How to find and process Google search results in Python.  I tried a couple different methods for this.  The obvious `google` package threw exceptions all over the place so I started writing my own solution using `requests` and `beautifulsoup4` until I realized that was against Google's TOS.  Finally I landed on Google's official API package, `google-api-python-client`.  While this requires more setup (registering an API key and a custom search engine), it ensures we can do up to 100 queries per day without having to worry about getting IP banned by Google.
- How to create a local spreadsheet using `openpyxl`