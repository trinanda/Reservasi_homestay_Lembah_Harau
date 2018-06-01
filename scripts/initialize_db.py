# @flask_objek.route('/addsuperuser')
#     def seed():
#         user_role = Role(name='user')
#         super_user_role = Role(name='superuser')
#         database.session.add(user_role)
#         database.session.add(super_user_role)
#         database.session.commit()
#
#         test_user = user_datastore.create_user(
#             first_name='Admin',
#             send_email='admin',
#             password=encrypt_password('admin'),
#             roles=[user_role, super_user_role]
#         )
#
#         database.session.add(test_user)
#         database.session.commit()