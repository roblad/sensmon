<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="pl">
<html xmlns:ng="http://angularjs.org" ng-app="sensmon">
<head>
    <base href="/">

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="sensmon - home automation">
    <meta name="author" content="Artur Wronowski">

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/styl.css">
    <link rel="stylesheet" href="/static/plugins/owfont/css/owfont-regular.min.css" type="text/css">
    <link rel="stylesheet" href="http://getbootstrap.com/examples/signin/signin.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <title>{% block title %}{% end %} - Rpi Automation</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <!--[if lte IE 8]>
      <script src="http://cdnjs.cloudflare.com/ajax/libs/json3/3.2.4/json3.min.js"></script>
    <![endif]-->
    <script src="/static/js/jquery.min.js" type="text/javascript"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="/static/js/highstock.src.js" type="text/javascript"></script>
    <script src="/static/js/underscore-min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular-animate.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular-route.js" type="text/javascript"></script>
    <script src="/static/js/highcharts-ng.js" type="text/javascript"></script>
    <script src="http://momentjs.com/downloads/moment-with-locales.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular-moment/0.10.3/angular-moment.js" type="text/javascript"></script>
    <script src="/static/js/require.js" type="text/javascript"></script>
    <script src="/static/js/sensmonjs.js" type="text/javascript"></script>
	<script src="/static/js/sensmonjsbis.js" type="text/javascript"></script>
</head>



    <div class="navbar-header" id="wrapper">
	
        <div class="navbar navbar-inverse navbar-fixed-top navbar-left" role="navigation">
			<div class="container-fluid">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
				
				</div>
				<div class="navbar-collapse collapse">

					<ul class="nav navbar-nav ">
					
						<li target="_self" href="" class="navbar-brand" <a onclick="window.location='http://' + window.location.hostname + ':80'">RPi automation</a></li>
						<li class="active"><a target="_self" href="/">Czujniki</a></li>
						<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Pogoda<span class="caret"></span></a>
                          <ul class="dropdown-menu">
                            <li><a target="_self" href="/intro">Pogoda</a></li>
						    <li> <a target="_self" href="http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IWARSZAW408">Pogoda Szamocin online</a></li>
							<li> <a target="_self" href="http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IWARSZAW117">Pogoda Marki online</a></li>
                          </ul>
                         </li>
						
						<!--<li ng-class="navClass('control')"><a href="/control">Sterowanie</a></li>-->
						<li><a target="_self" href="info">Info</a></li>
		                <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">RPi Automation<span class="caret"></span></a>
                          <ul class="dropdown-menu">
                             <li> <a target="_self" href="http://192.168.100.113/usbrelay2.sh">Przekaźniki</a></li>
                             <li> <a target="_self" href="http://192.168.100.113/cron2.sh">Crontab</a></li>
                             <li> <a target="_self" href="http://192.168.100.113/iradio2.sh">Radio</a></li>
                          </ul>
                         </li>
						<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Kamery<span class="caret"></span></a>
                          <ul class="dropdown-menu">
                             <li> <a target="_self" href="http://192.168.100.150/videostream.cgi?rate=0&user=admin&pwd=admin">Kamera Front</a></li>
						      <li> <a target="_self" href="http://192.168.100.160/web/mobile.html">Kamera Taras</a></li>
                          </ul>
                         </li>
						

					</ul>
					<ul class="nav navbar-nav navbar-right">
						{% if current_user %}
							<li><a target="_self" href="/logout?next={{ url_escape(request.uri) }}">Wyloguj</a></li>
						{% else %}
							<li><a target="_self" href="/login?next={{ url_escape(request.uri) }}">Zaloguj</a></li>
						{% end %}
					</ul>
				</div>
			</div>
        </div>

        <div id="content">
			<div class="container-fluid">
  <h2><div class="container">
   <div class="row">  
    <div class="left"><button type="button" class="btn btn-success btn-sm" data-toggle="collapse" data-target="#zegar">Data Godzina</button> </div>
     <div id="zegar"class="collapse">
       <div class="intro" ng-controller="introCtrl"><div class="date">Dziś jest {{! today(clock) }} </div> <div class="clock">{{! clock | date:'HH:mm:ss'}}</div></div>
     </div>
   </div></h2>
				{% block content %}{% end %}
			</div>
        </div>
	</div>

    {% block scripts %}
    {% end %}
    <!--
     <div class="footer">
   		  <div class="container text-center">
    		<p class="text-muted credit">
    			<a title="Source on Github" href="https://github.com/artekw/sensmon" target="_blank"><i class="fa fa-github fa-2x"></i></a>
    		</p>
  		</div>
 	</div>-->







