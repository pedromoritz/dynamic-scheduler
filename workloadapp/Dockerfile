FROM node:18.12.1-alpine3.16
WORKDIR /usr/src/app
COPY package*.json .
COPY app.js .
RUN npm install -g npm@9.1.2
RUN npm install
EXPOSE 3000
CMD [ "npm", "start" ]
