FROM node:18.12.0-alpine3.16
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY app.js .
EXPOSE 3000
CMD [ "node", "--max-old-space-size=8192", "--expose_gc", "app.js" ]
