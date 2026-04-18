import logging
import secrets
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger('apps.a12n.auth_email')


class AuthEmailService:
    def _generate_code(self) -> str:
        return f'{secrets.randbelow(1_000_000):06d}'

    def _generate_token(self) -> str:
        return secrets.token_urlsafe(32)

    def _login_code_key(self, email: str) -> str:
        return f'auth:login_code:{email}'

    def _login_code_cooldown_key(self, email: str) -> str:
        return f'auth:login_code_cooldown:{email}'

    def _login_code_attempts_key(self, email: str) -> str:
        return f'auth:login_code_attempts:{email}'

    def _invite_token_key(self, token: str) -> str:
        return f'auth:invite_token:{token}'

    def _invite_email_cooldown_key(self, email: str) -> str:
        return f'auth:invite_cooldown:{email}'

    def _send_email(
        self,
        email: str,
        subject: str,
        template_name: str,
        context: dict[str, str | int],
    ) -> None:
        full_context = {
            'site_name': settings.SITE_NAME,
            'site_url': settings.SITE_URL,
            'sender_name': settings.SITE_NAME,
            'support_email': settings.SUPPORT_EMAIL,
            **context,
        }

        text_body = render_to_string(
            f'emails/{template_name}.txt', full_context
        )
        html_body = render_to_string(
            f'emails/{template_name}.html', full_context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)

    def send_login_code(self, email: str) -> None:
        cooldown_key = self._login_code_cooldown_key(email)
        if cache.get(cooldown_key):
            return

        code = self._generate_code()

        cache.set(
            self._login_code_key(email),
            code,
            timeout=settings.EMAIL_CODE_TTL_SECONDS,
        )
        cache.set(
            cooldown_key,
            '1',
            timeout=settings.EMAIL_CODE_RESEND_COOLDOWN_SECONDS,
        )

        self._send_email(
            email=email,
            subject=f'{settings.SITE_NAME}: код для входа',
            template_name='login_code',
            context={
                'code': code,
                'ttl_minutes': settings.EMAIL_CODE_TTL_SECONDS // 60,
            },
        )

    def verify_login_code(self, email: str, code: str) -> bool:
        attempts_key = self._login_code_attempts_key(email)
        code_key = self._login_code_key(email)

        attempts = cache.get(attempts_key, 0)
        cached_code = cache.get(code_key)

        if not cached_code:
            return False

        if attempts >= settings.EMAIL_CODE_MAX_VERIFY_ATTEMPTS:
            cache.delete(code_key)
            cache.delete(attempts_key)
            return False

        if secrets.compare_digest(cached_code, code):
            cache.delete(code_key)
            cache.delete(attempts_key)
            return True

        attempts += 1
        if attempts >= settings.EMAIL_CODE_MAX_VERIFY_ATTEMPTS:
            cache.delete(code_key)
            cache.delete(attempts_key)
            return False

        cache.set(
            attempts_key,
            attempts,
            timeout=settings.EMAIL_CODE_TTL_SECONDS,
        )
        return False

    def send_invite_link(self, email: str) -> None:
        logger.info('Sending invite link ')
        cooldown_key = self._invite_email_cooldown_key(email)
        if cache.get(cooldown_key):
            return

        token = self._generate_token()

        cache.set(
            self._invite_token_key(token),
            {'email': email},
            timeout=settings.INVITE_TOKEN_TTL_SECONDS,
        )
        cache.set(
            cooldown_key,
            '1',
            timeout=settings.INVITE_RESEND_COOLDOWN_SECONDS,
        )

        link = urljoin(
            settings.SITE_URL,
            f'{settings.INVITE_CONFIRM_PATH.rstrip("/")}/{token}/',
        )

        self._send_email(
            email=email,
            subject=f'Добро пожаловать в {settings.SITE_NAME}!',
            template_name='invite_link',
            context={
                'link': link,
                'ttl_minutes': settings.INVITE_TOKEN_TTL_SECONDS // 60,
            },
        )

    def verify_invite_token(self, token: str) -> str | None:
        cache_key = self._invite_token_key(token)
        payload = cache.get(cache_key)

        if not payload:
            return None

        cache.delete(cache_key)
        return payload.get('email')  # type: ignore[no-any-return]
