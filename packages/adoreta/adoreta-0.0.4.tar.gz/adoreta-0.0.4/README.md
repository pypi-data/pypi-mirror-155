# adoreta_log

### installing the package
```
pip install adoreta
```

## Examples:


### Logging your logs
---

Default name of the log file `logs.csv`
```
from adoreta.log import Log

log = Log()
log.write("Please log this text to show this in the future")
```

Custom name of the log file
```
from adoreta.log import Log

log = Log("custom_filename.csv") # any custom file name you want
log.write("This text will go in the custom named file")
```

### Displaying your logs
---

Default logs file display `logs.csv`
```
from adoreta.log import Log

log = Log()
log.show()
```

Custom logs file display
```
from adoreta.log import Log

log = Log("custom_filename.csv")
log.show()
```
