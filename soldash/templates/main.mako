<%inherit file="base.mako"/>

<%def name="body_content()">
    % for core in c:
        <%
        for host in core['hosts']:
            if host.get('type') == 'master':
                master_version = host['indexVersion']
                break
        %>
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
                <th>Fetch Index</th>
                <th>Polling</th>
                <th>Replication</th>
                <th>File List</th>
                <th>Backup</th>
                <th>Query</th>
                <th>Reload Index</th>
            </tr>
        % for host in core['hosts']:
            <tr>
                <td class="address">
                    ${self.insert_host_link(host, core['core_name'])}
                </td>
                % if host['status'] == 'ok':
                    <td class="status ${host['status']}">
                        ${host['status']}
                    </td>
                    <td class="solr_version">
                        % if versions.get(host['hostname']):
                            ${versions[host['hostname']]}
                        % endif
                    </td>
                    <td class="type ${host['type']}">
                        ${host['type']}
                    </td>
                    <td class="version ${'out_of_sync' if host['indexVersion'] != master_version else ''}">
                        ${host['indexVersion']}
                    </td>
                    <td class="generation">${host['generation']}</td>
                    <td class="size">${host['indexSize']}</td>
                    <td class="command server_side fetchindex">
                        % if host['type'] == 'slave':
                            % if host['replicating']:
                                <span class="fade_in_and_out">${host['replicating']}</span>
                            % else:
                                <a href="${url_for('execute', command='fetchindex', hostname=host['hostname'], core=core['core_name'])}">
                                    <img src="/static/images/ready.png">
                                </a>
                            % endif
                        % endif
                    </td>
                    <td class="command server_side polling">
                        % if host['type'] == 'slave':
                            <% command = 'disablepoll' if host['pollingEnabled'] else 'enablepoll' %>
                            <a href="${url_for('execute', command=command, hostname=host['hostname'], core=core['core_name'])}">
                                <img src="/static/images/${'enabled' if host['pollingEnabled'] else 'disabled'}.png">
                            </a>
                        % endif
                    </td>
                    <td class="command server_side replication">
                        % if host['type'] == 'master':
                            <% command = 'disablereplication' if host['replicationEnabled'] else 'enablereplication' %>
                            <a href="${url_for('execute', command=command, hostname=host['hostname'], core=core['core_name'])}">
                                <img src="/static/images/${'enabled' if host['replicationEnabled'] else 'disabled'}.png">
                            </a>
                        % endif
                    </td>
                    <td class="command filelist">
                        <a href="javascript:filelist('${host['hostname']}', '${core['core_name'] or 'None'}', '${host['indexVersion']}')">
                            <img src="/static/images/ready.png">
                        </a>
                    </td>
                    <td class="command server_side backup">
                        <a href="${url_for('execute', command='backup', hostname=host['hostname'], core=core['core_name'])}">
                            <img src="/static/images/ready.png">
                        </a>
                    </td>
                    <td class="command query">
                        <a href="javascript:openQueryDialog('${host['hostname']}', '${core['core_name'] or 'None'}')">
                            <img src="/static/images/ready.png">
                        </a>
                    </td>
                    <td class="command server_side reload">
                        <a href="${url_for('execute', command='reload', hostname=host['hostname'], core=core['core_name'])}">
                            <img src="/static/images/reload.png">
                        </a>
                    </td>
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
    <% url += '/admin/' %>
    <a href="${url}">${host['hostname']}</a>
</%def>
