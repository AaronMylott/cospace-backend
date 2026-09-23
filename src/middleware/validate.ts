import { RequestHandler } from "express";
import { ZodSchema, z } from "zod";

export const validateSchema = (schema: ZodSchema): RequestHandler => {
	return (request, response, next) => {
		try {
			request.body = schema.parse(request.body);
			next();
		} catch (error) {
			if (error instanceof z.ZodError) {
				response.status(400).json({
					message: "Validation failed",
					errors: error.issues,
				});
				return;
			}

			next(error);
		}
	};
};

export default validateSchema;
