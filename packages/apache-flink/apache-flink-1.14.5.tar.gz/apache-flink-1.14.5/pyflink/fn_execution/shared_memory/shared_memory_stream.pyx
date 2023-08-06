################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
# cython: language_level = 3
# cython: infer_types = True
# cython: profile=True
# cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

from libc.stdlib cimport realloc, malloc, free

cdef class SharedMemoryInputStream(LengthPrefixInputStream):
    def __cinit__(self, queue):
        self._queue = queue
        self._input_data = <char*> malloc(1024)
        self._input_buffer_size = 1024

    cdef size_t read(self, char** data):
        cdef size_t length = 0
        cdef bint has_prefix = True
        cdef size_t shift = 0
        cdef char bits, read_byte
        # read the var-int size
        while has_prefix:
            read_byte = self._queue.read_byte()
            bits = read_byte & 0x7F
            length |= bits << shift
            shift += 7
            if not (read_byte & 0x80):
                has_prefix = False
        if length > self._input_buffer_size:
            self._input_buffer_size = length
            self._input_data = <char*> realloc(self._input_data, length)
        self._queue.read_data(self._input_data, 0, length)
        data[0] = self._input_data
        return length

    cdef size_t available(self):
        return self._queue.available()

    cdef bint is_finish(self):
        return self._queue.is_finish()

    def __dealloc__(self):
        if self._input_data:
            free(self._input_data)

cdef class SharedMemoryOutputStream(LengthPrefixOutputStream):
    def __cinit__(self, queue):
        self._queue = queue

    cdef void write(self, char*data, size_t length):
        cdef char bits
        cdef size_t size = length
        # write variable prefix length
        while size:
            bits = size & 0x7F
            size >>= 7
            if size:
                bits |= 0x80
            self._queue.write_byte(bits)
        self._queue.write_data(data, 0, length)

    cpdef void flush(self):
        self._queue.mark_finish()
