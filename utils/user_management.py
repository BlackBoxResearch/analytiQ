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

