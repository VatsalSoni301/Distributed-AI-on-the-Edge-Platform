#!/bin/sh

#Properties File
PROPERTY_FILE=servers.properties

#Function to read from Properties File
getProperty() {
   PROP_KEY=$1
   PROP_VALUE=`cat $PROPERTY_FILE | grep "$PROP_KEY" | cut -d'=' -f2`
   echo $PROP_VALUE
}

run_commands() {
    USERNAME=$1
    HOSTNAME=$2
    PASSWORD=$3
    SCRIPT=$4
    sshpass -p $PASSWORD ssh -o StrictHostKeyChecking=no $USERNAME@$HOSTNAME
}

############## Deploying and Starting Deployment Service Manager ########

MACHINE_DETAIL=$(getProperty "DEPLOYMENT_SERVICE")
HOST="$(echo $MACHINE_DETAIL | cut -d' ' -f1)"
USER="$(echo $MACHINE_DETAIL | cut -d' ' -f2)"
PWD="$(echo $MACHINE_DETAIL | cut -d' ' -f3)"
DOWNLOAD_URL="$(echo $MACHINE_DETAIL | cut -d' ' -f4)"
echo "Host Name is : "$HOST
echo "User Name is : " $USER
echo "URL : "$DOWNLOAD_URL

#Setup Commands
COMMANDS="cd ~/;
rm -rf DEPLOYMENT_SERVICE.zip;
rm -rf DEPLOYMENT_SERVICE;
wget $DOWNLOAD_URL;
unzip DEPLOYMENT_SERVICE.zip;
cd DEPLOYMENT_SERVICE;
python start.py"
run_commands $USER $HOST $PWD $COMMANDS

#########################################################################

############## Deploying and Starting Logging Services ##################

MACHINE_DETAIL=$(getProperty "LOGGING_SERVICE")
HOST="$(echo $MACHINE_DETAIL | cut -d' ' -f1)"
USER="$(echo $MACHINE_DETAIL | cut -d' ' -f2)"
PWD="$(echo $MACHINE_DETAIL | cut -d' ' -f3)"
DOWNLOAD_URL="$(echo $MACHINE_DETAIL | cut -d' ' -f4)"
echo "Host Name is : "$HOST
echo "User Name is : " $USER
echo "URL : "$DOWNLOAD_URL

#Setup Commands
COMMANDS="cd ~/;
rm -rf LOGGING_SERVICE.zip;
rm -rf LOGGING_SERVICE;
wget $DOWNLOAD_URL;
unzip LOGGING_SERVICE.zip;
cd LOGGING_SERVICE;
python start.py"
run_commands $USER $HOST $PWD $COMMANDS

#########################################################################

############## Deploying and Starting Logging Services ##################

MACHINE_DETAIL=$(getProperty "SCHEDULING_SERVICE")
HOST="$(echo $MACHINE_DETAIL | cut -d' ' -f1)"
USER="$(echo $MACHINE_DETAIL | cut -d' ' -f2)"
PWD="$(echo $MACHINE_DETAIL | cut -d' ' -f3)"
DOWNLOAD_URL="$(echo $MACHINE_DETAIL | cut -d' ' -f4)"
echo "Host Name is : "$HOST
echo "User Name is : " $USER
echo "URL : "$DOWNLOAD_URL

#Setup Commands
COMMANDS="cd ~/;
rm -rf SCHEDULING_SERVICE.zip;
rm -rf SCHEDULING_SERVICE;
wget $DOWNLOAD_URL;
unzip SCHEDULING_SERVICE.zip;
cd SCHEDULING_SERVICE;
python start.py"
run_commands $USER $HOST $PWD $COMMANDS

#########################################################################