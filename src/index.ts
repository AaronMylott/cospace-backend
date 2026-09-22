import express, { Request, Response } from "express";
import bookingRouter from "./routes/bookings";

const app = express();
const port = 5000;

app.use(express.json());

app.use("/bookings", bookingRouter);

app.get("/", (req: Request, res: Response) => {
	res.status(200).json({
		status: "active",
		message: "CoSpace API is running",
	});
});


app.listen(port);

process.on("SIGINT", () => {
	console.log("Server shutting down...");
	process.exit();
});

process.on("SIGTERM", () => {
	console.log("Server shutting down...");
	process.exit();
});

export default app;
