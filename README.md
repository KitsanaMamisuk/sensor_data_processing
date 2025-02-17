# sensor_data_processing

# Requirements

* docker >= 27.4.0
* docker-compose >= 1.27.4
* Node.js >= 18.12.0 (minimum 16.13.0)

# Setup Project (First time only)
1. Setup Minio for testing S3/Wasabi in local
   * https://docs.google.com/document/d/1jsamOyJsjq6mv7S7sOExrAaN38AmYx8N8hUU-GkHHJw/edit

1. cd to root of project
   ```
   cd <to root of project>
   ```

1. Clone sub-module project
   ```
   git config submodule.backend/core.url git@gitlab.c0d1um.io:products/e-memo/standard/memo-core-iv.git
   git submodule update --init --recursive 
   cd ./backend/core
   git fetch
   ```

1. Build
   ```
   make build-backend
   make build-frontend
   ```

1. Init DB
   ```
   make reset-init-db
   ```

# Run Project

1. cd to root of project
   ```
   cd <to root of project>
   ```
1. Run
   ```
   make run-backend
   ```
1. Open another terminal, run
   ```
   make run-frontend
   ```
1. Open another terminal, run
   ```
   make run-celery
   ```

# Accounts

* Initial User
  ```
  * Master Admin
    username: master
    password: X2X.Xfk>>ZE!y/x!
  
  * Admin
    username: admin
    password: memo
  
  * IT
    username: it
    password: memo
  
  * User
    username: test_user
    password: memo
  ```
* DB
  * url `localhost:5432`
  * database: standard
  * username: postgres
  * password: Codium123!
* Local URL: 
  * site 1: `http://localhost:4200`, backend url: `localhost:8000/api`
  * site 2: `http://127.0.0.1:4200`, backend url: `127.0.0.1:8000/api`
* Dev URL: 
  * site1: `https://site1.dev.memo.codium.co/`
  * site2: `https://site2.dev.memo.codium.co/`

# Miscellaneous Tools
## Reset DB

```
make reset-init-db
```

## Run unit test

```
make coverage
```

## SSH to dev server

1. download key from https://gitlab.c0d1um.io/internal/support/server-hardening/-/blob/master/keys/122.8.155.57.pem
1. run this command
   ```
   chmod 700 122.8.155.57.pem
   ssh -p 22222 -i 122.8.155.57.pem ubuntu@122.8.155.57
   ```
## SSH to production server
1. download key from https://gitlab.c0d1um.io/internal/support/server-hardening/-/blob/master/keys/110.238.119.127.pem
1. run this command
   ```
   ssh -p 22222 -i 110.238.119.127.pem ubuntu@110.238.119.127
   ```

## Run sonar scanner in your local computer
 1. Install SonarScanner by download from https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
 1. Extract .zip that downloaded from 1.
 1. Add sonar-scanner to your path by typing `sudo vi /etc/paths` and append path that you extracted .zip/bin 
    Example:
    ```
    /Users/bonus/sonar-scanner-4.2.0.1873/bin/
    ```
 1. Run SonarQube for web interface by typing (Should wait for awhile until it finishing setup and make sure not run another Postgres in another location)
    ```
    docker stop sonarqube
    docker rm sonarqube
    docker run -d --name sonarqube -p 9000:9000 -p 9092:9092 sonarqube:7.8-community
    ```
 1. Set environment, run command
    ```
    SONAR_HOST_URL='http://localhost:9000'
    CI_COMMIT_SHORT_SHA='1'
    CI_COMMIT_BRANCH='local'
    SONAR_TOKEN='admin'
    SONAR_PASSWORD='admin'
    QUALITY_GATE_WAIT='false'
    ```
 1. Run scanner
    ```
    cd <root project>/backend && sonar-scanner
    cd <root project>/frontend/src && sonar-scanner
    ```

# Test scan image in local
* run `brew install aquasecurity/trivy/trivy`
* download html template from https://github.com/aquasecurity/trivy/blob/main/contrib/html.tpl
```
# test scan
trivy image --cache-dir /tmp/trivycache/ --severity HIGH,CRITICAL --ignore-unfixed --format template --template "@/___PATH_TO_HTML_TEMAPLTE___" -o report.html ____YOUR_IMAGE_NAME_HERE____

# Example
trivy image --cache-dir /tmp/trivycache/ --severity HIGH,CRITICAL --ignore-unfixed --format template --template "@/home/trivy_html.tpl" -o report.html  general-memo-standard-django
```
