"""
Monitoring & Observability

Complete monitoring system with:
- Metrics
- Logging
- Tracing
- Alerting
- Dashboards

Reference:
- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
- OpenTelemetry: https://opentelemetry.io/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AlertStatus(Enum):
    FIRING = "firing"
    RESOLVED = "resolved"
    PENDING = "pending"


# =============================================================================
# METRICS
# =============================================================================

@dataclass
class Metric:
    """Metric"""
    name: str
    metric_type: MetricType
    
    value: float = 0
    
    labels: Dict[str, str] = field(default_factory=dict)
    
    timestamp: datetime = field(default_factory=datetime.now)
    
    unit: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Counter(Metric):
    """Counter metric"""
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name, MetricType.COUNTER, **kwargs)
    
    def inc(self, amount: float = 1):
        self.value += amount
        self.timestamp = datetime.now()


@dataclass
class Gauge(Metric):
    """Gauge metric"""
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name, MetricType.GAUGE, **kwargs)
    
    def set(self, value: float):
        self.value = value
        self.timestamp = datetime.now()
    
    def inc(self, amount: float = 1):
        self.value += amount
    
    def dec(self, amount: float = 1):
        self.value -= amount


@dataclass
class Histogram(Metric):
    """Histogram metric"""
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name, MetricType.HISTOGRAM, **kwargs)
        self.buckets: Dict[float, int] = {}
    
    def observe(self, value: float):
        self.value = value
        self.timestamp = datetime.now()


# =============================================================================
# LOGGING
# =============================================================================

@dataclass
class LogEntry:
    """Log entry"""
    timestamp: datetime = field(default_factory=datetime.now)
    
    level: LogLevel = LogLevel.INFO
    
    message: str = ""
    
    logger: Optional[str] = None
    
    context: Dict[str, Any] = field(default_factory=dict)
    
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    
    exception: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "logger": self.logger,
            "context": self.context,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "exception": self.exception
        }


class Logger:
    """Logger"""
    
    def __init__(self, name: str):
        self.name = name
        self.entries: List[LogEntry] = []
    
    def debug(self, message: str, **context):
        self._log(LogLevel.DEBUG, message, context)
    
    def info(self, message: str, **context):
        self._log(LogLevel.INFO, message, context)
    
    def warning(self, message: str, **context):
        self._log(LogLevel.WARNING, message, context)
    
    def error(self, message: str, **context):
        self._log(LogLevel.ERROR, message, context)
    
    def critical(self, message: str, **context):
        self._log(LogLevel.CRITICAL, message, context)
    
    def _log(self, level: LogLevel, message: str, context: Dict):
        entry = LogEntry(
            level=level,
            message=message,
            logger=self.name,
            context=context
        )
        self.entries.append(entry)
    
    def get_logs(self, level: LogLevel = None, limit: int = 100) -> List[LogEntry]:
        logs = self.entries
        
        if level:
            logs = [e for e in logs if e.level == level]
        
        return logs[-limit:]


# =============================================================================
# TRACING
# =============================================================================

@dataclass
class Span:
    """Trace span"""
    name: str
    
    trace_id: str
    span_id: str
    parent_id: Optional[str] = None
    
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    status: str = "ok"  # ok, error
    
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    events: List[Dict] = field(default_factory=list)
    
    def add_event(self, name: str, attributes: Dict = None):
        self.events.append({
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "attributes": attributes or {}
        })
    
    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value
    
    def finish(self, status: str = "ok"):
        self.end_time = datetime.now()
        self.status = status
    
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0


class Tracer:
    """Tracer"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: List[Span] = []
        self._span_id_counter = 0
    
    def start_span(self, name: str, trace_id: str = None, parent_id: str = None) -> Span:
        if not trace_id:
            import uuid
            trace_id = str(uuid.uuid4())
        
        self._span_id_counter += 1
        span_id = str(self._span_id_counter)
        
        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            parent_id=parent_id
        )
        
        self.spans.append(span)
        
        return span
    
    def get_trace(self, trace_id: str) -> List[Span]:
        return [s for s in self.spans if s.trace_id == trace_id]


# =============================================================================
# ALERTS
# =============================================================================

@dataclass
class Alert:
    """Alert"""
    name: str
    
    status: AlertStatus = AlertStatus.PENDING
    
    message: str = ""
    
    severity: str = "warning"  # critical, warning, info
    
    fired_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    labels: Dict[str, str] = field(default_factory=dict)
    
    annotations: Dict[str, str] = field(default_factory=dict)
    
    def fire(self, message: str):
        self.status = AlertStatus.FIRING
        self.message = message
        self.fired_at = datetime.now()
    
    def resolve(self):
        self.status = AlertStatus.RESOLVED
        self.resolved_at = datetime.now()


