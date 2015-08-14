/* javascripts for remote_ctl.py   */

function remoteCommand() {
    document.getElementById('output_area').innerHTML = "";
    form = document.getElementById('form1');
    form.y_scroll.value = document.documentElement.scrollTop || document.body.scrollTop;
    form.refresh.value = 0;
    form.submit();
}

function focusInput() {
    var input = document.getElementById('cmd_input');
    input.focus();
}