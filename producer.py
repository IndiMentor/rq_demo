"""
This module contains the code that schedules task for later decoupled execution by consumer.py
"""
from time import sleep
from consumer import add, mult
from redis import Redis
from rq import Queue
import logging

def main():

    # init logging
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG
        #,        filename="./task.log"
    )

    unfinished_jobs = []
    q = Queue(connection=Redis('everythingmixedmedia.com'))
    logging.info("Created queue")
    logging.info("Filling job queue")
    for num in range(1, 139, 1 ):
        result = q.enqueue(add,num)

        logging.info("\tqueued job Request {} parameter was {}".format(result,num))
        unfinished_jobs.append(result)

    for num in range(139,1,-1    ):
        result = q.enqueue(mult,num)
        logging.info("\tqueued job Request {} parameter was {}".format(result,num))
        unfinished_jobs.append(result)

    logging.info("Now polling for jobs to finish")
    while len(unfinished_jobs) > 0:
        sleep(5)
        logging.info('==============================================================')
        for test_job in unfinished_jobs:
            if test_job.result == None:
                pass
                # logging.info("{} hasn't finished yet".format(test_job))
            else:
                logging.info("{} returned {}".format(test_job,test_job.result))
                unfinished_jobs.remove(test_job)


if __name__ == '__main__':
    main()