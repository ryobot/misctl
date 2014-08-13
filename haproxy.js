/* javascripts for haproxy_ctl.py   */

function socketCommand() {
    form = document.getElementById('form1');
    form.y_scroll.value = document.documentElement.scrollTop || document.body.scrollTop;
    form.socket_command.value = form.socket_command_str.value;
    form.refresh.value = 0;
    form.command.value = "yes";
    form.submit();
}

function editServer(server) {
    form = document.getElementById('form1');
    form.refresh.value = 0;
    form.editServer.value = server;
    form.submit();
}

function addServer() {
    form = document.getElementById('form1');
    form.refresh.value = 0;
    form.addServer.value = "new_server";
    form.submit();
}

function deleteServer(server, msg) {
    if (window.confirm(msg)) {
        form = document.getElementById('form1');
        form.refresh.value = 0;
        form.delServer.value = server;
        form.submit();
    }
}

function editWeight(server) {
    form = document.getElementById('form1');
    form.refresh.value = 0;
    form.weightServer.value = server;
    form.submit();
}

function saveServer(server) {
    form = document.getElementById('form1');
    form.save.value = "yes";
    form.refresh.value = 10;
    form.editServer.value = server;
    form.name.disabled = false;
    form.ip_port.disabled = false;
    form.cookie.disabled = false;
    form.submit();
}

function saveAddServer() {
    form = document.getElementById('form1');
    form.save.value = "yes";
    form.refresh.value = 10;
    form.addServer.value = form.name.value;
    form.submit();
}

// socket commands:
function downServer(name) {
    form = document.getElementById('form1');
    form.socket_command.value = "disable server " + name;
    form.submit();
}

function upServer(name) {
    form = document.getElementById('form1');
    form.socket_command.value = "enable server " + name;
    form.submit();
}

function doEditWeight(name) {
    form = document.getElementById('form1');
    form.refresh.value = 10;
    form.socket_command.value = "set weight " + name + " " + form.weightValue.value;
    form.submit();
}
