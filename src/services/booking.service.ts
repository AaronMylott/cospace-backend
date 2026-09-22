import {
	Booking,
	BookingRepository,
} from "../repositories/booking.repository";

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

	create(booking: Booking): Booking {
		if (booking.desk.length < 3) {
			throw new Error("Desk name must be at least 3 characters long");
		}

		return this.repository.create(booking);
	}

	update(id: string, data: Partial<Booking>): Booking | undefined {
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
		return this.repository.delete(id);
	}
}
