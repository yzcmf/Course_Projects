package uiuc.cs463sp16.mp1;


public class DatasetReader {
	private String edgesFilePath = null;
	private String homesFilePath = null;

	private GroundTruth gt = null;
	private SocialNetwork sn = null;

	public DatasetReader(String edgesFilePath, String homesFilePath) {
		/* TODO: implement me */
	}

	/**
	 * Reads, parses the specified dataset, and constructs the SocialNetwork and
	 * GroundTruth objects. The operation should correctly separate the ground
	 * truth data from the social network data, and create 'gt', and 'sn'.
	 * 
	 * @return true, if the operation is successful, false otherwise.
	 **/
	public boolean read() {
		/* TODO: implement me */
		return false;
	}

	public SocialNetwork getSocialNetwork() {
		return sn;
	}

	public GroundTruth getGroundTruth() {
		return gt;
	}
}
