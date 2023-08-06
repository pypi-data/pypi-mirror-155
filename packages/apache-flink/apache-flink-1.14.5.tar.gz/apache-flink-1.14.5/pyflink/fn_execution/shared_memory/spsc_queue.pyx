#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# cython: language_level=3
from libc.stdint cimport *
from libc.stdlib cimport malloc, free

cdef class PySpscQueue:
    def __cinit__(self, bytes filename, size_t capacity, bint reset):
        self._queue = create_queue(filename, capacity, reset)
        self._one_byte_array = <char*> malloc(1)

    cdef void write_data(self, char*val, size_t offset, size_t length):
        write_data(self._queue, val, offset, length)

    cdef void write_byte(self, char val):
        self._one_byte_array[0] = val
        write_data(self._queue, self._one_byte_array, 0, 1)

    cdef int read_data(self, char*data, size_t offset, size_t length):
        cdef int read_length
        read_length = read_data(self._queue, data, 0, length)
        return read_length

    cdef char read_byte(self):
        read_data(self._queue, self._one_byte_array, 0, 1)
        return self._one_byte_array[0]

    cdef int available(self):
        return available(self._queue)

    cdef void mark_finish(self):
        mark_finish(self._queue)

    cdef bint is_finish(self):
        cdef long ret = isFinished(self._queue)
        return ret == 1

    cdef void close(self):
        if self._queue:
            close_queue(self._queue)
        if self._one_byte_array:
            free(self._one_byte_array)

    def __dealloc__(self):
        if self._queue:
            close_queue(self._queue)

cpdef bytes read_bytes(PySpscQueue send_queue):
    cdef int length
    cdef char*receive_data
    cdef bytes data
    length = read_var_int64(send_queue)
    receive_data = <char*> malloc(length)
    send_queue.read_data(receive_data, 0, length)
    data = <bytes> receive_data[:length]
    free(receive_data)
    return data

cdef read_var_int64(PySpscQueue queue):
    """Decode a variable-length encoded long from a stream."""
    cdef char bits
    cdef size_t shift = 0
    cdef size_t result = 0
    cdef char*data
    cdef bint has_prefix = True
    data = <char*> malloc(1)
    while has_prefix:
        queue.read_data(data, 0, 1)
        result |= bits << shift
        shift += 7
        if not (data[0] & 0x80):
            has_prefix = False
    free(data)
    return result
