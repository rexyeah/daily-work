#! /usr/bin/python

from mailman import _mail
from shutil import copyfile
from subprocess import Popen, PIPE
import os
import re

######
"""
If there is a new project, add the project name in
watching_dict
"""
######

pikachu_storage_path = '/home/linrex/build/pikachu_storage'
local_storage_path = '/home/linrex/build/sdk'
OS_PASSWORD = os.environ['OS_PASSWORD']
watching_dict = {
    'indigo_4.8_release': 'INDIGO',
    'pixel_4.8_release': 'PIXEL',
    'alishan_4.8_release': 'ALISHAN6',
    'jeju_4.8_release': 'JEJU'
}

watching_release = watching_dict.keys()


def execute(cmd, pwd):
    p = Popen(cmd, stdin=PIPE, stderr=PIPE, shell=True)
    sudo_prompt = p.communicate(pwd + '\n')[1]


def get_release_targets(job):
    targets = map(
        lambda x: x.replace('label=ipa,target=', ''),
        os.listdir(
            os.path.join(pikachu_storage_path, job, 'latest')
        )
    )
    targets.remove('increase-build-number')
    return targets


def get_watching_jobs(jobs, watching_list):
    watching_jobs = []
    for job in jobs:
        if ['', job][any(j in job for j in watching_list)]:
            watching_jobs.append(job)
    return watching_jobs


def get_qa_pkg_path(job):
    targets = get_release_targets(job)
    qa_pkgs = []
    for target in targets:
        path = os.path.join(
            pikachu_storage_path,
            job,
            'latest',
            'label=ipa,target={target}'.format(target=target),
            'tvsdk',
            'packages'
        )
        qa_pkgs.append(filter(
            lambda p: re.search('^QA[-\w\.]*[\d].tar.gz$', p),
            os.listdir(path)
        )[0])
    return qa_pkgs


def get_matching_project_name(watching_job):
    return watching_dict[watching_job]


# main program starts here ========================================
if not len(os.listdir(pikachu_storage_path)):
    cmd = 'sudo -S mount %s' % pikachu_storage_path
    pwd = OS_PASSWORD
    execute(cmd, pwd)

pikachu_jobs = filter(
    lambda x: re.search('release', x), os.listdir(pikachu_storage_path)
)
pikachu_jobs = get_watching_jobs(pikachu_jobs, watching_release)
mail_content = ''
for pj in pikachu_jobs:
    qa_pkgs = get_qa_pkg_path(pj)
    project_name = get_matching_project_name(pj)
    targets = get_release_targets(pj)
    if len(targets) != len(qa_pkgs):
        continue
    pkgs = zip(targets, qa_pkgs)
    for pkg in pkgs:
        # NOTE: pkg[0] = target, pkg[1] = tarball name
        target = pkg[0]
        pkg_name = pkg[1]

        # generate the build num by parse the build name string
        start_idx = pkg_name.find(project_name) + len(project_name)+1
        end_idx = start_idx+2
        build_num = pkg_name[start_idx:end_idx].replace('-', '')

        # read the flag see if we should skip the pkg
        flag_path = os.path.join(local_storage_path, pj, pkg[0], '.FLAG')
        if os.path.exists(flag_path):
            f = open(flag_path, 'r')
            flag = f.readline()
            f.close()
            if build_num == flag:
                print '[EXISTED] %s => %s: %s' % (pj, target, flag)
                continue
            else:
                f = open(flag_path, 'w+')
                f.write(build_num)
                f.close()
        else:
            os.makedirs(os.path.join(local_storage_path, pj, pkg[0]))
            open(flag_path, 'a').close()
            f = open(flag_path, 'w+')
            f.write(build_num)
            f.close()

        local_pkg_dir_path = os.path.join(
            local_storage_path,
            pj,
            target,
            build_num,
        )
        pikachu_pkg_path = os.path.join(
            pikachu_storage_path,
            pj,
            'latest',
            'label=ipa,target={target}'.format(target=target),
            'tvsdk',
            'packages',
            pkg_name
        )
        log = '\nRunning\n[{job}] {target}:\nsrc: {src}\ndst: {dst}\n'.format(
            job=pj,
            target=target,
            src=pikachu_pkg_path,
            dst=os.path.join(local_pkg_dir_path, pkg_name)
        )
        print log

        if not os.path.exists(pikachu_pkg_path):
            print 'The file path is not accessible: %s' % pikachu_pkg_path
            continue

        # make local directories
        if not os.path.exists(local_pkg_dir_path):
            os.makedirs(local_pkg_dir_path)

        copyfile(pikachu_pkg_path, os.path.join(local_pkg_dir_path, pkg_name))
        mail_content += '[OK] {job}    {target}: {build_num}\n'.format(
            job=pj,
            target=target,
            build_num=build_num
        )
if len(mail_content) > 1:
    _mail('[release_build_sync] release builds are synced', mail_content)
