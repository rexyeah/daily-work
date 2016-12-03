
import sys
import os
from subprocess import Popen, PIPE

sys.path.insert(0, os.environ['ERP_WORKING_DIR'])
from resource import *


def _execute(cmd):
    p = Popen(cmd, stdin=PIPE, stderr=PIPE, shell=True)


def _mail(subject, content):
    cmd = 'echo "{content}" | ' \
        'mailx -v ' \
        '-r "{from_user}" ' \
        '-s "{subject}" ' \
        '-S smtp="smtp.gmail.com:587" ' \
        '-S smtp-use-starttls ' \
        '-S smtp-auth=login ' \
        '-S smtp-auth-user="{username}" ' \
        '-S smtp-auth-password="{password}" ' \
        '-S ssl-verify=ignore ' \
        '{to}'.format(
            content=content,
            from_user=username,
            subject=subject,
            username=username,
            password=password,
            to=username
        )
    _execute(cmd)
