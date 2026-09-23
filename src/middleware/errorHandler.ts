import { Request, Response, NextFunction, ErrorRequestHandler } from "express";
import { ZodError } from "zod";

const errorHandler: ErrorRequestHandler = (
	error: unknown,
	_request: Request,
	response: Response,
	_next: NextFunction,
) => {
	if (error instanceof ZodError) {
		return response.status(400).json({
			message: "Validation Error",
			errors: error.issues.map((issue) => ({
				field: issue.path.join("."),
				message: issue.message,
			})),
		});
	}

	const message = error instanceof Error ? error.message : String(error);
	const stack = error instanceof Error ? error.stack : undefined;

	console.error(stack ?? message);

	return response.status(500).json({
		message: "Internal Server Error",
	});
};

export default errorHandler;