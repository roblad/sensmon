{% extends "base.tpl" %}
{% block title %}Info{% end %}
{% block content %}
    <h1 class="page-header">System <small>Informacje o systemie</small></h1>
    <ul>
        <li><b>System:</b> {{ system }}</li>
        <li><b>Architektura:</b> {{ arch }}</li>
        <li><b>Urządzenie:</b> {{ machine }}</li>

        {% if system == 'Linux' %}
            <li><b>Obciążenie:</b> {{ lavg }}</li>
            <li><b>Czas pracy:</b> {{ uptime }}</li>
            <li><b>Temperatura CPU:</b> {{ cpu_temp }} *C</li>
            
            
        {% end %}
		<div>
		<fieldset>
		<p><li><b>Przekaźniki:</b> 
		<table>
		 <tr>
		   <td <h4><strong>{{ usbrelay_status }}</strong></h4></td>
           
         </tr>
		 
		</table>
		</li></p>
		<br/><br/>
		</fieldset>
		</div>
		
		<div>
		

<p><li><b>Pogoda control:</b> <br/><br/> {{ wheather_status}} <br/><br/></li></p>

        </div>
		
		
    </ul>
{% end %}
<!--<li><b>Pogoda:</b> {{ pogoda_result }}</li> -->