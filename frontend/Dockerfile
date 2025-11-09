FROM node:20-alpine AS build
WORKDIR /app

# Copy package files first for better caching
COPY package.json ./
RUN npm install || npm ci

# Copy all frontend files
COPY . .

# Ensure index.html exists - create if missing
RUN if [ ! -f index.html ]; then \
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/><title>CyberSathi Admin</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>' > index.html; \
    fi

# Build the app
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Add nginx config for React Router
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]