from prometheus_client import Counter, Summary, Gauge


def init_prometheus_metrics():
    executions_total = Counter(
        namespace="piper",
        subsystem="executions",
        name="total",
        documentation="Total of executions processed",
        labelnames=("serviceName", "functionName", "executionStatus"),
    )

    executions_time_seconds = Summary(
        namespace="piper",
        subsystem="executions",
        name="executions_duration_seconds",
        documentation="Executions duration in seconds",
        labelnames=("serviceName", "functionName", "executionStatus"),
    )

    executions_time_since_creation_seconds = Summary(
        namespace="piper",
        subsystem="executions",
        name="executions_time_since_creation_seconds",
        documentation="Executions duration since it's creation in seconds",
        labelnames=("serviceName", "functionName", "executionStatus"),
    )

    inprogress_executions = Gauge(namespace="piper",
                                  subsystem="executions",
                                  name='inprogress_executions',
                                  documentation='Inprogress executions',
                                  labelnames=("serviceName", "functionName"))
    # cpu and ram
    ram_metric = Gauge(namespace="piper",
                       subsystem="agent",
                       name="memory_usage_bytes",
                       documentation="Memory usage in bytes.",
                       labelnames=("serviceName", "container", "hostname"))

    cpu_metric = Gauge(namespace="piper",
                       subsystem="agent",
                       name="cpu_usage_percent",
                       documentation="CPU usage percent.",
                       labelnames=("serviceName", "container", "hostname"))
    metrics = {
        'executions_total': executions_total,
        'executions_time_seconds': executions_time_seconds,
        'executions_time_since_creation_seconds': executions_time_since_creation_seconds,
        'inprogress_executions': inprogress_executions,
        'ram_metric': ram_metric,
        'cpu_metric': cpu_metric
    }

    return metrics
