package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class UserCluster {
	private Map<Long, List<String>> userMap; // Map a user id to a list of
												// bitcoin addresses
	private Map<String, Long> keyMap; // Map a bitcoin address to a user id

	public UserCluster() {
		userMap = new HashMap<Long, List<String>>();
		keyMap = new HashMap<String, Long>();
	}

	/**
	 * Read transactions from file
	 * 
	 * @param file
	 * @return true if read succeeds; false otherwise
	 */
	public boolean readTransactions(String file) {
		// TODO implement me
		return false;
	}

	/**
	 * Merge addresses based on joint control
	 */
	public void mergeAddresses() {
		// TODO implement me
	}

	/**
	 * Return number of users (i.e., clusters) in the transaction dataset
	 * 
	 * @return number of users (i.e., clusters)
	 */
	public int getUserNumber() {
		// TODO implement me
		return 0;
	}

	/**
	 * Return the largest cluster size
	 * 
	 * @return size of the largest cluster
	 */
	public int getLargestClusterSize() {
		// TODO implement me
		return 0;
	}

	public boolean writeUserMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (long user : userMap.keySet()) {
				List<String> keys = userMap.get(user);
				w.write(user + " ");
				for (String k : keys) {
					w.write(k + " ");
				}
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing user list!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeKeyMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (String key : keyMap.keySet()) {
				w.write(key + " " + keyMap.get(key) + "\n");
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing key map!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeUserGraph(String txFile, String userGraphFile) {
		try {
			BufferedReader r1 = new BufferedReader(new FileReader(txFile));
			Map<String, Long> txUserMap = new HashMap<String, Long>();
			String nextLine;
			while ((nextLine = r1.readLine()) != null) {
				String[] s = nextLine.split(" ");
				if (s.length < 5) {
					System.err.println("Invalid format: " + nextLine);
					r1.close();
					return false;
				}
				if (s[4].equals("in") && !txUserMap.containsKey(s[0])) { // new transaction 
					Long user;
					if ((user=keyMap.get(s[2])) == null) {
						System.err.println(s[2] + " is not in the key map!");
						r1.close();
						return false;
					}
					txUserMap.put(s[0], user);
				} 
			}
			r1.close();
			
			BufferedReader r2 = new BufferedReader(new FileReader(txFile));
			BufferedWriter w = new BufferedWriter(new FileWriter(userGraphFile));
			while ((nextLine = r2.readLine()) != null) {
				String[] s = nextLine.split(" ");
				if (s.length < 5) {
					System.err.println("Invalid format: " + nextLine);
					r2.close();
					w.flush();
					w.close();
					return false;
				}
				if (s[4].equals("out")) {
					if(txUserMap.get(s[0]) == null) {
						System.err.println("Did not find input transaction for Tx: " + s[0]);
						r2.close();
						w.flush();
						w.close();
						return false;
					}
					long inputUser = txUserMap.get(s[0]);
					Long outputUser;
					if ((outputUser=keyMap.get(s[2])) == null) {
						System.err.println(s[2] + " is not in the key map!");
						r2.close();
						w.flush();
						w.close();
						return false;
					}
					w.write(inputUser + "," + outputUser + "," + s[3] + "\n");
				} 
			}
			r2.close();
			w.flush();
			w.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return true;
	}

}
