import prometheus_client
from prometheus_client import Summary, Counter, Histogram, Gauge

metrics = {}

_INF = float("inf")

metrics['resources_created_total'] = Counter('se4ai_resource_created_total', 'The total number of resource created')
metrics['training_duration_seconds'] = Histogram('se4ai_training_duration_seconds',
                                                 'The total number of resource created',
                                                 buckets=(10, 20, 30, 60, 120, 300, 600, _INF))
