class int_mod_n(int):
    def __new__(self, a, n):
        return int.__new__(self, a)

    def __init__(self, a, n):
        super(int, self).__init__()
        self._n = n

    def __mul__(self, other):
        return self.__class__(int.__mul__(self, other) % self._n, self._n)

    def __rmul__(self, other):
        return self.__class__(int.__mul__(self, other) % self._n, self._n)

    def __eq__(self, other):
        return int(self) == int(other % self._n)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __pow__(self, n):
        return self.__class__(int.__pow__(self, n, self._n), self._n)

    def __hash__(self):
        return hash((int(self), self._n))

    def square(self):
        return self * self

    def serialize(self):
        return int(self).to_bytes(self._n.bit_length() // 8, "big",
                                  signed=False)


"""
Copyright 2018 Chia Network Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
