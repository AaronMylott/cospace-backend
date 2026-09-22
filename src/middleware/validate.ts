import { RequestHandler, Request, Response, NextFunction } from "express";

export const validate = (requiredFields: string[]): RequestHandler => {
	return (request: Request, response: Response, next: NextFunction) => {
		const body = request.body as Record<string, unknown>;
		const missingFields = requiredFields.filter(
			(field) => body[field] === undefined || body[field] === null,
		);

		if (missingFields.length > 0) {
			response.status(400).json({
				message: "Missing required fields",
				missingFields,
			});
			return;
		}

		next();
	};
};

export default validate;