class AlertManager:
    """Alert manager"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.handlers: List[Callable] = []
    
    def create_alert(self, name: str) -> Alert:
        alert = Alert(name=name)
        self.alerts[name] = alert
        return alert
    
    def fire_alert(self, name: str, message: str):
        if name in self.alerts:
            self.alerts[name].fire(message)
        
        # Notify handlers
        for handler in self.handlers:
            handler(self.alerts[name])
    
    def resolve_alert(self, name: str):
        if name in self.alerts:
            self.alerts[name].resolve()
    
    def get_firing(self) -> List[Alert]:
        return [a for a in self.alerts.values() if a.status == AlertStatus.FIRING]


# =============================================================================
# DASHBOARD
# =============================================================================

@dataclass
class Dashboard:
    """Dashboard"""
    name: str
    
    panels: List[Dict] = field(default_factory=list)
    
    variables: Dict[str, List[str]] = field(default_factory=dict)
    
    refresh_interval: int = 60  # seconds
    
    def add_panel(self, title: str, metric: str, type: str = "graph"):
        self.panels.append({
            "title": title,
            "metric": metric,
            "type": type
        })
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "panels": self.panels,
            "variables": self.variables,
            "refresh_interval": self.refresh_interval
        }


# =============================================================================
# MONITORING SYSTEM
# =============================================================================

class MonitoringSystem:
    """Complete monitoring system"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        
        # Metrics
        self.metrics: Dict[str, Metric] = {}
        
        # Logging
        self.loggers: Dict[str, Logger] = {}
        
        # Tracing
        self.tracer = Tracer(service_name)
        
        # Alerts
        self.alert_manager = AlertManager()
        
        # Dashboards
        self.dashboards: Dict[str, Dashboard] = {}
    
    # Metrics
    def counter(self, name: str, **labels) -> Counter:
        key = f"{name}:{labels}"
        
        if key not in self.metrics:
            self.metrics[key] = Counter(name, labels=labels)
        
        return self.metrics[key]
    
    def gauge(self, name: str, **labels) -> Gauge:
        key = f"{name}:{labels}"
        
        if key not in self.metrics:
            self.metrics[key] = Gauge(name, labels=labels)
        
        return self.metrics[key]
    
    def histogram(self, name: str, **labels) -> Histogram:
        key = f"{name}:{labels}"
        
        if key not in self.metrics:
            self.metrics[key] = Histogram(name, labels=labels)
        
        return self.metrics[key]
    
    def get_metric(self, name: str) -> Optional[Metric]:
        for key, metric in self.metrics.items():
            if metric.name == name:
                return metric
        return None
    
    def get_all_metrics(self) -> List[Metric]:
        return list(self.metrics.values())
    
    # Logging
    def get_logger(self, name: str) -> Logger:
        if name not in self.loggers:
            self.loggers[name] = Logger(name)
        
        return self.loggers[name]
    
    # Tracing
    def start_trace(self, name: str, **attributes) -> Span:
        span = self.tracer.start_span(name)
        
        for key, value in attributes.items():
            span.set_attribute(key, value)
        
        return span
    
    # Alerts
    def create_alert(self, name: str) -> Alert:
        return self.alert_manager.create_alert(name)
    
    def fire_alert(self, name: str, message: str):
        self.alert_manager.fire_alert(name, message)
    
    # Dashboards
    def create_dashboard(self, name: str) -> Dashboard:
        dashboard = Dashboard(name=name)
        self.dashboards[name] = dashboard
        return dashboard
    
    # Export
    def export_prometheus(self) -> str:
        """Export in Prometheus format"""
        lines = []
        
        for metric in self.metrics.values():
            name = metric.name.replace("-", "_")
            
            if metric.metric_type == MetricType.COUNTER:
                lines.append(f"# TYPE {name} counter")
            elif metric.metric_type == MetricType.GAUGE:
                lines.append(f"# TYPE {name} gauge")
            elif metric.metric_type == MetricType.HISTOGRAM:
                lines.append(f"# TYPE {name} histogram")
            
            labels = ",".join([f'{k}="{v}"' for k, v in metric.labels.items()])
            
            if labels:
                lines.append(f"{name}{{{labels}}} {metric.value}")
            else:
                lines.append(f"{name} {metric.value}")
        
        return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Monitoring System")
    print("=" * 50)
    
    # Create monitoring
    monitor = MonitoringSystem("agent-platform")
    
    # Metrics
    requests = monitor.counter("http_requests_total", method="GET", status="200")
    requests.inc()
    requests.inc()
    
    gauge = monitor.gauge("active_users")
    gauge.set(100)
    
    # Logging
    logger = monitor.get_logger("api")
    logger.info("Request received", user_id="123")
    logger.error("Error processing request", error="timeout")
    
    # Tracing
    with monitor.start_trace("process_request", operation="data_processing") as span:
        span.set_attribute("db.query", "SELECT * FROM users")
        # Do work
        span.finish()
    
    # Alerts
    alert = monitor.create_alert("high_error_rate")
    monitor.fire_alert("high_error_rate", "Error rate above threshold")
    
    # Export Prometheus
    print("\nPrometheus Metrics:")
    print(monitor.export_prometheus())


if __name__ == "__main__":
    main()


"""
Monitoring Usage

    # Create monitoring
    monitor = MonitoringSystem("my-service")
    
    # Metrics
    requests = monitor.counter("http_requests")
    requests.inc()
    
    gauge = monitor.gauge("active_users")
    gauge.set(100)
    
    # Logging
    logger = monitor.get_logger("api")
    logger.info("Request received")
    
    # Tracing
    with monitor.start_trace("operation") as span:
        span.set_attribute("key", "value")
    
    # Alerts
    monitor.fire_alert("alert_name", "message")
    
    # Export
    print(monitor.export_prometheus())
"""