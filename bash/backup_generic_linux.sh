#!/bin/sh 
echo "-----BEGIN"
date
echo "-----"

OLD_DIR=$(pwd)
TIMESTAMP=$(date +"%Y%m%d_%H.%M.%S")
BACKUP_DIR=/tmp/example.com_backup
BACKUP_TARGET=/tmp/example.com_backup_${TIMESTAMP}.tar.gz
PASSWORD_FILE=/home/example/.example_backup.passwd
DROPBOX_DIR=/home/example/Dropbox/backups/example.com
BACKUP_NAME_PREFIX="example.com_backup"
DAYLIMIT=14 # delete backups older than limit

rm -rf ${BACKUP_DIR}
mkdir -p ${BACKUP_DIR}
cd ${BACKUP_DIR}

mkdir etc
sudo cp /etc/fstab etc/
sudo cp /etc/hosts etc/
sudo cp -r /etc/openvpn etc/
sudo cp -r /etc/iptables etc/
sudo cp -r /etc/nginx etc/

mkdir -p home/example
cp -r $HOME/bin/*.sh home/example/
cp -r $HOME/.ssh home/example/
cp $HOME/.gitconfig* home/example/
cp $HOME/.profile home/example/
cp $HOME/.bashrc home/example/
cp $HOME/.vimrc home/example/
cp $HOME/.tmux.conf home/example/

mkdir -p var/spool/cron
sudo cp -r /var/spool/cron/crontabs var/spool/cron/

cd /tmp
sudo chown -R example:example ${BACKUP_DIR}
rm -f ${BACKUP_TARGET}*
tar zcf ${BACKUP_TARGET} ${BACKUP_DIR}
cat ${PASSWORD_FILE} | ccrypt -e -k - ${BACKUP_TARGET}

cd ${OLD_DIR}
rm -rf ${BACKUP_DIR}
mv ${BACKUP_TARGET}.cpt ${DROPBOX_DIR}/

ls -tlh ${DROPBOX_DIR}/${BACKUP_NAME_PREFIX}*.tar.gz.cpt

echo "deleting backups older than ${DAYLIMIT} days"
find ${DROPBOX_DIR}/ -type f -name "${BACKUP_NAME_PREFIX}*.tar.gz.cpt" -ctime +${DAYLIMIT} -delete

ls -tlh ${DROPBOX_DIR}/${BACKUP_NAME_PREFIX}*.tar.gz.cpt

echo "-----"
date
echo "-----END"
