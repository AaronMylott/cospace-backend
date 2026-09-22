# Express Setup Notes

## Health Check

With the development server running, `curl http://localhost:5000/` returns:

```json
{"status":"active","message":"CoSpace API is running"}
```

## Scaffold Correction

The first scaffold used TypeScript `7.0.2`. That version was incompatible with
the installed `ts-node@10.9.2`, causing `ts-node-dev` to fail while reading the
TypeScript configuration. TypeScript was changed to the compatible `5.9.3`
release line.

## Container Shutdown

The `SIGINT` and `SIGTERM` handlers let the server respond to shutdown signals
and exit cleanly. This matters in a container because orchestrators commonly
send `SIGTERM` during a stop or deployment, giving the application an
opportunity to close resources and finish cleanup before the container exits.

## Git Ignore Confirmation

`node_modules/` is ignored by both the workspace and backend `.gitignore`
files. The backend `.gitignore` also ignores `.DS_Store`, so dependency files
and macOS Finder metadata are not reported as untracked changes.
