const { ethers, upgrades } = require('hardhat');

async function main() {
  // Deploy Nexus
  const Nexus = await ethers.getContractFactory('Nexus');
  console.log('Deploying Nexus...');
  const nexus = await upgrades.deployProxy(Nexus, ['Nexus Revoluter', 'NEXUS', ethers.parseEther('0.0001')], {
    initializer: 'initialize',
    kind: 'uups',
  });
  await nexus.waitForDeployment();
  const nexusAddress = await nexus.getAddress();
  console.log(`Nexus deployed to: ${nexusAddress}`);

  // Deploy Lock
  const Lock = await ethers.getContractFactory('Lock');
  console.log('Deploying Lock...');
  const lock = await upgrades.deployProxy(Lock, [nexusAddress], {
    initializer: 'initialize',
    kind: 'uups',
  });
  await lock.waitForDeployment();
  console.log(`Lock deployed to: ${await lock.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
