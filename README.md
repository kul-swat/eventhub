# EventHub

A minimal Django REST Framework API for managing events and reservations.

## How to run the project

1. Activate the virtual environment:
   ```bash
   source eventenv/bin/activate
   ```
2. Install dependencies if needed:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open the API at:
   ```
   http://127.0.0.1:8000/api/
   ```

## What each endpoint does

### `/api/events/`

- `GET /api/events/`
  - List all events.
  - Supports filtering by query parameters:
    - `status` (e.g. `?status=upcoming`)
    - `venue` (case-insensitive substring search, e.g. `?venue=Hall`)
- `POST /api/events/`
  - Create a new event.
  - Request body should include:
    - `title`
    - `venue`
    - `date`
    - `total_seats`
    - `available_seats`
    - `status` (optional, defaults to `upcoming`)
- `GET /api/events/{id}/`
  - Retrieve a single event by ID.
- `PUT /api/events/{id}/` and `PATCH /api/events/{id}/`
  - Update event data.
- `DELETE /api/events/{id}/`
  - Delete an event.

Each event response also includes `reservations_count`, which reports how many confirmed reservations exist for that event.

### `/api/reservations/`

- `GET /api/reservations/`
  - List all reservations.
  - Supports filtering by query parameter:
    - `event_id` (e.g. `?event_id=1`)
- `POST /api/reservations/`
  - Create a reservation for an event.
  - Request body should include:
    - `event` (event ID)
    - `attendee_name`
    - `attendee_email`
    - `seats_reserved`
  - The API validates that:
    - the reservation is for an event with status `upcoming` or `ongoing`
    - enough seats remain available
    - at least one seat is reserved
  - On success, the event's `available_seats` is decremented automatically.
- `GET /api/reservations/{id}/`
  - Retrieve a reservation by ID.
- `PUT /api/reservations/{id}/` and `PATCH /api/reservations/{id}/`
  - Update reservation details.
- `DELETE /api/reservations/{id}/`
  - Delete a reservation.
- `POST /api/reservations/{id}/cancel/`
  - Cancel a reservation.
  - If the reservation is not already cancelled, it:
    - updates reservation status to `cancelled`
    - restores reserved seats to the associated event's `available_seats`

## One design decision and why

I chose to model the API with Django REST Framework `ModelViewSet`s and a router (`DefaultRouter`) for both `Event` and `Reservation`. This decision gives a clean RESTful structure with consistent CRUD endpoints, makes the code easier to extend, and keeps the implementation concise.

Additionally, I handled seat inventory updates inside the reservation serializer and cancellation action. That keeps the business rule centralized: creating a reservation reduces available seats, and cancelling restores them. This makes the data flow predictable and avoids leaving seat counts inconsistent across the two related models.

## Postman Screenshots

Each screenshot below shows a Postman request or response from the API.

- ![Create Event](PostmanScreenshots/create_event.png)
  - Create a new event using the `/api/events/` endpoint.
- ![Create Reservation](PostmanScreenshots/create_reservations.png)
  - Reserve seats for an event through `/api/reservations/`.
- ![Delete Event](PostmanScreenshots/delete_event_id.png)
  - Delete an event by ID with `/api/events/{id}/`.
- ![Get All Events](PostmanScreenshots/get_all_events.png)
  - List every event returned by `/api/events/`.
- ![Get All Reservations](PostmanScreenshots/get_all_reservations.png)
  - List every reservation returned by `/api/reservations/`.
- ![Filter Events by Venue](PostmanScreenshots/get_event_filter_venue.png)
  - Filter events by venue name using `?venue=`.
- ![Filter Events by Status](PostmanScreenshots/get_filter_status.png)
  - Filter events by status using `?status=`.
- ![Filter Reservations by Event ID](PostmanScreenshots/get_reservations_filter_eventid.png)
  - Filter reservations by `event_id`.
- ![Get Reservation by ID](PostmanScreenshots/get_reservations_id.png)
  - Retrieve a specific reservation by its ID.
- ![Middleware Request Logging](PostmanScreenshots/middleware_request_logging.png)
  - Example request logging output from custom middleware.
- ![Patch Event](PostmanScreenshots/patch_event_id.png)
  - Update event fields using `PATCH /api/events/{id}/`.
- ![Patch Reservation](PostmanScreenshots/patch_reservations_id.png)
  - Update reservation details with `PATCH /api/reservations/{id}/`.
- ![Cancel Reservation](PostmanScreenshots/post_reservation_cancel.png)
  - Cancel a reservation with `POST /api/reservations/{id}/cancel/`.
- ![Put Event](PostmanScreenshots/put_event_id.png)
  - Replace event data using `PUT /api/events/{id}/`.
- ![Put Reservation](PostmanScreenshots/put_reservation_id.png)
  - Replace reservation data using `PUT /api/reservations/{id}/`.
