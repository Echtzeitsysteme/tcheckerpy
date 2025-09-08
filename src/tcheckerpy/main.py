from fastapi import FastAPI
from tcheckerpy.routers import tck_syntax
from tcheckerpy.routers import tck_reach
from tcheckerpy.routers import tck_liveness
from tcheckerpy.routers import tck_compare
from tcheckerpy.routers import tck_simulate
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Timed Automata Analysis Backend",
    description="A backend service for analyzing timed automata using TChecker.",
    version="1.0.0"
)

# Include routers from separate files
app.include_router(tck_syntax.router)
app.include_router(tck_reach.router)
app.include_router(tck_liveness.router)
app.include_router(tck_compare.router)
app.include_router(tck_simulate.router)

# Add the middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Allow any origin
    allow_credentials=True,           # Allow cookies/auth headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

 










