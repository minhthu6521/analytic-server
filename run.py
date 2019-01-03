from Analytics import create_app

def get_user(current_user):
    app = create_app('../config.py')
    if app.config["PRODUCTION"] is False:
        app.run(debug=True, port=5005)
    else:
        app.run()

get_user()