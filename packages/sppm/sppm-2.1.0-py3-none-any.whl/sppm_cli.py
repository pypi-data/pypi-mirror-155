#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing
import argparse
import os
import pwd
import sys

from happy_python import HappyLog

from sppm_help import build_sppm_help

hlog = HappyLog.get_instance()


def child_callback(*args, **kwargs):
    from happy_python import get_exit_status_of_cmd
    from setproctitle import setproctitle

    hlog.debug(args)
    hlog.debug(kwargs)

    setproctitle(multiprocessing.current_process().name)

    try:
        user_info = pwd.getpwnam(kwargs['user'])

        # 切换系统用户，然后运行命令
        # 必须先设置组
        os.setgid(user_info.pw_gid)
        os.setuid(user_info.pw_uid)

        get_exit_status_of_cmd(kwargs['shell'])
    except KeyError:
        hlog.error('运行用户"%s"不存在' % kwargs['user'])
        exit(1)
    except PermissionError:
        hlog.error('无法切换至运行用户"%s"，没有系统权限' % kwargs['user'])
        exit(1)


def cli_build_help():
    cli_parser = argparse.ArgumentParser(prog=sys.argv[0],
                                         description='Sample Python Process Manager 客户端，直接将Shell命令'
                                                     '转换为可管理的服务进程，方便管理。比如管理SpringBoot程序',
                                         usage='%(prog)s '
                                               '--no-daemon '
                                               '-v '
                                               '-l '
                                               '--name progress_name '
                                               '[--start|--stop|--reload|--shutdown|--restart|--status] '
                                               '--user user'
                                               '[shell]'
                                         )

    build_sppm_help(cli_parser)

    cli_parser.add_argument('--name',
                            help='显示的进程名称，仅支持字母、数字和下划线组成的字符串',
                            type=str,
                            required=True)

    cli_parser.add_argument('--user',
                            help='指定运行Shell命令的用户，配合 --start 或 --restart 参数使用',
                            type=str,
                            required=False)

    cli_parser.add_argument('shell',
                            help='执行的Shell命令，配合 --start 或 --restart 参数使用',
                            nargs='?')

    return cli_parser


def build_sppm_cli_cfg(cfg_name):
    from pathlib import Path

    config = {
        'pid': ('/var/run/%s.pid' % cfg_name),
        'child_pid': ('/var/run/child_%s.pid' % cfg_name),
        'lock': ('/var/lock/subsys/%s' % cfg_name),
        'log': ('/var/log/sppm_cli/%s.log' % cfg_name),
        'timeout': 0
    }

    cfg_filename = Path('/tmp/sppm_cli/%s.env' % cfg_name)

    Path('/var/log/sppm_cli').mkdir(exist_ok=True)

    if not cfg_filename.parent.exists():
        cfg_filename.parent.mkdir(parents=True)

    with open(cfg_filename, 'w') as f:
        for k, v in config.items():
            f.write('%s=%s\n' % (k, v))

    os.environ['SPPM_ENV'] = str(cfg_filename)


def is_alnum_and_underscore(s):
    """
    判断字符串是否由字母、数字和下划线组成
    """
    return all(c.isalnum() or c == '_' for c in s)


def main():
    parser = cli_build_help()
    cmd_args = parser.parse_args()

    if not is_alnum_and_underscore(cmd_args.name):
        hlog.error('"name"参数值仅支持字母、数字和下划线组成的字符串')
        exit(1)

    is_start_type_cmd = cmd_args.start or cmd_args.restart
    is_shell = cmd_args.shell and len(cmd_args.shell) != 0
    is_user = cmd_args.user and len(cmd_args.user) != 0

    if is_start_type_cmd and not is_shell:
        hlog.error('指定"start"参数或"restart"参数后，必须同时指定Shell命令')
        exit(1)

    if is_start_type_cmd and not is_user:
        hlog.error('指定"start"参数或"restart"参数后，必须同时指定运行用户')
        exit(1)

    if os.getgid() != 0:
        hlog.error('sppm_cli必须使用root权限运行')
        exit(1)

    build_sppm_cli_cfg(cmd_args.name)

    try:
        import sppm
    except ModuleNotFoundError:
        import sys
        from pathlib import Path

        # 解决直接从源代码（未安装sppm包）运行时，"import sppm" 无法导入问题
        sppm_root_src = str(Path(__file__).absolute().parent.parent)
        sys.path.insert(0, sppm_root_src)

        import sppm

    sppm.sppm_start_shell(child_callback, cmd_args)


if __name__ == "__main__":
    main()
