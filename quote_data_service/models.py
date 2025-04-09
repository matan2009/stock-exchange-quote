from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class QuoteData:
    symbol: str
    update_time: datetime
    price: float
    change_percent: str

    @property
    def serialize(self):
        return {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in asdict(self).items()
        }
