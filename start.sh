#!/bin/sh
echo "Indexing documents..."
if python -m rag ingest --reindex -v; then
  echo "[INDEX] OK"
else
  echo "[INDEX] WARNING: indexing failed (exit $?). Starting server anyway."
  echo "[INDEX] Documents will be readable via /doc/; search and Q&A will be unavailable."
fi
echo "[ENV] ACCESS_CODE is: ${ACCESS_CODE:+SET (${#ACCESS_CODE} chars)}${ACCESS_CODE:-NOT SET}"
echo "Starting web server..."
exec gunicorn web.app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 --access-logfile - --error-logfile - --preload
