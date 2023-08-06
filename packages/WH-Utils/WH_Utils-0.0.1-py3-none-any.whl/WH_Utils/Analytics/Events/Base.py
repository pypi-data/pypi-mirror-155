from WH_Utils.Objects.Event import Event
from WH_Utils.Objects.Enums import EventType, EventStage
from WH_Utils.Utils.global_utils import backend_auth

"""Basic Event Analytics

This module handles the most basic

Public Functions:

Private functions:

TODO:


"""


def get_event_stage(event: Event) -> EventStage:
    """Classifies the stage of an event.

    Args:
        event: the event you want to classify

    Returns:
        EventStage

    Raises:
        NotImplementedError
    """
    if event.type == EventType.IPO or event.type == EventType.acquisition:
        return _get_event_stage_company(event)

    else:
        raise NotImplementedError("we working on it")


def _get_event_stage_company(event: Event) -> EventStage:
    """This is the classification function for company specific events like acquisitions and IPOs

    Args:
        event: event: the event you want to classify

    Returns:
        EventStage

    """
    raise NotImplementedError()


def _get_event_stage_divorce(event: Event) -> EventStage:
    """This is the classification function for divorces

    Args:
        event: event: the event you want to classify

    Returns:
        EventStage

    """
    raise NotImplementedError()


def get_num_beneficiaries(event: Event) -> int:
    """Returns the number of affiliated people for an event

    Args:
        event: event: the event you want to classify

    Returns:
        num_beneficiaries

    """
    auth_header = backend_auth()
    id = event.id
