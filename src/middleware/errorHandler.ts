import { Request, Response, NextFunction, ErrorRequestHandler } from "express";
import HTTP_STATUS from "../constants/httpStatus";
import { AppError } from "../utils/appError";
import { ZodError } from "zod";

type ParserError = Error & {
	status?: number;
	body?: unknown;
};

const isJsonSyntaxError = (error: unknown): error is ParserError => {
	return error instanceof SyntaxError
		&& "body" in error
		&& "status" in error
		&& (error as ParserError).status === HTTP_STATUS.BAD_REQUEST;
};

const errorHandler: ErrorRequestHandler = (
	error: unknown,
	_request: Request,
	response: Response,
	_next: NextFunction,
) => {
	if (error instanceof ZodError) {
		return response.status(HTTP_STATUS.BAD_REQUEST).json({
			message: "Validation Error",
			errors: error.issues.map((issue) => ({
				field: issue.path.join("."),
				message: issue.message,
			})),
		});
	}

	if (error instanceof AppError && error.isOperational) {
		return response.status(error.statusCode).json({
			status: error.status,
			message: error.message,
		});
	}

	if (isJsonSyntaxError(error)) {
		return response.status(HTTP_STATUS.BAD_REQUEST).json({
			status: "fail",
			message: "Invalid JSON payload",
		});
	}

	const message = error instanceof Error ? error.message : String(error);
	const stack = error instanceof Error ? error.stack : undefined;

	console.error(stack ?? message);

	return response.status(HTTP_STATUS.INTERNAL_SERVER_ERROR).json({
		message: "Something went wrong on our end",
	});
};

export default errorHandler;