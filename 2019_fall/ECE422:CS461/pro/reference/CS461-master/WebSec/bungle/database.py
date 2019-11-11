import MySQLdb as mdb
from bottle import FormsDict
from hashlib import md5


# connection to database project2
def connect():
    """makes a connection to MySQL database.
    @return a mysqldb connection
    """

    #TODO: fill out function parameters. Use the user/password combo for the user you created in 2.1.2.1
    username = 'xy21'
    filename = './../dbrw.secret'
    dbname = 'project2'
    with open(filename, 'rt') as f:
        ps = f.read()
    ps = ps.strip()

    return mdb.connect(host="localhost",
                       user=username,
                       passwd=ps,
                       db=dbname);


def createUser(username, password):
    """ creates a row in table named users
    @param username: username of user
    @param password: password of user
    """


    #TODO: Implement a prepared statement using cur.execute() so that this query creates a row in table user
    m = md5()
    m.update(password)
    passwordhash = m.digest()

    insert_stat = ("INSERT INTO users (username, password, passwordhash) VALUES (%s, %s, %s)")
    db_rw = connect()
    cur = db_rw.cursor()
    # print "*************this is insert hash: " + passwordhash
    data = [username, password, passwordhash]
    cur.execute(insert_stat, data)

    db_rw.commit()

def validateUser(username, password):
    """ validates if username,password pair provided by user is correct or not
    @param username: username of user
    @param password: password of user
    @return True if validation was successful, False otherwise.
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects a row from table user
    m = md5()
    m.update(password)
    input_passwordhash = m.digest()

    select_stat = ("SELECT passwordhash FROM users WHERE username = %s")
    cur.execute(select_stat, [username])

    if cur.rowcount < 1:
        return False

    rst = cur.fetchall();
    stored_passwordhash = rst[0][0]
    print stored_passwordhash
    # print '\n this is hash fetched from server **************'
    input_passwordhash = str(input_passwordhash)
    if stored_passwordhash != input_passwordhash:
        return False
    return True

def fetchUser(username):
    """ checks if there exists given username in table users or not
    if user exists return (id, username) pair
    if user does not exist return None
    @param username: the username of a user
    @return The row which has username is equal to provided input
    """

    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    print username
    #TODO: Implement a prepared statement so that this query selects a id and username of the row which has column username = username
    select_stat = ("SELECT id, username FROM users WHERE username = %s")
    data = username;
    cur.execute(select_stat, [data])

    if cur.rowcount < 1:
        return None
    return FormsDict(cur.fetchone())

def addHistory(user_id, query):
    """ adds a query from user with id=user_id into table named history
    @param user_id: integer id of user
    @param query: the query user has given as input
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statment using cur.execute() so that this query inserts a row in table history

    insert_stat = ("INSERT INTO history (user_id, query) VALUES (%s, %s)")
    data = [user_id, query]
    cur.execute(insert_stat, data)

    db_rw.commit()

#grabs last 15 queries made by user with id=user_id from table named history
def getHistory(user_id):
    """ grabs last 15 distinct queries made by user with id=user_id from
    table named history
    @param user_id: integer id of user
    @return a first column of a row which MUST be query
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects 15 distinct queries from table history

    # query contains 15 most newest insert
    # select_stat = ("SELECT * FROM (SELECT query FROM history ORDER BY id DESC) LIMIT 15")
    select_stat = ("SELECT query FROM (SELECT query, id from history WHERE user_id = %s ORDER BY id DESC)AS T LIMIT 15 ")
    data = [user_id]
    cur.execute(select_stat, data)

    rows = cur.fetchall();
    return [row[0] for row in rows]
