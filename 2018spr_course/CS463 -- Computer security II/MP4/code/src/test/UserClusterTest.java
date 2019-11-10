package test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import main.UserCluster;

public class UserClusterTest {
	public static void main(String[] args) {
		UserCluster uc = new UserCluster();
		uc.readTransactions("transactions.txt");
		uc.mergeAddresses();
		if (!uc.writeKeyMap("keyMap.txt")) {
			System.err.println("Cannot write to keyMap.txt!");
		}
		if (!uc.writeUserMap("userMap.txt")) {
			System.err.println("Cannot write to userMap.txt!");
		}
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(
					"cp2.txt"));
			w.write("1. " + uc.getUserNumber() + "\n");
			w.write("2. " + uc.getLargestClusterSize() + "\n");
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Cannot write to cp2.txt!");
			System.err.println(e.getStackTrace());
		}
		
		if (!uc.writeUserGraph("transactions.txt", "userGraph.txt")){
			System.err.println("Cannot write user graph!");
		}

	}
}
