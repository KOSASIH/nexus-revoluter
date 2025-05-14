require('@nomicfoundation/hardhat-toolbox');
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  // Solidity version from your project
  solidity: {
    version: '0.8.24',
    settings: {
      optimizer: {
        enabled: true,
        runs: 200, // Optimize for deployment cost vs. execution cost
      },
    },
  },
  // Network configurations for Pi Network Testnet and Mainnet
  networks: {
    hardhat: {
      // Local Hardhat network for testing
      chainId: 1337,
      accounts: {
        mnemonic: process.env.MNEMONIC || 'test test test test test test test test test test test junk',
        count: 10,
      },
    },
    pi_testnet: {
      url: process.env.PI_TESTNET_RPC_URL || 'https://api.testnet.minepi.com', // Replace with actual RPC URL
      chainId: parseInt(process.env.PI_TESTNET_CHAIN_ID || '314159'), // Placeholder; get from Pi Developer Portal
      accounts: process.env.PRIVATE_KEY ? [`0x${process.env.PRIVATE_KEY}`] : [],
      gas: 'auto',
      gasPrice: 'auto',
    },
    pi_mainnet: {
      url: process.env.PI_MAINNET_RPC_URL || 'https://api.mainnet.minepi.com', // Replace with actual RPC URL
      chainId: parseInt(process.env.PI_MAINNET_CHAIN_ID || '314159'), // Placeholder; get from Pi Developer Portal
      accounts: process.env.PRIVATE_KEY ? [`0x${process.env.PRIVATE_KEY}`] : [],
      gas: 'auto',
      gasPrice: 'auto',
    },
  },
  // Etherscan-like verification (if Pi Network supports a block explorer)
  etherscan: {
    // Placeholder for Pi Network's block explorer API (if available)
    apiKey: process.env.PI_EXPLORER_API_KEY || 'YOUR_API_KEY',
    customChains: [
      {
        network: 'pi_testnet',
        chainId: parseInt(process.env.PI_TESTNET_CHAIN_ID || '314159'),
        urls: {
          apiURL: 'https://api.testnet.minepi.com/api', // Replace with actual explorer API
          browserURL: 'https://explorer.testnet.minepi.com', // Replace with actual explorer URL
        },
      },
      {
        network: 'pi_mainnet',
        chainId: parseInt(process.env.PI_MAINNET_CHAIN_ID || '314159'),
        urls: {
          apiURL: 'https://api.mainnet.minepi.com/api', // Replace with actual explorer API
          browserURL: 'https://explorer.mainnet.minepi.com', // Replace with actual explorer URL
        },
      },
    ],
  },
  // Gas reporting for optimization
  gasReporter: {
    enabled: process.env.REPORT_GAS === 'true',
    currency: 'USD',
    coinmarketcap: process.env.COINMARKETCAP_API_KEY || '',
    token: 'PI', // Placeholder for Pi Network token
    gasPriceApi: 'https://api.testnet.minepi.com/gas', // Replace with actual gas price API if available
  },
  // Mocha settings for testing
  mocha: {
    timeout: 40000, // Increase timeout for blockchain tests
  },
};
