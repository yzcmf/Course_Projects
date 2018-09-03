package uiuc.cs463sp16.mp1;

public abstract class InferenceAlgorithm
{
    private SocialNetwork network = null;
    
    public InferenceAlgorithm(SocialNetwork network) { this.network = network; }

    public SocialNetwork getNetwork()
    {
	return network;
    }

    /** Infers the home location of user 'userId'.
     * @return a {@link InferredGPSPoint} represented the inferred home location. **/
    public abstract InferredGPSPoint inferHomeLocation(long userId);
}