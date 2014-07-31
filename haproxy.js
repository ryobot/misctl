function setRefresh(refresh) {
    form = document.getElementById('form1');
    form.refresh.value = refresh;
    form.submit();
}

function toggleDetail() {
    form = document.getElementById('form1');
    if (form.detail.value === "no") {
        form.detail.value = "yes";
    } else {
        form.detail.value = "no";
    }
    form.submit();
}

function toggleCommand() {
    form = document.getElementById('form1');
    if (form.command.value === "no") {
        form.command.value = "yes";
        form.refresh.value = 0;
    } else {
        form.command.value = "no";
    }
    form.submit();
}

function refresh() {
    form = document.getElementById('form1');
    form.y_scroll.value = document.documentElement.scrollTop || document.body.scrollTop;
    form.submit();
}

function socketCommand() {
    form = document.getElementById('form3');
    form.y_scroll.value = document.documentElement.scrollTop || document.body.scrollTop;
    form.submit();
}

function setRefreshTimerAndScroll(time, y_scroll) {
    if (time > 0) {
        setTimeout('refresh()', 1000*time);
    }
    window.scroll(0, y_scroll);
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

function deleteServer(server) {
    if (window.confirm("Deleting server " + server + ". OK?")) {
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

function saveServer() {
    form = document.getElementById('form2');
    form.submit();
}

// service commands:
function stop() {
    form = document.getElementById('form1');
    form.service_action.value = "stop";
    form.submit();
}

function start() {
    form = document.getElementById('form1');
    form.service_action.value = "start";
    form.submit();
}

function reload() {
    form = document.getElementById('form1');
    form.service_action.value = "reload";
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
    form = document.getElementById('form2');
    form.socket_command.value = "set weight " + name + " " + form.weightValue.value;
    form.submit();
}

