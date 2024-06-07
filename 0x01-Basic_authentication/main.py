#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.basic_auth import BasicAuth

    ba = BasicAuth()
    res1, res2 = ba.extract_user_credentials("Holberton:HBTN:is:so:cool")
    if res1 is None:
        print("extract_user_credentials must return the first part of 'decoded_base64_authorization_header' (separated by ':')")
        exit(1)
    if res2 is None:
        print("extract_user_credentials must return the last part of 'decoded_base64_authorization_header' (separated by ':')")
        exit(1)

    if res1 != "Holberton":
        print("Wrong first part of 'decoded_base64_authorization_header': {}".format(res1))
        exit(1)
    if res2 != "HBTN:is:so:cool":
        print("Wrong second part of 'decoded_base64_authorization_header': {}".format(res1))
        exit(1)
    
    print("OK", end="")
