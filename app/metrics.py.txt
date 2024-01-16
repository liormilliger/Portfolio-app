from flask import request
from prometheus_flask_exporter import PrometheusMetrics

# Initialize Prometheus Metrics
metrics = PrometheusMetrics(app)

# Custom Metrics
page_view_counter = metrics.counter(
    'page_views', 'Number of page views',
    labels={'endpoint': None}
)
unique_visitors_counter = metrics.counter(
    'unique_visitors', 'Number of unique visitors',
    labels={'visitor_id': None}
)
session_duration_summary = metrics.summary(
    'session_duration', 'Session duration',
    labels={'session_id': None}
)

# Example of incrementing page views in a route
@app.route('/view_blog/<blog_id>')
def view_blog(blog_id):
    # Increment the page view counter
    page_view_counter.labels(endpoint=request.path).inc()

    # Your existing logic to serve the blog post
    # ...

    return "Blog Content"

# Initialize the metrics endpoint
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)
