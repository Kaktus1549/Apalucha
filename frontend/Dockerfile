FROM node:current-slim

WORKDIR /usr/src/app

COPY . .

RUN npm install -g bun

RUN bun install 

RUN bun run build

EXPOSE 3000 

CMD ["bun", "run", "start"]