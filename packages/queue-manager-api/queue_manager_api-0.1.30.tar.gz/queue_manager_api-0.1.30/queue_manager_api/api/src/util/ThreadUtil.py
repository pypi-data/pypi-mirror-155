from python_helper import ObjectHelper, log
from threading import Thread


DEFAULT_TIMEOUT = 20


def runInSimpleThread(target, *args, threadTimeout=DEFAULT_TIMEOUT, **kwargs):
    applicationThread = ApplicationThread(target, *args, threadTimeout=DEFAULT_TIMEOUT, **kwargs)
    applicationThread.run()


class ApplicationThread:

    def __init__(self, target, *args, key=None, threadTimeout=DEFAULT_TIMEOUT, **kwargs):
        self.key = key
        self.running = False
        self.shouldStop = False
        self.thread = Thread(
            target = target,
            args = args,
            kwargs = kwargs
        )
        self.timeout = threadTimeout
        log.debug(self.__init__, f'''Thread "{self.key}" created''')


    def run(self, threadTimeout=DEFAULT_TIMEOUT):
        if not self.isRunning():
            self.thread.start()
            self.running = True
            self.shouldStop = False
            log.debug(self.run, f'''Thread "{self.key}" running''')
        else:
            log.warning(self.run, f'''Thread "{self.key}". "ApplicationThread.run()" called, but it is already running''')
        # self.thread.join(timeout=threadTimeout if ObjectHelper.isNone(self.timeout) else self.timeout)


    def kill(self):
        self.shouldStop = True
        self.running = False
        del self.thread
        self.thread = None
        log.debug(self.kill, f'''Thread "{self.key}" finished''')


    def isRunning(self):
        return (self.isAlive() or self.running) and not self.shouldStop


    def isAlive(self):
        return self.thread.is_alive()


    def shouldStopRunning(self):
        return True and self.shouldStop


    def runItIfItsNotRunningYet(self, threadTimeout=DEFAULT_TIMEOUT):
        if not self.isRunning():
            self.run(threadTimeout=threadTimeout)
