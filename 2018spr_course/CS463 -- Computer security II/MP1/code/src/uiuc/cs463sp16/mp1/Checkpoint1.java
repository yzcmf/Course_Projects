package uiuc.cs463sp16.mp1;

public class Checkpoint1 {
    private Checkpoint1() {}
    private static Checkpoint1 instance = null;
    
    public static synchronized Checkpoint1 getInstance()
    {
	if (instance == null) { instance = new Checkpoint1(); }
	return instance;
    }
    
    public DatasetReader GetDatasetReader(String homesFilePath, String edgesFilePath)
    {
	return new DatasetReader(edgesFilePath, homesFilePath);
    }
    
    public DatasetAnalyzer GetDatasetAnalyzer(SocialNetwork network)
    {
	return new DatasetAnalyzer(network);
    }
}
