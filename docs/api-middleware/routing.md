# Booking Route Plan

| Method | Path | Payload | Success status |
| --- | --- | --- | --- |
| `GET` | `/bookings` | None | `200 OK` |
| `GET` | `/bookings/:id` | None; `:id` is a string path parameter | `200 OK` |
| `POST` | `/bookings` | Full booking object: `id`, `desk`, `floor`, `date`, `active` | `201 Created` |
| `PUT` | `/bookings/:id` | Full replacement booking object: `id`, `desk`, `floor`, `date`, `active` | `200 OK` |
| `PATCH` | `/bookings/:id` | None; flips the booking's `active` status | `200 OK` |
| `DELETE` | `/bookings/:id` | None; `:id` is a string path parameter | `204 No Content` |
