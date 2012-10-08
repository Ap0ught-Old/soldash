<%inherit file="base.mako"/>

<%def name="body_content()">
    ${c}
    <P>${versions}</P>
    % for core in c:
        <h3>${core['core_name'] or 'Default Core'}</h3>
        <table class="instances" id="instances_${str(core['core_name'])}">
            <tr>
                <th>Host</th>
                <th>Status</th>
                <th>Solr Version</th>
                <th>Type</th>
                <th>Index Version</th>
                <th>Generation</th>
                <th>Index Size</th>
                % for command in config['COMMANDS']:
                    % if command.get('title'):
                        <th>${command['title']}</th>
                    % endif
                % endfor
            </tr>
        % for host in core['hosts']:
            <tr>
                <td class="address">
                    ${self.insert_host_link(host, core['core_name'])}
                </td>
                % if host['details']:
                    <% details = host['details']['details'] %>
                    <% status = host['details']['responseHeader']['status'] %>
                    <td class="status ${config['RESPONSEHEADERS'][status]}">
                        ${config['RESPONSEHEADERS'][status]}
                    </td>
                    <td class="solr_version">
                        tbd
                    </td>
                    <td class="type ${'master' if details['isMaster'] == 'true' else 'slave'}">
                        % if details['isMaster'] == 'true':
                            M
                        % else:
                            S
                        % endif
                    </td>
                    <td class="version fixed_width_font">${details['indexVersion']}</td>
                    <td class="generation">${details['generation']}</td>
                    <td class="size">${details['indexSize']}</td>
                    % for command in config['COMMANDS']:
                        <td>${self.insert_command_link(command)}</td>
                    % endfor
                % else:
                    <td class="status critical">${host['error']}</td>
                % endif
            </tr>
        % endfor
        </table>
    % endfor
</%def>

<%def name="insert_host_link(host, core_name)">
    <% url = 'http://%s:%s/solr' % (host['hostname'], host['port']) %>
    % if core_name:
        <% url += '/%s' % core_name %>
    % endif
    <% url += '/admin' %>
    <a href="${url}">${host['hostname']}</a>
</%def>

<%def name="insert_command_link(command)">
    ${command}
</%def>