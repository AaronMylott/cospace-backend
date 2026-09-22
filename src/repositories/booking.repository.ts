export interface Booking {
	id: string;
	desk: string;
	floor: number;
	date: string;
	active: boolean;
}

export class BookingRepository {
	private bookings: Booking[] = [
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

	findAll(): Booking[] {
        console.log("Repository: findAll called");
		return this.bookings;
	}

	findById(id: string): Booking | undefined {
		return this.bookings.find((booking) => booking.id === id);
	}

	create(booking: Booking): Booking {
		this.bookings.push(booking);
		return booking;
	}

	update(id: string, data: Partial<Booking>): Booking | undefined {
		const bookingIndex = this.bookings.findIndex((booking) => booking.id === id);
		const booking = this.bookings[bookingIndex];

		if (bookingIndex === -1 || !booking) {
			return undefined;
		}

		this.bookings[bookingIndex] = { ...booking, ...data, id };
		return this.bookings[bookingIndex];
	}

	delete(id: string): boolean {
		const bookingIndex = this.bookings.findIndex((booking) => booking.id === id);

		if (bookingIndex === -1) {
			return false;
		}

		this.bookings.splice(bookingIndex, 1);
		return true;
	}
}
