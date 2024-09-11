from website import create_app

app = create_app()

#used to run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)