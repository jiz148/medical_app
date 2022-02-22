FORGET_MY_PASSWORD_SUBJECT = """Password Change Confirmation"""
FORGET_MY_PASSWORD_CONTENT = """hello {user},\n
                                Please click the following link to change your password:\n
                                http://localhost:8080/#/newpass/?token={token}\n
                                This link will be expired in {minutes} minutes."""
