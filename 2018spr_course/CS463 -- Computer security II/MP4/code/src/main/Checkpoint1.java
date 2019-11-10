package main;

import java.util.List;

public class Checkpoint1 {

	/**
	 * Blocks-Q1: What is the size of this block?
	 * 
	 * Hint: Use method getSize() in Block.java
	 * 
	 * @return size of the block
	 */
	public long getBlockSize() {
		// TODO implement me
		return 0L;
	}

	/**
	 * Blocks-Q2: What is the Hash of the previous block?
	 * 
	 * Hint: Use method getPreviousBlockHash() in Block.java
	 * 
	 * @return hash of the previous block
	 */
	public String getPrevHash() {
		// TODO implement me
		return null;
	}

	/**
	 * Blocks-Q3: How many transactions are included in this block?
	 * 
	 * Hint: To get a list of transactions in a block, use method
	 * getTransactions() in Block.java
	 * 
	 * @return number of transactions in current block
	 */
	public int getTxCount() {
		// TODO implement me
		return 0;
	}

	/**
	 * Transactions-Q1: Find the transaction with the most outputs, and list the
	 * Bitcoin addresses of all the outputs.
	 * 
	 * Hint: To get the bitcoin address of an Output object, use method
	 * getAddress() in Output.java
	 * 
	 * @return list of output addresses
	 */
	public List<String> getOutputAddresses() {
		// TODO implement me
		return null;
	}

	/**
	 * Transactions-Q2: Find the transaction with the most inputs, and list the
	 * Bitcoin addresses of the previous outputs linked with these inputs.
	 * 
	 * Hint: To get the previous output of an Input object, use method
	 * getPreviousOutput() in Input.java
	 * 
	 * @return list of input addresses
	 */
	public List<String> getInputAddresses() {
		// TODO implement me
		return null;
	}

	/**
	 * Transactions-Q3: What is the bitcoin address that has received the
	 * largest amount of Satoshi in a single transaction?
	 * 
	 * Hint: To get the number of Satoshi received by an Output object, use
	 * method getValue() in Output.java
	 * 
	 * @return the bitcoin address that has received the largest amount of Satoshi
	 */
	public String getLargestRcv() {
		// TODO implement me
		return null;
	}

	/**
	 * Transactions-Q4: How many coinbase transactions are there in this block?
	 * 
	 * Hint: In a coinbase transaction, getPreviousOutput() == null
	 * 
	 * @return number of coin base transactions
	 */
	public int getCoinbaseCount() {
		// TODO implement me
		return 0;
	}

	/**
	 * Transactions-Q5: What is the number of Satoshi generated in this block?
	 * 
	 * @return number of Satoshi generated
	 */
	public long getSatoshiGen() {
		// TODO implement me
		return 0L;
	}

}
