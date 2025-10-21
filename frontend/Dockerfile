FROM nginx:alpine

EXPOSE 80

# 1. Copy the main index.html file directly to the Nginx root directory.
# This makes it the default page for the base URL (/).
COPY index.html /usr/share/nginx/html/

# 2. Copy the contents of the 'core' folder into the 'core' subdirectory 
# inside the Nginx web root.
COPY dist/core/ /usr/share/nginx/html/dist/core/

# 3. Copy the other sections into their own subdirectories.
COPY dist/products/ /usr/share/nginx/html/dist/products/
COPY dist/user/ /usr/share/nginx/html/dist/user/