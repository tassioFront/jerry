from __future__ import annotations

import sys
from typing import Optional

from app.database import SessionLocal
from app.models.OutboxEvent import OutboxEvent


# # default batch size = 100
# docker compose run --rm outbox-worker python -m app.scripts.outbox

# # custom batch size, e.g. 50
# docker compose run --rm outbox-worker python -m app.scripts.outbox 50


def get_outbox_events(batch_size: int = 100) -> None:
    """Print a batch of events from the outbox_event table.

    Args:
        batch_size: Maximum number of rows to fetch (default: 100).
    """
    with SessionLocal() as db:
        events = (
            db.query(OutboxEvent)
            .order_by(OutboxEvent.occurred_at)
            .limit(batch_size)
            .all()
        )

        print(f"Fetched {len(events)} outbox events (limit={batch_size})")
        for e in events:
            print(
                f"id={e.id} | type={e.event_type} | status={e.status} | "
                f"aggregate_id={e.aggregate_id} | occurred_at={e.occurred_at} | "
                f"retry_count={e.retry_count}"
            )


def _parse_batch_size(arg: Optional[str]) -> int:
    if not arg:
        return 100
    try:
        value = int(arg)
        return value if value > 0 else 100
    except ValueError:
        return 100


if __name__ == "__main__":
    # Usage:
    #   python -m app.scripts.outbox           # default batch size 100
    #   python -m app.scripts.outbox 50        # custom batch size
    batch_size_arg = sys.argv[1] if len(sys.argv) > 1 else None
    batch_size = _parse_batch_size(batch_size_arg)
    get_outbox_events(batch_size)


