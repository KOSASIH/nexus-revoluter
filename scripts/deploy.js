const { ethers, upgrades } = require('hardhat');

async function main() {
  const Nexus = await ethers.getContractFactory('Nexus');
  console.log('Deploying Nexus...');
  const nexus = await upgrades.deployProxy(Nexus, ['Nexus Revoluter', 'NEXUS', ethers.parseEther('0.0001')], {
    initializer: 'initialize',
    kind: 'uups',
  });
  await nexus.waitForDeployment();
  console.log(`Nexus deployed to: ${await nexus.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
