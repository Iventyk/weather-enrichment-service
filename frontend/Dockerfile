FROM node:24-alpine

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend ./

EXPOSE 4200

CMD ["npm", "start"]
