package uiuc.cs463sp16.mp1;

import java.security.InvalidParameterException;

public class WithinXkmMetric extends Metric
{
    private double threshold;
    
    public WithinXkmMetric(double threshold) { this.threshold = threshold; }
    
    /** Returns 0.0 if the prediction is within 'threshold' km of the actual location, 1.0 otherwise. **/
    public double distance(InferredGPSPoint inferred, GPSPoint actual)
    {
	if(actual == null) { throw new InvalidParameterException("actual location is null!"); }
	if(inferred == null) { throw new InvalidParameterException("inferred location is null!"); }
	
	double dist = actual.distanceTo(inferred);

	return (dist <= threshold) ? 0.0 : 1.0;
    }
}
