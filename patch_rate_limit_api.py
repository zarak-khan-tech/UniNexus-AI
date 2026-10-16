# English: Add rate-limit check to /agents/run and /agents/reason endpoints.
# Roman Urdu: /agents/run aur /agents/reason endpoints pe rate-limit check.
path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Import limiter + HTTPException already imported
old_import = "from backend.app.core.reasoning import reason as reasoning_loop"
new_import = (
    "from backend.app.core.reasoning import reason as reasoning_loop\n"
    "from backend.app.core.rate_limit import rate_limiter"
)
if old_import not in content:
    print("ERROR: reasoning import anchor not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

# 2. Insert rate check in /agents/run (right after def signature, before 
# start = time.time())
old_run = '''def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    start = time.time()
    orchestrator = OrchestratorAgent()'''

new_run = '''def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # English: Per-user rate limit — 30 requests / 60s by default.
    # Roman Urdu: Per-user rate limit — 30 requests / 60s default.
    allowed, retry_after = rate_limiter.check(current_user.email)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    start = time.time()
    orchestrator = OrchestratorAgent()'''

if old_run not in content:
    print("ERROR: /agents/run signature block not found")
    raise SystemExit(1)
content = content.replace(old_run, new_run, 1)

# 3. Insert rate check in /agents/reason
old_reason = '''def run_reasoning(
    task_req: ReasoningRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    start = time.time()
    history_dicts = [h.dict() for h in (task_req.history or [])]'''

new_reason = '''def run_reasoning(
    task_req: ReasoningRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # English: Per-user rate limit — same bucket as /agents/run.
    # Roman Urdu: Per-user rate limit — /agents/run wala same bucket.
    allowed, retry_after = rate_limiter.check(current_user.email)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    start = time.time()
    history_dicts = [h.dict() for h in (task_req.history or [])]'''

if old_reason not in content:
    print("ERROR: /agents/reason signature block not found")
    raise SystemExit(1)
content = content.replace(old_reason, new_reason, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: agents.py patched with rate limiting")
