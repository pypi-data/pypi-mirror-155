#
# Copyright (c) 2022 by Delphix. All rights reserved.
#


class ArithmeticException(Exception):

    @property
    def message(self):
        return self.args[0]

    def __init__(self, message):
        super(ArithmeticException, self).__init__(message)
