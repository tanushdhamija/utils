#!/bin/bash

CONFIG_FILE="/etc/systemd/logind.conf"
BACKUP_FILE="/etc/systemd/logind.conf.backup"

# make sure we're running with sudo
if [[ $EUID -ne 0 ]]; then
   echo "Please run this script with sudo:"
   echo "  sudo $0"
   exit 1
fi

echo "Choose lid behaviour:"
echo "1. Default - Suspend on lid close (always)"
echo "2. Dock-aware - Suspend only when undocked (Recommended)"
echo "3. Never suspend - Ignore lid close (always on)"
read -p "Enter option [1/2/3]: " choice

# create a backup file
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "Backup created at $BACKUP_FILE"

# clean previous settings
sed -i '/HandleLidSwitch/d' "$CONFIG_FILE"
sed -i '/HandleLidSwitchDocked/d' "$CONFIG_FILE"

# apply selected config
case $choice in
  1)
    echo "Applying default suspend behaviour..."
    echo "HandleLidSwitch=suspend" >> "$CONFIG_FILE"
    ;;
  2)
    echo "Applying dock-aware suspend behaviour..."
    echo "HandleLidSwitch=suspend" >> "$CONFIG_FILE"
    echo "HandleLidSwitchDocked=ignore" >> "$CONFIG_FILE"
    ;;
  3)
    echo "Disabling suspend on lid close completely..."
    echo "HandleLidSwitch=ignore" >> "$CONFIG_FILE"
    echo "HandleLidSwitchDocked=ignore" >> "$CONFIG_FILE"
    ;;
  *)
    echo "Invalid option. No changes made."
    exit 1
    ;;
esac

# restart systemd-logind
systemctl restart systemd-logind
echo "✅ Lid behaviour updated. Change takes effect immediately."
