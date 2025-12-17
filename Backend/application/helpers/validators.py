import re


def validate_email(email):
    if not email or not isinstance(email, str):
        return False, "Email is required"

    email = email.strip()
    if not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+$', email):
        return False, "Invalid email format"

    return True, email


def validate_password(password):
    if not password or not isinstance(password, str):
        return False, "Password is required"

    password = password.strip()
    if len(password) < 5:
        return False, "Password must be at least 5 characters long"

    return True, password


def validate_name(name):
    if not name or not isinstance(name, str):
        return False, "Name is required"

    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"

    return True, name


def validate_address(address):
    if not address or not isinstance(address, str):
        return False, "Address is required"

    address = address.strip()
    if len(address) < 5:
        return False, "Address must be at least 5 characters long"

    return True, address


def validate_pincode(pincode):
    if not pincode:
        return False, "Pincode is required"

    pincode_str = str(pincode).strip()
    if not pincode_str.isdigit() or len(pincode_str) != 6:
        return False, "Pincode must be a 6-digit number"

    return True, pincode_str


def validate_vehicle_number(vehicle_number):
    if not vehicle_number or not isinstance(vehicle_number, str):
        return True, None

    vehicle_number = vehicle_number.strip().upper()

    if not re.fullmatch(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$', vehicle_number):
        return False, "Invalid vehicle number format"

    return True, vehicle_number


def validate_price(price):
    try:
        price_float = float(price)
        if price_float <= 0:
            return False, "Price must be greater than 0"
        return True, price_float
    except (ValueError, TypeError):
        return False, "Invalid price format"


def validate_spot_count(count):
    try:
        count_int = int(count)
        if count_int <= 0:
            return False, "Spot count must be greater than 0"
        return True, count_int
    except (ValueError, TypeError):
        return False, "Invalid spot count format"
