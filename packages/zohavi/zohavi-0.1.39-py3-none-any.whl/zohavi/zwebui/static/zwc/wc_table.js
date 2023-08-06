    
    import C_UTIL from '/webui/static/zjs/common_utils.js'; //

    import ValidationHelper from '/webui/static/zjs/validation_helper.js'; //
    import WCFormControl from  "/webui/static/zwc/wc_form_main.js" 
    import WCModal from  "/webui/static/zwc/wc_modal.js" 
    import WCButton from  "/webui/static/zwc/wc_form_button.js" 
    // import WCButton from  "/common/st/_def/commonui/static/_def/wc/wc_form_button.js" 



    class WCTable extends WCFormControl { 
        define_template_globals(){
            return `:host{ 
                        --table_header_cell_color: var(--background_cat3_color);
                        --table_header_text_color: var(--light_text_color_cat1);

                        --table_cell_bg_key_color: var(--background_cat2_color);
                    }`
        }

        define_template(){
            var add_button_html = ""
            var template_str = ""
            if( this._inp.add_row ){
                add_button_html = `<div class="container mt-2 mb-2 level-right">
                                        <div class="level-item has-text-centered"> 
                                            <p class="control "> 
                                                <wc-button id="si_add_row" label="[placeholder::add_row]" active_class="is-success" > </wc-button>  
                                            </p>  
                                        </div>
                                    </div>`;
            }else{
                add_button_html = ""
            }

            template_str = super.define_template() + `   
                        <style>
                                ${this.define_template_globals()}

                                .sc_cell_validation_failed{  
                                    background-image: linear-gradient(225deg, red, red 10px, transparent 10px, transparent);
                                    color: red; 
                                }

                                .sc_cell_bg_key_color{
                                    background-color: var(--table_cell_bg_key_color);
                                    color: var(--light_text_color_cat1);
                                    font-weight: bold;
                                }
                                .sc_cell_disabled{
                                    background-color: grey
                                }

                                .table thead th{ /*over ride bulma setting */
                                    background-color: var(--table_header_cell_color);
                                    color: var(--table_header_text_color);
                                }
                        </style>

                        <div class="container">
                            ${ add_button_html }

                            <table id="si_field" class="table is-bordered is-striped is-hoverable is-fullwidth">
                                <thead id="si_thead"  >
                                  <!--
                                      <tr>
                                        <th width="20%" class="sc_table_header">Env</th>
                                        <th width="60%" class="sc_table_header">URL</th>
                                        <th width="20%" class="sc_table_header">Port</th>
                                      </tr>
                                  -->
                                </thead>
                                <tbody id="si_tbody">
                                    <!--
                                        <tr>
                                            <td  > Dev </td>
                                            <td class="sck_validation " data-validation="required|is_url" data-validation_msg="Must include a URL"  contenteditable> </td>
                                            <td class="sck_validation "  data-validation="required|num_gte:1000|num_lte:9999" data-validation_msg="Must include a 4 digit port number"  contenteditable> </td>
                                        </tr>
                                    -->
                                </tbody>
                            </table>
                        </div>` +
            this.define_template_modal();

            return template_str;
        }

        define_template_modal(){
            return ` <wc-modal id="si_modal" title="Edit"
                                fields='[]'> 
                    </wc-modal>`;
               
        }
                    // columns='[
                    //       {"col_label":"Name", "key":"ck_env_name" },
                    //       {"col_label":"Description", "key":"ck_env_desc" },
                    //       {"col_label":"Code", "key":"ck_env_code" },
                    //       {"col_label":"Action", "key":"ck_env_action" }
                    // ]'

                    // data='[ {"row_no":1, "data-id":"1",   
                    //                               "row":[  {"key":"ck_env_name", "value":"Dev", "data-value":"dev", "data-id":"1",     
                    //                               "cell_key_color":"true"},
                    //                               {"key":"ck_env_desc", "value":"Development"},
                    //                               {"key":"ck_env_code", "value":"dev"},
                    //                               {"key":"ck_env_action", 
                    //                                          "icons":[ {"icon":"fa-edit", "class_key":"ck_env_edit", "data-value":"1"},
                    //                                                    {"icon":"fa-trash", "class_key":"ck_env_delete", "data-value":"1"}] }
                    //                             ] },
                    //         {"row_no":2, "data-id":"2", 
                    //                               "row":[  {"key":"ck_env_name", "value":"Dev", "data-value":"dev", "data-id":"2" ,    
                    //                               "cell_key_color":"true"},
                    //                               {"key":"ck_env_desc", "value":"Development"},
                    //                               {"key":"ck_env_code", "value":"dev"},
                    //                               {"key":"ck_env_action", 
                    //                                          "icons":[ {"icon":"fa-edit", "class_key":"ck_env_edit", "data-value":"2"},
                    //                                                    {"icon":"fa-trash", "class_key":"ck_env_delete", "data-value":"2"}] }
                    //                             ] },
                    //         {"row_no":3, "data-id":"3", 
                    //                               "row":[  {"key":"ck_env_name", "value":"Dev", "data-value":"dev", "data-id":"3"},
                    //                               {"key":"ck_env_desc", "value":"Development"},
                    //                               {"key":"ck_env_code", "value":"dev"},
                    //                               {"key":"ck_env_action", 
                    //                                          "icons":[ {"icon_class":"fas fa-edit", "class_key":"ck_env_edit", "data-value":"3"},
                    //                                                    {"icon_class":"fas fa-trash", "class_key":"ck_env_delete", "data-value":"3"}] }
                    //                             ] }
                    //       ]'

        constructor(){
            super( {"add_row":"Add Env +", "data=json":"[]", "param=json":"[]", 
                    "action_icons=json":'{"edit":"fas fa-edit","delete":"fas fa-trash"}'}, ["columns=json"]); 
            // this.log('hello world')

            
        } 

        connectedCallback(){     
            // this.log('hello world')
             super.connectedCallback(); 
        } 

        //************************************************************************************
        //Update teh default settings per field once shadowdom is setup
        init_component(){
            var this_obj = this;
            this.log('initing')
            this.init_data()
            this.init_modal(this._inp.columns);

            this.create_table( this._inp.columns );
            // this.init_table_data(this._inp.data)
            this.init_table_data(this._inp.columns, this._inp.data)
            
            this._modal_ref = this.shadowRoot.querySelector('#si_modal')

            this.shadowRoot.querySelector('#si_add_row').addEventListener('click', this.evt_add_row_clicked.bind(this) );
            // this.init_modal( this._inp.columns);
        }

        init_data(){
            this._inp.data.forEach( function(item, index){
                item['data-row_no'] = index;
            });
        }
        //************************************************************************************
        init_modal(columns){
            // var this_obj = this;
            var field_list = []
            // debugger;
            for( var col_index in columns){
                const elt = columns[col_index ]
                if( elt.editable == "true"){
                    var field_data = {}
                    field_data.type = ( typeof elt.type  === 'undefined' ? 'input': elt.type );
                    field_data.label = elt.col_label;
                    field_data.id = elt.key;
                    field_data.validation = elt.validation;

                    if( "param" in elt){
                        for( var param_field in elt.param){
                            const param_name = elt.param[ param_field ]
                            field_data[ param_field ] = this._inp.param[ param_name  ]
                        }
                    }
                    
                    
                    field_list.push( field_data );
                }
                
            };



            this.shadowRoot.querySelector('#si_modal').fields = field_list;
        }

        

        //************************************************************************************
        //Delete row from table
        delete_row(row_no){
            // debugger
            var table_row = this.shadowRoot.querySelector(`tr[data-row_no='${row_no}']`)
            table_row.parentNode.removeChild(table_row);
        }

        //************************************************************************************
        //Add events to table cells
        add_table_row_item_events(){
            this.shadowRoot.querySelectorAll('.sc_icon_clickable').forEach(item =>{
                item.addEventListener( 'click',  (event)=> this.evt_icon_clicked(event) );  
            });
            
        }
        
        //************************************************************************************
        //Add events to table cells
        evt_add_row_clicked(event){
            this._modal_ref.show( null, null, this.callback_row_add.bind(this) );
        }
        //************************************************************************************
        //Add events to table cells
        evt_icon_clicked(event){ 
            // this.log('clicked')
            // debugger;
            if( event.path[1].dataset['action'] == 'edit' ){
                this.edit_row_entry( event.path[1].dataset['row_no'] )
                
            }else if( event.path[1].dataset['action'] == 'delete' ){
                this.delete_row( event.path[1].dataset['row_no'] )
            }

            var new_event = new CustomEvent( 'table_icon_click', { detail: {this:this, 
                                                                            elt:event.path[1], 
                                                                            key:event.path[1].dataset['key'], 
                                                                            id:event.path[1].dataset['value'],
                                                                            row_no:event.path[1].dataset['row_no'],  }}); 
            this.dispatchEvent(new_event , { bubbles:true, component:true} ); 
        }

        
        //************************************************************************************
        //edit row number (zero index entry)
        edit_row_entry(row_no){
            var curr_data_row = this._inp.data[ row_no ]
            this._modal_ref.show( curr_data_row, {'row_no':row_no}, this.callback_row_edited.bind(this) );
            this.log( 'showed modal')
        }


        //************************************************************************************
        callback_row_add(action,  ref_data,  new_data){
            // debugger;
            if( action != this._modal_ref.C_SAVE){ return }

            // debugger;

            this._callback_row_add_update_table(new_data);
            this._callback_row_add_update_data_twin(new_data);
            this.add_table_row_item_events()
        }

        _callback_row_add_update_data_twin(new_data){
            //Update the internal data records
            var inp_new_data_temp = []
            new_data.forEach( function(elt){
                var new_data_rec = {}
                new_data_rec['key'] = elt.id
                new_data_rec['value'] = elt.value
                if( 'data-value' in elt ){
                    new_data_rec['data-value'] = elt['data-value']    
                }
                inp_new_data_temp.push( new_data_rec )
            });
            this._inp.data.push( inp_new_data_temp )
        }
        //************************************************************************************
        _callback_row_add_update_table(new_data){
            var table_str = "";
            var tbody_ref = this.shadowRoot.getElementById('si_tbody')
            var new_row_no = tbody_ref.childNodes.length
            //Update the table row
            table_str += this.init_table_data_row( this._inp.columns, new_data, 'id', new_row_no )
            tbody_ref.innerHTML = tbody_ref.innerHTML + table_str;
            tbody_ref.childNodes[ new_row_no ].querySelector('.sc_icon_clickable').addEventListener( 'click',  (event)=> this.evt_icon_clicked(event) ); 
        }

        //************************************************************************************
        //edit row number (zero index entry)
        callback_row_edited(action, ref_data, new_data){
            var this_obj = this;
            
            if(action == this._modal_ref.C_SAVE ){
                // var row_elt = this.shadowRoot.querySelectorAll('tr.sck_data_row')[ ref_data['row_no'] ]
                var row_elt = this.shadowRoot.querySelector(`tr[data-row_no='${ ref_data['row_no'] }']` )
                // 
                for( const elt_key in new_data){
                    var data_item = new_data[ elt_key ]
                    var inp_data_fields = this._inp.data[  ref_data['row_no']  ] 
                     
                    for( const input_data_key  in inp_data_fields){
                        if( inp_data_fields[ input_data_key ].key == new_data[ elt_key ].id ){
                            inp_data_fields[ input_data_key ].value = new_data[ elt_key ].value 
                        }
                    };
                    
                    row_elt.querySelector('.' + data_item.id ).innerHTML = data_item.display_value;
                    row_elt.querySelector('.' + data_item.id ).dataset['value'] = data_item.value;
                };
                
            }
        }
        


        //************************************************************************************
        //Add attribute element
        add_attribute(search_attribute_name, attribute_data_obj, write_attrib_name){
            if( search_attribute_name in attribute_data_obj){
                var new_attrib_name = ( write_attrib_name ? write_attrib_name : search_attribute_name )
                return `${new_attrib_name}='${attribute_data_obj[search_attribute_name]}' `
            }
            return "";
        }

        //************************************************************************************
        add_table_attrb_class_list( attrib_data_obj, class_key_list, additional_class_list){
            var class_str = ""
            class_key_list.forEach( function(elt){
                if( elt in attrib_data_obj     ){ class_str += attrib_data_obj[ elt ] + " "; }
            });

            if( additional_class_list){
                additional_class_list.forEach( function(class_item){ class_str += class_item + " "; });    
            }
            
            return 'class ="' + class_str +'" '
        }

        //************************************************************************************
        init_table_data(cols, data){
            var table_str = ""; 
            var this_obj = this;
            // debugger
            data.forEach( function( data_row, row_no ){
                table_str += this_obj.init_table_data_row( this_obj._inp.columns, data_row, 'key', row_no )
            });
            this.shadowRoot.getElementById('si_tbody').innerHTML = table_str; 
            this.add_table_row_item_events()
        }

        
        //************************************************************************************
        init_table_data_row(cols, row_data, key_field_name, row_no){
            var this_obj = this;
            var row_str = "";

            row_str += `<tr `;
            row_str += this_obj.add_table_attrb_class_list( row_data, ['class'],  ['has-text-centered', 'sck_data_row'] )
            row_str += `data-row_no="${row_no}" `
            // row_str += this_obj.add_attribute( 'data-row_no', row_data )  
            // debugger;
            
            row_str += ">"
            cols.forEach( function( col){
                var data_cell = C_UTIL.search_list_dict_key_value( row_data, key_field_name , col[ 'key' ] );

                row_str += `<td `
                row_str += this_obj.add_attribute( 'width', col )
                row_str += `data-row_no="${row_no}" `

                if( data_cell ){  //in case this is a static cell - 
                    if( 'data-value' in data_cell){ row_str += `data-value="${ data_cell['data-value'] }"`
                    }else{  row_str += `data-value="${ data_cell['value']}"` }    

                    row_str += this_obj.add_attribute( 'validation', data_cell, 'data-validation' )

                    row_str += this_obj.add_table_attrb_class_list( data_cell, [ key_field_name ] ) 
                }

                // if( 'validation')


                //set background color
                if(  String( col['key_cell']).toLowerCase() == 'true'){ row_str += `class="sc_cell_bg_key_color" ` }
                row_str += '>'

                if( col['type'] == 'actions'){
                    row_str += this_obj._init_table_cell_add_actions( col,  row_no );
                }else if( data_cell ){
                    row_str += this_obj.shadowRoot.querySelector('#si_modal').get_field_display_value(data_cell.key,data_cell.value)
                } 
                row_str += '</td>'
            });

            row_str += `</tr>`;

            return row_str;
        }

        //************************************************************************************
        // Add any icon elements in a table cell
        //example: "icons":[ {"icon_class":"fa-edit", "class_key":"ck_env_edit", "data-value":"3"},
        //                   {"icon_class":"fa-trash", "class_key":"ck_env_delete", "data-value":"3"}] }
        _init_table_cell_add_actions( col_entry, row_no ){
            var cell_str = "";
            var this_obj = this;
            // debugger;
            col_entry.actions.forEach( function(action_item ){

                // var icon_class = search_list_dict_key_value( this_obj._inp.action_icons, 'action', action_item )

                cell_str += `<a href="#" ` 
                cell_str += `data-action="${action_item}" ` 
                cell_str += `data-row_no="${row_no}" `
                cell_str += `class="sc_icon_clickable" >`
                cell_str += `<i class="${ this_obj._inp.action_icons[ action_item ] }"></i>`
                cell_str += `</a>`
                // debugger
            });
            
            return cell_str; 
        }



        //************************************************************************************
        //Update teh default settings per field once shadowdom is setup
        create_table(columns){
            var table_str = "<tr>"; 
            var this_obj = this;
            columns.forEach( function( elt){
                table_str += `<th `;
                table_str += this_obj.add_table_attrb_class_list( elt, ['class', 'key'] )
                table_str += this_obj.add_attribute( 'width', elt );
                table_str += `>${elt.col_label}</th>`; 
            });
            table_str += `</tr>`;
            if(columns){ 
                this.shadowRoot.getElementById('si_thead').innerHTML = table_str; 
            }else{ 
                this.shadowRoot.getElementById('si_thead').innerHTML = ""; 
            }
        }

    

        is_debug(){ return false; } 

    }

    window.customElements.define('wc-table', WCTable);

