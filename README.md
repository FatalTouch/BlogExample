# Sample Blog Example

This project is a sample blog editor with many features that should be in a standard blog editor. This project is created using Google App Engine with python extension. You can see live example of the project at  
https://blogexample-158011.appspot.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Google account, follow the link to get one.  
https://accounts.google.com/signup

An app engine project on google developer console, follow the link to create one.  
https://console.cloud.google.com/start  

Latest version of python 2, follow the link to download.  
https://www.python.org/downloads/  


### Installing

Install the google cloud sdk, follow the link to download, switch to your environment from the left pane if it's not windows.  
https://cloud.google.com/sdk/docs/quickstart-windows


After downloading, follow the instruction on the quick-start page for your platform to properly initialize the gcloud sdk.

Then run the following command to install the app engine python extension.

```
gcloud components install app-engine-python
```

Now your environment is setup to work on this project.  

Download this project as zip or clone it on your system.  

Open up your terminal and cd to the root directory of the project.

To deploy locally use
```
dev_appserver.py .
```

You can browse the locally deployed project by navigating to module url.  
Default url is ```http://localhost:8080/```


## Deployment



To deploy the configured app engine project in gcloud use.
```
gcloud app deploy
```
and then use ```gcloud app deploy index.yaml``` to deploy our db indexes too because sometimes they don't get deployed by default.

Use ```gcloud app browse``` to browse your project that is deployed on gcloud.


## About the Code

This project uses google app engine along with Jinja2 templating engine to create a website that allows users to register, login, create,edit and delete blog posts, create,edit and delete comments on blogposts and like/unlike blogposts.  

This project also uses some custom client side javascript for validation and ajax requests.

## Built With

* [python](https://www.python.org/) - Main language used by the server side code
* [google app engine](https://cloud.google.com/appengine/docs) - Cloud computing platform
* [jinja2](http://jinja.pocoo.org/) - Templating engine
* [timeago.js](http://timeago.yarp.com/) - A jquery plugin to show relative time
* [bootstrap](http://getbootstrap.com/) - Html, Css and Js framework
* [jquery](https://jquery.com/) - Javascript plugin for Dom manipulation
* [font-awesome](http://fontawesome.io/) - Vector icons

## Contact

If you want to further improve this code, send a pull request or contact me at

contact@mohitmittal.me