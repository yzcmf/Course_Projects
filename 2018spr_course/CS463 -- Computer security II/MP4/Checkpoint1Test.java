package main;

import java.util.List;
import java.util.ArrayList;
import info.blockchain.api.blockexplorer.*;

public class Checkpoint1 {

	private Block block;
	private BlockExplorer blockExplorer;

	public Checkpoint1(){
		this.blockExplorer = new BlockExplorer();
		try{
			this.block = this.blockExplorer.getBlock("000000000000000f5795bfe1de0381a44d4d5ea2ad81c21d77f275bffa03e8b3");
		} catch(Exception e){
			e.printStackTrace();
		}
	}

	/**
	 * Blocks-Q1: What is the size of this block?
	 *
	 * Hint: Use method getSize() in Block.java
	 *
	 * @return size of the block
	 */
	public long getBlockSize() {
		return this.block.getSize();
	}

	/**
	 * Blocks-Q2: What is the Hash of the previous block?
	 *
	 * Hint: Use method getPreviousBlockHash() in Block.java
	 *
	 * @return hash of the previous block
	 */
	public String getPrevHash() {
		return this.block.getPreviousBlockHash();
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
		return this.block.getTransactions().size();
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
		List<Transaction> txs = this.block.getTransactions();
		Transaction[] txList = txs.toArray(new Transaction[0]);
		int index = 0;
		for(int i = 1; i < txList.length; i++){
			if(txList[i].getOutputs().size() > txList[index].getOutputs().size()){
				index = i;
			}
		}
		Transaction t = txList[index];
		List<Output> outsList = t.getOutputs();
		Output[] outs = outsList.toArray(new Output[0]);
		ArrayList<String> ret = new ArrayList(outs.length);
		for (int i = 0; i < outs.length; i++){
			ret.add(outs[i].getAddress());
		}
		return (List)ret;
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
		List<Transaction> txs = this.block.getTransactions();
		Transaction[] txList = txs.toArray(new Transaction[0]);
		int index = 0;
		for(int i = 1; i < txList.length; i++){
			if(txList[i].getInputs().size() > txList[index].getInputs().size()){
				index = i;
			}
		}
		Transaction t = txList[index];
		List<Input> inptList = t.getInputs();
		Input[] inpt = inptList.toArray(new Input[0]);
		ArrayList<String> ret = new ArrayList(inpt.length);
		for (int i = 0; i < inpt.length; i++){
			ret.add(inpt[i].getPreviousOutput().getAddress());
		}
		return (List)ret;
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
		List<Transaction> txs = this.block.getTransactions();
		Transaction[] txList = txs.toArray(new Transaction[0]);
		String addr = "";
		long amount = 0;
		for (int i = 0; i < txList.length; i++){
			List<Output> outs = txList[i].getOutputs();
			Output[] outsList = outs.toArray(new Output[0]);
			for (int j = 0; j < outsList.length; j++){
				if(outsList[j].getValue() > amount){
					amount = outsList[j].getValue();
					addr = outsList[j].getAddress();
				}
			}
		}
		return addr;
	}

	/**
	 * Transactions-Q4: How many coinbase transactions are there in this block?
	 *
	 * Hint: In a coinbase transaction, getPreviousOutput() == null
	 *
	 * @return number of coin base transactions
	 */
	public int getCoinbaseCount() {
		List<Transaction> txs = this.block.getTransactions();
		Transaction[] txList = txs.toArray(new Transaction[0]);
		int count = 0;
		for (int i = 0; i < txList.length; i++){
			List<Input> inpt = txList[i].getInputs();
			Input[] inptList = inpt.toArray(new Input[0]);
			for (int j = 0; j < inptList.length; j++){
				if(inptList[j].getPreviousOutput() == null){
					count++;
				}
			}
		}
		return count;
	}

	/**
	 * Transactions-Q5: What is the number of Satoshi generated in this block?
	 *
	 * @return number of Satoshi generated
	 */
	public long getSatoshiGen() {
		List<Transaction> txs = this.block.getTransactions();
		Transaction[] txList = txs.toArray(new Transaction[0]);
		for (int i = 0; i < txList.length; i++){
			List<Input> inpt = txList[i].getInputs();
			Input[] inptList = inpt.toArray(new Input[0]);
			for (int j = 0; j < inptList.length; j++){
				if(inptList[j].getPreviousOutput() == null){
					List<Output> outs = txList[i].getOutputs();
					Output[] outsList = outs.toArray(new Output[0]);
					return outsList[0].getValue();
				}
			}
		}
		return 1;
	}

}
