from fake_db.fake_users_db import fake_users_db


fake_user_credentials = fake_users_db['XYZ']
fake_user_username = fake_user_credentials['username']
fake_user_password = fake_user_credentials['password']


# if __name__ == '__main__':
#     print(fake_user_credentials)
#     print(fake_user_username)
#     print(fake_user_password)
