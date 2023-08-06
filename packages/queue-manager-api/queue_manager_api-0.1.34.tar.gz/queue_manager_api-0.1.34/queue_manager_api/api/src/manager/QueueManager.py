import time

from python_helper import Constant as c
from python_helper import log, ReflectionHelper
from python_framework import Serializer

try:
    import ThreadUtil
except:
    from queue_manager_api.api.src.util import ThreadUtil


DEFAULT_TIMEOUT = 20
QUEUE_MANAGER_KEY = 'queue-manager'


def handleNotRunningThreadDictionary(threadDictionary, threadTimeout=DEFAULT_TIMEOUT):
    while not threadDictionary.isRunning() and not threadDictionary.shouldStopRunning():
        time.sleep(0.1)
    while threadDictionary.isRunning() and not threadDictionary.shouldStopRunning():
        for k in [*threadDictionary.keys()]:
            threadDictionary.get(k).runItIfItsNotRunningYet(threadTimeout=threadTimeout)
            if not threadDictionary.get(k).isAlive():
                threadDictionary.pop(k).kill()
                log.log(handleNotRunningThreadDictionary, f'''Thread "{k}" finished and removed from queue''')
        time.sleep(0.07)
    for k in [*threadDictionary.keys()]:
        threadDictionary.pop(k).kill()
    log.debug(handleNotRunningThreadDictionary, f'Thread dictionary finished running')


class ThreadDictionary(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.shouldStop = False
        log.debug(self.__init__, f'{ReflectionHelper.getName(ThreadDictionary)} created')


    def run(self):
        self.running = True
        self.shouldStop = False


    def isRunning(self):
        return self.running and not self.shouldStop


    def shouldStopRunning(self):
        return True and self.shouldStop


    def kill(self):
        self.shouldStop = True
        self.running = False




class QueueManager:

    def __init__(self, threadTimeout=DEFAULT_TIMEOUT):
        self.threadDictionary = ThreadDictionary()
        self.timeout = threadTimeout
        self.threadDictionaryHandler = ThreadUtil.ApplicationThread(
            handleNotRunningThreadDictionary,
            self.threadDictionary,
            key = QUEUE_MANAGER_KEY,
            threadTimeout = self.timeout
        )
        log.debug(self.__init__, f'{ReflectionHelper.getName(QueueManager)} created')


    def newTimedUuid(self):
        return f'{f"{time.time():0<18}".replace(c.DOT, c.DASH)}{c.DASH}{Serializer.newUuid()}'


    def newMessageKey(self):
        return self.newTimedUuid()


    def new(self, target, *args, **kwargs):
        return ThreadUtil.ApplicationThread(target, *args, **kwargs)


    def runInAThread(self, target, *args, **kwargs):
        thread = self.new(target, *args, key=self.newTimedUuid(), threadTimeout=self.timeout, **kwargs)
        self.threadDictionary[thread.key] = thread
        log.log(self.runInAThread, f'''Thread "{thread.key}" created and added to queue''')


    def addResource(self, api, app):
        api.resource.manager.queue = self
        self.api = api


    def onHttpRequestCompletion(self, api, app):
        ...


    def onRun(self, api, app):
        ...


    def initialize(self, api, app):
        self.threadDictionaryHandler.run()
        self.threadDictionary.run()
        log.success(self.initialize, f'{ReflectionHelper.getClassName(self)} is running')


    def onShutdown(self, api, app):
        self.threadDictionary.kill()
        self.threadDictionaryHandler.kill()
        log.success(self.onShutdown, f'{ReflectionHelper.getClassName(self)} is successfuly closed')
