import os

if os.environ.get("HECTIQLAB_ENV")=="dev":
	server_url = "http://0.0.0.0:8080"
	app_url = "http://0.0.0.0:3000"
elif os.environ.get("HECTIQLAB_ENV")=="staging":
	server_url = " https://api.staging.lab.hectiq.ai"
	app_url = " https://lab-staging.hectiq.ai"
else:
	server_url = "https://api.lab.hectiq.ai"
	app_url = "https://lab.hectiq.ai"