#!/usr/bin/python

# Copyright (c) 2015 nexB Inc. http://www.nexb.com/ - All rights reserved.

"""
This script a configuration helper to select pip requirement files to install
and python and shell configuration scripts to execute based on provided config
directories paths arguments and the operating system platform. To use, create
a configuration directory tree that contains any of these:

 * Requirements files named with this convention:
 - base.txt contains common requirements installed on all platforms.
 - win.txt, linux.txt, mac.txt, posix.txt, cygwin.txt are platform-specific
   requirements to install.

 * Python scripts files named with this convention:
 - base.py is a common script executed on all platforms, executed before
   os-specific scripts.
 - win.py, linux.py, mac.py, posix.py, cygwin.py are platform-specific
   scripts to execute.

 * Shell or Windows CMD scripts files named with this convention:
 - win.bat is a windows bat file to execute
 - posix.sh, linux.sh, mac.sh, cygwin.sh  are platform-specific scripts to
   execute.

The config directory structure contains one or more directories paths. This
way you can have a main configuration and additional sub-configurations of a
product such as for prod, test, ci, dev, or anything else.

All scripts and requirements are optional and only used if presents. Scripts
are executed in sequence, one after the other after all requirements are
installed, so they may import from any installed requirement.

The execution order is:
 - requirements installation
 - python scripts execution
 - shell scripts execution

On posix, posix Python and shell scripts are executed before mac or linux 
scripts.

The base scripts or packages are always installed first before platform-
specific ones.

For example a tree could be looking like this::
    etc/conf
        base.txt : base pip requirements for all platforms
        linux.txt : linux-only pip requirements
        base.py : base config script for all platforms
        win.py : windows-only config script
        posix.sh: posix-only shell script

    etc/conf/prod
            base.txt : base pip requirements for all platforms
            linux.txt : linux-only pip requirements
            linux.sh : linux-only script
            base.py : base config script for all platforms
            mac.py : mac-only config script
"""

from __future__ import print_function

import os
import stat
import sys
import shutil
import subprocess


# platform-specific file base names
sys_platform = str(sys.platform).lower()
on_win = False
if 'linux' in sys_platform:
    platform_names = ('posix', 'linux',)
elif'win32' in sys_platform:
    platform_names = ('win',)
    on_win = True
elif 'darwin' in sys_platform:
    platform_names = ('posix', 'mac',)
elif 'cygwin' in sys_platform:
    platform_names = ('posix', 'cygwin',)
else:
    raise Exception('Unsupported OS/platform')
    platform_names = tuple()

# common file basenames for requirements and scripts
base = ('base',)

# known full file names with txt extension for requirements
# base is always last
requirements = tuple(p + '.txt' for p in platform_names + base)

# known full file names with py extensions for scripts
# base is always last
python_scripts = tuple(p + '.py' for p in platform_names + base)

# known full file names of shell scripts
# there is no base for scripts: they cannot work cross OS (cmd vs. sh)
shell_scripts = tuple(p + '.sh' for p in platform_names)
if on_win:
    shell_scripts = ('win.bat',)


def call(cmd):
    """ Run a `cmd` command (as a list of args) with all env vars."""
    cmd = ' '.join(cmd)
    if  subprocess.Popen(cmd, shell=True, env=dict(os.environ)).wait() != 0:
        print()
        print('Failed to execute command:\n%(cmd)s' % locals())
        sys.exit(1)


def clean(root_dir):
    """
    Remove cleanable directories and files.
    """
    print('* Cleaning ...')
    cleanable = '''build bin lib include 
                   django_background_task.log
                   develop-eggs eggs parts .installed.cfg 
                   .Python
                   .cache
                   .settings
                   pip-selfcheck.json
                   '''.split()

    for d in cleanable:
        loc = os.path.join(root_dir, d)
        if os.path.exists(loc):
            if os.path.isdir(loc):
                shutil.rmtree(loc)
            else:
                os.remove(loc)


def pip_dirs(tpp_dirs, flag='--extra-search-dir='):
    for tpp_dir in tpp_dirs:
        yield flag + tpp_dir


def create_virtualenv(std_python, tpp_dirs, root_dir):
    """
    Create a virtualenv in root_dir.
    """
    print()
    print("* Configuring Python ...")
    default_tpp_dir = tpp_dirs[0]
    venv = os.path.join(default_tpp_dir, 'virtualenv.py')
    vcmd = [std_python, venv, '--never-download']
    # third parties may be in more than one directory
    vcmd.extend(pip_dirs(tpp_dirs))
    # we create the env in root_dir
    vcmd.append(root_dir)
    call(vcmd)


