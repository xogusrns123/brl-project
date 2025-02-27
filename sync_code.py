import argparse
import subprocess
import socket

HOSTFILE = './elastic-switch/trace/hostfile_aws_T4' # can be set by --hostfile
# HOMEDIR = '/home/ubuntu/spot_inference'  # set this to the directory where this python script is
# MASTER = '172.31.28.108' # set this to the master(source) node's IP address
HOMEDIR = '/home/kth/brl/SpotServe'  # set this to the directory where this python script is
MASTER = 'mango4.kaist.ac.kr' # set this to the master(source) node's IP address

NNodes = None
PASSWORD = 'th28620720!'

def parse_args():
    global NNodes, HOSTFILE
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1)
    parser.add_argument('--hostfile', type=str, default=HOSTFILE)
    parser.add_argument('--sync-dataset', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    NNodes = args.n
    HOSTFILE = args.hostfile
    return args

def get_hosts():
    global NNodes
    hosts = []
    with open(HOSTFILE, 'r') as f:
        for ip in f.readlines():
            ip = ip.split()[0].strip()
            hosts.append(ip)

            if len(hosts) == NNodes:
                break
    return hosts

# aws에서는 기본적으로 ubuntu 계정을 사용함
# def get_rsync_FT_cmd(ip):
#     cmd = f'rsync -q --timeout=5 -avr --delete --exclude ".git" \
#             --exclude "*.pyc" {HOMEDIR}/FasterTransformer ubuntu@{ip}:{HOMEDIR}/'
#     return cmd

# def get_rsync_PC_cmd(ip):
#     cmd = f'rsync -q --timeout=5 -avr --delete --exclude ".git" \
#             --exclude "*.pyc" {HOMEDIR}/ParamsClient ubuntu@{ip}:{HOMEDIR}/'
#     return cmd

# def get_rsync_GS_cmd(ip):
#     cmd = f'rsync -q --timeout=5 -avr --delete --exclude ".git" \
#             --exclude "*.pyc" {HOMEDIR}/elastic-switch ubuntu@{ip}:{HOMEDIR}/'
#     return cmd

# 내 lab server: kth
# def create_directories(ip):
#     # Create necessary directories on the remote node
#     cmd = f'sshpass -p {PASSWORD} ssh kth@{ip} "mkdir -p  \
#             {HOMEDIR}/ckpt {HOMEDIR}/FasterTransformer {HOMEDIR}/ParamsClient {HOMEDIR}/elastic-switch"'
#     print(cmd)
#     p = subprocess.Popen(cmd, shell=True)
#     p.wait()

def get_rsync_FT_cmd(ip):
    cmd = f'sshpass -p {PASSWORD} rsync -q --timeout=5 -avr --delete --exclude ".git" \
            --exclude "*.pyc" {HOMEDIR}/FasterTransformer kth@{ip}:{HOMEDIR}/'
    return cmd

def get_rsync_PC_cmd(ip):
    cmd = f'sshpass -p {PASSWORD} rsync -q --timeout=5 -avr --delete --exclude ".git" \
            --exclude "*.pyc" {HOMEDIR}/ParamsClient kth@{ip}:{HOMEDIR}/'
    return cmd

def get_rsync_GS_cmd(ip):
    cmd = f'sshpass -p {PASSWORD} rsync -q --timeout=5 -avr --delete --exclude ".git" \
            --exclude "*.pyc" {HOMEDIR}/elastic-switch kth@{ip}:{HOMEDIR}/'
    return cmd

def sync_dataset(ip):
    cmd = f'sshpass -p {PASSWORD} rsync -q --timeout=5 -avr --delete {HOMEDIR}/ckpt kth@{ip}:{HOMEDIR}'
    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()


def sync_code(ip_lists, args):
    processes = []
    for ip in ip_lists:
        if ip == MASTER or ip == '.'.join(MASTER.split('-')[1:]):
            continue

        cmd = f'sshpass -p {PASSWORD} ssh kth@{ip} "mkdir -p {HOMEDIR}/"'
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

        # create_directories(ip)

        if args.sync_dataset:
            sync_dataset(ip)

        cmd = get_rsync_FT_cmd(ip)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        processes.append(p)

        cmd = get_rsync_PC_cmd(ip)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        processes.append(p)

        cmd = get_rsync_GS_cmd(ip)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        processes.append(p)

    for p in processes:
        p.wait()

if __name__ == '__main__':
    args = parse_args()
    if args.dry_run:
        exit()

    hosts = get_hosts()
    print(hosts)
    # sync_spotdl(hosts, args.init)
    # sync_example(hosts)

    sync_code(hosts, args)
