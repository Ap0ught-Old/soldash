<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>Solr Dashboard</title>
        ${self.head_css()}
        ${self.head_js()}
    </head>
    <body>
        <div id="header">
            ${self.body_header()}
        </div>
        <div id="page_container">
            ${self.body_content()}
        </div>
        <div id="footer">
            ${self.body_footer()}
        </div>
        ${self.footer_js()}
        <img src="${url_for('static', filename='images/throbber.gif')}" style="display:none;"/>
    </body>
</html>

<%def name="head_css()">
    <link rel="stylesheet" type="text/css" href="${url_for('static', filename='css/base.css')}" />
    <link rel="stylesheet" type="text/css" href="${url_for('static', filename='css/basicmodal/basic.css')}" />
</%def>

<%def name="head_js()">
</%def>

<%def name="body_header()">
    <h1>Soldash</h1>
</%def>

<%def name="body_content()">
</%def>

<%def name="body_footer()">
    <hr/>
    <div class="left">
        <span class="countdown"></span>
    </div>
    <div class="right">
        Powered by <a href="http://flask.pocoo.org" target="_new">flask</a> and <a href="https://github.com/tzellman/flask-mako" target="_new">flask-mako</a>.
    </div>
</%def>

<%def name="footer_js()">
    <script src="${url_for('static', filename='js/jquery-1.8.2.min.js')}"></script>
    <script src="${url_for('static', filename='js/jquery.throbber.js')}"></script>
    <script src="${url_for('static', filename='js/jquery.simplemodal.1.4.3.min.js')}"></script>
    <script src="${url_for('static', filename='js/base.js')}"></script>
</%def>