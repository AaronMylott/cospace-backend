import { Request, Response, Router } from "express";

const router = Router();

export interface Booking {
	id: string;
	desk: string;
	floor: number;
	date: string;
	active: boolean;
}

export const bookings: Booking[] = [
	{
		id: "1",
		desk: "A-101",
		floor: 1,
		date: "2026-09-23",
		active: true,
	},
	{
		id: "2",
		desk: "B-204",
		floor: 2,
		date: "2026-09-24",
		active: true,
	},
	{
		id: "3",
		desk: "C-305",
		floor: 3,
		date: "2026-09-25",
		active: false,
	},
];

router.get("/", (_req: Request, res: Response) => {
	res.status(200).json(bookings);
});

router.get("/:id", (req: Request<{ id: string }>, res: Response) => {
	const booking = bookings.find((booking) => booking?.id === req.params.id);

	if (!booking) {
		res.status(404).json({ message: "Booking not found" });
		return;
	}

	res.status(200).json(booking);
});

router.post("/", (req: Request<{}, {}, Booking>, res: Response) => {
	const newBooking = req.body;
	bookings.push(newBooking);

	res.status(201).json(newBooking);
});

router.put("/:id", (req: Request<{ id: string }, {}, Booking>, res: Response) => {
	const bookingIndex = bookings.findIndex((booking) => booking?.id === req.params.id);

	if (bookingIndex === -1) {
		res.status(404).json({ message: "Booking not found" });
		return;
	}

	bookings[bookingIndex] = req.body;
	res.status(200).json(bookings[bookingIndex]);
});

router.patch("/:id", (req: Request<{ id: string }, {}, Partial<Booking>>, res: Response) => {
	const bookingIndex = bookings.findIndex((booking) => booking?.id === req.params.id);

	if (bookingIndex === -1) {
		res.status(404).json({ message: "Booking not found" });
		return;
	}

	const booking = bookings[bookingIndex];
	if (!booking) {
		res.status(404).json({ message: "Booking not found" });
		return;
	}

	booking.active = !booking.active;
	res.status(200).json(booking);
});

router.delete("/:id", (req: Request<{ id: string }>, res: Response) => {
	const bookingIndex = bookings.findIndex((booking) => booking?.id === req.params.id);

	if (bookingIndex === -1) {
		res.status(404).json({ message: "Booking not found" });
		return;
	}

	bookings.splice(bookingIndex, 1);
	res.status(204).send();
});

export default router;