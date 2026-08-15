# Abia Transit — Django MVP Implementation Specification

## 1. Project Overview

**Abia Transit** is a digital mobility infrastructure platform for Abia State.

It adds a digital layer to existing transportation infrastructure by connecting:

- Passengers
- Abia State/government-owned transport
- Participating private transport operators
- Buses and drivers
- Routes and designated bus stops
- Trips and seats
- Fares and bookings
- Transport alerts and complaints
- Operational analytics

### Core positioning

> Abia Transit does not replace the transportation infrastructure Abia already has. It digitally connects and optimizes it.

---

## 2. MVP Goal

The MVP should demonstrate the core value without requiring real government integrations.

The prototype must prove that:

1. A passenger can find a trip.
2. A passenger can choose a boarding stop and destination.
3. The system can calculate a configurable fare using 5 km bands.
4. A passenger can select an available seat and book.
5. A passenger can view booking history and cancel an upcoming booking.
6. A passenger can see trip/bus status and simulated location.
7. A government administrator can manage government buses, routes, stops and trips.
8. A private operator can manage its own vehicles, drivers and trips.
9. Government can view basic transport analytics.
10. Different user roles cannot access unauthorized data.

Real GPS, payment, SMS, transport-card and government-system integrations are **future integrations**, not MVP requirements.

---

## 3. User Roles

### Super Admin

System-level administrator.

Can:
- Manage all users and organizations.
- Approve operators.
- Manage system configuration.
- View all data.

### Government Admin

Authorized Abia State transport administrator.

Can:
- Manage government fleet.
- Manage routes and bus stops.
- Create/manage trips.
- View participating operators according to policy.
- View transport analytics.
- Review complaints.
- Publish transport alerts.

### Operator Admin

Private transport company administrator.

Can only manage the operator's own:
- Vehicles
- Drivers
- Trips
- Bookings
- Reports

### Driver

Can:
- View assigned trips.
- Update trip status.
- Update simulated location during a prototype trip.

### Passenger

Can:
- Browse trips.
- View routes/stops/fare.
- Book seats.
- View/cancel own bookings.
- Track eligible trips.
- Submit complaints.
- Receive alerts.

---

## 4. MVP Modules

### A. Authentication and authorization

- Registration/login/logout
- Password reset
- Role-based permissions
- Organization-level data isolation
- Government/operator account approval where appropriate

### B. Route management

A route contains:
- Name
- Origin
- Destination
- Ordered bus stops
- Active/inactive status

Example:

`Umuahia → Umudike → Isiala Ngwa → Osisioma → Aba`

### C. Bus stops

Each stop contains:
- Name
- Description
- Latitude
- Longitude
- Stop order within a route
- Active status

For MVP, coordinates can be seeded manually.

### D. Organizations

Organizations represent:
- Abia State transport/government fleet
- Private transport companies

Each organization owns or manages its own vehicles, drivers and trips.

### E. Vehicles

Vehicle fields:
- Organization
- Vehicle code
- Registration number
- Vehicle type
- Seat capacity
- Status
- Active route/trip
- Maintenance note/status

### F. Drivers

Driver fields:
- User
- Organization
- Phone
- License/reference number
- Active status

### G. Trips

A trip connects:
- Route
- Organization
- Vehicle
- Driver
- Departure date/time
- Status
- Current/last stop
- Simulated location
- Available capacity

Trip statuses:

`SCHEDULED → BOARDING → DEPARTED → IN_TRANSIT → ARRIVED → CANCELLED`

### H. Seats

Each vehicle has numbered seats.

MVP should generate seats from vehicle capacity.

Seat status is derived from bookings where possible rather than manually maintained.

### I. Bookings

Booking contains:
- Passenger
- Trip
- Seat
- Boarding stop
- Destination stop
- Fare
- Booking reference
- Status
- Created timestamp

Booking statuses:

`CONFIRMED → CANCELLED → COMPLETED`

Use a unique booking reference.

### J. Fare engine

