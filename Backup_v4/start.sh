#!/bin/bash


mv /NAS/Maintain_False.txt /NAS/Maintain_False_before.txt
mv /NAS/MSS_False.txt /NAS/MSS_False_before.txt

year=`date +%Y`
month=`date +%m`

mkdir -p /backup_Config/Maintain/Backup_Axgate/
mkdir -p /backup_Config/Maintain/Backup_FG
mkdir -p /backup_Config/MSS/Backup_FG
mkdir -p /backup_Config/MSS/Backup_Axgate

python3 /usr/local/backup/Backup_v3/reader.py

mkdir -p /NAS/$year/$month
cp -r /backup_Config/* /NAS/$year/$month
rm -rf /backup_Config/*
