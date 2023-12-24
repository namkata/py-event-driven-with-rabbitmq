from config import (
    get_rabbitmq_connection,
    configure_exchange,
    configure_queue,
    RABBITMQ_EXCHANGE_NAME,
    RABBITMQ_ROUTING_KEY,
)
import json
from data import generate_invoice


def send_invoices():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Simulating 10 invoices
    for _ in range(1, 11):
        invoice = generate_invoice()
        # Convert invoice to JSON format
        message = json.dumps(invoice)

        # Publish invoice message to the queue
        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE_NAME,  # Default exchange
            routing_key=RABBITMQ_ROUTING_KEY,  # Queue name
            body=message,
        )
        print(f"Send invoicing {str(invoice['invoice_number'])}... [>>>] \n")
        print("Invoice Information:\n")
        print("--------------------------")
        for key, value in invoice.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        print("\nPlushing context: \n")
        print(json.dumps(invoice, indent=4))
        print(f"Invoice-{str(invoice['invoice_number'])} sent \n")
        print("==========================\n")

    connection.close()


if __name__ == "__main__":
    configure_exchange()
    configure_queue()
    send_invoices()
