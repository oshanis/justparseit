"""
6.863 Spring 2008 Project

A set of Exception classes that are used in the Policy Parser
"""

"""
    Thrown by the Policy Interpret during traversal of
    a logical expression
"""
class InvalidExpressionError(Exception):
    def __init__(self, value):
        self.value = value

