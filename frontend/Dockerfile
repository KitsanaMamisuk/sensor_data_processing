FROM node:22-alpine

# # Change Timezone to GMT+7
ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Location of source code
ENV PROJECT_ROOT /opt/app
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

# Installing packages
COPY ./package.json .
COPY ./package-lock.json .
RUN npm install

COPY ./src /opt/app/src
COPY ./public /opt/app/public
COPY ./env.d.ts .
COPY ./index.html .
COPY ./tsconfig.json .
COPY ./tsconfig.app.json .
COPY ./tsconfig.node.json .
COPY ./vite.config.ts .


# Build the application
RUN npm run build-only