import random
from faker import Faker

fake = Faker("vi_VN")  # Set the locale to Vietnamese


def generate_invoice():
    # Generate fake data for the invoice
    invoice_number = fake.random_int(min=1000, max=9999)
    invoice_date = fake.date_this_decade()
    # Convert date object to string in ISO 8601 format
    invoice_date_str = invoice_date.isoformat()
    due_date = fake.date_between(start_date=invoice_date, end_date="+30d")
    due_date_str = due_date.isoformat()
    customer_name = fake.name()
    customer_email = fake.ascii_safe_email()
    item = fake.word()
    quantity = random.randint(1, 10)
    unit_price = fake.random_number(digits=2)
    total_amount = quantity * unit_price

    # Create the invoice dictionary
    invoice = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date_str,
        "due_date": due_date_str,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "item": item,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": total_amount,
    }

    # # Display the fake invoice details
    # print("Fake Invoice Information:")
    # print("==========================")
    # for key, value in invoice.items():
    #     print(f"{key.replace('_', ' ').title()}: {value}")

    return invoice
