from django.template.loader import get_template

print(get_template('registration/password_reset.html'))
print(get_template('registration/password_reset_done.html'))
print(get_template('registration/password_reset_confirm.html'))
print(get_template('registration/password_reset_complete.html'))