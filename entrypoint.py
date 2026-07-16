"""Reusable container entrypoint for a vGreens model image.

Dispatches on JOB_TYPE: training -> train.py, processing -> process.py.
Copy this into a new model repo unchanged; implement train.py and process.py.
"""
import os
import runpy

mode = os.environ.get("JOB_TYPE", "training")
script = "/app/process.py" if mode == "processing" else "/app/train.py"
print(f"[entrypoint] JOB_TYPE={mode} -> {script}", flush=True)
runpy.run_path(script, run_name="__main__")
