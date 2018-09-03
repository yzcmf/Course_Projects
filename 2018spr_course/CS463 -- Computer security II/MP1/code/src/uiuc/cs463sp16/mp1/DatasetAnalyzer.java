package uiuc.cs463sp16.mp1;

import java.util.Set;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.NumberFormat;

public class DatasetAnalyzer {
	private SocialNetwork network;

	public DatasetAnalyzer(SocialNetwork network) {
		/* TODO: Implement me */
	}

	/** Prints the answers for checkpoint 1 Q1--Q6. You DO NOT need to modify this method. **/
	public boolean printResult(String file) {
		BufferedWriter w;
		NumberFormat formatter = new DecimalFormat("#0.00");
		try {
			w = new BufferedWriter(new FileWriter(file));
			w.write("1. " + getSize());
			w.newLine();
			w.write("2. " + getUnknownCount());
			w.newLine();
			w.write("3. " + getUnknownIsolatedCount());
			w.newLine();
			w.write("4. " + formatter.format(getBaseAccuracy()));
			w.newLine();
			w.write("5. " + formatter.format(getMaxAccuracy1()));
			w.newLine();
			w.write("6. " + formatter.format(getMaxAccuracy2()));
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("DatasetAnalyzer printResult(" + file
					+ ") IO error: " + e.getLocalizedMessage());
			return false;
		}
		System.out.println("Output file: " + file);
		return true;
	}

	/** Q1. How many users are there in dataset 1? **/
	private long getSize() {
		/* TODO: Implement me */
		return 0;
	}

	/** Q2. How many users in dataset 1 have unknown locations? **/
	private long getUnknownCount() {
		/* TODO: Implement me */
		return 0;
	}

	/** Q3. How many users in dataset 1 have unknown locations and no friends? **/
	private long getUnknownIsolatedCount() {
		/* TODO: Implement me */
		return 0;
	}

	/** Q4. What is the baseline inference accuracy for dataset 1? **/
	private double getBaseAccuracy() {
		/* TODO: Implement me */
		return  0;
	}

	/** Q5. What is the upper bound on inference accuracy for dataset 1 if we assume that we can 
		correctly infer all unknown home locations EXCEPT for users with NO friends?**/
	private double getMaxAccuracy1() {
		/* TODO: Implement me */
		return  0;
	}

	/** Q6. What is the upper bound on inference accuracy for dataset 1 if we assume that we can
		correctly infer all unknown home locations EXCEPT for users with NO friends who have shared
		their locations? **/
	private double getMaxAccuracy2() {
		/* TODO: Implement me */
		return 0;
	}
}
