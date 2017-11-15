# FootyAlert
Got sick of repeatedly going on the bbc results page so I wrote an EPL and Man Utd fixture inboxer. Wrapped it in a windows service to run the scheduling job as a native OS task. Being a native windows service, footy-alert can be configured to automtically come on during windows start up. It sends the fixtures and results to your inbox as scheduled without you lifting a finger.

Will be looking to write in some international fixture support as well, especially since Nigeria's punched their Russia '18 ticket.

## Installation
[Python 3.4+](https://www.python.org/downloads/) is required.

Clone the git repo
```
git clone https://github.com/vaakinmade/footy-alert.git
```

### Dependencies

##### Pycairo
Pycairo is required by cairosvg which this application uses to convert the football team crests images from svg to png. Using Christopher Gohlke's [libraries](https://www.lfd.uci.edu/~gohlke/pythonlibs/), download the appropriate pycairo .whl file for python version and bit version. Confirm your python bit version from the welcome banner in the python shell.

From the confines of your virtualenv, install the .whl file
```python
pip install pycairo-1.15.2-cp34-cp34m-win_amd64.whl
```

Install the other dependencies
```
pip install -r requirements.txt
```


## Steps
1. Request is fired off to football-data.org's amazing API, gets a bunch of data we are interested in.
2. JSON response is then crunched and undergoes timezone conversion operations.
3. Large response datasets are stored in a redis hash so as to adhere to football-data's throttling limitations, and also for performance reasons.
4. Relevant data is painfully formatted into good old html and written to file.
5. Team crests are converted from svg to png images as the former is not supported by gmail.
6. The new png files are hurled up into AWS S3 making it accessible to gmail.
7. Custom pseudo-email server reads the html file from disk, establishes an smtp conn with gmail client, and encrypts the content with tls before mailing off.
8. Python scheduler wraps all the above steps as a single job which it runs at scheduled intervals
9. A Windows service turns the scheduler into a native OS task. App is now viewable from service manager like any other windows service.

## TO-DOs
- unit tests
- a bit of design glossing maybe, maybe not 

