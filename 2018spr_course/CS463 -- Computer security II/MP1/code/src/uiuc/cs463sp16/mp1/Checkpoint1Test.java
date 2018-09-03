package uiuc.cs463sp16.mp1;

public class Checkpoint1Test {
	public static void main(String[] args) {
		Checkpoint1 instance = Checkpoint1.getInstance();

		String basePath = "./";

		String homesFilePath = basePath + "dataset1/homes.txt";
		String edgesFilePath = basePath + "dataset1/friends.txt";
		String outFilePath = basePath + "checkpoint1_results.txt";

		DatasetReader reader = instance.GetDatasetReader(homesFilePath,
				edgesFilePath);
		boolean ok = reader.read();

		if (!ok) {
			System.out.println("Failed to read dataset1, exiting.");
			return;
		}

		SocialNetwork network = reader.getSocialNetwork();
		GroundTruth gt = reader.getGroundTruth();

		if (network == null || gt == null) {
			return;
		}
		
		DatasetAnalyzer analyzer = instance.GetDatasetAnalyzer(network);
		analyzer.printResult(outFilePath);

	}
}
