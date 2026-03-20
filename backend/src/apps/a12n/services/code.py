import secrets

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class CodeService:
    def _generate_code(self) -> str:
        return f'{secrets.randbelow(1_000_000):06d}'

    def _build_email_message(
        self, email: str, code: str
    ) -> EmailMultiAlternatives:

        context = {
            'code': code,
            'ttl_minutes': settings.EMAIL_CODE_TTL_SECONDS // 60,
            'site_name': settings.SITE_NAME,
            'site_url': settings.SITE_URL,
            'sender_name': 'Отправитель2222',  # Чаще всего совпадает с названием
            'support_email': settings.DEFAULT_FROM_EMAIL,
        }

        subject = f'{context["site_name"]}: код для входа на сайт.'
        text_body = render_to_string('emails/login_code.txt', context)
        html_body = render_to_string('emails/login_code.html', context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_body, 'text/html')
        return msg

    def send_code(self, email: str) -> None:
        code = self._generate_code()
        cache.set(
            f'login_code_{email}',
            code,
            timeout=settings.EMAIL_CODE_TTL_SECONDS,
        )

        msg = self._build_email_message(email, code)
        msg.send()

    def verify_code(self, email: str, code: str) -> bool:
        cached_code = cache.get(f'login_code_{email}')
        if cached_code == code:
            cache.delete(f'login_code_{email}')
            return True
        return False
