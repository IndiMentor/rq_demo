# RQ

## Todo

* ~~define a pattern so infrastructure can be deployed in any app 
fairly easily.~~
* ~~Have pool of workers running continuously ***config file***~~
* ~~Have pool restart when machine reboots ***supervisord***~~
* ~~Define mechanism for starting real pool of n workers 
***supervisord***~~
* ~~Define mechanism for deploying tasks that will be run on the queue 
could be from multiple projects. ***module search paths***  Ideally 
specified in some generic way which allows you to have multiple 
directories one for each project / initiative  ~~
* ~~configure results to stay around for a day~~

### Steps

* ~~install supervisor according to [this][1]~~
* ~~create settings.py & supervisor configuration according to [this][2]
and [this][3]~~
* ~~use sudo supervisorctl to start / stop etc~~
* ~~view log files in /var/log/supervisor~~
* ~~Path for task moduoles in settings file so can deploy multiple 
projects~~
* ~~tasks are added to rq_tasks direcotry under devel~~

[1]: https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps
[2]: http://python-rq.org/patterns/supervisor/
[3]: http://python-rq.org/docs/workers/ 

## using

Client-side i.e. the web app/producer

* pip install rq
* create queue & enqueue job
```
q = Queue(connection=Redis('emm.com'))
result = q.enqueue(add,num)

# check if job finished and if so what result
if test_job.result == None:
```
Note results only stay around for 1 day before auto expiring so if 
you need them make sure to check them

Tasks which are rmeote executed should be written ina seperate module
.  This should be uploaded to the task server and placed in
 the devel/rq_tasks directory.  Note dependencies will need to be 
 installed in the rq virtualenv
 
## How it works

Using rq to enable async job execution.

Three main parts:

1. producer.py - this puts jobs in the queue
2. Consumer.py - this executes the jobs
3. Queue Infrastructure  - installed on emm.com, this has the queues.

### Producer.py

Import from consumer module which contains all the methods that can 
be queued

Create a connection to the queue using Redis object
Enqueue a pointer to the function and it's parms
Result is a job id that can be used to check status

When all queued, check for completions by verifying job.result
if it is None job hasn't finished. else it's return value from job
Keep going until all done

### consumer.py

A module that if imported by both the producer and the queue manager 
which contains the jobs that may be queued

All jobs that need to be submitted need to be defined in here 
(defined or visible anyway)

### Queue Infrastructure

Consists of the Redis database (, listening on 6387, emm
.com via bind statement in /etc/redis.conf) installed on server along
with the python s/w including the rq s/w (for rq workers) & consumer
.py s/w which contains the enqueued jobs.
 
The queue is really worker processes installed as part of rq and 
which import consumer.py, for details of what to do.
 
workers are started with rq worker command in a directory which also
has consu,er.py so it can be imported and the tasks run.
  
settings.py is part of queue infrastructure, it tells a worker what 
redis / queue to use
   
    rq commands
     RQ command line tool.

    Options:
      --help  Show this message and exit.
    
    Commands:
      empty    Empty given queues.
      info     RQ command-line monitor.
      requeue  Requeue failed jobs.
      resume   Resumes processing of queues, that where...
      suspend  Suspends all workers, to resume run `rq...
      worker   Starts an RQ worker.

Redis restarts on server reboot rq worker doesn't 



 
