FROM node:lts-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install -g npm@8.12.1
RUN npm install
COPY app.js .
EXPOSE 8080
CMD [ "node", "--max-old-space-size=8192", "--expose_gc", "app.js" ]
