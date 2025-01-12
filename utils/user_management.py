from utils.database_management import execute_query, hash_password

def register_user(first_name, last_name, email, country, password, password_hint, marketing):
    """
    Registers a new user in the database.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        country (str): The user's country of residence.
        password_hash (str): The hashed password for the user.
        password_hint (str): A password hint for the user.
        marketing (bool): Whether the user opts into marketing communications.

    Returns:
        dict: A success message if the user is registered successfully, or an error message if something goes wrong.
    """
    query = '''
        INSERT INTO users (
            first_name, 
            last_name, 
            email, 
            country, 
            password_hash, 
            password_hint, 
            marketing
        ) 
        VALUES (
            %s, %s, %s, %s, %s, %s, %s
        );
    '''
    params = (
        first_name,
        last_name,
        email,
        country,
        hash_password(password),
        password_hint,
        marketing
    )

    try:
        # Execute the query without fetching results
        execute_query(query, params, fetch_results=False)
        print(f"User {email} registered successfully.")
        return {"status": "success", "message": f"User {email} registered successfully."}
    except Exception as e:
        print(f"Error registering user {email}: {e}")
        return {"status": "error", "message": f"An error occurred while registering the user: {str(e)}"}

def check_user(email, password):
    # """
    # Validates user credentials by checking the email and password against the database.

    # Args:
    #     email (str): The email address of the user.
    #     password (str): The plaintext password provided by the user.

    # Returns:
    #     tuple: A tuple containing the user's details (user_id, email, first_name, last_name, subscription_level)
    #            if the credentials are valid. Returns (None, None, None, None, None) otherwise.
    # """
    # # Query to fetch user details by email
    # query = '''
    #     SELECT user_id, email, first_name, last_name, subscription_level, password_hash
    #     FROM users
    #     WHERE email = :email
    # '''
    # # Execute the query to get the user details
    # result = execute_query(query, {'email': email})

    # if result:
    #     # Extract user details
    #     user_id, email, first_name, last_name, subscription_level, password_hash = result[0]
    #     print(f"User found: {email}, {first_name}, {subscription_level}")
    #     print(f"Stored hash: {password_hash}")
    #     print(f"Computed hash: {hash_password(password)}")

    #     # Validate the password
    #     if hash_password(password) == password_hash:
    #         return user_id, email, first_name, last_name, subscription_level

    # # Return None values if authentication fails
    # return None, None, None, None, None