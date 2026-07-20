from contextlib import asynccontextmanager
from uuid import uuid4
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from app.config import settings
from app.graph import build_graph


# This will hold the compiled LangGraph
graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Creates a PostgreSQL connection pool for the
    LangGraph checkpointer when FastAPI starts.
    """

    global graph

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }

    with ConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=10,
        kwargs=connection_kwargs,
    ) as pool:

        # Create the PostgreSQL-backed checkpointer
        checkpointer = PostgresSaver(pool)

        # Creates LangGraph checkpoint tables if needed
        checkpointer.setup()

        # Compile the graph with persistent checkpointing
        graph = build_graph(checkpointer)

        print(
            "LangGraph initialized with "
            "Neon PostgreSQL connection pool"
        )

        yield

    print("Application shutting down")


app = FastAPI(
    title="AI-Powered SDLC Automation",
    description="Automates the Software Development Life Cycle using LangGraph",
    version="1.0.0",
    lifespan=lifespan
)


#-------------------------------------------
# REQUEST SCHEMA!!!!
#-------------------------------------------

class RequirementsRequest(BaseModel):
    requirements: str
    project_id: str | None = None


# -------------------------------------------
# TEST ENDPOINT!!!!
# -------------------------------------------

@app.get("/")
def root():
    return {
        "message": "SDLC Automation API is running"
    }


#-------------------------------------------
# PHASE 1 ENDPOINT
#-------------------------------------------

@app.post("/sdlc/requirements-to-stories")
def requirements_to_stories(
    request: RequirementsRequest
):
    """
    Phase 1:
    Converts software requirements into
    Agile user stories using LangGraph.
    """

    if graph is None:
        raise HTTPException(
            status_code=500,
            detail="LangGraph has not been initialized"
        )

    # Use supplied project ID or generate a new one
    project_id = (
        request.project_id
        if request.project_id
        else str(uuid4())
    )

    # LangGraph uses thread_id to identify
    # and save this workflow's checkpoints
    config = {
    "configurable": {
        "thread_id": project_id
    },
    "recursion_limit": 25
}

    # Initial LangGraph state
    initial_state = {
        "project_id": project_id,
        "requirements": request.requirements,
        "current_stage": "requirements_received"
    }

    try:
        # Run the graph
        result = graph.invoke(
            initial_state,
            config=config
        )

        return {
    "project_id": project_id,
    "current_stage": result.get("current_stage"),
    "requirements": result.get("requirements"),
    "user_stories": result.get("user_stories"),
    "product_owner_status": result.get("product_owner_status"),
    "product_owner_review": result.get("product_owner_review"),
    "product_owner_attempts": result.get("product_owner_attempts"),
    "design_docs": result.get("design_docs"),
    "generated_code": result.get("generated_code"),
    "code_review_status": result.get("code_review_status"),
    "code_review_feedback": result.get("code_review_feedback"),
    "code_review_attempts": result.get("code_review_attempts")
}

    except Exception:
        traceback.print_exc()
        raise


#-------------------------------------------
# CHECK SAVED STATE
#-------------------------------------------

@app.get("/sdlc/{project_id}/state")
def get_project_state(project_id: str):
    """
    Retrieves the latest saved LangGraph state
    for a project from the checkpointer.
    """

    if graph is None:
        raise HTTPException(
            status_code=500,
            detail="LangGraph has not been initialized"
        )

    config = {
        "configurable": {
            "thread_id": project_id
        }
    }

    snapshot = graph.get_state(config)

    if not snapshot.values:
        raise HTTPException(
            status_code=404,
            detail="No saved state found for this project"
        )

    return {
        "project_id": project_id,
        "state": snapshot.values
    }



