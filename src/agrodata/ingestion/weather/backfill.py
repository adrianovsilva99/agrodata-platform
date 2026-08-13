from datetime import date

from agrodata.ingestion.weather.run import run


BACKFILL_END_DATE = date(2024, 12, 31)

MAX_BATCHES = 5


def backfill():
    batches_processed = 0

    while batches_processed < MAX_BATCHES:
        processed = run(
            target_end_date=BACKFILL_END_DATE
        )

        if not processed:
            print("Backfill completed.")
            break

        batches_processed += 1

    print(
        f"Backfill execution finished. "
        f"Batches processed: {batches_processed}"
    )


if __name__ == "__main__":
    backfill()