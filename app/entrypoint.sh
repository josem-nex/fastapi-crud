#!/bin/sh
set -e

export DATABASE_URL="$POSTGRESS_URL"

echo "=> Waiting for database to be ready..."
python - <<PY
import os, time, sys
from urllib.parse import urlparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("POSTGRESS_URL")
if not DATABASE_URL:
    print("DATABASE_URL not set", file=sys.stderr)
    sys.exit(1)

async def wait():
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    for i in range(60):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(lambda conn: None)
            print("DB ready.")
            await engine.dispose()
            return
        except Exception as e:
            print("DB not ready, waiting...", file=sys.stderr)  
            await asyncio.sleep(1)
    print("DB not ready after 60 seconds, exiting.", file=sys.stderr)
    sys.exit(1)

asyncio.run(wait())
PY

echo "=> Applying database migrations..."
alembic upgrade head

echo "=> Starting application..."
CMD="${CMD:-uvicorn main:app --host 0.0.0.0 --port ${UVICORN_PORT:-8000} --workers ${UVICORN_WORKERS:-1} --proxy-headers}"
exec $CMD
