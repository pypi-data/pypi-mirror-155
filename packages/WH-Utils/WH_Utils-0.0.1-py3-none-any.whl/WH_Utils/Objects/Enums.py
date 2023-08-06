"""
This is a simple module that is largly for type safty. It's more lightly documented that
most of the library because it should be pretty self explanitory. They are just simple
enum classes for the most part.
"""

from enum import Enum


class UserRank(str, Enum):
    """Enum for the possible ranks of users

    Simple enum class for the possible ranks a user can have. These are linked to permissions.

    Args
    ---------

        admin: Highest rank available. Can do literally anything. This should probably only ever be Ethan and McClain.

        analyst: Developed specifically for internal WH employees. They should have the ability to read update and soft delete.

        user: This is the default class for a paying user.

        user_expired: If they were once a user but no longer. Basically a user soft delete.


    """

    admin = "admin"
    analyst = "analyst"
    user = "user"
    user_expired = "user_expired"


class Followables(str, Enum):
    """All available followable entities

    Args
    -----
        company
        client
        event
    """

    company = "company"
    client = "client"
    event = "event"


class EventType(str, Enum):
    """The possible MIM events.

    Args
    -----
        IPO
        acquisition
        trust_dis
        divorce
        lottery
        injury
        other
    """

    IPO = "IPO"
    acquisition = "acquisition"
    fund_raise = "fund_raise"
    trust_dis = "trust_dis"
    divorce = "divorce"
    lottery = "lottery"
    injury = "injury"
    other = "other"


class CompanyType(str, Enum):
    """Possible stages of company.

    Args
    ------

        public: a publicly traded company
        private: a privatly held company
        state_owned: self explanitory
        subsidiary_of_public: I honestly don't know
        sole_proprietor: a small company owned by a single person
        partnership: like a sole_proprietor but with > 1 person

    """

    public = "public"
    private = "private"
    state_owned = "state_owned"
    subsidiary_of_public = "subsidiary_of_public"
    sole_proprietor = "sole proprietor"
    partnership = "partnership"


class JobRank(str, Enum):
    """
    The possible ranks a person can have within their company ranked from most to least equity
    """

    founder = "founder"
    c_suite = "c-suite"
    vice_president = "vp"
    director = "director"
    manager = "manager"
    senior = "senior"
    entry_level = "entry"
    intern = "intern"
    other = "other"


class EventStage(str, Enum):
    """
    The possible stages an event can take
    """

    not_started = "Not Started"
    early_stage = "Early Stage"
    in_progress = "In Progress"
    late_stage = "Late Stage"
    closed = "Closed"
