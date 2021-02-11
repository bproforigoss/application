from prometheus_client import Counter, Summary

performance_metrics = {
    "http_counter": Counter("http_requests", "HTTP requests served"),
    "events_produced": Counter(
        "events_produced", "Events sent out by this microservice"
    ),
    "http_request_duration": Summary(
        "http_request_duration", "Duration of HTTP request being served"
    ),
    "event_send_duration": Summary(
        "event_send_duration", "Duration of sending an event"
    )
}
