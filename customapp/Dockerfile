FROM node:lts-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY app.js .
EXPOSE 8080
CMD [ "node", "app.js" ]