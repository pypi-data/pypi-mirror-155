# MCLogger: Multi color logger to log to screen and file



## MCLogger to log to file AND to the console

### What problem does this solve?
A challenge for web-server applications (e.g. such as Flask) is to decipher what's going on from a long logging window.  The standard loggers are all single color console test which you have to trawl through manually one by one.

MCLogger helps to solve this by colorising the debug, info, warning, into different colors so that it is much easier to read.  The logger will output to both on screen and also a file

### How does it do this?
MCLogger builds on the logging library and adds console color libraries to add colors to debug, info, error, warning entries

* DEBUG - blue
* WARNING - yellow
* ERROR - red
* INFO - cyan

### How to install?
MCLogger is avaialble through PyPi and you may use pip:

```
	pip install mclogger
```

Or, through git:
```
	git clone https://github.com/pub12/mclogger.git
```



### How to use the logger?
The logger is super easy to use.  You need to simply create an instance and add a file/filepath for the logfile

```
from mclogger import MCLogger

filename = 'log_file.txt'
logger = MultiLogger(filename).getLogger()

logger.debug("hello world - debug")
logger.info("hello world - info")
logger.error("hello world - error")
logger.warning("hello world - warning")
```
Output will be:
![Output for mclogger](https://github.com/pub12/mclogger/blob/master/readme/mclogger.png)

### Class Methods overview

- #### getLogger(*filename*):
	Generates the log instance which can be called with .debug(*message*); .info(*message*); .error(*message*); .info(*message*) which will be displayed in color format.

	Format of the output message will be: 
		"`<current server timestamp> [<Filename and line number - function name()>] [<DEBUG | INFO | WARN | ERROR >] - < Message >`"

	- *filename* - filename with optional relative of optional filepath - e.g. `temp/log_file.txt`

- #### read_log_file(*last_n_rows = 20*):
	Return in an array the `last_n_rows` in an array in the order listed within the file.  This will include the color codes for the message

	- *last_n_rows* - Number of lines to read

- #### read_log_file_as_text(*last_n_rows = 20*):
	Return in an array the `last_n_rows` in an array in the order listed within the file.  This will have color codes removed

	- *last_n_rows* - Number of lines to read