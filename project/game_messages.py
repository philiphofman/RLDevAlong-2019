#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod
import textwrap


class Message:
    """Class for text messages.


    Attributes:
        text(str): Message contents.
        color(TCOD.color): Color of message.
    """

    def __init__(self, text, color=libtcod.white):
        """Inits some message values.

        Args:
            text(str): Message contents.
            color(TCOD.color): tcod Color of message.
        """

        self.text = text
        self.color = color


class MessageLog:
    """Log for messages."""

    def __init__(self, x, width, height):
        """Inits some values for a message log.

        Args:
            x(int): x coordinate.
            width(int): Width.
            height(int): Height of log in text lines.
        """

        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """Adds a message to the log.

        Args:
            message(Message): A Message object message.
        """

        # Split the message if necessary, among multiple lines.
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one.
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a message object, with the text and the color
            self.messages.append(Message(line, message.color))
