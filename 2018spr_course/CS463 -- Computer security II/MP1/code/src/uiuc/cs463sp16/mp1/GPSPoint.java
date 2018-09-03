package uiuc.cs463sp16.mp1;

public class GPSPoint
{
    public double latitude;
    public double longitude;
    
    private static final double EARTH_MEAN_RADIUS_METERS = 6371009.0;
    private static final double RADS_IN_DEGREE = Math.PI / 180.0;
    
    private static final double EPSILON = 1.0E-9;
    
    public GPSPoint(GPSPoint homeLocation)
    {
	if(homeLocation == null) { throw new NullPointerException("Can't copy a null GPSPoint"); }
	latitude = homeLocation.latitude;
	longitude = homeLocation.longitude;
    }

    public GPSPoint(double latitude, double longitude)
    {
	this.latitude = latitude;
	this.longitude = longitude;
    }

    /** @return the <i>approximate</i> distance (using the spherical law of cosines)
     *  of 'this' GPSPoint to 'other' in kilometers. **/
    public double distanceTo(GPSPoint other)
    {
	double firstLatRads = this.latitude * RADS_IN_DEGREE;
	double firstLongRads = this.longitude * RADS_IN_DEGREE;
	
	double secondLatRads = other.latitude * RADS_IN_DEGREE;
	double secondLongRads = other.longitude * RADS_IN_DEGREE;
	
	double cosVal = Math.cos(firstLatRads) * Math.cos(secondLatRads) * Math.cos(firstLongRads - secondLongRads);
	double sinVal = Math.sin(firstLatRads) * Math.sin(secondLatRads);
	
	if(Math.abs((cosVal + sinVal) - 1.0) <= EPSILON) { return 0.0; } // prevents NaN on acos(1+).
	
	double acosVal = Math.acos(cosVal + sinVal); 
	assert(Double.isNaN(acosVal) == false);
	
	return (acosVal * EARTH_MEAN_RADIUS_METERS) / 1000.0;
    }
}
