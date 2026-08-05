"""
Vercel Serverless entry point for the Django application.

Vercel's Python runtime invokes the ``handler`` callable in this module for
every request. This handler bridges Vercel's request/response model to
Django's WSGI application by building a WSGI ``environ`` from the incoming
event and reading the WSGI ``start_response`` output back into a response.

This approach requires no third-party ``vercel-wsgi`` package and works
reliably on Vercel's ``@vercel/python`` builder.
"""
import io
import os
import sys

# Ensure Django can locate the settings module when running serverless.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssm_config.settings')

# Make the project root importable (Vercel runs from the repo root).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ssm_config.wsgi import application  # noqa: E402


def handler(request):
    """
    Vercel serverless function handler.

    ``request`` is a Vercel Python request object exposing ``body``,
    ``method``, ``path``, ``headers``, and ``query``.
    """
    # Build the WSGI environ from the Vercel request.
    body = request.body if hasattr(request, 'body') else b''
    if isinstance(body, str):
        body = body.encode('utf-8')

    method = getattr(request, 'method', 'GET')
    path = getattr(request, 'path', '/')
    query = getattr(request, 'query', '')
    headers = getattr(request, 'headers', {}) or {}

    # Normalize HTTP headers to WSGI format ("CONTENT_TYPE", "HTTP_*").
    content_type = headers.get('content-type', '')
    content_length = str(len(body))

    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query or '',
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': io.BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': True,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': content_length,
    }

    # Copy remaining headers into the environ as HTTP_*.
    for key, value in headers.items():
        header_key = f'HTTP_{key.upper().replace("-", "_")}'
        if header_key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH'):
            environ[header_key] = value

    # Set the proxy SSL header so Django security checks pass.
    environ['HTTP_X_FORWARDED_PROTO'] = 'https'

    # Capture the WSGI response.
    status_headers = {}
    status_code = 200

    def start_response(status, response_headers, exc_info=None):
        nonlocal status_code, status_headers
        status_code = int(status.split(' ')[0])
        status_headers = dict(response_headers)
        return lambda data: None

    response_body = b''.join(application(environ, start_response))

    # Determine response content type.
    content_type = status_headers.get('Content-Type', 'text/html; charset=utf-8')

    # Vercel returns the body as text; decode if it's a text response.
    if 'text' in content_type or 'json' in content_type or 'xml' in content_type:
        body_out = response_body.decode('utf-8')
    else:
        body_out = response_body

    return {
        'statusCode': status_code,
        'headers': status_headers,
        'body': body_out,
    }
