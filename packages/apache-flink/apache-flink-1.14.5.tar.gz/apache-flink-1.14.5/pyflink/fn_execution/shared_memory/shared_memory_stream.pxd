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

from pyflink.fn_execution.stream_fast cimport LengthPrefixInputStream, LengthPrefixOutputStream
from pyflink.fn_execution.shared_memory.spsc_queue cimport PySpscQueue

cdef class SharedMemoryInputStream(LengthPrefixInputStream):
    cdef PySpscQueue _queue
    cdef char*_input_data
    cdef size_t _input_buffer_size
    cdef bint is_finish(self)

cdef class SharedMemoryOutputStream(LengthPrefixOutputStream):
    cdef PySpscQueue _queue
