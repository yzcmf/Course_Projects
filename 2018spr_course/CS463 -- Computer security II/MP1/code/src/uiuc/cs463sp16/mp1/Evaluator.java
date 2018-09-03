package uiuc.cs463sp16.mp1;

import java.security.InvalidParameterException;
import java.util.HashSet;

public class Evaluator
{
    private static Evaluator instance = null;
    
    public static synchronized Evaluator getInstance()
    {
	if (instance == null) { instance = new Evaluator(); }
	return instance;
    }
    
    /** 
     * Evaluates the inference algorithm 'algo' according to 'metric' using the 'gt' as ground truth.
     * @return averaged normalized error of 'algo' according to 'metric'.
     **/
    public double EvaluateInference(InferenceAlgorithm algo, GroundTruth gt, Metric metric)
    {
	double out = 0.0;
	
	if(algo == null) { throw new InvalidParameterException("InferenceAlgorithm is null!"); }
	if(gt == null) { throw new InvalidParameterException("GroundTruth is null!"); }
	if(metric == null) { throw new InvalidParameterException("Metric is null!"); }
	
	SocialNetwork network = algo.getNetwork();
	if(network == null) { throw new InvalidParameterException("Network is null!"); }
	
	long visited = 0;
	for(User node : network.getNodes())
	{
	    long id = node.getId();
	    InferredGPSPoint inferred = algo.inferHomeLocation(id);
	    
	    GPSPoint actual = gt.getHomeLocation(id);
	    
	    double dist = metric.distance(inferred, actual);
	    out += dist;
	    		
	    visited++;
	}
	
	return out / visited; /* this is the normalized error, rather than accuracy */
    }
}
