"""
Main entry point for running from command line.
"""

import os
import sys
import multiprocessing as mp

_PATH_ = os.path.dirname(os.path.dirname(__file__))


if _PATH_ not in sys.path:
    sys.path.append(_PATH_)


if __name__ == "__main__":
    mp.set_start_method('spawn')
    sys.setrecursionlimit(10000)
    from chess_zero import manager
    manager.start()

# import os
# import sys
# import time
# import subprocess
# import multiprocessing as mp

# _PATH_ = os.path.dirname(os.path.dirname(__file__))
# if _PATH_ not in sys.path:
#     sys.path.append(_PATH_)

# def run_selfplay():
#     # start subprocess với pipe
#     proc = subprocess.Popen(
#         ["python", "src/chess_zero/run.py", "--cmd", "self"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,  # trả về str thay vì bytes
#         bufsize=1
#     )

#     # đọc từng dòng nhưng không in tất cả
#     for line in proc.stdout:
#         if "Some summary string" in line:  # thay bằng 1 keyword tóm tắt
#             print(line.strip())
#     proc.wait()
#     return proc.returncode

# if __name__ == "__main__":
#     mp.set_start_method('spawn')
#     sys.setrecursionlimit(10000)

#     num_loops = 10
#     sleep_time = 5

#     for i in range(num_loops):
#         print(f"\n===== LOOP {i+1}/{num_loops} =====")

#         print(">>> [1/3] Self-play phase...")
#         ret = run_selfplay()
#         if ret == 0:
#             print("Self-play completed.")
#         else:
#             print("Self-play failed!")

#         print(">>> [2/3] Optimize phase...")
#         subprocess.run(
#             ["python", "src/chess_zero/run.py", "--cmd", "opt"],
#             stdout=sys.stdout,
#             stderr=sys.stderr
#         )

#         print(">>> [3/3] Evaluate phase...")
#         subprocess.run(
#             ["python", "src/chess_zero/run.py", "--cmd", "eval"],
#             stdout=sys.stdout,
#             stderr=sys.stderr
#         )

#         print(f"✅ Done loop {i+1}/{num_loops}. Waiting {sleep_time}s...\n")
#         time.sleep(sleep_time)
