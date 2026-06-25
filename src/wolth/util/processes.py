"""Process-management utilities.

Provides functions to terminate a process and all of its children in a
controlled manner, with support for both graceful (``SIGTERM``) and
forced (``SIGKILL``) shutdown.
"""

import time
import psutil


def kill(pid, timeout=5):
    """Terminate a process tree by PID, with graceful-then-forceful strategy.

    First tries a graceful shutdown of the entire process tree.  If the
    root process has not exited within *timeout* seconds, the tree is
    forcibly killed.

    Args:
        pid: Process ID of the root process.
        timeout: Maximum seconds to wait for graceful exit before forcing.
    """
    pid = int(pid)
    kill_process_tree(pid, force=False)  # graceful first
    start = time.time()
    while psutil.pid_exists(pid):
        if time.time() - start > timeout:
            kill_process_tree(pid, force=True)  # force after timeout
            break
        time.sleep(0.1)


def kill_process_tree(pid, force=True):
    """Terminate a process and all of its descendants.

    Children are killed **before** the parent to prevent orphan processes.
    After sending the termination signal, the function waits up to 3
    seconds for each child to exit and forcefully kills any survivors.

    Args:
        pid: Process ID of the root process.
        force: If ``True``, send ``SIGKILL`` (``kill``).
               If ``False``, send ``SIGTERM`` (``terminate``).
    """
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    # 1. Collect all children recursively
    children = parent.children(recursive=True)

    # 2. Terminate / kill children
    for child in children:
        try:
            if force:
                child.kill()
            else:
                child.terminate()
        except psutil.NoSuchProcess:
            pass

    # 3. Wait for children (reap zombies)
    gone, alive = psutil.wait_procs(children, timeout=3)

    # 4. Force-kill any children that didn't exit within 3s
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass

    # 5. Finally terminate the parent
    try:
        if force:
            parent.kill()
        else:
            parent.terminate()
        parent.wait(timeout=3)
    except psutil.NoSuchProcess:
        pass
    except psutil.TimeoutExpired:
        parent.kill()
