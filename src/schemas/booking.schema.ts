import { z } from "zod";

export const createBookingSchema = z.object({
	id: z.string().min(1),
	desk: z.string().trim().min(3).max(100),
	floor: z.string().trim().min(5).max(200),
	date: z.iso.date(),
	active: z.boolean().default(true),
});

export type Booking = z.infer<typeof createBookingSchema>;
