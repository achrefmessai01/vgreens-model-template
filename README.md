# vgreens-model-template

Template + shared CI/CD for vGreens model repos. Every model (detection,
classification, regression, …) is its own repo that plugs into the same platform
pipeline — this repo keeps that pipeline in ONE place so all models stay in sync.

## What's here

```
ci/model-ci.yml          the reusable pipeline (lint -> test -> build+push -> manual submit)
entrypoint.py            reusable dispatch on JOB_TYPE (training -> train.py, processing -> process.py)
configs/model.yaml.example   per-model config skeleton (train params + validation thresholds)
.gitlab-ci.yml.example   what a model repo's whole pipeline looks like (an include + a few vars)
```

## Start a new model

1. Create a repo, e.g. `vgreens-model-<name>`.
2. Add `entrypoint.py` (copy as-is), a `Dockerfile`, `train.py`, `process.py`, `configs/<name>.yaml`, `tests/`.
3. Add a `.gitlab-ci.yml` = the `.gitlab-ci.yml.example` here, with your `MODEL_NAME` / `DATASET_*` / `CONFIG_PATH`.
4. Set CI/CD variables `VGREENS_API_URL` and `VGREENS_API_TOKEN`.

Reference implementation: **`vgreens-model-strawberry`** (a complete, working example).

## What the pipeline does on each push

`lint` → `test` → `build_image` (docker build + push to the Container Registry, tag =
commit SHA) → `submit_training` (**manual**: calls the Job API to enqueue a training with
that exact image). Training runs on a GPU worker via the queue; the result is validated
against the config's thresholds and versioned in the registry. **CI never touches a GPU.**

Change the pipeline once here → every model repo picks it up on its next run.

## To run CI live

- Register a **GitLab Runner** (CPU-only, anywhere) to the model projects.
- One-time `docker login` on the GPU host so the worker can pull images from the registry.
