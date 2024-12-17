FROM node:current-slim

WORKDIR /usr/src/app

COPY . .

RUN npm install -g bun

RUN bun install 

RUN bun run build

RUN groupadd -r frontend && useradd -r -g frontend frontend
RUN chown -R frontend:frontend /usr/src/app
USER frontend

EXPOSE 3000 

CMD ["bun", "run", "start"]