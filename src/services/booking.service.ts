import { BookingRepository } from "../repositories/booking.repository";
import { Booking } from "../schemas/booking.schema";

interface PaginatedBookings {
	data: Booking[];
	meta: {
		page: number;
		limit: number;
		total: number;
		totalPages: number;
	};
}

export class BookingService {
	private readonly repository: BookingRepository;

	constructor(repository?: BookingRepository) {
		this.repository = repository ?? new BookingRepository();
	}

	findAll(): Booking[] {
		console.log("Service: findAll called");
		return this.repository.findAll();
	}

	findById(id: string): Booking | undefined {
		return this.repository.findById(id);
	}

	getPaginatedShifts(page: number, limit: number): PaginatedBookings {
		const safePage = Math.max(1, page);
		const safeLimit = Math.max(1, limit);
		const skip = (safePage - 1) * safeLimit;
		const total = this.repository.count();
		const totalPages = Math.ceil(total / safeLimit);

		return {
			data: this.repository.findPaginated(skip, safeLimit),
			meta: {
				page: safePage,
				limit: safeLimit,
				total,
				totalPages,
			},
		};
	}

	create(booking: Booking): Booking {
		if (booking.desk.length < 3) {
			throw new Error("Desk name must be at least 3 characters long");
		}

		return this.repository.create(booking);
	}

	update(id: string, data: Partial<Booking>): Booking | undefined {
		const existingBooking = this.repository.findById(id);

		if (!existingBooking) {
			return undefined;
		}

		return this.repository.update(id, data);
	}

	toggleActive(id: string): Booking | undefined {
		const booking = this.repository.findById(id);

		if (!booking) {
			return undefined;
		}

		return this.repository.update(id, { active: !booking.active });
	}

	delete(id: string): boolean {
		const existingBooking = this.repository.findById(id);

		if (!existingBooking) {
			return false;
		}

		return this.repository.delete(id);
	}
}
