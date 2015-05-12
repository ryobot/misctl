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
    options = "dialogLeft=200;dialogTop=200;dialogWidth=600;dialogHeight=200;center=1;status=0;scroll=0;resizable=0;minimize=0;maximize=0;";
    pass = window.showModalDialog("auth.html", msg, options);
    if ( pass ) {
        form = document.getElementById('form1');
        form.config_action.value = "do_auth";
        form.service_id.value = service_id;
        form.passwd.value = pass;
        form.submit();
    }
}
