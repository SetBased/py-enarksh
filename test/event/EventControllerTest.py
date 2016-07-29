import unittest
from io import StringIO

from enarksh.event.EventActor import EventActor
from enarksh.event.Event import Event
from enarksh.event.EventController import EventController


class EventControllerTest(unittest.TestCase):
    """
    Test cases for MySqlLoaderWriter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_run_to_completion(self):
        """
        Test each event is processed completely before any other event is processed. And test events are processed in
        the order they are fired.
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def __init__(self, message):
                EventActor.__init__(self)

                self.message = message
                self.event = Event(self)

        class Eggs(EventActor):
            def __init__(self, spam):
                EventActor.__init__(self)
                self.spam = spam

            def handle_event(self, event, again, *_):
                if again:
                    self.spam.event.fire(False)

                out.write('Processing: ' + event.source.message + ' ' + str(again))
                out.write('\n')

        # Create object for firing events.
        spam1 = Spam('spam1')
        spam2 = Spam('spam2')
        spam3 = Spam('spam3')
        spam4 = Spam('spam4')

        # Create objects for handling events. During handling they fire the event again.
        eggs1 = Eggs(spam1)
        eggs2 = Eggs(spam2)
        eggs3 = Eggs(spam3)
        eggs4 = Eggs(spam4)

        # Register event listeners.
        spam1.event.register_listener(eggs1.handle_event)
        spam2.event.register_listener(eggs2.handle_event)
        spam3.event.register_listener(eggs3.handle_event)
        spam4.event.register_listener(eggs4.handle_event)

        # Fire some events before the event loop.
        spam1.event.fire(True)
        spam2.event.fire(True)
        spam3.event.fire(True)
        spam4.event.fire(True)

        # Start the event loop.
        controller.loop()

        actual = out.getvalue()

        expected = """
Processing: spam1 True
Processing: spam2 True
Processing: spam3 True
Processing: spam4 True
Processing: spam1 False
Processing: spam2 False
Processing: spam3 False
Processing: spam4 False
"""

        self.assertEqual(expected.strip(), actual.strip())

# ----------------------------------------------------------------------------------------------------------------------
