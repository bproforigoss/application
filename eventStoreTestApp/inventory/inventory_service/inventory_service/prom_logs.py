from prometheus_client import Counter

performance_metrics = {
    "http_request_counter": Counter(
        "inventory_http_request_counter",
        "Counter of HTTP requests being served",
        ["method", "endpoint"],
    ),
    "event_send_counter": Counter(
        "inventory_event_send_counter", "Counter of egress events"
    ),
    "network_timeout_error_counter": Counter(
        "inventory_network_timeout_error_counter",
        "Errors caused by timeouts while establishing connection",
    ),
    "http_error_counter": Counter(
        "inventory_http_error_counter",
        "Errors caused by HTTP unsuccessful status code response",
    ),
    "connection_timeout_error_counter": Counter(
        "inventory_connection_timeout_error_counter",
        "Errors caused by timeouts during data transmission",
    ),
    "redirect_error_counter": Counter(
        "inventory_redirect_error_counter",
        "Errors caused by exceeding redirection limits",
    ),
    "connection_error_counter": Counter(
        "inventory_connection_error_counter",
        "Errors caused by general network connection failure",
    ),
    "ambiguous_network_error_counter": Counter(
        "inventory_ambiguous_network_error_counter",
        "Errors caused by exceptions not specifically measured",
    ),
}

performance_metrics["http_request_counter"].labels("GET", "/")
performance_metrics["http_request_counter"].labels("GET", "/health")
performance_metrics["http_request_counter"].labels("GET", "/metrics")
performance_metrics["http_request_counter"].labels("POST", "/create")
performance_metrics["http_request_counter"].labels("POST", "/delete")
performance_metrics["http_request_counter"].labels("POST", "/add")
performance_metrics["http_request_counter"].labels("POST", "/submit")
