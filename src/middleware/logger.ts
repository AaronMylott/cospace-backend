import { RequestHandler, Request, Response, NextFunction } from "express";

const logger: RequestHandler = (request: Request, _response: Response, next: NextFunction) => {
	console.log(`${new Date().toISOString()} ${request.method} ${request.originalUrl}`);
	next();
};

export default logger;
