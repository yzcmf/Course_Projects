package main;

public class DatasetGenerator {
	String file;

	public DatasetGenerator(String file) {
		this.file = file;
	}

	public boolean writeTransactions() {
		// TODO implement me
		return false;
	}

	/**
	 * Generate a record in the transaction dataset
	 * 
	 * @param txIndex
	 *            Transaction index
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Previous output address of the input
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the input
	 */
	private String generateInputRecord(long txIndex, String txHash,
			String address, long value) {
		return txIndex + " " + txHash + " " + address + " " + value + " in";
	}

	/**
	 * Generate a record in the transaction dataset
	 * 
	 * @param txIndex
	 *            Transaction index
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Output bitcoin address
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the output
	 */
	private String generateOutputRecord(long txIndex, String txHash,
			String address, long value) {
		return txIndex + " " + txHash + " " + address + " " + value + " out";
	}

}
