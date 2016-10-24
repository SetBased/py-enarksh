"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os
import smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller.node import ScheduleNode
from enarksh.controller.node.SimpleNode import SimpleNode


class MailOperatorEventHandler:
    """
    An event handler for event were an mail must be send to the operators.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __send_mail(to, subject, body):
        """
        Sends an email to the operators.

        :param str|list[str] to: The email addresses of the operator(s).
        :param str subject: The subject op the email.
        :param str body: The email body.
        """
        config = ConfigParser()
        config.read(os.path.join(enarksh.HOME, 'etc/enarksh.cfg'))

        from_email = config.get('controller', 'email')

        # Concat To mail addresses
        to_email = ''
        if isinstance(to, list):
            for email in to:
                if to_email:
                    to_email += ', '
                to_email += email
        else:
            to_email = to

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = to_email
        msg['From'] = from_email

        # Send the message via our local SMTP server.
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __send_mail_simple_node_failed(rnd_id):
        """
        Sends a mail to operators that a simple node has terminated with an error.

        :param int rnd_id: The ID of the run node.
        """
        node = DataLayer.enk_back_run_node_get_details(rnd_id)
        operators = DataLayer.enk_back_get_operators()

        if operators:
            body = """Dear Enarksh operator,

Job {} has run unsuccessfully.

Greetings from Enarksh""".format(str(node['uri_uri'], 'utf-8'))

            subject = "Job of schedule {} failed".format(str(node['sch_name'], 'utf-8'))

            to = []
            for operator in operators:
                to.append(operator['usr_email'])

            MailOperatorEventHandler.__send_mail(to, subject, body)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __send_mail_schedule_node_failed(rnd_id):
        """
        Sends a mail to operators that a schedule has terminated unsuccessfully.

        :param int rnd_id: The ID of the schedule.
        """
        node = DataLayer.enk_back_run_node_get_details(rnd_id)
        operators = DataLayer.enk_back_get_operators()

        if operators:
            body = """Dear Enarksh operator,

Schedule {} finished unsuccessfully.

Greetings from Enarksh""".format(str(node['sch_name'], 'utf-8'))

            subject = "Schedule {} finished unsuccessfully".format(str(node['sch_name'], 'utf-8'))

            to = []
            for operator in operators:
                to.append(operator['usr_email'])

            MailOperatorEventHandler.__send_mail(to, subject, body)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __send_mail_schedule_node_success(rnd_id):
        """
        Sends a mail to operators that a schedule has terminated successfully.

        :param int rnd_id: The ID of the schedule.
        """
        node = DataLayer.enk_back_run_node_get_details(rnd_id)
        operators = DataLayer.enk_back_get_operators()

        if operators:
            body = """Dear Enarksh operator,

Schedule {} finished successfully.

Greetings from Enarksh""".format(str(node['sch_name'], 'utf-8'))

            subject = "Schedule {} finished successfully".format(str(node['sch_name'], 'utf-8'))

            to = []
            for operator in operators:
                to.append(operator['usr_email'])

            MailOperatorEventHandler.__send_mail(to, subject, body)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __handle_simple_node_stop(_event, event_data, _listener_data):
        """
        Handles the termination of a simple node.

        :param * _event: Not used.
        :param tuple[dict] event_data: The old and new node status.
        :param * _listener_data: Not used.
        """
        del _event, _listener_data

        if event_data[1]['rst_id'] == enarksh.ENK_RST_ID_ERROR:
            MailOperatorEventHandler.__send_mail_simple_node_failed(event_data[1]['rnd_id'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __handle_schedule_stop(_event, event_data, _listener_data):
        """
        Handles the termination of a schedule node.

        :param * _event: Not used.
        :param tuple[dict] event_data: The old and new node status.
        :param * _listener_data: Not used.
        """
        del _event, _listener_data

        if event_data[0]['rst_id'] != event_data[1]['rst_id']:
            # If status is error send mail.
            if event_data[1]['rst_id'] == enarksh.ENK_RST_ID_ERROR:
                MailOperatorEventHandler.__send_mail_schedule_node_failed(event_data[1]['rnd_id'])

            # If status is success send mail.
            if event_data[1]['rst_id'] == enarksh.ENK_RST_ID_COMPLETED:
                MailOperatorEventHandler.__send_mail_schedule_node_success(event_data[1]['rnd_id'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle_node_creation(_event, node, _listener_data):
        """
        Handles a node creation event.

        :param * _event : Not used.
        :param enarksh.controller.node.Node.Node node: The created node.
        :param * _listener_data: Not used.
        """
        del _event, _listener_data

        if isinstance(node, SimpleNode):
            node.event_state_change.register_listener(MailOperatorEventHandler.__handle_simple_node_stop)

        if isinstance(node, ScheduleNode):
            node.event_state_change.register_listener(MailOperatorEventHandler.__handle_schedule_stop)


# ----------------------------------------------------------------------------------------------------------------------
