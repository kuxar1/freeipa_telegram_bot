#!/bin/bash

yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel wget
yum -y install readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install -y python3 epel-release python-pip libffi-deve python36-virtualenv

cd /tmp/
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar xzf Python-3.7.9.tgz
cd Python-3.7.9
./configure --enable-optimizations
make altinstall

ln -sfn /usr/local/bin/python3.7 /usr/bin/python3.7
ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3.7

rm -rf /tmp/Python-3.7.9.tgz

# mkdir myapp && cd myapp
# python3 -m venv env
# source env/bin/activate