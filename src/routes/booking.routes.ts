import { NextFunction, Request, Response, Router } from "express";
import { BookingController } from "../controllers/booking.controller";
import { Booking, createBookingSchema } from "../schemas/booking.schema";
import auth from "../middleware/auth";
import validateSchema from "../middleware/validate";

const router = Router();
const bookingController = new BookingController();

router.get("/", (req: Request, res: Response, next: NextFunction) =>
	bookingController.getAll(req, res, next),
);
router.get("/:id", auth, (req: Request<{ id: string }>, res: Response, next: NextFunction) =>
	bookingController.getById(req, res, next),
);
router.post(
	"/",
	auth,
	validateSchema(createBookingSchema),
	(req: Request<{}, {}, Booking>, res: Response, next: NextFunction) =>
		bookingController.create(req, res, next),
);
router.put(
	"/:id",
	auth,
	(req: Request<{ id: string }, {}, Partial<Booking>>, res: Response, next: NextFunction) =>
		bookingController.update(req, res, next),
);
router.patch("/:id", auth, (req: Request<{ id: string }>, res: Response, next: NextFunction) =>
	bookingController.patch(req, res, next),
);
router.delete("/:id", auth, (req: Request<{ id: string }>, res: Response, next: NextFunction) =>
	bookingController.delete(req, res, next),
);

export default router;