# coding=utf-8


def send_email(request, to, tpl, subject, **kwargs):
    """Шорткат для отправки писем"""
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    import cmedu.settings as settings

    if not isinstance(to, list) or not isinstance(to, tuple):
        to = [to]

    current_site = "www.vrachivmeste.ru"
    params = dict(host=current_site)
    params.update(kwargs)

    email = EmailMessage(
        subject.strip(),
        render_to_string('emails/%s.html' % tpl, params),
        settings.DEFAULT_FROM_EMAIL,
        to)
    email.content_subtype = "html"
    email.send(fail_silently=True)
    return True


# Improve the error message output, so I can actually debug / figure out
# what the hell went wrong during postmortems of HTTP 500 Server Errors.
#
# Based on http://djangosnippets.org/snippets/2244/
#
# Modifies the mixin in a similar way, but doesn't rewrite the whole thing.
# Just specifies additional behavior then calls to the saved handler.

from django.core.handlers.base import BaseHandler


def better_uncaught_exception_emails(self, request, resolver, exc_info):
    """
    Processing for any otherwise uncaught exceptions (those that will
    generate HTTP 500 responses). Can be overridden by subclasses who want
    customised 500 handling.

    Be *very* careful when overriding this because the error could be
    caused by anything, so assuming something like the database is always
    available would be an error.
    """
    from django.conf import settings
    from django.core.mail import EmailMultiAlternatives
    from django.views.debug import ExceptionReporter

    # Only send details emails in the production environment.
    if settings.DEBUG == False:
        reporter = ExceptionReporter(request, *exc_info)

        # Prepare the email headers for sending.
        from_ = settings.DEFAULT_FROM_EMAIL
        to_ = u"logs@vprosto.ru"

        subject = "Detailed stack trace."

        message = EmailMultiAlternatives(subject, reporter.get_traceback_text(), from_, [to_])
        message.attach_alternative(reporter.get_traceback_html(), 'text/html')
        message.send()

    # Make sure to then just call the base handler.
    return self.original_handle_uncaught_exception(request, resolver, exc_info)

# Save the original handler.
BaseHandler.original_handle_uncaught_exception = BaseHandler.handle_uncaught_exception

# Override the original handler.
BaseHandler.handle_uncaught_exception = better_uncaught_exception_emails


def dictfetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

