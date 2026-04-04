# Idea: Faster CI Pipeline with Cached Layers

**Created**: 2026-01-15
**Status**: inbox
**Category**: tool
**Effort**: M

## What
Build a CI caching layer that persists Docker build layers and cargo/npm caches across runs. Currently every CI run starts from scratch, rebuilding all dependencies.

## Why
CI runs take 12 minutes on average. With proper caching, dependency resolution could be skipped entirely, dropping to ~3 minutes. This would save 30+ developer-hours per week across the team.

## Next Steps
- [ ] Audit current CI pipeline for cacheable steps
- [ ] Evaluate GitHub Actions cache vs self-hosted cache (S3)
- [ ] Prototype with a single build target

## Notes
Similar to what Turborepo does for monorepos but at the Docker layer level. #ci-cd #docker #optimization
