import { AppError } from "../utils/appError";
import HTTP_STATUS from "../constants/httpStatus";

export class NotFoundError extends AppError {
	constructor(message = "Not Found") {
		super(message, HTTP_STATUS.NOT_FOUND);
	}
}
