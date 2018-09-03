package uiuc.cs463sp16.mp1;

/** Exposes the public interface of the assignment. This uses the <i>Singleton</i> design pattern.
 * @see <a href="http://en.wikipedia.org/wiki/Singleton_pattern">Singleton</a> **/
public final class MP1
{
    private MP1() {}
    private static MP1 instance = null;
    
    public static synchronized MP1 getInstance()
    {
	if (instance == null) { instance = new MP1(); }
	return instance;
    }
    
    public DatasetReader GetDatasetReader(String homesFilePath, String edgesFilePath)
    {
	return new DatasetReader(edgesFilePath, homesFilePath);
    }
    
    public InferenceAlgorithm GetSimpleInferenceAlgorithm(SocialNetwork network)
    {
	return new SimpleInferenceAlgorithm(network);
    }
    
    public InferenceAlgorithm GetPart2InferenceAlgorithm(SocialNetwork network)
    {
	/* TODO: Implement me */
	return null;
    }
}
