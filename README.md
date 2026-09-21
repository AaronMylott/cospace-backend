# CoSpace Backend

Backend repository for CoSpace, a workspace booking platform designed to support hybrid working through the management of desks, bookings, and users.

## Overview

This repository currently contains the database layer for the CoSpace application, including SQL migration scripts, seed data, and supporting documentation.

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

Contains project documentation, design notes, and planning materials.

### migrations/

Contains SQL migration scripts used to create and update the database schema.

### scripts/

Contains utility scripts such as `seed.sql`, which populates the database with sample data.

### server.js

Placeholder entry point for future backend server configuration.

### users.js

Placeholder file for future user-related functionality.

## Technology Stack

- SQL
- MySQL Server
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
- MySQL Server
- MySQL Workbench

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AaronMylott/cospace-backend.git
cd cospace-backend
```

### 2. Create the Database

Create a new schema in MySQL Workbench.

### 3. Run the Migration Scripts

Execute the SQL migration files located in the `migrations` folder in numerical order.

### 4. Load Sample Data

Run the `seed.sql` script located in the `scripts` folder to populate the database with sample data.

## Running the Project

The backend application is currently under development.

At present, the repository contains:

- Database migrations
- Seed data
- Project documentation
- Initial backend structure

Once backend functionality has been implemented, the project will be started using:

```bash
npm install
npm start
```

## Current Features

- Database schema management
- SQL migration scripts
- Seed data scripts
- Technical documentation
- Version control using Git and GitHub

## Roadmap

### Completed 

- Repository setup
- Database schema design
- Migration scripts
- Seed data script
- Technical documentation

### Planned 

- Express server configuration
- Database connectivity
- User management endpoints
- Desk management endpoints
- Booking endpoints
- Authentication and authorisation
- Input validation
- Automated testing

## Author

Aaron Mylott
