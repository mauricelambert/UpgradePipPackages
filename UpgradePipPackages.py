#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file updates all python packages in this environment
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This file updates all python packages in this environment.
"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = "This file updates all python packages in this environment."
__license__ = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/UpgradePipPackages"

copyright = """
UpgradePipPackages  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
license = __license__
__copyright__ = copyright

print(copyright)

__all__ = []

import os

try:
    from asyncio import create_subprocess_exec, run, gather
    if os.name == 'nt':
        from asyncio import set_event_loop, ProactorEventLoop
except ImportError:
    ASYNC = False
else:
    ASYNC = True

from subprocess import PIPE, Popen
from os import device_encoding
from typing import List, Tuple
import sys

FIRST = True

def print_clear(string: str, precedent_length: int = 0, **kwargs) -> int:

    """This function print and clear the line."""

    if precedent_length:
        clear = '\b' * precedent_length

        print(f"{' ' * precedent_length}{clear}{string}", **kwargs)
        return 0

    length = len(string)
    clear = "\b" * length

    print(f'\x1b[34m{string}{clear}', end="\x1b[0m", **kwargs)
    sys.stdout.flush()
    return length

def get_packages() -> Tuple[List[str], str]:

    """This function execute a "pip freeze" 
    and return packages."""

    length = print_clear("[-] Getting packages and encoding...")
    encoding = device_encoding(0)
    process = Popen([sys.executable, '-m', 'pip', 'freeze'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print_clear("[+] Packages and encoding are defined.", length)
    return stdout.decode(encoding).split(), encoding

async def async_updates(packages: List[str], encoding: str):
    
    """This function updates packages using pip (asynchronous)."""

    ouputs = await gather(*(async_update(package, encoding) for package in packages))

    for i, (stdout, exitcode) in enumerate(ouputs):
        package = packages[i]

        if "=" not in package:
            print(f"\x1b[31m[!] This package is not updatable: {package}\x1b[0m")
            continue

        package = package.split("=")[0]

        if exitcode:
            print(f"\x1b[31m[!] {package} is not upgraded (exit code: {exitcode})\x1b[0m")
        else:
            print(f"\x1b[32m[+] {package} is upgraded\x1b[0m\n\t[*] ", end="")

        data = [x for x in stdout.split('\n') if x]
        if data:
            print(data[-1].strip())

async def async_update(package: str, encoding: str) -> Tuple[str, int]:
    
    """This function updates package using pip (asynchronous)."""

    global FIRST
    if FIRST:
        length = print_clear("[-] Creating processes...")
        first = True
        FIRST = False
    else:
        first = False

    package = package.split("=")[0]
    process = await create_subprocess_exec(sys.executable, '-m', 'pip', 'install', '--upgrade', package, stdout=PIPE, stderr=PIPE)

    if first:
        print_clear("[+] Processes are created.", length)
        print("[-] Waiting processes...")
#    stdout, stderr = await proc.communicate()

    await process.wait()
    stdout = await process.stdout.read()
    return stdout.decode(encoding), process.returncode

def updates(packages: List[str], encoding: str) -> None:

    """This function updates packages using pip."""

    for package in packages:
        if "=" not in package:
            print(f"\x1b[31m[!] This package is not updatable: {package}\x1b[0m")
            continue

        package = package.split("=")[0]
        length = print_clear(f"[-] Updating package named: {package}")

        process = Popen([sys.executable, '-m', 'pip', 'install', '--upgrade', package], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        if process.returncode:
            print_clear(f"\x1b[31m[!] {package} is not upgraded (exit code: {process.returncode})\x1b[0m")
        else:
            print_clear(f"\x1b[32m[+] {package} is upgraded\x1b[0m\n\t[*] ", length, end="")
        
        data = [x for x in stdout.split(b'\n') if x]
        if data:
            print(data[-1].decode(encoding).strip())

def main() -> None:

    """This function execute the file."""

    if os.name == "nt":
        os.system(r"reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f > NUL")

    if "-h" in sys.argv or "--help" in sys.argv:
        print(
            "USAGES:\n\tpython3 UpgradePipPackages.py -h/--help"
            "\n\tpython3 UpgradePipPackages.py"
            "\n\tpython3 UpgradePipPackages.py [package1] [package2] ..."
        )
        sys.exit(2)

    if len(sys.argv) == 1:
        packages, encoding = get_packages()
    else:
        encoding = device_encoding(0)
        packages = [f"{p}=" for p in sys.argv[1:]]

    if ASYNC:
        if os.name == "nt":
            set_event_loop(ProactorEventLoop())
        run(async_updates(packages, encoding))
    else:
        print(f"\x1b[31m[!] Error importing asyncio. Asynchronous is not available.\x1b[0m")
        updates(packages, encoding)

if __name__ == "__main__":
    main()
    sys.exit(0)
