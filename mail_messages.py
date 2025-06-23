
import time

date=time.strftime("%d-%b-%Y")

# ---here modify your email and app password---




def send_otp(otp="",name=""):#----this function to send mail for forgot password
    return f"""Dear {name} ,

We received a request to reset your password. Please use the following One-Time Password (OTP) to proceed:

OTP: {otp}

This OTP is valid for only 2 min. If you did not request this, please ignore this email.

Best regards,
ABC Bank"""

def delete_ac_otp(otp="",name=""):
    return f"""Hi {name},
                
Your code to confirm account deletion is:
Verification Code : {otp}
If you didn't request this, please ignore the email.
— ABC Bank"""

def ac_deleted_msg(name="",acn=""):
    return f"""Dear {name} ,

Your account {acn} has been successfully closed as per your request on {date}.

If this was not requested by you, please contact us immediately.

Thank you for banking with Kisis Bank.

Regards,
ABC Bank Support"""

def admin_deposit_msg(name="",ref="",amount="",acn=""):
    return f"""Dear {name},
                    
₹{amount} has been successfully
credited to your account ({acn}) on {date}
from Admin
Ref No.:{ref}
Thank you for banking with us."""

def detail_update_msg(befor_name="",after_name="",email="",mob="",pw="",):
    return f"""Dear {befor_name},
We wanted to let you know that your account details have been successfully updated.

Here are your updated details:

- Name:  {after_name}
- Email: {email}
- Mobile: {mob}
- Password: {pw}
If you did not request these changes, please contact our support team immediately.

Thank you,  
ABC Bank
"""   

def widhraw_msg(amount="",name="",ref="",avl_bal=""):
    return f"""dear {name},
                
Amount: ₹{amount} has been successfully withdrawn from your account.
Ref No.: {ref}
Remaining Balance: ₹{avl_bal}
Thank you for banking with us.
    """

def transfer_amt_msg(transfer_amt="",trasfer_acn="",receiver_acn="",receiver_name="",ref="",avl_bal=""):
    return f"""Sent Rs.{transfer_amt} from ABC Bank Ac X{trasfer_acn} on {date} to {receiver_name} A/c-{receiver_acn}
Ref No.: {ref}
Availble Balance ₹{avl_bal}"""

def receiver_amt_msg(transfer_amt="",receiver_acn="",sender_name="",sender_acn="",total_bal="",ref=""):
    return f"""Received Rs.{transfer_amt} in your ABC Bank AC X{receiver_acn} on {date} from {sender_name} A/c-{sender_acn}
Ref No.: {ref}
Total Balance ₹{total_bal}"""

def ac_opening_msg(acn="",name="",ac_type="",password="",ifsc=""):
    return f"""Dear {name},\n
Welcome to our bank!  
We are pleased to inform you that your account has been successfully opened.  
Thank you for choosing us — we look forward to serving you.

A/C No.      : {acn}
IFSC Code    : {ifsc}
Account Type : {ac_type}
Password     : {password}

Your default password has been set.
Please change your password after first login for security reasons.
Warm regards,  
ABC Bank"""

def help_msg(name="",acn="",issue=""):
    return f"""Dear {name},

Thank you for reaching out to our Help Desk.

We have received your request regarding the issue you are facing with your account (A/c No.: {acn}). Our support team is currently reviewing the details you've provided:

---
Issue Description:
{issue}
---

We appreciate your patience, and one of our team members will get back to you shortly with a resolution or further assistance.

If you have any additional information to share, feel free to reply to this email.

Best regards,  
Help & Support Team  
ABC Bank  
support@abcbank.com"""

                    




            