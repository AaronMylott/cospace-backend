# Pagination Verification

Verified `GET /bookings` pagination behavior through the controller.

| Request query | Status | Data length | Meta |
| --- | --- | --- | --- |
| `?page=1&limit=2` | `200` | `2` | `{ "page": 1, "limit": 2, "total": 3, "totalPages": 2 }` |
| `?page=-3&limit=0` | `200` | `1` | `{ "page": 1, "limit": 1, "total": 3, "totalPages": 3 }` |

The second case confirms request-level minimum constraints for both `page` and `limit`.
