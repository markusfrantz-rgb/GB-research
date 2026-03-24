#!/bin/sh
echo "Indexing documents..."
python -m rag ingest --reindex -v
echo "Starting web server..."
exec gunicorn web.app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120
