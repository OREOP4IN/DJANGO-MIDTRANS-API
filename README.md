# Django Midtrans Payment API

A robust Backend API built with Django Rest Framework (DRF) to handle e-commerce checkouts and secure automated payment notifications using the Midtrans Payment Gateway.

## Features
* **Product Management**: CRUD operations for products with stock tracking.
* **Atomic Transactions**: Uses `transaction.atomic()` and `select_for_update()` to prevent race conditions during checkout.
* **Midtrans Snap Integration**: Generates secure payment URLs for frontend redirection.
* **Secure Webhooks**: Implements SHA512 signature validation for Midtrans notifications (Settlement, Pending, Expire).
* **Environment Security**: Sensitive keys managed via `.env`.

---

## Prerequisites
* Python 3.10+
* Midtrans Sandbox Account
* [ngrok](https://ngrok.com/) (for local webhook testing)

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/OREOP4IN/DJANGO-MIDTRANS-API.git
cd DJANGO-MIDTRANS-API

```

2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables**
Create a `.env` file in the root directory:
```ini
SECRET_KEY="SECRET_KEY_HERE"
DEBUG=True
MIDTRANS_IS_PRODUCTION=False
MIDTRANS_SERVER_KEY=MIDTRANS_SERVER_KEY_HERE
MIDTRANS_CLIENT_KEY=MIDTRANS_CLIENT_KEY_HERE
```


5. **Run Migrations & Create Superuser**
```bash
python manage.py migrate
python manage.py createsuperuser

```


6. **Start the Server**
```bash
python manage.py runserver

```



---

## Testing the Webhook (Local)

Because Midtrans needs a public URL to send notifications, use **ngrok**:

1. Start ngrok on port 8000:
```bash
ngrok http 8000

```


2. Copy the `Forwarding` URL (e.g., `https://xyz.ngrok-free.dev`).
3. Add this URL to your **Midtrans Dashboard > Settings > Payment > Notification URL**:
`https://xyz.ngrok-free.dev/api/webhook/midtrans/`
4. Ensure your `ALLOWED_HOSTS` in `settings.py` includes your ngrok domain or `['*']`.

---

## API Endpoints

### 1. Checkout (Create Order)

* **URL**: `/api/checkout/`
* **Method**: `POST`
* **Payload**:
```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}

```


* **Response**: Returns `order_id` and `payment_url`.

### 2. Midtrans Webhook

* **URL**: `/api/webhook/midtrans/`
* **Method**: `POST`
* **Security**: Validates `signature_key` using SHA512.

---

## Postman Collection

A pre-configured Postman collection is included in the root folder: `orders_test.postman_collection.json`. Import this into Postman to test the flow immediately.
