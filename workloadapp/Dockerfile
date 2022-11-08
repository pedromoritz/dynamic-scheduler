FROM node:18.12.0-alpine3.16
WORKDIR /usr/src/app
COPY package*.json .
COPY app.js .
RUN npm install -g npm@8.19.3
RUN npm install
EXPOSE 3000
CMD [ "npm", "start" ]