MVP uses configurable 5 km fare bands.

Example configuration:

| Distance | Band | Fare |
|---|---|---:|
| 0–5 km | 1 | configurable |
| >5–10 km | 2 | configurable |
| >10–15 km | 3 | configurable |
| >15–20 km | 4 | configurable |

Do not hard-code official government fares.

The fare table should be configurable by an authorized administrator.

Distance can initially be stored/calculated from seeded stop distances. Real road-distance routing can be integrated later.

### K. Booking management

Passenger can:
- View upcoming bookings
- View past bookings
- Cancel eligible upcoming bookings

Cancellation must release the seat.

### L. Tracking simulation

MVP does not need physical GPS.

A simulation service can move a vehicle through the ordered stops.

Example:

`Umuahia → Umudike → Isiala Ngwa → Osisioma → Aba`

Trip status and current stop update as the simulation progresses.

The UI can display:

> Bus ABIA-024 is approximately 15 minutes from Umudike.

Label simulated data clearly in the prototype.

### M. Notifications

MVP can use in-app notifications/toasts.

Examples:
- Booking confirmed
- Booking cancelled
- Trip boarding
- Trip departed
- Bus approaching stop
- Government transport alert

SMS/email integrations are future work.

### N. Complaints

Passenger can submit:
- Category
- Description
- Trip
- Vehicle
- Optional attachment later

Government/operator staff can update:

`OPEN → INVESTIGATING → RESOLVED`

### O. Government dashboard

Dashboard cards:
- Active government buses
- Scheduled trips
- Trips in progress
- Passenger bookings
- Average occupancy
- Open complaints

Charts:
- Bookings by route
- Occupancy by route
- Trips by date
- Popular boarding stops

### P. Operator dashboard

Show only the operator's data:
- Vehicles
- Drivers
- Today's trips
- Bookings
- Occupancy
- Revenue/booking totals where appropriate

### Q. Passenger dashboard

Show:
- Upcoming trips
- Recent bookings
- Active trip
- Notifications
- Quick booking/search

---

## 5. Suggested Django Apps

Keep the Django project modular.

```text
abia_transit/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── transport/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── admin.py
│
├── bookings/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── admin.py
│
├── tracking/
│   ├── models.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── complaints/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── notifications/
│   ├── models.py
│   ├── services.py
│   └── views.py
│
├── analytics/
│   ├── views.py
│   └── services.py
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── passenger/
│   ├── operator/
│   ├── government/
│   ├── bookings/
│   └── transport/
│
└── static/
```

For a small MVP, `tracking`, `notifications`, and `analytics` can initially live inside `transport` or `core`; splitting them later is fine.

---

## 6. Core Data Model

Recommended relationships:

```text
User
 ├── PassengerProfile
 ├── DriverProfile
 └── Government/Operator profile

Organization
 ├── Vehicle
 ├── Driver
 └── Trip

Route
 └── RouteStop → BusStop

Trip
 ├── Route
 ├── Organization
 ├── Vehicle
 ├── Driver
 └── Booking

Booking
 ├── Passenger
 ├── Trip
 ├── Seat
 ├── Boarding Stop
 └── Destination Stop

Complaint
 ├── Passenger
 ├── Trip
 └── Vehicle

Notification
 └── User
```

---

## 7. Important Model Design Rules

### Use a custom User model

Create the custom user model at the beginning rather than relying on Django's default User and changing later.

Suggested fields:
- email
- phone
- first_name
- last_name
- role
- is_active
- date_joined

Roles should be choices, not free text.

### Organization isolation

Every operator-owned resource should be linked to an `Organization`.

A query from an operator should always be filtered by:

```python
organization=request.user.organization
```

Government users should have broader permissions.

### Booking integrity

A seat must not be double-booked.

Use:
- database constraints where possible
- transactions
- `select_for_update()` when confirming a booking under concurrent requests

### Fare configuration

Never hard-code the final government fare values.

Store fare bands in the database.

---

## 8. Suggested Models

