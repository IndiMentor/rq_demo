# RQ

## Todo

* define a pattern so infrastructure can be deployed in any app 
fairly easily.
* Have pool of workers running continuously
* Have pool restart when machine reboots
* Define mechanism for starting real pool of n workers
* Define mechanism for deploying tasks that will be run on the queue 
could be from multiple projects.


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

Consists of the Redis database (no password, listening on 6387, emm
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



 
