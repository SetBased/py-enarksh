"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

import enarksh


class ChunkLogger:
    """
    A class for logging the first and last chunk of a stream.
    """
    __file_count = 0
    """
    The number of files (with chunks) written.

    :type: int
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__chunk_count = 0
        """
        The total number of chunks to are writen.

        :type: int
        """

        self.__position = 0
        """
        The current position for writing the next byte in the buffer.

        :type: int
        """

        self.__buffer = bytearray(b' ' * enarksh.CHUNK_SIZE)
        """
        The buffer.

        :type: bytes
        """

        self.__filename1 = ''
        """
        The filename where the first chunk has been stored.

        :type: str
        """

        self.__filename2 = ''
        """
        The filename where the last chunk has been stored.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def filename1(self):
        """
        Getter for the filename where the first chunk has been stored. Empty if no first chunk has been stored.

        :rtype: str
        """
        return self.__filename1

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def filename2(self):
        """
        Getter for the filename where the last chunk has been stored. Empty if no last chunk has been stored.

        :rtype: str
        """
        return self.__filename2

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __get_filename():
        """
        Returns an unique filename for storing a chunk.

        :rtype: str
        """
        ChunkLogger.__file_count += 1

        return os.path.join(enarksh.HOME, 'var/lib/logger', '{0:010d}.log'.format(ChunkLogger.__file_count))

    # ------------------------------------------------------------------------------------------------------------------
    def write(self, buffer):
        """
        Writes bytes from a buffer to this chunk logger.

        :param bytes buffer: The buffer.
        """
        bytes_remaining = len(buffer)
        pos = 0

        while bytes_remaining > 0:
            size = min(bytes_remaining, enarksh.CHUNK_SIZE - self.__position)
            self.__buffer[self.__position:self.__position + size] = buffer[pos:pos + size]

            if size < bytes_remaining:
                if self.__chunk_count == 0:
                    self.__filename1 = self.__get_filename()
                    with open(self.__filename1, "wb") as file:
                        file.write(self.__buffer[:enarksh.CHUNK_SIZE])

                self.__position = 0
                self.__chunk_count += 1
            else:
                self.__position += size

            bytes_remaining -= size
            pos += size

    # ------------------------------------------------------------------------------------------------------------------
    def get_total_log_size(self):
        """
        Returns the total number of bytes written to the chunk logger.

        :rtype: int
        """
        return self.__chunk_count * enarksh.CHUNK_SIZE + self.__position

    # ------------------------------------------------------------------------------------------------------------------
    def close(self):
        """
        Closes this chunk logger. Remaining bytes are flushed.
        """
        if self.__position != 0:
            if self.__chunk_count == 0:
                # Write first chunk to the file system.
                self.__filename1 = self.__get_filename()
                with open(self.__filename1, "wb") as file:
                    file.write(self.__buffer[:self.__position])
                    file.close()

            else:
                self.__filename2 = self.__get_filename()
                with open(self.__filename2, "wb") as file:
                    if self.__chunk_count >= 2:
                        file.write(self.__buffer[self.__position:enarksh.CHUNK_SIZE])
                    file.write(self.__buffer[:self.__position])
                    file.close()

# ----------------------------------------------------------------------------------------------------------------------
