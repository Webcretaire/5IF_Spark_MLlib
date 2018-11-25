#!/usr/bin/env bash
# spark install

sudo apt-get update
sudo apt-get install default-jdk -y
sudo apt-get install scala -y
tar -zxvf spark-2.3.2-bin-hadoop2.7.tgz
echo -e '\nSPARK_HOME=/root/spark-2.3.2-bin-hadoop2.7\n\nexport PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
source .bashrc
sudo apt-get install python3 -y
sudo apt-get install python-pip  -y
sudo apt-get install htop  -y
sudo pip install numpy scipy