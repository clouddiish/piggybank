FROM node:22.16.0

WORKDIR /frontend
COPY package.json .
COPY package-lock.json .
RUN npm install

COPY public ./public
COPY src ./src 

EXPOSE 3000

CMD ["npm", "start"]