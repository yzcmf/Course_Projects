package uiuc.cs463sp16.mp1;

/** This main class is meant to be use as a way to test your code during development. 
 * It will not be used as part of the evaluation your assignment. **/
public class MP1Test
{
    public static void main(String[] args)
    {
	MP1 instance = MP1.getInstance();
	
	String basePath = "./";
	
	String homesFilePath = basePath + "dataset1/homes.txt"; 
	String edgesFilePath = basePath + "dataset1/friends.txt";
	
	DatasetReader reader = instance.GetDatasetReader(homesFilePath, edgesFilePath);
	boolean ok = reader.read();
	
	if(!ok) 
	{
	    System.out.println("Failed to read dataset1, exiting.");
	    return; 
	}
	
	SocialNetwork network = reader.getSocialNetwork();
	GroundTruth gt = reader.getGroundTruth();
	
	if(network == null || gt == null) { return; }
	
	Evaluator evaluator = Evaluator.getInstance();
	Metric metric = new WithinXkmMetric(25.0);
	
	InferenceAlgorithm simpleAlgo = instance.GetSimpleInferenceAlgorithm(network);
	double simpleAvgAccuracy = 1.0 - evaluator.EvaluateInference(simpleAlgo, gt, metric);
	
	System.out.println("SimpleAlgo mean accuracy: " + simpleAvgAccuracy);
	
    }
}
