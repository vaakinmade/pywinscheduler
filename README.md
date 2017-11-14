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
As they are a few dependencies this application uses, it isn't advisable to let them roam freely in your universal python path. Be sure to activate a virtualenv before proceeding beyond this point. See [virtualenv](https://docs.python.org/3/library/venv.html) to get cracking.
#### 1. Pywin32
The win32 API for writing windows os applications, are notoriously tricky to get going for python. However, you are sure to avoid murky waters if you follow this guide.

##### Using a .whl file
Download wheel files from [Pypi](https://pypi.python.org/pypi/pypiwin32/219) for versions < 3.6. Wheel files for 3.6+ can found [here](https://pypi.python.org/pypi/pypiwin32). Be sure that your .whl version isn't only appropriate for the python version but also its bit (32 or 64) version to avoid errors. Confirm the bit version in the first line of the banner in your python shell.

Navigate to the .whl file via cmd prompt, and install it using pip
```python
pip install pypiwin32-219-cp34-none-win_amd64
```

From within the confinements of your virtualenv, install the dependencies from the requirements file
```
pip install -r requirements.txt
```
#### Pycairo inst

## 

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

