/* javascript for iptables  */

var interfaces = [];

function addInterface(ifname) {
    interfaces.push(ifname);
}

function ruleOperation(rule_id, target, prot, opt, ifin, ifout, source, sport, destination, dport, misc, state)
{
    options = "dialogLeft=200;dialogTop=200;dialogWidth=720;dialogHeight=350;center=1;status=0;scroll=0;resizable=0;minimize=0;maximize=0;";
    var params = { rule_id:rule_id,  target:target, prot:prot, opt:opt, ifin:ifin, ifout:ifout, 
                             source:source, sport:sport, destination:destination, dport:dport, 
                             misc:misc, state:state, interfaces:interfaces };
    var fprm = window.showModalDialog("iptables_rule.html", params, options);
    if ( fprm.command.value  !== "" ) {
        f = document.getElementById('form1');
        f.command.value = fprm.command.value;
        f.rule_id.value = fprm.rule_id.value;
        f.target.value = fprm.target.value;
        f.prot.value = fprm.prot.value;
        f.ifin.value = fprm.ifin.value;
        f.ifout.value = fprm.ifout.value;
        f.source.value = fprm.source.value;
        f.destination.value = fprm.destination.value;
        f.sport.value = fprm.sport.value;
        f.dport.value = fprm.dport.value;
        f.state.value = fprm.state.value;
        f.submit();
    }
}

function ruleAdd(num_rules)
{
    options = "dialogLeft=200;dialogTop=200;dialogWidth=720;dialogHeight=350;center=1;status=0;scroll=0;resizable=0;minimize=0;maximize=0;";
    var params = { rule_id:"new",  target:"REJECT", prot:"all", opt:"", ifin:"*", ifout:"*", 
                             source:"0.0.0.0/0", sport:"", destination:"0.0.0.0/0", dport:"", 
                             misc:"", state:"", interfaces:interfaces, num_rules:num_rules };
    var fprm = window.showModalDialog("iptables_rule_add.html", params, options);
    if ( fprm.command.value  !== "" ) {
        f = document.getElementById('form1');
        f.command.value = fprm.command.value;
        f.rule_id.value = fprm.rule_id.value;
        f.target.value = fprm.target.value;
        f.prot.value = fprm.prot.value;
        f.ifin.value = fprm.ifin.value;
        f.ifout.value = fprm.ifout.value;
        f.source.value = fprm.source.value;
        f.destination.value = fprm.destination.value;
        f.sport.value = fprm.sport.value;
        f.dport.value = fprm.dport.value;
        f.state.value = fprm.state.value;
        f.submit();
    }
}



