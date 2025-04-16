from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers.stories import router
from slowapi.middleware import SlowAPIMiddleware
from app.scheduler import start_scheduler


app = FastAPI(
    title="HackerNews Stories API",
    description="An API to explore Hacker News top stories",
    version="1.0.0"
)
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
# Include routers
app.include_router(router)

# Start the scheduler if needed
start_scheduler()
