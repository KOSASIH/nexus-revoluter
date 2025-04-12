#!/bin/bash

# Set the script to exit immediately if any command fails
set -e

# Constants
LOG_FILE="logs/deploy_mainnet.log"
CONFIG_FILE="config/mainnet_config.json"
DEPLOY_DIR="/opt/my_blockchain"
NODE_BINARY="my_blockchain_node"
EMAIL_NOTIFICATIONS=true
ADMIN_EMAIL="admin@example.com"

# Function to log messages
log() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a "$LOG_FILE"
}

# Function to send email notifications
send_email() {
    local subject="$1"
    local body="$2"
    echo -e "$body" | mail -s "$subject" "$ADMIN_EMAIL"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to deploy the mainnet
deploy_mainnet() {
    log "Starting mainnet deployment..."

    # Check if required commands are available
    for cmd in jq curl; do
        if ! command_exists "$cmd"; then
            log "Error: $cmd is not installed. Please install it before running the script."
            exit 1
        fi
    done

    # Create deployment directory if it doesn't exist
    if [ ! -d "$DEPLOY_DIR" ]; then
        log "Creating deployment directory at $DEPLOY_DIR"
        mkdir -p "$DEPLOY_DIR"
    fi

    # Copy configuration file
    log "Copying configuration file to $DEPLOY_DIR"
    cp "$CONFIG_FILE" "$DEPLOY_DIR/config.json"

    # Start the blockchain node
    log "Starting the blockchain node..."
    nohup "$DEPLOY_DIR/$NODE_BINARY" --config "$DEPLOY_DIR/config.json" > "$DEPLOY_DIR/node.log" 2>&1 &

    # Wait for the node to start
    sleep 10

    # Check if the node is running
    if pgrep -f "$NODE_BINARY" > /dev/null; then
        log "Mainnet deployed successfully."
        if [ "$EMAIL_NOTIFICATIONS" = true ]; then
            send_email "Mainnet Deployment Successful" "The mainnet has been deployed successfully."
        fi
    else
        log "Error: Mainnet deployment failed. The node is not running."
        if [ "$EMAIL_NOTIFICATIONS" = true ]; then
            send_email "Mainnet Deployment Failed" "The mainnet deployment failed. Please check the logs."
        fi
        exit 1
    fi
}

# Main script execution
log "Deployment script started."
deploy_mainnet
log "Deployment script completed."
