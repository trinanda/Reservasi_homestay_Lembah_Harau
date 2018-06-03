## buat route dan fungsi ini pada web_app.app.py, kemudian jalankan url nya di browser untuk menambahkan isi table role
## kemudian register user melalui menu register http://128.199.80.54:7575/admin/register/
## selanjutnya insert user_id dan role_id pada table roles_users secara manual melalui pgadmin
## sesuaikan kolom role_id (user or superuser) pada user_id

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