A high-level model plan:

```python
User
    role

Organization
    name
    organization_type

BusStop
    name
    latitude
    longitude
    is_active

Route
    name
    origin
    destination
    is_active

RouteStop
    route
    bus_stop
    stop_order
    distance_from_origin_km

Vehicle
    organization
    vehicle_code
    registration_number
    vehicle_type
    capacity
    status

Seat
    vehicle
    seat_number

DriverProfile
    user
    organization
    license_number
    is_active

Trip
    organization
    route
    vehicle
    driver
    departure_time
    status
    current_stop

Booking
    passenger
    trip
    seat
    boarding_stop
    destination_stop
    fare
    reference
    status

FareBand
    min_distance_km
    max_distance_km
    amount
    is_active

Complaint
    passenger
    trip
    category
    description
    status

Notification
    user
    title
    message
    notification_type
    is_read
```

---

## 9. Booking Flow

```text
Passenger logs in
      ↓
Search route
      ↓
Select date
      ↓
Choose boarding stop
      ↓
Choose destination stop
      ↓
System calculates journey distance
      ↓
System selects fare band
      ↓
Show available trips
      ↓
Select trip
      ↓
Show seat map
      ↓
Select available seat
      ↓
Confirm booking
      ↓
Create booking reference
      ↓
Show confirmation
```

---

## 10. Booking Cancellation

```text
Passenger opens booking
        ↓
Check eligibility
        ↓
Cancel booking
        ↓
Booking status = CANCELLED
        ↓
Seat becomes available
```

Define a cancellation policy before production.

For MVP, cancellation can be allowed while the trip is still `SCHEDULED` or `BOARDING`.

---

## 11. Government Workflow

```text
Government login
      ↓
Government dashboard
      ↓
Manage fleet
      ↓
Manage routes
      ↓
Manage bus stops
      ↓
Create trips
      ↓
Monitor trips
      ↓
View passengers/occupancy
      ↓
View analytics
      ↓
Review complaints
      ↓
Publish alerts
```

---

## 12. Operator Workflow

```text
Operator login
      ↓
Operator dashboard
      ↓
Manage vehicles
      ↓
Manage drivers
      ↓
Create trips
      ↓
Assign vehicle/driver
      ↓
View bookings
      ↓
View occupancy
```

Operators must never receive unrestricted access to another operator's records.

---

## 13. MVP Pages

### Public

- Home
- About
- Routes
- Bus stops
- Login
- Register

### Passenger

- Dashboard
- Search trips
- Trip results
- Seat selection
- Booking confirmation
- My bookings
- Booking details
- Track trip
- Notifications
- Complaints
- Profile

### Operator

- Dashboard
- Vehicles
- Vehicle create/edit
- Drivers
- Trips
- Trip create/edit
- Bookings
- Reports

### Government

- Dashboard
- Government fleet
- Vehicles
- Drivers
- Routes
- Bus stops
- Trips
- Operators
- Complaints
- Alerts
- Analytics

---

## 14. UI Direction

Use a clean, professional government/transportation interface.

Brand:
- Red
- Yellow
- White
- Dark neutral

Typography:
- Poppins for headings
- Inter for body text

Prioritize:
- Mobile-first passenger experience
- Responsive dashboards
- Clear status badges
- Accessible buttons/forms
- Map/trip information
- Minimal clutter

---

## 15. Security Requirements

Even for an MVP, implement:

- CSRF protection
- Password hashing through Django authentication
- Login-required views
- Role-based permissions
- Object-level access checks
- Operator data isolation
- Server-side validation
- Secure environment variables
- No hard-coded secrets
- Database constraints
- Audit-friendly timestamps

Never trust the role supplied by the browser.

Permissions must be enforced server-side.

---

## 16. Prototype Data

Seed realistic mock data.

Example:

### Organizations

- Abia State Transport
- ABC Transport
- XYZ Transport

### Route

`Umuahia → Umudike → Isiala Ngwa → Osisioma → Aba`

