# FootyAlert
Got sick of repeatedly going on the bbc results page so I wrote an EPL and Man Utd fixture inboxer. Wrapped it in a windows service to run the scheduling job as a native OS task.

Will be looking to write in some international fixtures support as well, especially since Nigeria's punched their Russia '18 ticket.

## Steps
1. Request is fired off to football-data.org's amazing API, gets a bunch of stuff I am interested in.
2. JSON response is then crunched, undergoes timezone conversion operations yada yada
3. Relevant data is formatted into html (painful, boring) and saved to disk
4. Custom pseudo-email server reads the html file from disk, opens smtp conn, encrypts the content with tls before mailing off
5. Python scheduler wraps all the above steps as a single job and runs it at scheduled intervals
6. A Windows service written to turn the scheduler into a native OS task. App is now viewable from task manager like any other app.

## TO-DOs
- unit tests
- a bit of design glossing maybe, maybe not 

Full docs coming in a bit. 
