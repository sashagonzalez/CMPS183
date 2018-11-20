import datetime

#function to get email of user if they are logged in
def get_user_email():
    return None if auth.user is None else auth.user.email

#function to get the current date and time
def get_current_time():
    return datetime.datetime.utcnow()

#Definition for the Post db
db.define_table('post',
                Field('post_author', default=get_user_email()),
                Field('post_title'),
                Field('post_description', 'text'),
                Field('post_time', 'datetime', default=get_current_time()),
                Field('post_location'),
                Field('post_price'),
                Field('post_image'),
                Field('post_contact'),
                )