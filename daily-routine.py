import os
from subprocess import Popen, PIPE
import pexpect


pwd = 'xup6vup4cj/6'

def _execute(cmd, pwd):
	p = Popen(cmd, stdin=PIPE, stderr=PIPE, shell=True)
	sudo_prompt = p.communicate(pwd + '\n')[1]

def _update_ubuntu_start_vm(pwd):
	cmd = 'sudo -S apt-get dist-upgrade ; sudo -S apt-get update ; sudo -S apt-get upgrade -y ; sudo -S apt-get autoremove -y ; sudo -S apt-get autoclean ; sudo -S VBoxManage startvm WinXP'
	_execute(cmd, pwd)


def _update_git():
	cmd += 'eval $(ssh-agent) ; '
	cmd += '/home/linrex/sshadd xup6vup4cj/6 ; '
	cmd += 'cd ~/gitroot/4.5_work/ ; git fetch --all ; git pull ; git submodule update -- chromium/src tvsdk/uva/netview'
	_execute(cmd, pwd)

if __name__ == '__main__':
	_update_ubuntu_start_vm(pwd)