from Analytics import create_app
app = create_app('../config.py')
app.run(debug=True)