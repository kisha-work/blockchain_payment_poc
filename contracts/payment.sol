// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Payment {
    address public owner;
    uint256 public contractBalance;

    event Deposit(address indexed sender, uint256 amount);
    event Withdrawal(address indexed receiver, uint256 amount);
    event PaymentSent(address indexed from, address indexed to, uint256 amount);

    mapping(address => uint256) public balances;
    address[] public transactionHistory;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
        contractBalance += msg.value;
        transactionHistory.push(msg.sender);
        emit Deposit(msg.sender, msg.value);
    }

    function deposit() external payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
        contractBalance += msg.value;
        transactionHistory.push(msg.sender);
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        contractBalance -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
        transactionHistory.push(msg.sender);
        emit Withdrawal(msg.sender, amount);
    }

    function pay(address payable receiver, uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(receiver != address(0), "Invalid receiver");
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        transactionHistory.push(msg.sender);
        emit PaymentSent(msg.sender, receiver, amount);
    }

    function getBalance(address account) external view returns (uint256) {
        return balances[account];
    }

    function getContractBalance() external view returns (uint256) {
        return contractBalance;
    }

    function getTransactionCount() external view returns (uint256) {
        return transactionHistory.length;
    }

    function getTransaction(uint256 index) external view returns (address) {
        require(index < transactionHistory.length, "Index out of bounds");
        return transactionHistory[index];
    }
}
