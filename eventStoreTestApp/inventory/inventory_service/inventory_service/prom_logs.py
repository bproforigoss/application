from prometheus_client import Counter, Summary

performance_metrics = {
    "http_request_summary": Summary(
        "inventory_http_request_summary", "Summary of HTTP request being served"
    ),
    "event_send_summary": Summary(
        "inventory_event_send_summary", "Summary of egress events"
    ),
    "network_error_counter": Counter(
        "inventory_network_error_counter",
        "Errors caused by network problems, e.g. DNS failure, refused connection",
    ),
    "http_error_counter": Counter(
        "inventory_http_error_counter",
        "Errors caused by HTTP unsuccessful status code response",
    ),
    "timeout_error_counter": Counter(
        "inventory_timeout_error_counter", "Errors caused by request timeouts"
    ),
    "redirect_error_counter": Counter(
        "inventory_redirect_error_counter",
        "Errors caused by exceeding redirection limits",
    ),
}
