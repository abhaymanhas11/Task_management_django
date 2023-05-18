from enum import Enum


class TaskStatus(Enum):
    Assigned = "Assigned"
    Submitted = "Submitted"
    Revision_Required = "Revision_Required"
    Approved = "Approved"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TaskFeedback(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class UserType(Enum):
    content_writer = "content_writer"
    editor = "editor"
    admin = "admin"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