//#################################################################################################################
//#################################################################################################################
//#################################################################################################################
//#################################################################################################################
//#################################################################################################################
//#################################################################################################################
    // const template = document.createElement('template');

    // template.innerHTML = ` 
    //         <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css">
    //         <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma-tooltip@3.0.2/dist/css/bulma-tooltip.min.css">
    //         <style>
    //             .sc_cell_validation_failed{  
    //                 background-image: linear-gradient(225deg, red, red 10px, transparent 10px, transparent);
    //                 color: red; 
    //             }

    //             .sc_table_header{
    //                 background-color: lightgrey;
    //             }

    //             .sc_cell_disabled{
    //                 background-color: grey
    //             }
    //         </style>

    //         <table id="si_table" class="table is-bordered  is-hoverable is-fullwidth">
    //             <thead id="si_thead">
    //               <!--
    //                   <tr>
    //                     <th width="20%" class="sc_table_header">Env</th>
    //                     <th width="60%" class="sc_table_header">URL</th>
    //                     <th width="20%" class="sc_table_header">Port</th>
    //                   </tr>
    //               -->
    //             </thead>
    //             <tbody id="si_tbody">
    //                 <!--
    //                     <tr>
    //                         <td  > Dev </td>
    //                         <td class="sck_validation " data-validation="required|is_url" data-validation_msg="Must include a URL"  contenteditable> </td>
    //                         <td class="sck_validation "  data-validation="required|num_gte:1000|num_lte:9999" data-validation_msg="Must include a 4 digit port number"  contenteditable> </td>
    //                     </tr>
    //                 -->
    //             </tbody>
    //         </table>
    // `; 



    // // sleep(1);
    // // class WCTable extends WCMaster { 
    // class WCTableXX extends WCFormControl { 
    //     constructor() {
    //           super();

    //           this.attachShadow({ mode: 'open' }); 
    //           this.shadowRoot.appendChild(template.content.cloneNode(true)); 

    //           // this._debug = true

    //     }
    //     // static help(){
    //     //     console.log('helping now')
    //     // }
    //     //************************************************************************************
    //     //Setup the defaults and events
    //     connectedCallback(){  
    //         this.log( "hello world ") 
    //         this.init_table();

    //         this.check_attributes( [] , ["data", "columns"] );
    //     }

    //     init_table(){
    //         this._data = []
    //         this.load_table_data();

    //         this.shadowRoot.querySelectorAll('.sck_validation').forEach(element =>{
    //             element.addEventListener("blur", this.evt_table_cell_changed.bind(this));  
    //         });
    //     }

    //     //***************************************************************************************
    //     //Load the table with the data provided
    //     load_table_data(){
    //         // console.log( 'loading json data')
    //         // console.log( this.getAttribute('columns') )

    //         var inp_col_info = JSON.parse( this.getAttribute('columns') );
    //         var inp_col_data = JSON.parse( this.getAttribute('data') );
    //         var data_defs;
    //         var data_def_keys;
    //         if( this.getAttribute('data_defs') ){
    //             data_defs = JSON.parse( this.getAttribute('data_defs') );
    //             data_def_keys = JSON.parse( this.getAttribute('data_def_search_keys') );
    //         } 
            
    //         // debugger;

    //         if( inp_col_info && inp_col_data ){     //make sure there is data provided
    //             var thead_str = this._load_table_data_render_header(inp_col_info);
    //             var tbody_str = this._load_table_data_render_rows(inp_col_info, inp_col_data) ;


    //             var inp_col_data_defs = this._filter_data_defs( data_defs, data_def_keys, inp_col_data);
    //             this.log( "Data  for:" + this.id )
    //             this.log( JSON.stringify( inp_col_data ) )
    //             this.log( "Data defaults for:" + this.id )
    //             this.log( JSON.stringify( inp_col_data_defs ) )



    //             tbody_str += this._load_table_data_render_rows(inp_col_info, inp_col_data_defs) ;

    //             this.log( "Data internal:" + this.id  )
    //             this.log( JSON.stringify( this.get_display_data()  ) )
    //             // debugger;

    //             this.shadowRoot.getElementById('si_thead').innerHTML = "<tr>" + thead_str + "</tr>"     //add to shadow DOM
    //             this.shadowRoot.getElementById('si_tbody').innerHTML =  tbody_str;
    //         }else{
    //             throw ": Please include attributes 'columns' and 'data' in wc-table"
    //         }

    //     }

    //     //************************************************************************************
    //     // Return just the rows that we should add as defaults which are not in the data that's provided
    //     _filter_data_defs( data_defs, data_def_keys, inp_col_data ){ 
    //         if( ! inp_col_data || inp_col_data.length == 0 ){ return data_defs; } //no input data, so all defaults will be used 
    //         if( ! data_defs || data_defs.length == 0 ){ return null; } //no input data, so all defaults will be used 
            
    //         var _this  = this;
    //         var found_item;
    //         var return_data = [] 
    //         data_defs.forEach( function( def_item){
    //             // debugger;
    //             _this.log( `Def : ${JSON.stringify( def_item)}`)

    //             found_item = false;
    //             inp_col_data.forEach( data_item =>{
    //                 _this.log( `Checking against data item: ${JSON.stringify( data_item)}`)
                    
    //                 data_def_keys.forEach( function( search_key){
    //                     if( data_item[ search_key["id"] ] == def_item[ search_key["id"] ] ){ found_item = true; return true; }
    //                 });
    //                 if( found_item ){ return true; }
    //             });
    //             if( ! found_item )
    //             { 
    //                     _this.log( `Adding item: ${JSON.stringify( def_item)}`)
    //                     // def_item["_status"] = 'disabled';   //as we ahve some col data already return it as a disabled item
    //                     return_data.push( def_item );       
    //                     return true; 
    //             }

    //         });
    //         return return_data;
    //     }

    //     //************************************************************************************
    //     // Render the data of the table
    //     _load_table_data_render_rows( inp_col_info, inp_col_data){
    //         if( ! inp_col_data ){ return ""}
    //         // console.log( inp_col_data )
    //         var tbody_str = "";
    //         var _this = this;
    //         inp_col_data.forEach( function( row_data, row_data_index){     //add the data rows
    //                 _this._data.push( row_data )
    //                 tbody_str += "<tr class=' ";
    //                 if( row_data['_status'] == 'disabled' ){ tbody_str += ` sc_cell_disabled ` }
    //                 if( row_data['_status'] == 'hidden' ){ tbody_str += ` is-hidden ` }
    //                 tbody_str += "'> "

    //                 inp_col_info.forEach( function( col_info, col_info_index){
    //                     tbody_str += "<td class='sck_validation  "
    //                         //If there are visible / disable parameters, then hide or disable via CSS classes
    //                         if( row_data['_status'] == 'disabled' ){ tbody_str += ` sc_cell_disabled ` }
    //                         if( row_data['_status'] == 'hidden' ){ tbody_str += ` is-hidden ` }
    //                     tbody_str += "' " //close the class tag
    //                     if( col_info['validation']     ){ tbody_str += `data-validation    ='${ JSON.stringify( col_info['validation'])}' ` }
    //                     if( col_info['validation_msg'] ){ tbody_str += `data-validation_msg="${col_info['validation_msg']}" ` }
    //                     if( row_data['id']             ){ tbody_str += ` data-id="${row_data['id']}" ` }
    //                     if( col_info['editable'] && row_data['_status'] != 'disabled' ){ tbody_str += ` contenteditable ` }

    //                     //If there's the same data field with a prefix underscore, then store this as a data value

    //                     if( typeof row_data[ '_' + col_info['name'] ] != 'undefined'  ){  //If there's a key value (i.e. _xxx), then set data-value with key value
    //                         // console.log( "adding value for 1:" +col_info['name'] + ":" + row_data[ col_info['name'] ]  )
    //                         tbody_str += ` data-value="${row_data[ '_' + col_info['name'] ]}" ` 
    //                     }else if( col_info['name'] in row_data) {
    //                         // console.log( "adding value for 2:" +col_info['name'] + ":" + row_data[ col_info['name'] ]  )
    //                         tbody_str += ` data-value="${ row_data[ col_info['name'] ]  }" `
    //                     }
    //                     tbody_str += ` data-column="${col_info['name']}" `
    //                     tbody_str += '>' + ( typeof row_data[ col_info['name'] ] != 'undefined' ? row_data[ col_info['name'] ] : "") + '</td>' 
    //                 });
    //                 tbody_str += "</tr>";
    //             });
    //         return tbody_str;
    //     }

    //      //************************************************************************************
    //     // Get the row which matches the dictionary search criteria
    //     get_table(  ){
    //         return this.shadowRoot.getElementById('si_table')
    //     }

    //     //************************************************************************************
    //     // Get the row which matches the dictionary search criteria
    //     get_row( search ){
    //         _this.log( JSON.stringify( search) )
    //         var table_ref = this.shadowRoot.getElementById('si_table')

    //         for (var i = 0, curr_row; curr_row = table_ref.rows[i]; i++) {  //Walkthroguh each row
    //             var search_found = []
                    
    //             for (var j = 0, curr_cell; curr_cell = curr_row.cells[j]; j++) { //for each row, check each cell
    //                 search.forEach( function( search_item ){
    //                     for (const [key, value] of Object.entries(search_item)) {    //see if any search key matches all attributes
    //                       var attrib_val = curr_cell.getAttribute( key )
    //                       if( attrib_val == value ){
    //                         search_found.push( { key:value } )
    //                         }
    //                     } 
    //                 });
                    
    //             }
    //             if( Object.entries(search_found).length == Object.entries(search).length ){ 
    //                 _this.log( JSON.stringify( search_found ) )
    //                 return curr_row;  
    //             }  //if all matched, then return row
    //         }
    //     }

    //     //************************************************************************************
    //     // Get the cell which matches the dictionary search criteria
    //     get_cell( search ){
    //         _this.log( JSON.stringify( search) )
    //         var table_ref = this.shadowRoot.getElementById('si_table')

    //         for (var i = 0, curr_row; curr_row = table_ref.rows[i]; i++) {  //Walkthroguh each row
    //             var search_found = {}
                    
    //             for (var j = 0, curr_cell; curr_cell = curr_row.cells[j]; j++) { //for each row, check each cell
    //                 for (const [key, value] of Object.entries(search)) {    //see if any search key matches all attributes
    //                   var attrib_val = curr_cell.getAttribute( key )
    //                   if( attrib_val == value ){
    //                     search_found[key]  = value 
    //                     }
    //                 }  
    //                 if( Object.entries(search_found).length == Object.entries(search).length ){ 
    //                     _this.log( JSON.stringify( search_found ) )
    //                     return curr_cell;  
    //                 }  //if all matched, then return row
    //             }
    //         }
    //     }


    //     //************************************************************************************
    //     // Render the header of the table
    //     _load_table_data_render_header( inp_col_info ){
    //         var thead_str = ""
    //         inp_col_info.forEach( function( col_info, col_info_index){  //add the header columns
    //                 thead_str += '<th class="sc_table_header" ';
    //                 if( col_info['width'] ){ thead_str += ` width="${col_info['width']}" `}
    //                 thead_str += `>${col_info['label']}</th>` + "\n";
    //         });
    //         return thead_str;
    //     }
    //     //************************************************************************************
    //     //Validation event
    //     evt_table_cell_changed( evt ){ 
    //        this._field_changed( evt.path[0] )
    //         // // evt.path[0].dataset("value") = evt.path[0].innerHTML;
    //         // this.validate_table_cell( evt.path[0] ); 
    //         // evt.path[0].dataset['value'] = evt.path[0].innerHTML
            
    //         // // var value = this.shadowRoot.getElementById('si_field').value;
    //         // const event = new CustomEvent('change', { detail: {this:this, elt:evt.path[0], value:evt.path[0].innerHTML  }});
    //         // this.dispatchEvent(event , { bubbles:true, component:true} );
    //         // debugger;
    //     }

    //     _field_changed( elt ){
    //         // evt.path[0].dataset("value") = evt.path[0].innerHTML;
    //         this.validate_table_cell( elt ); 
    //         elt.dataset['value'] = elt.innerHTML
            
    //         // var value = this.shadowRoot.getElementById('si_field').value;
    //         const event = new CustomEvent('change', { detail: {this:this, elt:elt, value:elt.innerHTML  }});
    //         this.dispatchEvent(event , { bubbles:true, component:true} );
    //     }

    //     //************************************************************************************
    //     //Validation given cell element
    //     validate_table_cell(cell){ 
    //         var result;
    //         // console.log(`Vlalidate_table_cell = ${cell.innerHTML} `)
    //         if(! ValidationHelper.validate( cell.innerText, cell.dataset['validation'] ) ){ 
    //             cell.classList.add('sc_cell_validation_failed', 'has-tooltip-active', 'has-tooltip-danger');
    //             if( cell.dataset['validation_msg'] ){ 
    //                 cell.setAttribute('data-tooltip', cell.dataset['validation_msg'] );
    //             }
    //             cell.dataset["validation_status"] = false
    //             result = false;   //return validation failed
    //         }else{ 
    //             cell.classList.remove('sc_cell_validation_failed', 'has-tooltip-active', 'has-tooltip-danger');
    //             delete cell.dataset.tooltip; 
    //             cell.dataset["validation_status"] = true
    //             result = true;    //return validation was ok
    //         }

    //         const event = new CustomEvent('validated', { detail: {this:this, elt:cell, value:cell.innerHTML, validation_result:result  }});
    //         this.dispatchEvent(event , { bubbles:true, component:true} ); 
    //         return result;
    //     }

    //     //************************************************************************************
    //     //return if cells are all valid or not
    //     is_valid(){
    //         var validation_ok = true;
    //         var this_obj = this;
    //         this.shadowRoot.querySelectorAll('td[contenteditable]').forEach( function(element, index){ 
    //             if( typeof element.dataset["validation_status"] != "undefined"){
    //                 // console.log( `${element.innerHTML} => ${ element.dataset["validation_status"]}`)
    //                 validation_ok = validation_ok & ( element.dataset["validation_status"] == 'true')
    //             }
    //         });
    //         return validation_ok;
    //     }
        

    //     //************************************************************************************
    //     //Validate all editalbe data fields
    //     validate(){
    //         var validation_ok = true;
    //         var this_obj = this;
    //         this.shadowRoot.querySelectorAll('td[contenteditable]').forEach( function(element, index){
    //             // console.log( element.innerHTML);
    //             validation_ok = validation_ok & this_obj.validate_table_cell(element);
    //         });
    //         return validation_ok;
    //     }

    //     //************************************************************************************
    //     //Extract all data into a json format object
    //     set_data( row, col, value, internal_value = null){
    //         var table_data =   this.shadowRoot.getElementById('si_table');
    //         // debugger;
    //         var elt = table_data.rows[row].cells[col]
    //         elt.innerHTML = value;
    //         if( internal_value ){ 
    //             elt.setAttribute( "data-value", value);
    //         }else{
    //             elt.setAttribute( "data-value", internal_value) ;
    //         }
            
    //         this._field_changed( elt )
    //     }

    //     //************************************************************************************
    //     //Extract all data into a json format object
    //     get_display_data(){
    //         return this._data;
    //     }

    //     //************************************************************************************
    //     //Extract all data into a json format object
    //     get_submit_data(){
    //         var row_data = [];
    //         var _this = this;
    //         this.shadowRoot.querySelectorAll('tbody > tr:not([class*="sc_cell_disabled"])').forEach(  table_row => {
    //             var col_data = {}

    //             table_row.querySelectorAll('td').forEach( table_row_col_data => { 
    //                 // if( table_row_col_data.dataset["column"] == "sql_name"){ debugger; }
    //                 //if there is an internal value stored in data-value, then get that, otherwise get what's in the cell (innerHTML)
    //                 _this.log( "get data:" + table_row_col_data.dataset["column"] + ":" + table_row_col_data.dataset["value"]  )
    //                 var value = (  "value" in table_row_col_data.dataset ?  table_row_col_data.dataset["value"] : ""  )
    //                 col_data[ table_row_col_data.dataset["column"]  ] = value;
    //                 _this.log( "==>added " + col_data[ table_row_col_data.dataset["column"]  ] ); 
    //             });
    //             row_data.push( col_data ) 

    //         });

    //         var return_data = {id:this.id, _value:row_data };  
    //         _this.log( "returning table data: " + JSON.stringify( return_data ))
    //         return return_data  ;
    //     }

    // }

        // //************************************************************************************
        // //add table data
        // init_table_data2(data){
        //     var table_str = ""; 
        //     var this_obj = this;
        //     debugger
        //     data.forEach( function( elt){
        //         table_str += `<tr `;
        //         table_str += this_obj.add_table_attrb_class_list( elt, ['class'],  ['has-text-centered', 'sck_data_row'] )
        //         table_str += this_obj.add_attribute( 'data-row_no', elt )  
        //         table_str += ">"
        //         elt.row.forEach( function(data_col){
        //             table_str += `<td `
        //             table_str += this_obj.add_attribute( 'width', data_col )
        //             table_str += this_obj.add_attribute( 'data-value', data_col ) 
        //             table_str += this_obj.add_attribute( 'data-row_no', elt ) 
        //             table_str += this_obj.add_table_attrb_class_list( data_col, ['key'] ) 

        //             if(  String(data_col['cell_key_color']).toLowerCase() == 'true'){
        //                 table_str += `class="sc_cell_bg_key_color" `
        //             }

        //             if('value' in data_col){
        //                 table_str += '>' + data_col.value + '</td>'
        //             }else if('icons' in data_col){
        //                 table_str += '>'
        //                 table_str += this_obj._init_table_cell_add_icons( elt, data_col.icons);
        //                 table_str += '</td>'
        //             } 
        //         });
        //         table_str += `</tr>`;
        //     });
            
        //     this.shadowRoot.getElementById('si_tbody').innerHTML = table_str; 
        //     this.add_table_row_item_events()
        // }

        // //************************************************************************************
        // // Add any icon elements in a table cell
        // //example: "icons":[ {"icon_class":"fa-edit", "class_key":"ck_env_edit", "data-value":"3"},
        // //                   {"icon_class":"fa-trash", "class_key":"ck_env_delete", "data-value":"3"}] }
        // _init_table_cell_add_icons2( elt, icon_list ){
        //     var table_str = "";
        //     var this_obj = this;
        //     icon_list.forEach( function(icon){
        //         table_str += `<a href="${ ('link' in icon ? icon.link : '#')}"`
        //         table_str += this_obj.add_attribute( 'data-value', icon )
        //         table_str += this_obj.add_attribute( 'data-key', icon )
        //         table_str += this_obj.add_attribute( 'data-row_no', elt ) 
        //         table_str += this_obj.add_attribute( 'data-action', icon ) 
        //         table_str += `class="sc_icon_clickable" >`
        //         table_str += `<i class="${icon.icon_class}"></i>`
        //         table_str += `</a>`
        //     });
            
        //     return table_str; 
        // }

    // //************************************************************************************
        // //Setup the fields for the modal box
        // init_model(columns){
        //     // var table_str = "<tr>"; 
        //     // var this_obj = this;
        //     // columns.forEach( function( elt){
        //     //     table_str += `<th `;
        //     //     table_str += this_obj.add_table_attrb_class_list( elt, ['class', 'key'] )
        //     //     table_str += this_obj.add_attribute( 'width', elt );
        //     //     table_str += `>${elt.col_label}</th>`; 
        //     // });
        //     // table_str += `</tr>`;
        //     // if(columns){ 
        //     //     this.shadowRoot.getElementById('si_thead').innerHTML = table_str; 
        //     // }else{ 
        //     //     this.shadowRoot.getElementById('si_thead').innerHTML = ""; 
        //     // }
        // }
 
// })();
