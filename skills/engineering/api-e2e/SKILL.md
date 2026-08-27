---
name: api-e2e
description: "Run a real HTTP API E2E check with visible header, request, and response steps."
disable-model-invocation: true
---

# API E2E

Invoke this skill only when you want to extend a TDD run with a real API check.
It does not change default `/tdd` behavior.

## Workflow

1. **Extend**. Add the API E2E gate to the active TDD run.
2. **Target**. Identify the running API URL, startup command, and required environment.
3. **Script**. Use `./e2e-scripts/api_e2e.py`. Write it if missing.
4. **Request**. Send the request to the running service over HTTP.
5. **Response**. Verify status, body text, or exact JSON.
6. **Trace**. Output `header`, `request`, and `resp` records in that order.

```bash
python3 ./e2e-scripts/api_e2e.py \
  --url "$API_BASE_URL/health" \
  --method GET \
  --expect-status 200 \
  --expect-json '{"status":"ok"}'
```

Use a real running service.
Do not use a mock, stub, or in-process handler.

## Completion

Finish with `API trace`, `Passing check`, `Normal command`, and `Untestable`.
Report `Untestable: no API boundary` when the change has no HTTP boundary.
