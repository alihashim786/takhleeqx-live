import shutil
import os

src_dir = r"d:\fyp marketing\final Eval\Marketing Project\TakhleeqX"
dest_dir = r"d:\fyp marketing\final Eval\Marketing Project\TakhleeqX\takhleeqx_live_build"

def ignore_files(dir, files):
    return [f for f in files if f in ('node_modules', 'dist', 'venv', '.git', '__pycache__', 'takhleeqx_live_build', 'campaign_exports', 'scratch', '.tempmediaStorage')]

try:
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir, ignore=ignore_files)
    print("Copy successful")
except Exception as e:
    print(f"Copy failed: {e}")
