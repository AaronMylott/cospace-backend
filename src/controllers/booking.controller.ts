import { NextFunction, Request, Response } from "express";
import HTTP_STATUS from "../constants/httpStatus";
import { NotFoundError } from "../errors/notFoundError";
import { BookingService } from "../services/booking.service";
import { Booking } from "../schemas/booking.schema";

export class BookingController {
	private readonly service: BookingService;

	constructor(service?: BookingService) {
		this.service = service ?? new BookingService();
	}

	getAll = (request: Request, response: Response, next: NextFunction): void => {
		try {
			const pageParsed = parseInt(request.query.page as string, 10);
			const limitParsed = parseInt(request.query.limit as string, 10);

			const page = Math.max(1, Number.isNaN(pageParsed) ? 1 : pageParsed);
			const limit = Math.max(1, Number.isNaN(limitParsed) ? 10 : limitParsed);
			const safeLimit = Math.min(limit, 50);
			response.status(HTTP_STATUS.OK).json(this.service.getPaginatedShifts(page, safeLimit));
		} catch (error) {
			next(error);
		}
	};

	getById = (request: Request<{ id: string }>, response: Response, next: NextFunction): void => {
		try {
			const booking = this.service.findById(request.params.id);

			if (!booking) {
				next(new NotFoundError("Booking not found"));
				return;
			}

			response.status(HTTP_STATUS.OK).json(booking);
		} catch (error) {
			next(error);
		}
	};

	create = (request: Request<{}, {}, Booking>, response: Response, next: NextFunction): void => {
		try {
			const booking = this.service.create(request.body);
			response.status(HTTP_STATUS.CREATED).json(booking);
		} catch (error) {
			next(error);
		}
	};

	update = (
		request: Request<{ id: string }, {}, Partial<Booking>>,
		response: Response,
		next: NextFunction,
	): void => {
		try {
			const booking = this.service.update(request.params.id, request.body);

			if (!booking) {
				next(new NotFoundError("Booking not found"));
				return;
			}

			response.status(HTTP_STATUS.OK).json(booking);
		} catch (error) {
			next(error);
		}
	};

	patch = (request: Request<{ id: string }>, response: Response, next: NextFunction): void => {
		try {
			const booking = this.service.toggleActive(request.params.id);

			if (!booking) {
				next(new NotFoundError("Booking not found"));
				return;
			}

			response.status(HTTP_STATUS.OK).json(booking);
		} catch (error) {
			next(error);
		}
	};

	delete = (request: Request<{ id: string }>, response: Response, next: NextFunction): void => {
		try {
			const deleted = this.service.delete(request.params.id);

			if (!deleted) {
				next(new NotFoundError("Booking not found"));
				return;
			}

			response.status(HTTP_STATUS.NO_CONTENT).send();
		} catch (error) {
			next(error);
		}
	};
}
