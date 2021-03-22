from prometheus_client import Counter, Summary

performance_metrics = {
    "http_request_counter": Counter(
        "inventory_http_request_counter", "Counter of HTTP requests being served",
        ["method", "endpoint"]
    ),
    "event_send_counter": Counter(
        "inventory_event_send_counter", "Counter of egress events"
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

performance_metrics["http_request_counter"].labels("GET", "/")
performance_metrics["http_request_counter"].labels("GET", "/health")
performance_metrics["http_request_counter"].labels("GET", "/metrics")
performance_metrics["http_request_counter"].labels("POST", "/create")
performance_metrics["http_request_counter"].labels("POST", "/delete")
performance_metrics["http_request_counter"].labels("POST", "/add")
performance_metrics["http_request_counter"].labels("POST", "/subtract")
