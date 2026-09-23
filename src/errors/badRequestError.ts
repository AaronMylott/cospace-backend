import { AppError } from "../utils/appError";
import HTTP_STATUS from "../constants/httpStatus";

export class BadRequestError extends AppError {
	constructor(message = "Bad Request") {
		super(message, HTTP_STATUS.BAD_REQUEST);
	}
}
