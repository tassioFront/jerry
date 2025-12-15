"""Outbox worker for reliable event publishing.

This script implements the dispatcher/worker part of the transactional outbox
pattern. It periodically scans the `outbox_event` table for pending events,
publishes them via `EventPublisher`, and marks them as processed.

You can run it as a separate process, for example:

    poetry run python -m app.scripts.outbox_worker
    # or
    python -m app.scripts.outbox_worker
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import logging
from typing import Sequence

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.events import EventPublisher
from app.models.OutboxEvent import OutboxEvent

logger = logging.getLogger(__name__)


async def process_outbox_batch(
    db: Session,
    batch_size: int = 100,
) -> int:
    """Process a batch of pending outbox events.

    Returns:
        Number of events processed in this batch.
    """
    # Fetch a batch of pending events ordered by occurrence time
    pending_events: Sequence[OutboxEvent] = (
        db.query(OutboxEvent)
        .filter(OutboxEvent.status == "pending")
        .order_by(OutboxEvent.occurred_at)
        .limit(batch_size)
        .all()
    )

    if not pending_events:
        return 0

    logger.info("Found %d pending outbox events to process", len(pending_events))

    processed_count = 0

    for event in pending_events:
        try:
            # Mark as processing (optional but useful for observability)
            event.status = "processing"
            db.flush()

            logger.info(
                "Publishing outbox event id=%s type=%s",
                event.id,
                event.event_type,
            )

            await EventPublisher.publish(
                event.event_type,
                event.payload,
            )

            event.status = "published"
            event.published_at = datetime.now(timezone.utc)
            event.last_error = None
            processed_count += 1

        except Exception as exc:  # noqa: BLE001
            # Do not raise – we want to keep processing the rest of the batch.
            logger.exception(
                "Failed to publish outbox event id=%s type=%s",
                event.id,
                event.event_type,
            )
            event.status = "failed"
            event.retry_count += 1
            event.last_error = str(exc)

        finally:
            db.add(event)

    db.commit()
    return processed_count


async def run_outbox_worker(
    poll_interval_seconds: float = 5.0,
    batch_size: int = 100,
) -> None:
    """Continuously poll and process outbox events."""
    logger.info(
        "Starting outbox worker (poll_interval=%ss, batch_size=%s)",
        poll_interval_seconds,
        batch_size,
    )

    while True:
        db: Session = SessionLocal()
        try:
            processed = await process_outbox_batch(db, batch_size=batch_size)
        except Exception:  # noqa: BLE001
            logger.exception("Unexpected error while processing outbox batch")
            processed = 0
        finally:
            db.close()

        if processed == 0:
            # No work; sleep for the full interval
            await asyncio.sleep(poll_interval_seconds)
        else:
            # If we processed something, loop again immediately to drain backlog faster
            await asyncio.sleep(0)


def _configure_logging() -> None:
    """Configure basic logging for the worker."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )


if __name__ == "__main__":
    _configure_logging()
    try:
        asyncio.run(run_outbox_worker())
    except KeyboardInterrupt:
        logger.info("Outbox worker stopped by user")


