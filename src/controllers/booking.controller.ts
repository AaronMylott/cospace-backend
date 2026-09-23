import { Request, Response } from "express";
import { BookingService } from "../services/booking.service";
import { Booking } from "../schemas/booking.schema";

export class BookingController {
	private readonly service: BookingService;

	constructor(service?: BookingService) {
		this.service = service ?? new BookingService();
	}

	getAll = (request: Request, response: Response): void => {
		try {
			const pageParsed = parseInt(request.query.page as string, 10);
			const limitParsed = parseInt(request.query.limit as string, 10);

			const page = Math.max(1, Number.isNaN(pageParsed) ? 1 : pageParsed);
			const limit = Math.max(1, Number.isNaN(limitParsed) ? 10 : limitParsed);
			const safeLimit = Math.min(limit, 50);
			response.status(200).json(this.service.getPaginatedShifts(page, safeLimit));
		} catch {
			response.status(500).json({ message: "Unable to retrieve bookings" });
		}
	};

	getById = (request: Request<{ id: string }>, response: Response): void => {
		try {
			const booking = this.service.findById(request.params.id);

			if (!booking) {
				response.status(404).json({ message: "Booking not found" });
				return;
			}

			response.status(200).json(booking);
		} catch {
			response.status(500).json({ message: "Unable to retrieve booking" });
		}
	};

	create = (request: Request<{}, {}, Booking>, response: Response): void => {
		try {
			const booking = this.service.create(request.body);
			response.status(201).json(booking);
		} catch (error) {
			const message = error instanceof Error ? error.message : "Invalid booking";
			response.status(400).json({ message });
		}
	};

	update = (
		request: Request<{ id: string }, {}, Partial<Booking>>,
		response: Response,
	): void => {
		try {
			const booking = this.service.update(request.params.id, request.body);

			if (!booking) {
				response.status(404).json({ message: "Booking not found" });
				return;
			}

			response.status(200).json(booking);
		} catch {
			response.status(500).json({ message: "Unable to update booking" });
		}
	};

	patch = (request: Request<{ id: string }>, response: Response): void => {
		try {
			const booking = this.service.toggleActive(request.params.id);

			if (!booking) {
				response.status(404).json({ message: "Booking not found" });
				return;
			}

			response.status(200).json(booking);
		} catch {
			response.status(500).json({ message: "Unable to update booking" });
		}
	};

	delete = (request: Request<{ id: string }>, response: Response): void => {
		try {
			const deleted = this.service.delete(request.params.id);

			if (!deleted) {
				response.status(404).json({ message: "Booking not found" });
				return;
			}

			response.status(204).send();
		} catch {
			response.status(500).json({ message: "Unable to delete booking" });
		}
	};
}
