import enarksh


class ChunkLogger:
    _file_count = 0

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._chunk_count = 0
        self._position = 0
        self._buffer = bytearray(b' ' * enarksh.CHUNK_SIZE)
        self._filename1 = ''
        self._filename2 = ''

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_filename():
        ChunkLogger._file_count += 1

        return '%s/%s/%010d.log' % (enarksh.HOME, 'var/lib/logger', ChunkLogger._file_count)

    # ------------------------------------------------------------------------------------------------------------------
    def write(self, buffer: bytes):
        size = len(buffer)
        pos = 0

        while size > 0:
            n = min(size, enarksh.CHUNK_SIZE - self._position)
            self._buffer[self._position:self._position + n] = buffer[pos:pos + n]

            if n < size:
                if self._chunk_count == 0:
                    self._filename1 = self._get_filename()
                    with open(self._filename1, "wb") as file:
                        file.write(self._buffer[:enarksh.CHUNK_SIZE])

                self._position = 0
                self._chunk_count += 1
            else:
                self._position += n

            size -= n
            pos += n

    # ------------------------------------------------------------------------------------------------------------------
    def get_total_log_size(self):
        return self._chunk_count * enarksh.CHUNK_SIZE + self._position

    # ------------------------------------------------------------------------------------------------------------------
    def get_filename1(self):
        return self._filename1

    # ------------------------------------------------------------------------------------------------------------------
    def get_filename2(self):
        return self._filename2

    # ------------------------------------------------------------------------------------------------------------------
    def close(self):
        if self._position != 0:
            if self._chunk_count == 0:
                # Write first chunk to the file system.
                self._filename1 = self._get_filename()
                with open(self._filename1, "wb") as file:
                    file.write(self._buffer[:self._position])
                    file.close()

            else:
                self._filename2 = self._get_filename()
                with open(self._filename2, "wb") as file:
                    if self._chunk_count >= 2:
                        file.write(self._buffer[self._position:enarksh.CHUNK_SIZE])
                    file.write(self._buffer[:self._position])
                    file.close()


# ----------------------------------------------------------------------------------------------------------------------
