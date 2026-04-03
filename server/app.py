import argparse
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

for path in (ROOT_DIR, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from supply_chain_env.environment import Action, SupplyChainEnv
from supply_chain_env.grader import grade
from supply_chain_env.inference import inference_agent, run_all_tasks
from supply_chain_env.tasks import TASKS


class StepRequest(BaseModel):
    session_id: str
    orders: List[float]


class SessionData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    env: Any
    task: str
    seed: int
    trajectory: List[Dict[str, Any]]


app = FastAPI(title="Supply Chain OpenEnv API", version="0.1.0")
SESSIONS: Dict[str, SessionData] = {}


def _ensure_session(session_id: str) -> SessionData:
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Unknown session_id. Call /reset first.")
    return SESSIONS[session_id]


def _create_session(task: str, seed: int) -> Dict[str, Any]:
    if task not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task: {task}")

    env = SupplyChainEnv(task=task, seed=seed)
    obs = env.reset(seed=seed)
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = SessionData(
        env=env,
        task=task,
        seed=seed,
        trajectory=[],
    )
    return {
        "session_id": session_id,
        "task": task,
        "observation": obs.model_dump(),
    }


@app.get("/")
def root() -> Dict[str, Any]:
    return {"ok": True, "service": "supply-chain-openenv"}


@app.post("/reset")
async def reset(request: Request, task: str = "easy", seed: int = 42) -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    try:
        parsed = await request.json()
        if isinstance(parsed, dict):
            body = parsed
    except Exception:
        body = {}

    req_task = str(body.get("task", task))
    req_seed = int(body.get("seed", seed))
    return _create_session(task=req_task, seed=req_seed)


@app.get("/reset")
def reset_get(task: str = "easy", seed: int = 42) -> Dict[str, Any]:
    return _create_session(task=task, seed=seed)


@app.post("/step")
def step(payload: StepRequest) -> Dict[str, Any]:
    session = _ensure_session(payload.session_id)
    obs, reward, done, info = session.env.step(Action(orders=payload.orders))
    session.trajectory.append({"reward": reward, "info": info})
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/state")
def state(session_id: str) -> Dict[str, Any]:
    session = _ensure_session(session_id)
    return session.env.state().model_dump()


@app.get("/tasks")
def tasks() -> Dict[str, Any]:
    return {
        "tasks": [
            {
                "name": cfg.name,
                "description": cfg.description,
                "demand_std": cfg.demand_std,
                "seasonal_amplitude": cfg.seasonal_amplitude,
                "disruption_prob": cfg.disruption_prob,
                "delay_prob": cfg.delay_prob,
            }
            for cfg in TASKS.values()
        ]
    }


@app.get("/baseline")
def baseline(episodes: int = 1, seed: int = 42) -> Dict[str, Any]:
    safe_episodes = max(1, episodes)
    return {
        "episodes": safe_episodes,
        "seed": seed,
        "scores": run_all_tasks(episodes=safe_episodes, seed=seed),
    }


@app.get("/grader")
def grader(session_id: str) -> Dict[str, Any]:
    session = _ensure_session(session_id)
    return {
        "task": session.task,
        "steps": len(session.trajectory),
        "score": grade(session.task, session.env, session.trajectory),
    }


@app.post("/autostep")
def autostep(session_id: str) -> Dict[str, Any]:
    session = _ensure_session(session_id)
    action = inference_agent(session.env._get_observation())
    step_result = step(StepRequest(session_id=session_id, orders=action.orders))
    step_result["action"] = action.orders
    return step_result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Supply Chain OpenEnv server")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=7860, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable Uvicorn auto-reload")
    args = parser.parse_args()
    uvicorn.run("server.app:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
