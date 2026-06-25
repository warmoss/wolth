import time
import psutil


def kill(pid, timeout=5):
    pid = int(pid)
    kill_process_tree(pid, force=False)  # 先优雅
    start = time.time()
    while psutil.pid_exists(pid):
        if time.time() - start > timeout:
            kill_process_tree(pid, force=True)  # 超时强杀
            break
        time.sleep(0.1)


def kill_process_tree(pid, force=True):
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    # 1. 获取所有子进程(递归), 必须先杀子进程再杀父进程, 否则子进程变孤儿
    children = parent.children(recursive=True)

    # 2. 终止子进程
    for child in children:
        try:
            if force:
                child.kill()  # 对应 SIGKILL
            else:
                child.terminate()  # 对应 SIGTERM
        except psutil.NoSuchProcess:
            pass

    # 3. 等待子进程结束(超时回收), 防止变成僵尸进程(Zombie)
    gone, alive = psutil.wait_procs(children, timeout=3)

    # 4. 对于3秒内没结束的, 补刀强制杀死
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass

    # 5. 最后终止父进程
    try:
        if force:
            parent.kill()
        else:
            parent.terminate()
        parent.wait(timeout=3)  # 关键! 回收父进程资源, 避免僵尸
    except psutil.NoSuchProcess:
        pass
    except psutil.TimeoutExpired:
        parent.kill()  # 实在杀不死就强制
