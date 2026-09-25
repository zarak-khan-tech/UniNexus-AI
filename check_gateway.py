from backend.app.core.llm_gateway import get_gateway
gw = get_gateway()
import json
print(json.dumps(gw.status(), indent=2, default=str))
