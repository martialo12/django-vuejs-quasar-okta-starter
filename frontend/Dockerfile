FROM node:20.10.0-slim AS develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 9005
CMD ["npm", "run", "dev"]
FROM develop-stage as build-stage
RUN npm run build
FROM nginx:1.17.5-alpine as production-stage
COPY django_staticfiles /usr/share/nginx/html
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
COPY .nginx/prod.conf /etc/nginx/nginx.conf
