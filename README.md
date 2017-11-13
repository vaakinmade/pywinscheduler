# FootyAlert
Got sick of repeatedly going on the bbc results page so I wrote an EPL and Man Utd fixture inboxer. Wrapped it in a windows service to run the scheduling job as a native OS task. Being a native windows service, footy-alert is configurable to automtically come on during windows start up.

Will be looking to write in some international fixture support as well, especially since Nigeria's punched their Russia '18 ticket.

## Steps
1. Request is fired off to football-data.org's amazing API, gets a bunch of data I am interested in.
2. JSON response is then crunched, undergoes timezone conversion operations etc.
3. Large response datasets are stored in a redis hash so as to adhere to throttling limitations, and for performance reasons.
4. Relevant data is painfully formatted into good old html and saved to disk.
5. Team crests are converted from svg to png images as the former is not supported by gmail.
6. The new png files are hurled up into AWS S3 making accessible to gmail.
7. Custom pseudo-email server reads the html file from disk, establishes an smtp conn with gmail client, and encrypts the content with tls before mailing off.
8. Python scheduler wraps all the above steps as a single job which it runs at scheduled intervals
9. A Windows service turns the scheduler into a native OS task. App is now viewable from service manager like any other windows service.

## TO-DOs
- unit tests
- a bit of design glossing maybe, maybe not 

