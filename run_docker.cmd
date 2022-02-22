if not exist data\token.txt (
    echo "No token file found in 'data\token.txt'"
    exit /b 1
)

set /P TOKEN=<data\token.txt
docker run -dv plates-bot-data:/bot/data -e "TOKEN=%TOKEN%" bot