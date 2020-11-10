from order_service import order_aggregate
from order_service.domain import domain_events
from order_service.domain.enumerations import OrderEventEnumeration as ORDER_EVENT_TYPE

user_sessions = {}


def create_order_session():
    session = order_aggregate.OrderAggregate()
    user_sessions[str(session.aggregate_id)] = session
    session.raise_event(
        domain_events.OrderEvent(
            ORDER_EVENT_TYPE.OrderStarted,
            session.aggregate_id,
            {"reason": "new session"},
        )
    )
    return str(session.aggregate_id)


def add_item(item, amount, session_id):
    session = user_sessions[session_id]
    session.add_order_item(item, amount)


def remove_item(item, session_id):
    session = user_sessions[session_id]
    return session.remove_order_item(item)


def submit_order(name, address, session_id):
    session = user_sessions[session_id]
    session.submit_order(name, address)
