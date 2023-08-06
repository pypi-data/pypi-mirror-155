import hmac
import hashlib
import sys


from ..errors import SignatureVerificationError


class Utility(object):
    def __init__(self, client=None):
        self.client = client

    # Taken from Django Source Code
    # Used in python version < 2.7.7
    # As hmac.compare_digest is not present in prev versions
    def compare_string(self, expected_str, actual_str):
        """
        Returns True if the two strings are equal, False otherwise
        The time taken is independent of the number of characters that match
        For the sake of simplicity, this function executes in constant time only
        when the two strings have the same length. It short-circuits when they
        have different lengths
        """
        if len(expected_str) != len(actual_str):
            return False
        result = 0
        for x, y in zip(expected_str, actual_str):
            result |= ord(x) ^ ord(y)
        return result == 0
