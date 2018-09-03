package uiuc.cs463sp16.mp1;


/** Represents a user in the social network. 
 * Each user has a unique non-negative integer id, and a home location (i.e., GPSPoint).
 * Not all users have chosen to share their home locations, so it may or may not be known.
 * @see {@link #getId()}, {@link #getHomeLocation()}, {@link #isHomeLocationKnown()} **/
public class User
{   
    private long id; 
    private GPSPoint home; 
    private Set<User> friends; /* TODO: Implement me */

    public long getId() 
    { 
	/* TODO: Implement me */ 
	return 0; 
    }
    public GPSPoint getHomeLocation() 
    { 
	/* TODO: Implement me */ 
	return null;
    }
    
    public boolean isHomeLocationKnown() 
    { 
	/* TODO: Implement me */
	return false;
    }
    
    /** Returns the set of friends of friends of this user. **/
    public Set<User> getFriendsOfFriends()
    {
	Set<User> friendsOfFriends = new HashSet<User>();
	
	for(User friend : getFriends())
	{
	    friendsOfFriends.addAll(friend.getFriends());
	}
	return friendsOfFriends;
    }

    public Set<User> getFriends()
    {
    /* TODO: Implement me */
	return null;
    }

    public void addFriend(User friend)
    {
	/* TODO: Implement me */
    }
}
