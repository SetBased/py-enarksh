import unittest
from io import StringIO

import gc

from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor
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

    # ------------------------------------------------------------------------------------------------------------------
    def test_deletion1(self):
        """
        Test event actors are removed from the event system.
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def __init__(self, name):
                EventActor.__init__(self)

                self.name = name
                self.event = Event(self)

            def __del__(self):
                out.write('Deleting ' + self.name)
                out.write('\n')

            def handle_event(self, *_):
                pass

        # Create object for firing events.
        spam1 = Spam('spam1')
        spam2 = Spam('spam2')
        spam3 = Spam('spam3')

        # Register event listeners in a nice loop.
        spam1.event.register_listener(spam2.handle_event)
        spam2.event.register_listener(spam3.handle_event)
        spam3.event.register_listener(spam1.handle_event)

        # And a self loop.
        spam1.event.register_listener(spam1.handle_event)

        # Fire some events before the event loop.
        spam1.event.fire(True)
        spam2.event.fire(True)
        spam3.event.fire(True)

        # Start the event loop.
        controller.loop()

        # Remove the objects (actually the variables).
        del spam1
        del spam2
        del spam3

        actual = out.getvalue()

        # The objects are still referenced by the event system. So, we don't expect any deletions.
        expected = ''

        self.assertEqual(expected.strip(), actual.strip())

    # ------------------------------------------------------------------------------------------------------------------
    def test_deletion2(self):
        """
        Test event actors are removed from the event system.
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def __init__(self, name):
                EventActor.__init__(self)

                self.name = name
                self.event = Event(self)

            def __del__(self):
                out.write('Deleting ' + self.name)
                out.write('\n')

            def handle_event(self, *_):
                pass

        # Create objects for firing events.
        spam1 = Spam('spam1')
        spam2 = Spam('spam2')
        spam3 = Spam('spam3')

        # Register event listeners in a nice loop.
        spam1.event.register_listener(spam2.handle_event)
        spam2.event.register_listener(spam3.handle_event)
        spam3.event.register_listener(spam1.handle_event)

        # And a self loop.
        spam1.event.register_listener(spam1.handle_event)

        # Fire some events before the event loop.
        spam1.event.fire(True)
        spam2.event.fire(True)
        spam3.event.fire(True)

        # Start the event loop.
        controller.loop()

        # Remove the objects (actually the variables).
        del spam1
        gc.collect()
        del spam2
        gc.collect()
        del spam3
        gc.collect()

        actual = out.getvalue()

        expected = """
Deleting spam1
Deleting spam2
Deleting spam3
"""

        self.assertEqual(expected.strip(), actual.strip())

    # ------------------------------------------------------------------------------------------------------------------
    def test_register(self):
        """
        Test event listeners can be registered multiple times for the same event.
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def __init__(self, name):
                EventActor.__init__(self)

                self.name = name
                self.event = Event(self)

            def handle_event(self, event, event_data, listener_data):
                out.write(event.source.name + ' ' + event_data + ' ' + listener_data)
                out.write('\n')

        # Create objects for firing events.
        spam1 = Spam('spam1')
        spam2 = Spam('spam2')

        # Register event listeners in a nice loop.
        spam1.event.register_listener(spam2.handle_event, 'spam')
        spam1.event.register_listener(spam2.handle_event, 'eggs')

        # Fire some events before the event loop.
        spam1.event.fire('event 1')

        # Start the event loop.
        controller.loop()

        actual = out.getvalue()

        expected = """
spam1 event 1 spam
spam1 event 1 eggs
"""

        self.assertEqual(expected.strip(), actual.strip())

    # ------------------------------------------------------------------------------------------------------------------
    def test_event_queue_empty(self):
        """
        Test event_queue_empty
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def __init__(self, n):
                EventActor.__init__(self)
                self.n = n

                self.event = Event(self)

            def handle_event(self, *_):
                if self.n:
                    out.write(str(self.n))
                    out.write('\n')
                    self.event.fire()
                    self.n -= 1
                else:
                    out.write('Ignition ...')

        # Create object for firing events.
        spam = Spam(10)

        # Register event listener
        controller.event_queue_empty.register_listener(spam.handle_event)

        # Start the event loop.
        controller.loop()

        actual = out.getvalue()

        expected = """
10
9
8
7
6
5
4
3
2
1
Ignition ...
"""

        self.assertEqual(expected.strip(), actual.strip())

    # ------------------------------------------------------------------------------------------------------------------
    def test_with_empty_queue(self):
        """
        Test start with empty queue.
        """
        out = StringIO()

        controller = EventController()

        class Spam(EventActor):
            def handle_event(self, even, event_data, listener_data):
                out.write(listener_data)
                out.write('\n')

        # Create object for firing events.
        spam = Spam()

        # Register event listener
        controller.event_loop_start.register_listener(spam.handle_event, 'event_loop_start')
        controller.event_loop_end.register_listener(spam.handle_event, 'event_loop_end')
        controller.event_queue_empty.register_listener(spam.handle_event, 'event_queue_empty')

        # Start the event loop.
        controller.loop()

        actual = out.getvalue()

        expected = """
event_loop_start
event_queue_empty
event_loop_end
"""

        self.assertEqual(expected.strip(), actual.strip())

        # ------------------------------------------------------------------------------------------------------------------
        def test_with_none_empty_queue(self):
            """
            Test start with empty queue.
            """
            out = StringIO()

            controller = EventController()

            class Spam(EventActor):
                def __init__(self):
                    EventActor.__init__(self)

                    self.event = Event(self)

                def handle_event(self, even, event_data, listener_data):
                    out.write(listener_data)
                    out.write('\n')

            # Create object for firing events.
            spam = Spam()

            # Register event listener
            controller.event_loop_start.register_listener(spam.handle_event, 'event_loop_start')
            controller.event_loop_end.register_listener(spam.handle_event, 'event_loop_end')
            controller.event_queue_empty.register_listener(spam.handle_event, 'event_queue_empty')
            spam.event.register_listener(spam.handle_event, 'spam')

            # Fire an event.
            spam.event.fire()

            # Start the event loop.
            controller.loop()

            actual = out.getvalue()

            expected = """
    event_loop_start
    spam
    event_queue_empty
    event_loop_end
    """

            self.assertEqual(expected.strip(), actual.strip())

    # ------------------------------------------------------------------------------------------------------------------
    def test_destroy_event_multiple_times(self):
        """
        Test destroying an event 2 times has no side effects.
        """
        controller = EventController()

        class Spam(EventActor):
            def __init__(self):
                EventActor.__init__(self)

                self.event = Event(self)

            def handle_event(self, *_):
                pass

        # Create object for firing events.
        spam = Spam()

        # Register event listener
        spam.event.register_listener(spam.handle_event)

        # Start the event loop.
        controller.loop()

        gc.collect()

        # Expect no exception.
        self.assertTrue(True)

# ----------------------------------------------------------------------------------------------------------------------
