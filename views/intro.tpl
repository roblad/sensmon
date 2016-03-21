
  <!--
    <div class="row" style="text-align:center;">
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading ">Jakość powietrza</div>
      <div class="panel-body">
        <h1 class="text-primary">{% raw aqi['title'] %}</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Ciśnienie</div>
      <div class="panel-body">
        <h1 class="text-primary">None</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Wilgotość</div>
      <div class="panel-body">
        <h1 class="text-primary">None</h1>
      </div>
    </div>
   </div>
  -->
{% extends "base.tpl" %}
{% block title %}Intro{% end %}

{% block content %}

<!--h1 class="page-header">Pogoda dom<!--small>Odczyty z czujników</small--></h1 -->

  
<!-- tu wykomentowane -->  

  </div>

  <div class="row">
  <div class="weather">
    
	<div><h1><b>Stanisławów Pierwszy</b></h1></div>
	{% for list in w['list'] %}
  
	<div class="col-sm-2">
      <div class="panel panel-success">
        <div class="panel-heading"><b>{{! {% raw list['dt'] %}|dayOfweekPL|capitalize}}</b></div>
          <div class="panel-body">
            {% for weather in list['weather'] %}
              <i class="owf owf-{% raw weather['id'] %} owf-5x"></i>
              <p style="text-transform: capitalize;"><b>{% raw weather['description'] %}</b></p>
			  
      {% end %}
	  <li><b>
	  Temperatura min:
	  </b></li>
      {% raw list['temp']['min']%}°C 
	  <li><b>
	  Temperatura max.:
	  </b></li>
	  {% raw list['temp']['max']%}°C 
      <li><b>
	  Wilgotność:
	  </b></li>
	  {% raw list['humidity'] %} %
      <li><b>
	  Ciśnienie: 
	  </b></li>
	  {% raw list['pressure'] %} hPa
      <li><b>
	  Prędkość wiatru:
	  </b></li>
	  {% raw list['speed'] %} km/h
	  


	  </div>
    </div>
    </div>
    {% end %}
</div>
</div>
<!-- /div -->
{% end %}