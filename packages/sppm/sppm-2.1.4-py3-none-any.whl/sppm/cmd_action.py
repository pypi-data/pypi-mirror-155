#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
from multiprocessing import Process

from sppm.process_status import ProcessStatus
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG
from sppm.utils import cleanup, setting_resource_permission


def kills(pid, sig):
    import psutil

    parent = psutil.Process(pid)

    for child in parent.children(recursive=True):
        child.kill()

    os.kill(pid, sig)


def action_start(is_no_daemon, target_callback, child_callback, *child_args, **child_kwargs):
    with open(SPPM_CONFIG.pid_file, 'w') as f:
        f.write(str(os.getpid()) + '\n')

    if is_no_daemon:
        hlog.info('**** 按Ctrl+C可以终止运行 ****')

    child_process = Process(name='sppm: worker process',
                            target=target_callback,
                            args=(child_callback, *child_args),
                            kwargs=child_kwargs)
    child_process.start()

    ProcessStatusLock.lock(child_process.pid, SPPM_CONFIG.lock_file)

    with open(SPPM_CONFIG.child_pid_file, 'w') as f:
        f.write(str(child_process.pid) + '\n')

    if 'user' in child_kwargs:
        setting_resource_permission(child_kwargs['user'])

    child_process.join()

    # 不管子进程是否切换运行用户，在此处都是root权限，可成功删除
    cleanup()


def action_stop(child_pid):
    # noinspection PyBroadException
    try:
        kills(child_pid, signal.SIGTERM)
    except ProcessLookupError:
        cleanup()

    ProcessStatusLock.wait_unlock(SPPM_CONFIG.lock_file)

    if SPPM_CONFIG.enable_timeout:
        action_shutdown(child_pid)


def action_reload(child_pid, target_callback, is_no_daemon, child_callback, *child_args, **child_kwargs):
    action_stop(child_pid)
    action_start(is_no_daemon, target_callback, child_callback, *child_args, **child_kwargs)


def action_shutdown(child_pid):
    # noinspection PyBroadException
    try:
        kills(child_pid, signal.SIGTERM)
        hlog.info('当前处于强杀模式下，子进程 %d 将被强制杀死......' % child_pid)

        kills(child_pid, signal.SIGKILL)
    except Exception:
        hlog.info('子进程已经退出')

    # 强杀模式，子进程无法自己释放资源文件，需要父进程手动释放
    cleanup()


def action_restart(child_pid, target_callback, is_no_daemon, child_callback, *child_args, **child_kwargs):
    action_shutdown(child_pid)
    action_start(is_no_daemon, target_callback, child_callback, *child_args, **child_kwargs)


def action_status():
    ps = ProcessStatus(SPPM_CONFIG.lock_file)
    print(ps)
