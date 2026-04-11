

def test_cache(settings):
    pass


def test_mail(mailoutbox, auth_email_service):
    auth_email_service.send_login_code('test@mail.ru')

    assert len(mailoutbox) == 1
