from forumFlask import create_app


app = create_app()

#just run as python xxx
if __name__ == '__main__':
    app.run(debug=1)