### Vehicles

- ABIA-024
- ABIA-025
- ABC-101
- XYZ-201

### Trips

- 8:00 AM
- 10:30 AM
- 2:30 PM
- 5:00 PM

### Passengers

Create several test accounts.

### Bookings

Seed bookings to make analytics meaningful.

---

## 17. Implementation Order

Build in this order.

### Phase 1 — Project setup

1. Create Django project.
2. Create custom User model.
3. Configure PostgreSQL.
4. Configure templates/static files.
5. Configure environment variables.
6. Create base layout.

### Phase 2 — Accounts

7. Login
8. Logout
9. Passenger registration
10. Role-based dashboards
11. Permission decorators/mixins

### Phase 3 — Transport data

12. Organization model
13. BusStop
14. Route
15. RouteStop
16. Vehicle
17. Seat
18. DriverProfile
19. Admin configuration

### Phase 4 — Trips

20. Trip model
21. Trip creation
22. Trip status
23. Vehicle/driver assignment
24. Passenger trip search

### Phase 5 — Fare engine

25. FareBand model
26. Distance calculation
27. Fare calculation service
28. Fare display

### Phase 6 — Booking

29. Seat map
30. Booking creation
31. Booking reference
32. Booking history
33. Cancellation
34. Concurrency protection

### Phase 7 — Tracking

35. Trip tracking page
36. Simulated vehicle movement
37. Stop progression
38. ETA/status display

### Phase 8 — Dashboards

39. Passenger dashboard
40. Operator dashboard
41. Government dashboard
42. Occupancy analytics
43. Route analytics

### Phase 9 — Communication

44. Notifications
45. Transport alerts
46. Complaints

### Phase 10 — Testing/polish

47. Permission tests
48. Booking tests
49. Fare tests
50. UI responsiveness
51. Seed/demo data
52. Deployment preparation

---

## 18. What NOT to build in the first sprint

Do not start with:

- Real GPS hardware
- Real government API integrations
- Transport-card integration
- SMS gateway
- Complex payment processing
- AI predictions
- Full mobile app
- Advanced route optimization

The MVP should first prove the **core transportation workflow**.

---

## 19. Definition of Done for MVP

The MVP is successful when you can demonstrate this complete scenario:

1. Government creates a route.
2. Government adds bus stops.
3. Government registers a bus.
4. Government adds a driver.
5. Government creates a trip.
6. Passenger logs in.
7. Passenger searches the route.
8. Passenger selects boarding and destination stops.
9. System calculates the fare.
10. Passenger selects a seat.
11. Passenger books.
12. Seat becomes unavailable.
13. Booking reference is generated.
14. Passenger sees the trip in My Bookings.
15. Tracking simulation shows trip progress.
16. Passenger receives status notifications.
17. Passenger can cancel an eligible booking.
18. Seat becomes available again.
19. Government dashboard reflects trip/booking/occupancy information.
20. Operator can manage its own resources without accessing another operator's data.

If these 20 steps work reliably, you have a strong MVP.

---

## 20. Future Vision

After validating the MVP with users and stakeholders, Abia Transit can evolve toward:

- Real-time GPS
- Mobile applications
- Online payments
- Transport-card integration
- Digital wallet
- SMS notifications
- Operator verification
- Government fleet telemetry
- Advanced analytics
- Demand forecasting
- Traffic/road-condition integration
- Open APIs for approved government systems
- More routes and operators across Abia

These are expansion paths, not MVP requirements.

---

## 21. Final Product Definition

### Short version

> **Abia Transit is a Django-based digital mobility platform that connects passengers, government-owned transportation and participating private operators through routes, bus stops, trips, bookings, fares, tracking and transportation analytics.**

### Core value

**Passenger:** better information and predictable travel.

**Operator:** better digital operations.

**Government:** better visibility and data for transport management and planning.

### Core differentiator

> **One digital network, distributed physical access.**

### Core philosophy

> **Digitize the existing transportation system rather than trying to replace it.**
