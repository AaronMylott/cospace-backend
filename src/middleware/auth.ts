import { RequestHandler, Request, Response, NextFunction } from "express";

const auth: RequestHandler = (request: Request, response: Response, next: NextFunction) => {
	const authorization = request.headers.authorization;
	const token = authorization?.startsWith("Bearer ")
		? authorization.slice("Bearer ".length)
		: authorization;

	if (token !== "super-secret-key") {
		response.status(401).json({ message: "Unauthorized" });
		return;
	}

	next();
};

export default auth;
