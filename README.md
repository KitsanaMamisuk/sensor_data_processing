# sensor_data_processing
# Requirements

* docker >= 20.10.2
* docker-compose >= 2.31.0
* Node.js >= 22.12.0

# Setup Project 
1. Build
   ```
   make build-backend
   make build-frontend
   ```

2. Init DB
   ```
   make reset-db
   ```

# Run Project

1. cd to root of project
   ```
   cd <to root of project>
   ```
2. Run
   ```
   make run-backend
   ```
3. Open another terminal, run
   ```
   make run-frontend
   ```

# Optional step

# Run all services

1. Run
   ```
   make up
   ```


# Down all services

1. Run
   ```
   make down
   ```

# Migrations 

1. Run
   ```
   make migrations
   ```

# Migrate 

1. Run
   ```
   make migrate
   ```
