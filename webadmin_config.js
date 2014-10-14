/* javascripts for webadmin_config.py   */

function addService() {
    form = document.getElementById('form1');
    form.config_action.value = "add_service";
    form.submit();
}

function deleteService(service_id, msg) {
    if (window.confirm(msg)) {
        form = document.getElementById('form1');
        form.config_action.value = "delete_service";
        form.service_id.value = service_id;
        form.submit();
    }
}

function doAuth(service_id, msg) {
    pass = window.prompt(msg, "");
    if ( pass ) {
        form = document.getElementById('form1');
        form.config_action.value = "do_auth";
        form.service_id.value = service_id;
        form.passwd.value = pass;
        form.submit();
    }
}
