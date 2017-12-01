import time


def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    try:
         while True:
             line = thefile.readline()
             if not line:
                 time.sleep(0.1)    # Sleep briefly
                 continue
             yield line
    except GeneratorExit:
         print "Follow: Shutting down"

logfile  = open("access-log")
loglines = follow(logfile)
for line in loglines:
    print line,
    if i == 10: lines.close()

# Turn the real-time log file into records
logfile  = open("access-log")
loglines = follow(logfile)
log      = apache_log(loglines)

# Print out all 404 requests as they happen
r404  = (r for r in log if r['status'] == 404)
for r in r404:
    print r['host'],r['datetime'],r['request']

# Feed a pipeline from multiple generators in real-time--producing values as they arrive
log1 = follow(open("foo/access-log"))
log2 = follow(open("bar/access-log"))
lines = multiplex([log1,log2])