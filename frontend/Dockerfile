FROM nginx:alpine

# Remove a página padrão do Nginx

RUN rm -rf /usr/share/nginx/html/*

# Copia o Front-end para o diretório público do Nginx

COPY . /usr/share/nginx/html

# Porta HTTP

EXPOSE 80

# Mantém o Nginx em primeiro plano

CMD ["nginx", "-g", "daemon off;"]
