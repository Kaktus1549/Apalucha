#!/bin/bash

clear
cd backend/
base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="

echo "Welcome to the Apalucha 2024 installation script!"
echo "This script will guide you through the installation process."
echo "Please make sure you have Docker and Docker Compose installed. If you want leave default values, just press Enter."

# Prompt for environment variables
read -p "Enter database user (default: apalucha): " DATABASE_USER
DATABASE_USER=${DATABASE_USER:-apalucha} # Default value if none provided
read -p "Enter database password: (default: jkklf84ZZFaIkcula#_??) " DATABASE_PASSWORD
DATABASE_PASSWORD=${DATABASE_PASSWORD:-jkklf84ZZFaIkcula#_??} # Default value if none provided
read -p "Enter pool size (default: 20): " POOL_SIZE
POOL_SIZE=${POOL_SIZE:-20} # Default value if none provided
read -p "Enter database port (default: 3306): " DATABASE_PORT
DATABASE_PORT=${DATABASE_PORT:-3306} # Default value if none provided
read -p "Enter JWT secret: " JWT_SECRET
read -p "Enter JWT expiration time in days (default: 10): " JWT_EXPIRATION
JWT_EXPIRATION=${JWT_EXPIRATION:-10} # Default value if none provided
read -p "Enter JWT issuer (default: https://apalucha.kaktusgame.eu): " JWT_ISSUER
JWT_ISSUER=${JWT_ISSUER:-https://apalucha.kaktusgame.eu} # Default value if none provided
read -p "Enter PDF login URL (default: https://apalucha.kaktusgame.eu/login): " PDF_LOGIN_URL
PDF_LOGIN_URL=${PDF_LOGIN_URL:-https://apalucha.kaktusgame.eu/login} # Default value if none provided
read -p "Enter PDF URL (default: https://apalucha.kaktusgame.eu/pdf): " PDF_URL
PDF_URL=${PDF_URL:-https://apalucha.kaktusgame.eu/pdf} # Default value if none provided
read -p "Enter vote duration in seconds (default: 180): " VOTE_DURATION
VOTE_DURATION=${VOTE_DURATION:-180} # Default value if none provided
read -p "Enter web port (default: 5000): " DOCKER_WEB_PORT
DOCKER_WEB_PORT=${DOCKER_WEB_PORT:-5000} # Default value if none provided
read -p "Is debug mode on? (true/false, default: false): " DEBUG
DEBUG=${DEBUG:-false} # Default value if none provided

clear

base64 -d <<< "ICAgIF9fXyAgICAgICAgICAgICAgICBfXyAgICAgICAgICAgX18gICAgICAgICAgICAgX19fICAgX19fXyBfX18gIF9fIF9fCiAgIC8gICB8ICBfX19fICBfX19fIF8vIC9fICBfX19fX19fLyAvXyAgX19fXyBfICAgfF9fIFwgLyBfXyBcX18gXC8gLy8gLwogIC8gL3wgfCAvIF9fIFwvIF9fIGAvIC8gLyAvIC8gX19fLyBfXyBcLyBfXyBgLyAgIF9fLyAvLyAvIC8gL18vIC8gLy8gL18KIC8gX19fIHwvIC9fLyAvIC9fLyAvIC8gL18vIC8gL19fLyAvIC8gLyAvXy8gLyAgIC8gX18vLyAvXy8gLyBfXy9fXyAgX18vCi9fLyAgfF8vIC5fX18vXF9fLF8vXy9cX18sXy9cX19fL18vIC9fL1xfXyxfLyAgIC9fX19fL1xfX19fL19fX18vIC9fLyAgIAogICAgICAvXy8gCgo="
echo "Pulling images from Docker Hub..."

# Write environment variables to .env file

cat << EOF > .env
DB_PASSWORD=$DATABASE_PASSWORD
DB_USERNAME=$DATABASE_USER
DATABASE_USER=$DATABASE_USER
DATABASE_PASSWORD=$DATABASE_PASSWORD
DATABASE_PORT=$DATABASE_PORT
POOL_SIZE=$POOL_SIZE
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

# Run Docker Compose
docker-compose up --build -d