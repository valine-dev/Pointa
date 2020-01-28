import asyncio
import threading


class DynamicEventLoop:
    '''Creating a thread runs the event loop that can insert coroutine dynamically.
    '''

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        thread: threading.Thread = None
    ):
        'Define a loop and run it in a seperate thread'

        # Creating Event Loop
        if loop is not None:
            self.loop = loop
        else:
            try:
                self.loop = asyncio.get_event_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)

        # Creating thread
        if thread is not None:
            self.thread = thread
        else:
            self.thread = threading.Thread(
                target=lambda x: x.run_forever(),
                args=(self.loop,)
            )

        self.taskList = {}
        self.temp = [None, None]

    def run(self):
        'Starting Event Loop'
        self.thread.start()

    def append(self, mark, coroutine):
        '''Returns the list of tasks
        Append a coroutine to eventloop
        mark can be **Anything**
        coroutine should be a coroutine
        '''
        self.taskList.update(
            {
                mark: self.loop.create_task(coroutine)
            }
        )
        # Send updated signal to loop
        self.loop._csock.send(b'\0')
        return self.taskList

    def pop(self, mark):
        '''Returns the result of the marked task
        Delete the marked task in loop'''
        try:
            self.taskList.pop(mark).cancel()  # Cancel the task
        except KeyError:
            return 'Incorrect Mark!'
