from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.docker_manager import create_workspace_container, get_docker_status


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/workspace/status")
def workspace_status():
    status = get_docker_status()
    if not status["available"]:
        raise HTTPException(status_code=503, detail=status["error"])
    return status


class WorkspaceRequest(BaseModel):
    name: str


@app.post("/workspace/start")
def start_workspace(data: WorkspaceRequest):
    try:
        result = create_workspace_container(data.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "status": "running",
        "workspace": data.name,
        "url": result["url"],
    }
