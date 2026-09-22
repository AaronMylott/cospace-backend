import { Request, Response, NextFunction } from "express";  
import { ErrorRequestHandler } from "express";

const errorHandler: ErrorRequestHandler = (error: unknown, _request: Request, response: Response, _next: NextFunction) => {
	const message = error instanceof Error ? error.message : String(error);
	const stack = error instanceof Error ? error.stack : undefined;

	console.error(stack ?? message);
	response.status(500).json({ message: "Internal Server Error" });
};

export default errorHandler;
