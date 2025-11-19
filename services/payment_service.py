"""
Payment Service
Handles payment processing for online and card payments
"""
import random
import string
from datetime import datetime

class PaymentService:
    """Service for handling payment operations"""
    
    @staticmethod
    def validate_card_details(card_number, expiry, cvv):
        """Validate card details"""
        # Remove spaces from card number
        card_number = card_number.replace(' ', '')
        
        # Validate card number (basic Luhn algorithm)
        if not card_number.isdigit() or len(card_number) != 16:
            return False, "Card number must be 16 digits"
        
        # Validate expiry date format (MM/YY)
        if len(expiry) != 5 or expiry[2] != '/':
            return False, "Expiry date format should be MM/YY"
        
        try:
            month, year = expiry.split('/')
            month = int(month)
            year = int(year)
            
            if month < 1 or month > 12:
                return False, "Invalid month"
            
            if year < 25:  # Assuming current year is 2025
                return False, "Card expired"
        except ValueError:
            return False, "Invalid expiry date format"
        
        # Validate CVV
        if not cvv.isdigit() or len(cvv) != 3:
            return False, "CVV must be 3 digits"
        
        return True, "Valid"
    
    @staticmethod
    def validate_paypal_email(email):
        """Validate PayPal email format"""
        if '@' not in email:
            return False, "Invalid PayPal email format"
        
        parts = email.split('@')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False, "Invalid PayPal email format"
        
        return True, "Valid"
    
    @staticmethod
    def validate_gpay_phone(phone):
        """Validate GPay phone number format"""
        # Remove any non-digit characters
        phone = ''.join(c for c in phone if c.isdigit())
        
        if len(phone) < 10:
            return False, "Phone number must be at least 10 digits"
        
        return True, "Valid"
    
    @staticmethod
    def generate_transaction_id():
        """Generate unique transaction ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TXN{timestamp}{random_str}"
    
    @staticmethod
    def process_card_payment(card_number, expiry, cvv, amount, cardholder_name):
        """Process card payment (simulated)"""
        # Validate card details
        is_valid, msg = PaymentService.validate_card_details(card_number, expiry, cvv)
        if not is_valid:
            return False, msg
        
        # Simulate payment processing
        transaction_id = PaymentService.generate_transaction_id()
        
        # In real scenario, this would connect to payment gateway (Stripe, PayPal, etc.)
        # For now, we simulate successful payment
        return True, {
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'card',
            'cardholder': cardholder_name,
            'timestamp': datetime.now(),
            'status': 'completed'
        }
    
    @staticmethod
    def process_paypal_payment(email, amount):
        """Process PayPal payment (simulated)"""
        # Validate PayPal email
        is_valid, msg = PaymentService.validate_paypal_email(email)
        if not is_valid:
            return False, msg
        
        # Simulate payment processing
        transaction_id = PaymentService.generate_transaction_id()
        
        # In real scenario, this would connect to PayPal API
        # For now, we simulate successful payment
        return True, {
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'paypal',
            'email': email,
            'timestamp': datetime.now(),
            'status': 'completed'
        }
    
    @staticmethod
    def process_gpay_payment(phone_number, amount):
        """Process Google Pay (GPay) payment (simulated)"""
        # Validate GPay phone number
        is_valid, msg = PaymentService.validate_gpay_phone(phone_number)
        if not is_valid:
            return False, msg
        
        # Simulate payment processing
        transaction_id = PaymentService.generate_transaction_id()
        
        # In real scenario, this would connect to Google Pay API
        # For now, we simulate successful payment
        return True, {
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'gpay',
            'phone': phone_number,
            'timestamp': datetime.now(),
            'status': 'completed'
        }
    
    @staticmethod
    def process_net_banking_payment(bank_name, account_number, amount):
        """Process net banking payment (simulated)"""
        if not bank_name or not account_number:
            return False, "Please fill in all fields"
        
        if not account_number.isdigit() or len(account_number) < 8:
            return False, "Invalid account number"
        
        # Simulate payment processing
        transaction_id = PaymentService.generate_transaction_id()
        
        return True, {
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'net_banking',
            'bank': bank_name,
            'timestamp': datetime.now(),
            'status': 'completed'
        }
