echo `hostname -I` `hostname -s` >> /etc/hosts
yum -y install ovirt-engine wget
wget -O /root/answers.txt https://raw.githubusercontent.com/karmab/kcli/master/samples/ovirt/answers.txt
sed -i "s/0000/`hostname -s`/" /root/answers.txt
engine-setup --config=/root/answers.txt
yum -y install vdsm