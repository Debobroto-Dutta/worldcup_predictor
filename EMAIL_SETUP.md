# 📧 Email Configuration Guide

This guide explains how to set up email functionality for password reset features.

## Overview

The application uses Flask-Mail to send password reset emails. Admins can trigger password reset emails for users, and users receive a secure link to reset their password.

## Quick Setup (Gmail)

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: https://myaccount.google.com
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", enable **2-Step Verification**
4. Follow the prompts to set it up

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: **World Cup Predictor**
5. Click **Generate**
6. Copy the 16-character password (remove spaces)

### Step 3: Update .env File

Edit your `.env` file:

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

Replace:
- `your-email@gmail.com` with your Gmail address
- `your-16-char-app-password` with the generated app password

### Step 4: Restart Backend

```bash
cd backend
python app.py
```

## Other Email Providers

### Outlook/Hotmail

```bash
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

### Yahoo Mail

```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

Note: Yahoo also requires app passwords. Generate one at: https://login.yahoo.com/account/security

### Custom SMTP Server

```bash
MAIL_SERVER=smtp.yourprovider.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

## Testing Email Configuration

### Method 1: Using Python Shell

```bash
cd backend
python

from app import app, mail
from flask_mail import Message

with app.app_context():
    msg = Message(
        subject='Test Email',
        recipients=['test@example.com'],
        body='This is a test email from World Cup Predictor'
    )
    mail.send(msg)
    print("Email sent successfully!")
```

### Method 2: Using Admin Panel

1. Go to admin panel
2. Click "Users" tab
3. Click "Reset Password" for any user
4. Check if email is sent

## How Password Reset Works

### For Admins:

1. Admin clicks "Reset Password" button for a user
2. System generates a secure token (valid for 1 hour)
3. Email is sent to user's registered email
4. User clicks link in email
5. User enters new password
6. Password is updated

### Email Content:

The email includes:
- User's username
- Secure reset link
- Expiration time (1 hour)
- Professional HTML formatting

### Security Features:

- ✅ Token expires after 1 hour
- ✅ Token is cryptographically signed
- ✅ One-time use (token becomes invalid after password reset)
- ✅ Secure password hashing

## Troubleshooting

### "Failed to send email"

**Check:**
1. Email credentials are correct in `.env`
2. App password is used (not regular password for Gmail)
3. 2FA is enabled for Gmail
4. Internet connection is working
5. SMTP server and port are correct

**Test connection:**
```bash
telnet smtp.gmail.com 587
```

### "Authentication failed"

**Solutions:**
- For Gmail: Use app password, not regular password
- For Yahoo: Generate app password
- For Outlook: Use regular password (app passwords not required)
- Check username is complete email address

### "Connection refused"

**Check:**
- Port number is correct (usually 587 for TLS)
- Firewall isn't blocking SMTP
- MAIL_USE_TLS is set to `true`

### "Email not received"

**Check:**
- Spam/Junk folder
- Email address is correct in user profile
- Email quota not exceeded
- Email provider isn't blocking automated emails

## Development Mode (No Email)

If you don't want to set up email during development, you can:

1. **Use console output** (emails printed to terminal):

```python
# In app.py, add after app configuration:
if app.config['FLASK_ENV'] == 'development':
    app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_DEBUG'] = True
```

2. **Use a test email service**:
   - Mailtrap: https://mailtrap.io (free tier available)
   - MailHog: Local email testing tool

## Production Considerations

### Use a Dedicated Email Service

For production, consider using:

1. **SendGrid** (Free tier: 100 emails/day)
   ```bash
   MAIL_SERVER=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=your-sendgrid-api-key
   ```

2. **Mailgun** (Free tier: 5,000 emails/month)
3. **Amazon SES** (Pay as you go)
4. **Postmark** (Free tier: 100 emails/month)

### Security Best Practices

1. **Never commit .env file** (already in .gitignore)
2. **Use environment variables** in production
3. **Rotate passwords** regularly
4. **Monitor email sending** for abuse
5. **Implement rate limiting** on password reset requests

### Email Templates

The current implementation includes:
- Plain text version (for email clients that don't support HTML)
- HTML version (with styling and branding)
- Responsive design (works on mobile)

To customize, edit the email content in `backend/app.py` in the `send_password_reset_email` function.

## API Endpoints

### Send Reset Email (Admin Only)
```
POST /api/admin/users/<user_id>/send-reset-email
Authorization: Required (Admin)
```

### Reset Password (Public)
```
POST /api/reset-password
Content-Type: application/json

{
  "token": "reset-token-from-email",
  "new_password": "newpassword123"
}
```

### Verify Token (Public)
```
POST /api/verify-reset-token
Content-Type: application/json

{
  "token": "reset-token-from-email"
}
```

## Support

If you encounter issues:

1. Check the backend console for error messages
2. Verify email configuration in `.env`
3. Test with a simple email first
4. Check email provider's documentation
5. Review Flask-Mail documentation: https://pythonhosted.org/Flask-Mail/

---

**Email functionality is now ready! Users can securely reset their passwords via email. 📧✅**