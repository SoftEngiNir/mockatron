from __future__ import annotations

from datetime import date, datetime, timedelta

from ddgen.engines.base import RandEngine
from ddgen.engines.registry import register_engine
from ddgen.utilities.helper_functions import (convert_to_date,
                                              convert_to_datetime)


@register_engine
class DateRandEngine(RandEngine[date]):
    def __init__(self, start_date=date(1900, 1, 1), end_date=date.today()) -> None:
        super().__init__()
        self.start_date = convert_to_date(start_date)
        self.end_date = convert_to_date(end_date)

    def sample(self):
        random_number_of_days = self._engine.randint(
            0,
            (self.end_date - self.start_date).days,
        )
        return self.start_date + timedelta(days=random_number_of_days)


@register_engine
class DateTimeRandEngine(RandEngine[datetime]):
    def __init__(
        self,
        start_datetime=datetime(1900, 1, 1),
        end_datetime=datetime.now(),
    ) -> None:
        super().__init__()
        self.start_datetime = convert_to_datetime(start_datetime)
        self.end_datetime = convert_to_datetime(end_datetime)

    def sample(self):
        random_seconds = self._engine.randint(
            0,
            int((self.end_datetime - self.start_datetime).total_seconds()),
        )
        return self.start_datetime + timedelta(seconds=random_seconds)


@register_engine
class TimedeltaRandEngine(RandEngine[timedelta]):
    def __init__(self, start_date=date(1900, 1, 1)) -> None:
        super().__init__()
        self.max_val = date.today() - convert_to_date(start_date)

    def sample(self):
        random_number_of_days = self._engine.randint(1, self.max_val.days)
        return timedelta(days=random_number_of_days)
