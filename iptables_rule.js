   var params;

   var source_val;
   var destination_val;
   var sport_val;
   var dport_val;
   var timer = null;

   function isChanged() {
      var f = document.getElementById("params");
      return ( f.target.value !== params['target']
       || f.prot.value !== params['prot']
       || f.ifin.value !== params['ifin']
       || source_val !== params['source']
       || sport_val !== params['sport']
       || f.ifout.value !== params['ifout']
       || destination_val !== params['destination']
       || dport_val !== params['dport'] );
   }
   
   function onParamChange() {
       //buttons:
       var b_del = document.getElementById("delete_button");
       var b_rep = document.getElementById("replace_button");
       var b_ins = document.getElementById("insert_button");
       if ( isChanged() ) {
          b_del.innerHTML = '<span class="disabled">Delete Rule</span>';
          b_rep.innerHTML = '<a href="javascript:replaceRule()">Replace Rule</a>';
          b_ins.innerHTML = '<a href="javascript:insertRule()">Insert Rule</a>';
       } else {
          b_del.innerHTML = '<a href="javascript:deleteRule()">Delete Rule</a>';
          b_rep.innerHTML = '<span class="disabled">Replace Rule</span>';
          b_ins.innerHTML = '<span class="disabled">Insert Rule</span>';
       }
       // protocols:
       var prot_sel = document.getElementById("prot_select");
       var dport_input = document.getElementById("dport_input");
       var sport_input = document.getElementById("sport_input");
       var state_input = document.getElementById("state_input");
       if ( prot_sel.value == "icmp" ) {
           dport_input.value = "";
           dport_input.disabled = true;
           sport_input.value = "";
           sport_input.disabled = true;
           state_input.value = "";
           state_input.disabled = true;
       } else {
           if ( dport_input.value == "" ) {
               dport_input.value = params['dport'];
           }
           dport_input.disabled = false;
           if ( sport_input.value == "" ) {
               sport_input.value = params['sport'];
           }
           sport_input.disabled = false;
           if ( state_input.value == "" ) {
               state_input.value = params['state'];
           }
           state_input.disabled = false;
       }
   }

   function initEvents() {
        source_input = document.getElementById("source_input");
        destination_input = document.getElementById("destination_input");
        sport_input = document.getElementById("sport_input");
        dport_input = document.getElementById("dport_input");
        source_val = source_input.value;
        destination_val = destination_input.value;
        sport_val = sport_input.value;
        dport_val = dport_input.value;

        timer = window.setInterval(function(){
            source_val = source_input.value;
            destination_val = destination_input.value;
            sport_val = sport_input.value;
            dport_val = dport_input.value;
            onParamChange();
        }, 500);
    }
    
    function quitEvents() {
        window.clearInterval(timer);
    }

   function addOption(select, optionName) {
        var option = document.createElement('option');
        option.value = optionName;
        option.selected = false;
        option.innerHTML = optionName;
        select.appendChild(option);
   }

   function setSelected(options, value) {
        for ( i = 0; i < options.length; i++ ) {
             if ( options[i].value === value ) {
                 options[i].selected = true;
             }
         }
    }
    
   function setParams() {
      params = window.dialogArguments;
      document.getElementById("message").innerHTML = params['rule_id'];
      var f = document.getElementById("params");
      // id:
      f.rule_id.value = params['rule_id'];
      // interfaces:
      for ( i = 0; i < params['interfaces'].length; i++ ) {
          addOption(f.ifin, params['interfaces'][i]);
          addOption(f.ifout, params['interfaces'][i]);
      }
      setSelected(f.target.options, params['target']);
      setSelected(f.prot.options, params['prot']);
      setSelected(f.ifin.options, params['ifin']);
      f.source.value = params['source'];
      f.sport.value = params['sport'];
      setSelected(f.ifout.options, params['ifout']);
      f.destination.value = params['destination'];
      f.dport.value = params['dport'];
      f.state.value = params['state'];
      
      initEvents();
   }

   function setParamsAdd() {
      params = window.dialogArguments;
      document.getElementById("message").innerHTML = params['rule_id'];
      var f = document.getElementById("params");
      // id:
      f.rule_id.value = params['rule_id'];
      // interfaces:
      for ( i = 0; i < params['interfaces'].length; i++ ) {
          addOption(f.ifin, params['interfaces'][i]);
          addOption(f.ifout, params['interfaces'][i]);
      }
      setSelected(f.target.options, params['target']);
      setSelected(f.prot.options, params['prot']);
      setSelected(f.ifin.options, params['ifin']);
      f.source.value = params['source'];
      f.sport.value = params['sport'];
      setSelected(f.ifout.options, params['ifout']);
      f.destination.value = params['destination'];
      f.dport.value = params['dport'];
      f.state.value = params['state'];
      
        for ( i = 1; i <= params['num_rules'] + 1; ++i ) {
            addOption(f.new_rule_id, i.toString());
        }
        setSelected(f.new_rule_id, (params['num_rules'] + 1).toString());
   }

   function replaceRule() {
      f = document.getElementById("params");
      f.command.value = "replace";
      window.returnValue = f;
      quitEvents();
      window.close();
   }

   function deleteRule() {
      f = document.getElementById("params");
      f.command.value = "delete";
      window.returnValue = f;
      quitEvents();
      window.close();
   }

   function insertRule() {
      f = document.getElementById("params");
      f.command.value = "insert";
      window.returnValue = f;
      quitEvents();
      window.close();
   }

   function addRule() {
      f = document.getElementById("params");
      if ( f.new_rule_id.value <= params['num_rules'] ) {
          f.rule_id.value = f.new_rule_id.value;
          return insertRule();
      }
      f.command.value = "add";
      window.returnValue = f;
      quitEvents();
      window.close();
   }

   function cancel() {
      quitEvents();
      window.close();
   }
   
   function setFocus(id) {
      var f = document.getElementById(id);
      f.value = f.list.hidden;
   }
   


