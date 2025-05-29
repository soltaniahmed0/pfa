# accounts/utils.py or accounts/services.py

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(user):
    """Send welcome email"""
    if not user.profile.email_notifications:
        return False
        
    try:
        subject = 'Welcome to our platform!'
        html_content = render_to_string('accounts/emails/welcome_email.html', {
            'user': user,
            'site_name': 'Your Site'
        })
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending welcome email to {user.email}: {str(e)}")
        return False

def send_profile_update_notification(user):
    """Profile update notification"""
    if not user.profile.email_notifications:
        return False
        
    try:
        subject = 'Profile Updated Successfully'
        message = f"""
Hello {user.get_full_name() or user.username},

Your profile has been successfully updated.

If this wasn't you, please contact us immediately.

Best regards,
The Your Site Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Profile update notification sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending profile update notification to {user.email}: {str(e)}")
        return False

def send_password_change_notification(user):
    """Password change notification"""
    if not user.profile.email_notifications:
        return False
        
    try:
        subject = 'Password Changed'
        message = f"""
Hello {user.get_full_name() or user.username},

Your password has been successfully changed.

If this wasn't you, please contact us immediately.

Best regards,
The Your Site Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Password change notification sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending password change notification to {user.email}: {str(e)}")
        return False

def send_analysis_result_email(user, analysis_result):
    """Send analysis results by email"""
    if not user.profile.email_notifications:
        return False
        
    try:
        subject = 'Your Analysis Results'
        html_content = render_to_string('accounts/emails/analysis_result.html', {
            'user': user,
            'analysis': analysis_result,
            'site_name': 'Your Site'
        })
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Analysis result email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending analysis result email to {user.email}: {str(e)}")
        return False