def activate(root_dir):
    """ Activate a virtualenv in the current process."""
    activate_this = os.path.join(bin_dir, 'activate_this.py')
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))


def install_3pp(configs, root_dir, tpp_dirs):
    """ Install requirements with pip."""
    print()
    print("* Installing components ...")
    for req_file in get_conf_files(configs, requirements):
        pcmd = ['pip', 'install', '--no-allow-external', 
                '--use-wheel', '--no-index']
        pcmd.extend(pip_dirs(tpp_dirs, '--find-links='))
        req_loc = os.path.join(root_dir, req_file)
        pcmd.extend(['-r' , req_loc])
        call(pcmd)


def run_scripts(configs, root_dir, configured_python):
    """ Run py_script and sh_script scripts."""
    print()
    print("* Configuring ...")
    # Run Python scripts for each configurations
    for py_script in get_conf_files(configs, python_scripts):
        cmd = [configured_python, os.path.join(root_dir, py_script)]
        call(cmd)

    # Run sh_script scripts for each configurations
    for sh_script in get_conf_files(configs, shell_scripts):
        # we source the scripts on posix
        cmd = ['.']
        if on_win:
            cmd = []
        cmd = cmd  + [os.path.join(root_dir, sh_script)]
        call(cmd)


def chmod_bin(directory):
    """
    Makes the directory and its children executable recursively.
    """
    rwx = (stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR
           | stat.S_IXGRP | stat.S_IXOTH)
    for path, _, files in os.walk(directory):
        for f in files:
            os.chmod(os.path.join(path, f), rwx)


def get_conf_files(config_dir_paths, file_names=requirements):
    """
    Based on config_dir_paths return a list of collected path-prefixed file
    paths matching names in a file_names tuple. Returned paths are posix
    paths.

    @config_dir_paths: Each config_dir_path is a relative from the project
    root to a config dir. This script should always be called from the project
    root dir.

    @file_names: get requirements, python or shell files based on list of
    supported file names provided as a tuple of supported file_names.

    Scripts or requirements are optional and only used if presents. Unknown
    scripts or requirements file_names are ignored (but they could be used
    indirectly by known requirements with -r requirements inclusion, or
    scripts with python imports.)

    Since Python scripts are executed after requirements are installed they
    can import from any requirement-installed component such as Fabric.
    """
    # collect files for each requested dir path
    collected = []

    for config_dir_path in config_dir_paths:
        # Support args like enterprise or enterprise/dev
        paths = config_dir_path.strip('/').replace('\\', '/').split('/')
        # a tuple of (relative path, location,)
        current = None
        for path in paths:
            if not current:
                current = (path, os.path.abspath(path),)
            else:
                base_path, base_loc = current
                current = (os.path.join(base_path, path),
                           os.path.join(base_loc, path),)

            path, loc = current
            # we iterate on known filenames to ensure the defined precedence
            # is respected (posix over mac, linux), etc
            for n in file_names:
                for f in os.listdir(loc):
                    if f == n:
                        f_loc = os.path.join(path, f)
                        if f_loc not in collected:
                            collected.append(f_loc)

    return collected


if __name__ == '__main__':
    # define/setup common directories
    etc_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.dirname(etc_dir)

    args = sys.argv[1:]
    if args[0] == '--clean':
        clean(root_dir)
        sys.exit(0)

    sys.path.insert(0, root_dir)
    bin_dir = os.path.join(root_dir, 'bin')
    standard_python = sys.executable

    if on_win:
        configured_python = os.path.join(bin_dir, 'python.exe')
        scripts_dir = os.path.join(root_dir, 'Scripts')
        bin_dir = os.path.join(root_dir, 'bin')
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
        if not os.path.exists(bin_dir):
            cmd = ('mklink /J %(bin_dir)s %(scripts_dir)s' % locals()).split()
            call(cmd)
    else:
        configured_python = os.path.join(bin_dir, 'python')
        scripts_dir = bin_dir

    # one or more third-party directories may exist
    # as env vars prefixed with TPP_DIR
    thirdparty_dirs = [v for k, v in sorted(os.environ.items())
                       if k.startswith('TPP_DIR')]

    if not os.path.exists(configured_python):
        create_virtualenv(standard_python, thirdparty_dirs, root_dir)
    activate(root_dir)

    # get requested configuration paths and install components and run scripts
    configs = args[:]
    install_3pp(configs, root_dir, thirdparty_dirs,)
    run_scripts(configs, root_dir, configured_python)
    chmod_bin(bin_dir)
