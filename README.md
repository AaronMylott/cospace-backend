# CoSpace Backend

Backend repository for CoSpace, a workspace booking platform designed to support hybrid working through the management of desks, bookings, rooms, and users.

## Overview

This repository currently contains the database layer for the CoSpace application, including SQL migration scripts, seed data, reporting queries, and supporting documentation.

The backend API has not yet been implemented. `server.js` and supporting JavaScript files are retained as placeholders for future Node.js and Express development.

## Repository Structure

```text
cospace-backend/
├── docs/
├── migrations/
├── scripts/
├── README.md
├── server.js
└── users.js
```

### docs/

Contains project documentation, schema notes, planning materials, and SQL exercises.

### migrations/

Contains SQL migration scripts used to create, update, and roll back the database schema.

### scripts/

Contains utility scripts such as seed data and reporting queries.

### server.js

Placeholder entry point for future backend server configuration.

### users.js

Placeholder file for future user-related functionality.

## Technology Stack

- SQL
- MySQL Server
- MySQL Client
- MySQL Workbench
- JavaScript
- Node.js
- npm
- Git
- GitHub

## Prerequisites

Before using this project, ensure the following software is installed:

- Git
- Node.js
- npm
- MySQL Server 8.x
- MySQL Client or MySQL Workbench

## Database Schema

The schema is made up of five tables:

- `teams` - Organisational teams and departments
- `users` - Colleagues and their optional team assignment
- `desks` - Physical desks and their floor numbers
- `rooms` - Meeting rooms, floors, and capacities
- `bookings` - Desk reservations linked to a user and desk

Foreign key constraints preserve referential integrity throughout the database.

Key relationships include:

- Deleting a user cascades to their bookings
- Deleting a desk cascades to its bookings
- Deleting a team sets related users' `team_id` to `NULL`

Migration `002` introduces a unique constraint on `(desk_id, booking_date)` to prevent multiple bookings for the same desk on the same day.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AaronMylott/cospace-backend.git
cd cospace-backend
```

### 2. Connect to MySQL

Open a terminal and connect to your local MySQL instance:

```bash
mysql -u root -p
```

View existing databases:

```sql
SHOW DATABASES;
```

### 3. Create the Database

Create and select the CoSpace database:

```sql
CREATE DATABASE cospace;
USE cospace;
```

Verify the active database:

```sql
SELECT DATABASE();
```

### 4. Run the Migration Scripts

Apply the migrations in numerical order from the project root:

```sql
SOURCE migrations/001_init_schema.up.sql;
SOURCE migrations/002_add_indexing.up.sql;
```

### 5. Load Sample Data

Load the sample data and reporting queries:

```sql
SOURCE scripts/seed_and_queries.sql;
```

> **Note**
>
> The seed script clears existing data from the database before inserting sample records. It should only be used in a development environment.

### 6. Verify the Setup

Confirm the tables have been created successfully:

```sql
SHOW TABLES;
```

Inspect the sample data:

```sql
SELECT * FROM bookings;
```

The following tables should be present:

- teams
- users
- desks
- rooms
- bookings

## Rolling Back Migrations

To remove the database schema, roll back the migrations in reverse order:

```sql
SOURCE migrations/002_add_indexing.down.sql;
SOURCE migrations/001_init_schema.down.sql;
```

## Running the Project

The backend API is currently under development.

At present, the repository contains:

- Database migrations
- Seed data
- Reporting queries
- Technical documentation
- Initial backend structure

Once backend functionality has been implemented, the application will be started using:

```bash
npm install
npm start
```

## Current Features

- Database schema management
- SQL migration scripts
- Database rollback scripts
- Sample seed data
- Reporting queries
- Referential integrity through foreign keys
- Unique desk booking constraint
- Technical documentation
- Version control using Git and GitHub

## Roadmap

### Completed

- Repository