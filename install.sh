#!/bin/bash

clear
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="

echo "Welcome to the Apalucha 2024 installation script!"
echo "This script will guide you through the installation process."
echo "Please make sure you have Docker and Docker Compose installed. If you want leave default values, just press Enter."
echo ""

echo "Database configuration"
echo "----------------------"
echo ""

# Prompt for environment variables
read -p "Enter database user (default: apalucha): " DATABASE_USER
DATABASE_USER=${DATABASE_USER:-apalucha} # Default value if none provided
read -p "Enter database password: (default: jkklf84ZZFaIkcula#_??) " DATABASE_PASSWORD
DATABASE_PASSWORD=${DATABASE_PASSWORD:-jkklf84ZZFaIkcula#_??} # Default value if none provided
read -p "Enter pool size (default: 20): " POOL_SIZE
POOL_SIZE=${POOL_SIZE:-20} # Default value if none provided
read -p "Enter database port (default: 3306): " DATABASE_PORT
DATABASE_PORT=${DATABASE_PORT:-3306} # Default value if none provided

clear
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="

echo "Backend configuration"
echo "----------------------"
echo ""

read -p "Enter JWT secret: " JWT_SECRET
read -p "Enter JWT expiration time in days (default: 10): " JWT_EXPIRATION
JWT_EXPIRATION=${JWT_EXPIRATION:-10} # Default value if none provided
read -p "Enter JWT issuer (default: https://apalucha.kaktusgame.eu): " JWT_ISSUER
JWT_ISSUER=${JWT_ISSUER:-https://apalucha.kaktusgame.eu} # Default value if none provided
read -p "Enter PDF login URL (default: https://apalucha.kaktusgame.eu/login): " PDF_LOGIN_URL

clear
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="
echo "Login and vote configuration"
echo "----------------------"

PDF_LOGIN_URL=${PDF_LOGIN_URL:-https://apalucha.kaktusgame.eu/login} # Default value if none provided
read -p "Enter PDF URL (default: https://apalucha.kaktusgame.eu/pdf): " PDF_URL
PDF_URL=${PDF_URL:-https://apalucha.kaktusgame.eu/pdf} # Default value if none provided
read -p "Enter vote duration in seconds (default: 180): " VOTE_DURATION
VOTE_DURATION=${VOTE_DURATION:-180} # Default value if none provided

clear
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="
echo "Backend configuration"
echo "----------------------"
echo ""

read -p "Enter web port (default: 5000): " DOCKER_WEB_PORT
DOCKER_WEB_PORT=${DOCKER_WEB_PORT:-5000} # Default value if none provided
read -p "Is debug mode on? (true/false, default: false): " DEBUG
DEBUG=${DEBUG:-false} # Default value if none provided

clear
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="
echo "Frontend and master user configuration"
echo "----------------------"
echo ""

read -p "Enter website URL (default: https://apalucha.kaktusgame.eu): " WEBSITE_URL
WEBSITE_URL=${WEBSITE_URL:-https://apalucha.kaktusgame.eu} # Default value if none provided
read -p "Enter master username: (default: admin) " MASTER_USERNAME
MASTER_USERNAME=${MASTER_USERNAME:-admin} # Default value if none provided
read -p "Enter master password: (default: klfdjlajflculakjfa099_) " MASTER_PASSWORD
MASTER_PASSWORD=${MASTER_PASSWORD:-klfdjlajflculakjfa099_} # Default value if none provided
read -p "Enter frontend port (default: 3000): " DOCKER_FRONTEND_PORT
DOCKER_FRONTEND_PORT=${DOCKER_FRONTEND_PORT:-3000} # Default value if none provided

clear

base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="
echo "Pulling images from Docker Hub..."

# Write environment variables to .env file

cat << EOF > ./backend/.env
DB_PASSWORD=$DATABASE_PASSWORD
DB_USERNAME=$DATABASE_USER
DATABASE_USER=$DATABASE_USER
DATABASE_PASSWORD=$DATABASE_PASSWORD
DATABASE_PORT=$DATABASE_PORT
POOL_SIZE=$POOL_SIZE
MASTER_USERNAME=$MASTER_USERNAME
MASTER_PASSWORD=$MASTER_PASSWORD
JWT_SECRET=$JWT_SECRET
JWT_EXPIRATION=$JWT_EXPIRATION
JWT_ISSUER=$JWT_ISSUER
JWT_ALGORITHM=HS256
PDF_LOGIN_URL=$PDF_LOGIN_URL
PDF_URL=$PDF_URL
VOTE_DURATION=$VOTE_DURATION
DOCKER_WEB_PORT=$DOCKER_WEB_PORT
DEBUG=$DEBUG
EOF

cat << EOF > ./frontend/.env
URL=$WEBSITE_URL
EOF

cd Docker

# Creates .env with environment variables for Docker Compose
cat << EOF > .env
DATABASE_PORT=$DATABASE_PORT
DATABASE_USER=$DATABASE_USER
DATABASE_PASSWORD=$DATABASE_PASSWORD
DOCKER_WEB_PORT=$DOCKER_WEB_PORT
DOCKER_FRONTEND_PORT=$DOCKER_FRONTEND_PORT
EOF

# Run Docker Composer
docker-compose up --build -d