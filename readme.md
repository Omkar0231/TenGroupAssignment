# Ten Assignment

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Create a Super User

```bash
python manage.py createsuperuser
```

2. Run Server
```bash
python manage.py runserver
```

3. Go to http://localhost:8000/admin/booking/upload-csv-admin/

*NOTE:* Here you can upload the csv files to input the data to the database. You can also find the sample file to download.

4. Booking API Endpoint:
```bash
http://localhost:8000/book/
```
Body:
```json
{
    "member": 1, // Member ID
    "item": 7 // Inventory ID
}
```
Response:
```json
{
    "id": 4,
    "item": 7,
    "member": 1,
    "booking_time": "2025-03-20T21:58:31.990284Z"
}
```

5. Cancel Booking Endpoint:
```bash
localhost:8000/cancel/
```

Body:
```json
{
    "member": 1, // Member ID
    "booking": 4 // Booking ID
}
```
Response:
```json
{
    "message": "Booking has been cancelled."
}
```

*NOTE:* You can find the Postman Collection in the root folder.

6. Run the Test Cases
```bash 
python manage.py test booking.tests
```