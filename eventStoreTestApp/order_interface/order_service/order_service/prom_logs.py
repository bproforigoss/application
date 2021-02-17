from prometheus_client import Counter, Summary

performance_metrics = {
    "http_request_summary": Summary(
        "http_request_summary", "Summary of HTTP request being served"
    ),
    "event_send_summary": Summary(
        "event_send_summary", "Summary of sending events"
    ),
    "connection_error_counter": Counter(
        "connection_error_counter",
        "Counter of errors related to connection to database services"
    ),
}
