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

cdef extern from "mmap_writer.h" nogil:
    ctypedef struct SPSCQueue:
        int capacity_
        int mmapLen_
    SPSCQueue *create_queue(const char*file_name, size_t length, int reset)
    void close_queue(SPSCQueue *queue);
    void write_data(SPSCQueue *queue, const char *val, size_t offset, size_t length);
    int read_data(SPSCQueue *queue, void *buf, size_t offset, size_t length);
    int available(SPSCQueue *queue);
    long isFinished(SPSCQueue *queue)
    void mark_finish(SPSCQueue *queue)

cdef class PySpscQueue:
    cdef SPSCQueue*_queue
    cdef char* _one_byte_array

    cdef void write_data(self, char*val, size_t offset, size_t length)
    cdef void write_byte(self, char val)
    cdef int read_data(self, char*data, size_t offset, size_t length)
    cdef char read_byte(self)
    cdef int available(self)
    cdef void mark_finish(self)
    cdef bint is_finish(self)
    cdef void close(self)

