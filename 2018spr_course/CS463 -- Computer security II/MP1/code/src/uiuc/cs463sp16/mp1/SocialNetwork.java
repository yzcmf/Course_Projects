package uiuc.cs463sp16.mp1;

import java.util.Map;

/** Represents the social network, i.e., a set of {@link User}s connected by a friendship graph. **/
public class SocialNetwork
{

    private Map<Long, User> nodes; /* TODO: Implement me */

    /** @return the number of users in the social network **/
    public long getSize()
    {
	/* TODO: Implement me */
	return 0;
    }

    /** @return the {@link User} object of user 'userId' **/
    public User getNodeById(long id)
    {
	/* TODO: Implement me */
	return null;
    }

    /** @return an iterable collection of the {@link User}s of the social network **/
    public Iterable<User> getNodes()
    {
	/* TODO: Implement me */
	return null;
    }

    /** Add user 'user' to the social network. **/
    public void addUser(User user)
    {
	/* TODO: Implement me */
    }

    /** Sets the friendship of two (existing) social network users (i.e., 'userId' and 'friendId')
     * @return true, if the friendship was set, false otherwise. **/
    public boolean setFriends(long userId, long friendId)
    {
	if(userId == friendId) { return false; }

	User user = (User)getNodeById(userId);
	User friend = (User)getNodeById(friendId);

	if(user == null || friend == null) { return false; }

	user.addFriend(friend);
	friend.addFriend(user);

	return true;
    }
}
