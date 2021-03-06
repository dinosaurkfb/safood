upstream safood_www {
    server 127.0.0.1:9336;
}

server {
    listen 80;
    server_name lc.safood.com;
    client_max_body_size 5M;
	access_log ${base_dir}log/nginx/access.log;
	error_log ${base_dir}log/nginx/error.log;

    location /static/ {
        alias ${base_dir}src/sites/www/static/;
    }

    location / {
        include ${base_dir}etc/nginx/proxy.conf;
        proxy_pass http://safood_www;
    }
}

server {
    listen 80;
    server_name photo.lc.safood.com;
    location / {
        alias ${base_dir}upload/photos/;
    }
}

server {
    listen 80;
    server_name avatar.lc.safood.com;
    location / {
        alias ${base_dir}upload/avatars/;
    }
}
