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
    </body>
</html>

<%def name="head_css()">
    <link rel="stylesheet" type="text/css" href="${url_for('static', filename='css/base.css')}" />
    <link rel="stylesheet" type="text/css" href="${url_for('static', filename='css/basicmodal/basic.css')}" />
</%def>

<%def name="head_js()">
    <script src="${url_for('static', filename='js/jquery-1.6.4.min.js')}"></script>
    <script src="${url_for('static', filename='js/simplemodal/jquery.simplemodal.js')}"></script>
    <script src="${url_for('static', filename='js/instances_table.js')}"></script>
</%def>

<%def name="body_header()">
    <h1>Soldash</h1>
</%def>

<%def name="body_content()">
</%def>

<%def name="body_footer()">
    <hr/>
    Powered by <a href="http://flask.pocoo.org" target="_new">flask</a> and <a href="https://github.com/tzellman/flask-mako" target="_new">flask-mako</a>.
</%def>