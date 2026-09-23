import { AppError } from "../utils/appError";
import HTTP_STATUS from "../constants/httpStatus";

export class UnauthorizedError extends AppError {
	constructor(message = "Unauthorized") {
		super(message, HTTP_STATUS.UNAUTHORIZED);
	}
}
