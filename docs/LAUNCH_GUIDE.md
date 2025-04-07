# Nexus Revoluter Mainnet Launch Guide

Welcome to the Nexus Revoluter project! This guide will help you set up and participate in the mainnet. Follow the instructions carefully to ensure a smooth launch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Launching the Node](#launching-the-node)
5. [Participating in the Network](#participating-in-the-network)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Community and Support](#community-and-support)

## Prerequisites

Before you begin, ensure you have the following:

- A server or machine with at least:
  - 4 CPU cores
  - 8 GB RAM
  - 100 GB SSD storage
  - A stable internet connection
- Operating System: Ubuntu 20.04 or later
- Docker and Docker Compose installed
- Git installed

## Installation

1. **Clone the Repository**

   Open your terminal and clone the Nexus Revoluter repository:

   ```bash
   git clone https://github.com/KOSASIH/nexus-revoluter.git
   cd nexus-revoluter
   ```

2. **Build the Docker Images**

   Use Docker Compose to build the necessary images:

   ```bash
   docker-compose build
   ```

3. **Pull Required Docker Images**

   Ensure you have the latest images:

   ```bash
   docker-compose pull
   ```

## Configuration

1. **Create a Configuration File**

   Copy the example configuration file and edit it:

   ```bash
   cp config/example-config.yaml config/config.yaml
   nano config/config.yaml
   ```

   Update the following fields in `config.yaml`:

   - `node_name`: Your unique node name
   - `rpc_port`: The port for RPC communication
   - `staking_address`: Your wallet address for staking rewards
   - `network_id`: Set to `mainnet`

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory:

   ```bash
   nano .env
   ```

   Add the following variables:

   ```env
   NODE_NAME=your_node_name
   RPC_PORT=your_rpc_port
   STAKING_ADDRESS=your_staking_address
   NETWORK_ID=mainnet
   ```

## Launching the Node

1. **Start the Node**

   Use Docker Compose to start your node:

   ```bash
   docker-compose up -d
   ```

   This command will run your node in detached mode.

2. **Check Node Status**

   To check if your node is running correctly, use:

   ```bash
   docker-compose logs -f
   ```

   Look for messages indicating that the node has successfully connected to the network.

## Participating in the Network

1. **Staking Tokens**

   To stake tokens, use the following command:

   ```bash
   docker-compose exec app stake --amount <amount> --address <your_address>
   ```

   Replace `<amount>` with the number of tokens you wish to stake and `<your_address>` with your wallet address.

2. **Voting on Proposals**

   To vote on governance proposals, use:

   ```bash
   docker-compose exec app vote --proposal_id <proposal_id> --support <true|false>
   ```

   Replace `<proposal_id>` with the ID of the proposal you wish to vote on.

## Monitoring and Maintenance

- **Monitor Node Performance**

  Use the following command to monitor your node's performance:

  ```bash
  docker stats
  ```

- **Update the Node**

  To update your node to the latest version, pull the latest changes and rebuild:

  ```bash
  git pull origin main
  docker-compose build
  ```

## Troubleshooting

- **Node Not Syncing**

  If your node is not syncing, check your internet connection and ensure that the configuration file is correct.

- **Error Messages**

  Review the logs for any error messages:

  ```bash
  docker-compose logs
  ```

## Community and Support

For further assistance, join our community:

- **Discord**: [Join our Discord](https://discord.gg/yourdiscordlink)
- **Telegram**: [Join our Telegram](https://t.me/yourtelegramlink)
- **GitHub Issues**: [Report an issue](https://github.com/KOSASIH/nexus-revoluter/issues)

Thank you for participating in the Nexus Revoluter mainnet! Together, we can build a powerful and decentralized network.
