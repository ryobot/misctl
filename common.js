/* common javascripts  */

function setRefresh(refresh) {
    form = document.getElementById('form1');
    form.refresh.value = refresh;
    form.submit();
}

function refresh() {
    form = document.getElementById('form1');
    form.y_scroll.value = document.documentElement.scrollTop || document.body.scrollTop;
    form.submit();
}

function setRefreshTimerAndScroll(time, y_scroll) {
    if (time > 0) {
        setTimeout('refresh()', 1000*time);
    }
    window.scroll(0, y_scroll);
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

// language
function langSelect() {
    form = document.getElementById('form1');
    form.submit();
}

// for toggle (open/close) div
function toggleDisplay(name, state) {
    if ( state === "open" ) {
        document.getElementById(name + "_open").style.display = 'block';
        document.getElementById(name + "_close").style.display = 'none';
    } else {
        document.getElementById(name + "_close").style.display = 'block';
        document.getElementById(name + "_open").style.display = 'none';
    }
    form = document.getElementById('form1');
    form[name + "_div"].value = state;
}
