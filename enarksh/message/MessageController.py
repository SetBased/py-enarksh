"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from time import sleep

import zmq

from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor
from enarksh.message.Message import Message


class MessageController(EventActor):
    """
    A message controller for receiving messages and firing the appropriate events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        EventActor.__init__(self)

        Message.message_controller = self

        self._zmq_context = zmq.Context()
        """
        The ZMQ context.

        :type: None|zmq.Context
        """

        self._message_types = {}
        """
        All registered message types. A dict from message type to the event that must fire when a message of
        that message type has been received.

        :type: dict[str,enarksh.event.Event.Event]
        """

        self._end_points = {}
        """
        All registered end points.

        :type: dict[str,zmq.sugar.socket.Socket]
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_points(self):
        """
        Returns all end points.

        :rtype: dict[str,zmq.sugar.socket.Socket]
        """
        return self._end_points

    # ------------------------------------------------------------------------------------------------------------------
    def register_end_point(self, name, socket_type, end_point):
        """
        Registers an end point.

        :param str name: The name of the end point.
        :param int socket_type: The socket type, one of
                                - zmq.PULL for asynchronous incoming messages
                                - zmq.REP for lockstep incoming messages
                                - zmq.PUSH for asynchronous outgoing messages
        :param str end_point: The end point.
        """
        socket = self._zmq_context.socket(socket_type)
        self._end_points[name] = socket
        if socket_type in [zmq.PULL, zmq.REP]:
            socket.bind(end_point)
        elif socket_type == zmq.PUSH:
            socket.connect(end_point)
        else:
            raise ValueError("Unknown socket type {0}".format(socket_type))

    # ------------------------------------------------------------------------------------------------------------------
    def register_message_type(self, message_type):
        """
        Registers a message type together with the event and message constructor.

        :param str message_type: The message type to register.
        """
        self._message_types[message_type] = Event(self)

    # ------------------------------------------------------------------------------------------------------------------
    def get_event_by_message_type(self, message_type):
        """
        Returns the event that will be fired when a message a certain message type is been received.

        :param str message_type: The messaged type

        :rtype: enarksh.event.Event.Event
        """
        if message_type not in self._message_types:
            raise ValueError("Unknown message type '{0}'".format(message_type))

        return self._message_types[message_type]

    # ------------------------------------------------------------------------------------------------------------------
    def register_listener(self, message_type, listener, listener_data=None):
        """
        Registers an object as a listener for the event fired when a message has been received.

        :param str message_type: The message type.
        :param callable listener: An object that listen for an event.
        :param * listener_data: Additional data supplied by the listener destination.
        """
        self.get_event_by_message_type(message_type).register_listener(listener, listener_data)

    # ------------------------------------------------------------------------------------------------------------------
    def _receive_message(self, name, socket):
        """
        Receives an incoming message from a ZMQ socket.

        :param str name: The name of the end point of source of the message.
        :param zmq.sugar.socket.Socket socket: The ZMQ socket.

        XXX @todo Support JSON messages for communication with PHP front end.
        """
        message = socket.recv_pyobj()
        """:type: enarksh.message.Message.Message"""
        message.message_source = name

        if message.message_type not in self._message_types:
            raise ValueError("Received message with unknown message type '{0}'".format(message.message_type))

        event = self._message_types[message.message_type]
        event.fire(message)

    # ------------------------------------------------------------------------------------------------------------------
    def receive_message(self, event, event_data, listener_data):
        """
        Receives a messages from another processes.

        :param * event: Not used.
        :param * event_data: Not used.
        :param * listener_data: Not used.
        """
        del event, event_data, listener_data

        # Make a poller for all incoming sockets.
        poller = zmq.Poller()
        for socket in self._end_points.values():
            if socket.type in [zmq.PULL, zmq.REP]:
                poller.register(socket, zmq.POLLIN)

        # Wait for socket is ready for reading.
        socks = dict(poller.poll())

        for name, socket in self._end_points.items():
            if socket in socks:
                self._receive_message(name, socket)

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point, message):
        """
        Sends a message to an end point.

        :param str end_point: The name of the end point.
        :param enarksh.message.Message.Message message: The message.
        """
        socket = self._end_points[end_point]
        socket.send_pyobj(message)

    # ------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        """
        Removes this object from the event system. This as preparation for removing this object such that there aren't
        references to this object and the garbage collector can remove this object.
        """
        EventActor.destroy(self)

        self._message_types = {}

    # ------------------------------------------------------------------------------------------------------------------
    def no_barking(self, seconds):
        """
        During start up of ZMQ the incoming file descriptors become 'ready for reading' while there is no message on
        the socket. This method prevent incoming sockets barking that the are ready the for reading.

        :param int seconds: The number of seconds the give the other ZMQ thread to start up.
        """
        sleep(seconds)

        for _ in range(1, len(self.end_points)):
            poller = zmq.Poller()
            for socket in self.end_points.values():
                if socket.type in [zmq.PULL, zmq.REP]:
                    poller.register(socket, zmq.POLLIN)

            poller.poll(1)

# ----------------------------------------------------------------------------------------------------------------------