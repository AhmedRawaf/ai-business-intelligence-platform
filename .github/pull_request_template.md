## Why

<!-- Explain business reason, bug, or feature goal. -->

## What Changed

- 
- 
- 

## Architecture / Risk Notes

- Impacted areas:
  - [ ] Backend API
  - [ ] Celery tasks
  - [ ] RAG / AI behavior
  - [ ] Frontend UI/UX
  - [ ] Security / auth / RBAC
  - [ ] Data model / migration
- Multi-tenant isolation risk: low / medium / high
- Breaking change: yes / no

## Test Plan

- [ ] Unit tests updated
- [ ] Manual API test done
- [ ] Frontend flow tested
- [ ] No secrets committed
- [ ] Logs/errors checked

## Review Focus (for CodeRabbit & humans)

Please prioritize:
1. Security vulnerabilities (auth, RBAC, data isolation)
2. Regression risks and edge cases
3. Async/background task correctness
4. API contract consistency and error handling
5. Performance concerns (N+1, heavy loops, large payloads)

## Deployment Notes

<!-- Any env vars, migrations, or rollout sequencing needed. -->
