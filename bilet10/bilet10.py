import re
from datetime import datetime


class Validator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        if not isinstance(phone, str):
            return False
        pattern = r"^\+?[1-9]\d{1,14}$"
        cleaned = re.sub(r"[\s\-()]", "", phone)
        return bool(re.match(pattern, cleaned))

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        if not isinstance(date_str, str):
            return False
        formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]
        for fmt in formats:
            try:
                datetime.strptime(date_str.strip(), fmt)
                return True
            except ValueError:
                continue
        return False


class FormValidator:
    def __init__(self, validator: Validator):
        self.validator = validator

    def validate(self, data: dict, schema: dict) -> dict:
        errors = {}
        
        for field, rule in schema.items():
            value = data.get(field)
            
            if value is None or (isinstance(value, str) and value.strip() == ""):
                errors[field] = "Field is required or empty"
                continue

            if rule == "email" and not self.validator.is_valid_email(value):
                errors[field] = "Invalid email format"
            elif rule == "phone" and not self.validator.is_valid_phone(value):
                errors[field] = "Invalid phone format"
            elif rule == "date" and not self.validator.is_valid_date(value):
                errors[field] = "Invalid date format"
                
        return errors


def test_email_validation():
    v = Validator()
    
    test_cases = [
        ("test@example.com", True),
        ("user.name+tag@domain.co.uk", True),
        ("123456@domain.com", True),
        ("", False),
        ("   ", False),
        ("plainaddress", False),
        ("@missinguser.com", False),
        ("user@.com", False),
        ("user@missingtld.", False),
        ("user@domain,com", False),
        ("user#name@domain.com", False),
        (None, False)
    ]
    
    print("Running Validator.is_valid_email() tests...")
    all_passed = True
    
    for email, expected in test_cases:
        result = v.is_valid_email(email)
        if result == expected:
            print(f"PASSED: '{email}' -> {result}")
        else:
            print(f"FAILED: '{email}' -> Expected {expected}, got {result}")
            all_passed = False
            
    if all_passed:
        print("All email validation tests passed successfully!\n")
    else:
        print("Some email validation tests failed.\n")


if __name__ == "__main__":
    test_email_validation()

    val = Validator()
    form_val = FormValidator(val)

    validation_schema = {
        "user_email": "email",
        "user_phone": "phone",
        "birth_date": "date"
    }

    valid_form_data = {
        "user_email": "developer@python.org",
        "user_phone": "+7 (999) 123-45-67",
        "birth_date": "2026-05-15"
    }

    invalid_form_data = {
        "user_email": "invalid_email@@@.com",
        "user_phone": "123",
        "birth_date": "32.13.2026"
    }

    print("Validating valid form data:")
    valid_errors = form_val.validate(valid_form_data, validation_schema)
    print(f"Errors: {valid_errors} (Success if empty)\n")

    print("Validating invalid form data:")
    invalid_errors = form_val.validate(invalid_form_data, validation_schema)
    print(f"Errors: {invalid_errors}")