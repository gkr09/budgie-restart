#!/bin/bash
#Budgie Restart Applet
#Gopikrishnan.R
#This script basically just copies the files to approproate directories.

APPLETDIR=/lib/budgie-desktop/plugins

ICONDIR=/usr/share/icons/hicolor/scalable/apps

echo "Installing Budgie Restart Applet....."

mkdir $APPLETDIR/org.budgie-desktop.applet.budgierestart

for file in BudgieRestart/*;do

    install -m 0755 "$file" $APPLETDIR/org.budgie-desktop.applet.budgierestart/

done

for file in icons/*;do

    install -m 0755 "$file" $ICONDIR/

done

echo "Finished Installing Applet. Restart or Re-login to find the applet in Budgie."
