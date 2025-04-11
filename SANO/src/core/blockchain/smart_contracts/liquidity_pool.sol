// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LiquidityPool is Ownable {
    IERC20 public tokenA;
    IERC20 public tokenB;

    uint256 public totalLiquidity;
    mapping(address => uint256) public liquidityOf;
    uint256 public feeRate; // Fee rate in basis points (1/100 of a percent)

    event LiquidityAdded(address indexed provider, uint256 amountA, uint256 amountB);
    event LiquidityRemoved(address indexed provider, uint256 amountA, uint256 amountB);
    event TokensSwapped(address indexed trader, address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut);

    constructor(address _tokenA, address _tokenB, uint256 _feeRate) {
        tokenA = IERC20(_tokenA);
        tokenB = IERC20(_tokenB);
        feeRate = _feeRate;
    }

    function addLiquidity(uint256 amountA, uint256 amountB) external returns (uint256 liquidity) {
        require(amountA > 0 && amountB > 0, "Invalid amounts");

        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        totalLiquidity += amountA + amountB;
        liquidity = amountA + amountB; // Simplified liquidity calculation
        liquidityOf[msg.sender] += liquidity;

        emit LiquidityAdded(msg.sender, amountA, amountB);
    }

    function removeLiquidity(uint256 liquidity) external returns (uint256 amountA, uint256 amountB) {
        require(liquidityOf[msg.sender] >= liquidity, "Insufficient liquidity");

        amountA = (liquidity * tokenA.balanceOf(address(this))) / totalLiquidity;
        amountB = (liquidity * tokenB.balanceOf(address(this))) / totalLiquidity;

        totalLiquidity -= liquidity;
        liquidityOf[msg.sender] -= liquidity;

        tokenA.transfer(msg.sender, amountA);
        tokenB.transfer(msg.sender, amountB);

        emit LiquidityRemoved(msg.sender, amountA, amountB);
    }

    function swap(address tokenIn, uint256 amountIn) external returns (uint256 amountOut) {
        require(amountIn > 0, "Invalid amount");
        require(tokenIn == address(tokenA) || tokenIn == address(tokenB), "Invalid token");

        IERC20 tokenOut = tokenIn == address(tokenA) ? tokenB : tokenA;
        uint256 reserveIn = tokenIn == address(tokenA) ? tokenA.balanceOf(address(this)) : tokenB.balanceOf(address(this));
        uint256 reserveOut = tokenOut.balanceOf(address(this));

        // Calculate amount out using the constant product formula
        amountOut = (amountIn * reserveOut) / (reserveIn + amountIn) * (10000 - feeRate) / 10000;

        tokenIn.transferFrom(msg.sender, address(this), amountIn);
        tokenOut.transfer(msg.sender, amountOut);

        emit TokensSwapped(msg.sender, tokenIn, tokenOut, amountIn, amountOut);
    }

    function setFeeRate(uint256 _feeRate) external onlyOwner {
        require(_feeRate <= 1000, "Fee rate too high"); // Max 10%
        feeRate = _feeRate;
    }

    function getLiquidity(address provider) external view returns (uint256) {
        return liquidityOf[provider];
    }
}
