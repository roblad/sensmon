{% extends "base.tpl" %}
{% block title %}Czujniki{% end %}
{% block content %}
 
 

 

 
 
 <h1 class="page-header">Pomiary dom<small>   odczyt z czujników </small></h1>
 
 
 
    <div class="table-responsive" ng-controller="dashCtrl">

        <table class="table" >
  			<body>
            <tr ng-repeat="(k,v)  in array">
            	<td class="name-node"><h4>{{! v.title}}</h4><h5><i class="fa fa-refresh"></i> {{! v.sensors.timestamp.raw|parsedate }}</h5></td>

            	<td style="text-align:center" ng-repeat="(i,j) in v.sensors|orderBy: i.sensors |nodate  " ng-mouseover="hoverIn()" ng-mouseleave="hoverOut()" 
                    ng-class="{danger: i=='ftank' && j.raw==1 || i=='batvol' && j.raw<3.5 || i=='temp' && j.raw<-10, warning: i=='temp' && j.raw<0 || i=='deszcz' && j.raw==1 || i=='ewob' && j.raw==1 || i=='prad' && j.raw>2 || i=='temp' && j.raw<20|| i=='tgroundhumi' && j.raw>90, success: i=='temp' && j.raw>23 || v.sensors.zdewpoint.raw > v.sensors.tempground.raw }">
                    <div class="info"><h5>{{! j.desc}}</h5><h4 animate-on-change='j.raw'> {{! j.raw }} {{! j.unit}}</h4></div>
                    <div class="menu">
                    <span ng-show="hoverEdit">
					<a href="/graphs/{{! k}}/{{! i}}/week"><i class="fa fa-bar-chart-o"> Wykres</i></a>
                    <a href="/history/{{! k}}/{{! i}}/8h"><i class="fa fa-search""> Historia 8h</i></a>
                    <!-- <a href="/{{! k}}/{{! i}}/action"><i class="fa fa-bolt"></i></a>-->
                     </span>
                </div>
                </td>
            </tr>
		</table>
    </div>





{% end %}
