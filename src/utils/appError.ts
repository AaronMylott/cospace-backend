import HTTP_STATUS from "../constants/httpStatus";

export class AppError extends Error {
	readonly status: "fail" | "error";
	readonly isOperational = true;

	constructor(
		message: string,
		readonly statusCode: number,
	) {
		super(message);
		this.status = statusCode >= HTTP_STATUS.BAD_REQUEST && statusCode < HTTP_STATUS.INTERNAL_SERVER_ERROR
			? "fail"
			: "error";

		Error.captureStackTrace(this, this.constructor);
		Object.setPrototypeOf(this, new.target.prototype);
	}
}
