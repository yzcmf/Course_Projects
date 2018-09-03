package uiuc.cs463sp16.mp1;

import java.io.BufferedWriter;

import java.io.FileWriter;
import java.io.IOException;

public class Visualizer
{
    private static Visualizer instance = null;
    
    private Visualizer() {}
    
    public static synchronized Visualizer getInstance()
    {
	if (instance == null) { instance = new Visualizer(); }
	return instance;
    }
    
    private String APIKey = "";
    
    public void setAPIKey(String key) { APIKey = key; }
    
    private String getHeader(String title, GPSPoint center)
    {
	String ret = "";
	
	ret += "<!DOCTYPE html>\n<html>\n<head>\n<meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=no\" />"
		+ "\n<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"/>\n"
		+ "<title>MP1 Visualizer: " + title + "</title>\n"
		+ "<link href=\"https://code.google.com/apis/maps/documentation/javascript/examples/default.css\" "
		+ "rel=\"stylesheet\" type=\"text/css\" />\n"
		+ "<script type=\"text/javascript\" src=\"https://maps.google.com/maps/api/js?key="
		+ APIKey + "&sensor=false\"></script>\n<script type=\"text/javascript\">\n\n";

	ret += "function initialize() {\n "
	+ "var centerlatLong = new google.maps.LatLng(" + center.latitude + ", " + center.longitude + "); \n"
	+ "var mapOptions = {\n    zoom: 5,\n    center: centerlatLong\n };";
	ret += "\n\n var map = new google.maps.Map(document.getElementById(\"map-canvas\"), mapOptions);\n";
	
	return ret;

    }
    
    private String getFooter()
    {
	String ret = "";
	
	ret += "}\n";
        ret += "google.maps.event.addDomListener(window, \'load\', initialize);\n"
        	+ "</script>\n</head>\n<body>\n<div id=\"map-canvas\"></div>\n</body>\n</html>\n";
        
        return ret;
    }
    
    private String getHomeString(long userId, GPSPoint home, String color, boolean shared, boolean inferred)
    {
	String ret = "";
	
	String infSuffix = "";
	if(inferred == true) { infSuffix = "inf"; }
	
	String sharedInfStr = "";
	if(inferred == true) { sharedInfStr = " (inferred home)"; }
	else if(shared == true) { sharedInfStr = " (home shared)"; }
	else { sharedInfStr = " (home not shared)"; }
	
	ret += "\nvar contentVal" + userId + infSuffix
		+ " = \'<div id=\"content\">\'+ \n\'<div id=\"siteNotice\">\'+ \n\'</div>\'+"
		+ " \n\'<div id=\"bodyContent\">\'+ \n\'<p><b>User" + userId + sharedInfStr
		+ "</b></p>\' + \n \'<p>Latitude : " + home.latitude
		+ "</p> \' + \'<p>Longitude : " + home.longitude
		+ "</p> \' + \n\'</div>\'+ \n\'</div>\';\n\n";

	ret += "\n var infoWnd" + userId + infSuffix
		+ " = new google.maps.InfoWindow({\n	content: contentVal" +  userId + infSuffix
		+ "\n    });\n";
	
	ret += "\n var latLongMarker" + userId + infSuffix
		+ " = new google.maps.LatLng(" + home.latitude + ", " + home.longitude 
		+ ");\n";
	
	String iconURL = "http://www.google.com/mapfiles/ms/micons/" + color;
	if(inferred == false) { iconURL += "-dot"; }
	iconURL += ".png";	
		
	
	ret += "\n var marker" + userId + infSuffix
		+ " = new google.maps.Marker({\n        position: latLongMarker" + userId + infSuffix
		+ ",\n        map: map,\n		icon: \'" + iconURL 
		+ "\',\n        title: \'" + (inferred == true ? "(Inferred) " : "")
		+ "Home of User" + userId
		+ "\'\n    });\n\n";
    
	ret += "\ngoogle.maps.event.addListener(marker" + userId + infSuffix
		+ ", \'click\', function() {\n      infoWnd" + userId + infSuffix
		+ ".open(map, marker" + userId + infSuffix
		+ ");\n    });\n\n";
	
	return ret;
    }
    
    /** Draws a map (HTML format, using Google Maps JS v3 API) of a user and his/her friends to the file specified by 'outputFilePath'. **/
    public boolean drawFriendsMap(String outputFilePath, User user, GroundTruth gt)
    {
	if(APIKey == null || user == null || gt == null) { return false; }
	
	try
	{
	    BufferedWriter bw = new BufferedWriter(new FileWriter(outputFilePath));
	    GPSPoint center = gt.getHomeLocation(user.getId());
	    bw.write(getHeader("drawFriendsMap()", center));
	    
	    GPSPoint home = null;
	    
	    if(user.isHomeLocationKnown()) { home = user.getHomeLocation(); }
	    else { home = gt.getHomeLocation(user.getId()); }
	    
	    bw.write(getHomeString(user.getId(), home, "red", user.isHomeLocationKnown(), false));
	    
	    for(User friend : user.getFriends())
	    {
		if(friend.isHomeLocationKnown()) { home = friend.getHomeLocation(); }
		else { home = gt.getHomeLocation(friend.getId()); }
		    
		bw.write(getHomeString(friend.getId(), home, "blue", friend.isHomeLocationKnown(), false));
	    }
	    
	    bw.write(getFooter());
	    bw.close();
	}
	catch(IOException e)
	{
	    System.err.println("Visualizer write() IO error: " + e.getLocalizedMessage());
	    return false; 
	}
	
	return true;
    }
    
    /** Draws a map (HTML format, using Google Maps JS v3 API) of the users and their inferred locations (according to 'algo') to the file specified by 'outputFilePath'. **/
    public boolean drawInferenceMap(String outputFilePath, Iterable<User> users, GroundTruth gt, InferenceAlgorithm algo)
    {
	if(APIKey == null || users == null || gt == null || algo == null) { return false; }
	
	try
	{
	    BufferedWriter bw = new BufferedWriter(new FileWriter(outputFilePath));
	    
	    boolean first = true;
	    for(User user : users)
	    {
		if(first) 
		{ 
		    GPSPoint center = gt.getHomeLocation(user.getId());
		    bw.write(getHeader("drawInference()", center));  first = false; 
		}
		
		GPSPoint home = gt.getHomeLocation(user.getId());
		bw.write(getHomeString(user.getId(), home, "red", user.isHomeLocationKnown(), false));
		
		InferredGPSPoint inferred = algo.inferHomeLocation(user.getId());
		bw.write(getHomeString(user.getId(), inferred, "red", user.isHomeLocationKnown(), true));
	    }
	    
	    bw.write(getFooter());
	    bw.close();
	}
	catch(IOException e)
	{
	    System.err.println("Visualizer write() IO error: " + e.getLocalizedMessage());
	    return false; 
	}
	
	return true;
    }
}
