pragma solidity ^0.5.5;

// Define a new contract named `AccountTransfer`
contract AccountTransfer {

    address payable ethAcct;
    address payable mktAcct;
    address payable firmAcct;
    uint public ethBalance;
    uint public mktBalance;
    uint public transferAmount;
    uint public gasFee = 21000; //21000 GWEI
    uint public conversionFee = 11000000; //0.011 ETH = 11000000 GWEI
    uint public fees = gasFee + conversionFee;

    /*
    Define a `public` function named `setAccounts` that receives two `address payable` arguments named `account1` and `account2`.
    */
    function setAccounts(address payable account1, address payable account2) public{

        // Set the values of `mktAcct` and `firmAcct`
        mktAcct = account1;
        firmAcct = account2;
    }

    function ethToMkt(uint amount) public {

        // Verify Ethereum account balance capable of payment
        require(address(this).balance >= fees, "Insufficient funds to transfer from Ethereum account to market account!");
        
        // Verify amount to transfer is sufficient to cover fees
        require(amount > fees, "Amount to Transfer is Insufficient to cover the fees!");
        
        //Calculate transferAmount
        transferAmount = amount - fees;
        
        // Call the `transfer` function of the `mktAcct` and pass it the `amount` to transfer as an argument.
        mktAcct.transfer(transferAmount);
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);

        // Call the `mktBalance` variable and set it equal to the balance of the `mktAcct.balance`
        mktBalance = mktAcct.balance;
        
        // Call the `ethBalance` variable and set it equal to the balance of the contract by using `address(this).balance` to reflect the new balance of the contract.
        ethBalance = address(this).balance;
        
    }

    function mktToEth () private {
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);
        
    }
    
    function deposit(uint amount) public payable {
            
        // Verify market account balance capable of payment
        require(mktAcct.balance >= fees, "Insufficient funds to transfer from market account to Ethereum account!");
        
        // Verify amount to transfer is sufficient to cover fees
        require(amount > fees, "Amount to Transfer is Insufficient to cover the fees!");
        
        //Call mktToEth function
        mktToEth();
        
        //Calculate transferAmount
        transferAmount = amount - fees;
        
        // Call the `mktBalance` variable and set it equal to the balance of the `mktAcct.balance`
        mktBalance = mktAcct.balance;
        
        // Call the `ethBalance` variable and set it equal to the balance of the contract by using `address(this).balance` to reflect the new balance of the contract.
        ethBalance = address(this).balance;
    
    }
    
}
