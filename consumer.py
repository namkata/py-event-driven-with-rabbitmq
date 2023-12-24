from config import (
    get_rabbitmq_connection,
    configure_exchange,
    configure_queue,
    RABBITMQ_QUEUE_NAME,
)
import json


def callback(ch, method, properties, body):
    invoice = json.loads(body)
    invoice_number = invoice["invoice_number"]

    # Process the received invoice
    print(f"[<<<] Received invoice: {invoice_number}\n")
    print("----------------------------\n")
    print("Received invoice information: \n")
    for key, value in invoice.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    print("\nPlushed context: \n")
    print(json.dumps(invoice, indent=4))  # Indentation of 4 spaces
    print(f"\n[Completed] {invoice_number}")
    print("==========================\n")


def consume_invoices():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare and bind the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=True
    )

    print("Waiting for invoices...")
    channel.start_consuming()


if __name__ == "__main__":
    configure_exchange()
    configure_queue()
    consume_invoices()
