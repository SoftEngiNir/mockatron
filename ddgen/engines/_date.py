from datetime import datetime, timedelta, date
from ddgen.engines.base import RandEngine


class DateRandEngine(RandEngine[date]):

    def __init__(self, start_date=date(1900, 1, 1) , end_date=date.today()) -> None:
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        
    def sample(self):
        random_number_of_days = self._engine.randint(0, (self.end_date - self.start_date).days)
        return self.start_date + timedelta(days=random_number_of_days)
    
class DateTimeRandEngine(RandEngine[datetime]):

    def __init__(self, start_datetime=datetime(1900, 1, 1) , end_datetime=datetime.now()) -> None:
        super().__init__()
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        
    def sample(self):
        random_seconds = self._engine.randint(0, int((self.end_datetime - self.start_datetime).total_seconds()))
        return self.start_datetime + timedelta(seconds=random_seconds)
    
