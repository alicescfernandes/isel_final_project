source venv/Scripts/activate
# loads dev env into the shell
export $(grep -v '^#' ./infra/.env.dev | xargs)

cd backend
python manage.py makemigrations