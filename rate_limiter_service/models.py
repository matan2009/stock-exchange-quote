from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimiterClient:
    quote_data_service_url: str
