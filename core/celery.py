"""Celery initialization and configuration."""

from celery import Celery, signature
from src.db.db_session import SessionLocal
from src.repositories.sync_repos import SyncContactRepository, \
    SyncUserRepository, SyncMeetingRepository
from src.services.datetime_service import DateTimeService
from src.usecases.bingo_usecase import BingoUsecase

app = Celery("catchapp")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    """Periodic tasks go here."""
    sender.add_periodic_task(
        10,  # every 10 seconds
        signature("core.celery.schedule_meeting"),
        name="Schedule meeting.",
    )


@app.task
def schedule_meeting():
    """Schedule meeting."""
    with SessionLocal() as session:
        usecase = BingoUsecase(
            contact_repository=SyncContactRepository(session),
            user_repository=SyncUserRepository(session),
            meeting_repository=SyncMeetingRepository(session),
            service=DateTimeService()
        )
    usecase.schedule_meeting()
