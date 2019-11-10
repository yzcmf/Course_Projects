package test;

import main.DatasetGenerator;

public class DatasetGeneratorTest {
	public static void main(String[] args) {
		DatasetGenerator dw = new DatasetGenerator("transactions.txt");
		if (!dw.writeTransactions()) {
			System.err.println("Cannot generate transaction dataset!");
		}
	}
}
