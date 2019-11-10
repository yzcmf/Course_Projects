package test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Arrays;

import main.Checkpoint1;

public class Checkpoint1Test {
	public static void main(String[] args) {
		Checkpoint1 cp1 = new Checkpoint1();

		try {
			BufferedWriter w = new BufferedWriter(new FileWriter("cp1.txt"));
			w.write("3.1.2\n");
			w.write("1." + cp1.getBlockSize() + "\n");
			w.write("2." + cp1.getPrevHash() + "\n");
			w.write("3." + cp1.getTxCount() + "\n");
			w.newLine();
			w.write("3.1.3\n");
			w.write("1.\n");
			List<String> outAddr = cp1.getOutputAddresses();
			String[] outArray = new String[outAddr.size()];
			outAddr.toArray(outArray);
			Arrays.sort(outArray);
			for (String s : outArray) {
				w.write(s + "\n");
			}
			w.write("2.\n");
			List<String> inAddr = cp1.getInputAddresses();
			String[] inArray = new String[inAddr.size()];
			inAddr.toArray(inArray);
			Arrays.sort(inArray);
			for (String s : inArray) {
				w.write(s + "\n");
			}
			w.write("3." + cp1.getLargestRcv() + "\n");
			w.write("4." + cp1.getCoinbaseCount() + "\n");
			w.write("5." + cp1.getSatoshiGen() + "\n");
			w.flush();
			w.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
