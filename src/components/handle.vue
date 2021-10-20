<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/deep/ .avatar-uploader{
  top: -60px;
  position: relative;
}
.el-table /deep/ .exceed-row {
    background: #FFF0D2;
}
.el-table /deep/ .warning-row {
    color: red;
}
.el-table /deep/ .success-row {
    background: #FFF0D2;
}
.el-table /deep/ th{
    background-color: #FFBE3F;
    color:#000;
    border: solid 1.5px #c0c0c0;
    font-size: 18px;
}
.el-table /deep/ td{
    background-color: #fff0d2;
    color:#000;
}
.el-table /deep/ .cell{
    word-break: break-word;
    display: contents;
}
.memeber_button {
    font-size: 30px;
    padding: 0px 0px;
    position:absolute;
    top: 10px;
    right:35px;
    color:#8E6109;
    background-color: #EBD1A0;
    border-color: #EBD1A0;
    cursor: pointer;
    text-align:center;  
    vertical-align:middle; 
    margin-top: 2px;
}
.heading{
    font-size: 40px;
    color: #000;
    font-weight: bold;
    position: relative;
    top: -20px;
}
.submit_dialog /deep/ .el-dialog{
    background-color:#C4C4C4;
}
.contact-input /deep/ .el-select__input{
    width: 170px !important;
}
/deep/ .el-tag.el-tag--info{
    margin: 6px;
}
/deep/ .el-select__tags{
    max-width: none !important;
}
/deep/ .el-slider__bar{
  background: rgb(241,241,241);
}
/deep/ .el-slider__runway{
  background: rgb(241,241,241);
}
/deep/ .el-slider__button{
  width: 13px;
  height: 20px;
  border-radius: 0%;
  background: rgb(193,193,193);
  border-color: rgb(193,193,193);
}
</style>

<style>
.cc-opt{
  min-width: auto !important;
}
.handletable > .el-table__body-wrapper {
  overflow-y: auto;
}
</style>
</style>
<template>
  <div>
    <transition name="fade"><!--loading動畫-->
      <loading v-if="isLoading"></loading>
    </transition>
    <div>
        <el-header style="top:-60px; text-align: right; font-size:20px; position:relative; background-color:#EBD1A0 ; ">
            <div style="position:absolute;left:30px;top:3px;cursor:pointer;" @click="cancel">License Application Service</div>

            <el-popover trigger="hover" width="200" placement="bottom" :close-delay="delay_time">
            
            <div><span>成員名稱: {{user[0]}}</span></div>
            <div><span>-----------------------------------------</span></div>
            <div><el-button  @click="$router.push({name: 'admin', query:{}})"  type="primary" icon="el-icon-setting">後台管理</el-button></div>
            <div><el-button  @click="Logout"  icon="el-icon-switch-button" style="background:#F56C6C; color:#FFFFFF; width:117px;">登出</el-button></div>
            
            <el-button  class="memeber_button" slot="reference" icon="el-icon-s-custom"></el-button>
            </el-popover>
        </el-header>
    </div>

      <!-- 主要表格 -->
      <div class="heading">確認</div>
      <div v-show="warning" style="color: red; font-size:20px; font-weight: bold;">{{warning_message}}</div>
      <div style="position:relative; top:0px; z-index: 110; margin:0px auto; width:90%">
          <div style="display:flex; position:relative;">
            <el-table
              class="handletable"
              ref="handletable"
              :data="tableData.slice(scroll_position, scroll_position+20)"
              :row-style="{background: '#FFF0D2'}"
              :cell-style="setCellColor"
              :row-key="row_key_id"
              height= 650px>
            <el-table-column align="center" width=70 label=" ">
                <template slot-scope="scope">
                  {{ scroll_position + scope.$index + 1 }}
                </template>
              </el-table-column>
            <el-table-column type="" align="center" prop="" label="編輯" width="100">
              <template slot-scope = "{row,$index}" >
              <el-row>
                <el-button type="danger"  style="position:relative;right:5px;" size="mini"@click="deleterow(row, $index)"  icon="el-icon-delete" circle></el-button>
                <el-popover ref="popover" width="1010px" trigger="hover" placement="top-start" offset="200">
                  <el-table :cell-class-name="cell_color" :data="compare_Data" :cell-style="{border: 'solid 1px #EAEAEA'}">
                    <el-table-column align="center" width="100px" prop="customer" label="客戶"></el-table-column>
                    <el-table-column align="center" width="70px" prop="sn" label="KeyID"></el-table-column>
                    <el-table-column align="center" width="100px" prop="product" label="產品"></el-table-column>
                    <el-table-column align="center" width="100px" prop="module" label="模組"></el-table-column>
                    <el-table-column align="center" width="70px" prop="version" label="版本"></el-table-column>
                    <el-table-column align="center" width="70px" prop="count" label="數量"></el-table-column>
                    <el-table-column align="center" width="70px" prop="type" label="類型"></el-table-column>
                    <el-table-column align="center" width="70px" prop="region" label="地區"></el-table-column>
                    <el-table-column align="center" width="130px" prop="expiration" label="使用期限"></el-table-column>
                    <el-table-column align="center" width="150px" prop="user" label="負責人"></el-table-column>
                    <el-table-column align="center" width="150px" prop="contact" label="聯絡人"></el-table-column>
                    <el-table-column align="center" width="140px" prop="comment" label="備註"></el-table-column>
                  </el-table>
                <el-button v-show="row.operator=='修改'" type="info " size="mini" slot="reference" @mouseenter.native="compare_row(row,$index)" icon="el-icon-view" circle></el-button>
                </el-popover>
              </el-row>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="operator" label="操作" width="80">
            </el-table-column>
            <el-table-column align="center" prop="customer" label="客戶">
              <template slot-scope = "{row,$index}" >
                  <span>{{row.customer}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="sn" label="KeyID"> 
              <template slot-scope = "{row,$index}" >
                <span>{{row.sn}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="product" label="產品"> 
              <template slot-scope = "{row,$index}" >
                  <span>{{row.product}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="module" label="模組"> 
                <template slot-scope = "{row,$index}" >
                  <span>{{row.module}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="version" label="版本" width=100> 
              <template slot-scope = "{row,$index}" >
                  <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.version}}</span>
                  <el-input v-else type="text" name="version" v-model="row.version" ></el-input>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="count" label="數量" width=100> 
              <template slot-scope = "{row,$index}" >
                <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.count}}</span>
                <el-input v-else type="number" name="count" v-model="row.count"></el-input>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="type" label="類型" width=100> 
              <template slot-scope = "{row,$index}" >
                  <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.type}}</span>
                  <el-select  v-else v-model="row.type"  @change="type_change($index)">
                      <el-option v-for="item in type_opt" :key="item.value" :label="item.label" :value="item.value">
                          <el-tooltip placement="right">
                              <div v-if="item.value=='測試'" slot="content">測試 - 借用給客戶(3個月)<br>審核單位: 產品 BU<br>申請新的 key 須填寫領用單，行政查詢用</div>
                              <div v-if="item.value=='出貨'" slot="content">出貨 - 尚未完全付完款項(6個月)<br>審核單位: 財會部<br>請提供訂單編號供行政查詢</div>
                              <div v-if="item.value=='正式'" slot="content">正式 - 付完全部款項(隔年1月31日)<br>審核單位: 財會部<br>請提供訂單編號供行政查詢<br>系統會自動延期一年</div>
                              <div v-if="item.value=='永久'" slot="content">台灣區需提供客戶切結書<br>目前試用電測付完尾款之客戶</div>
                              <span style="color: #8492a6; font-size: 13px; padding:10px">{{ item.value }}</span>
                          </el-tooltip>
                      </el-option>
                  </el-select>
              </template>
              </el-table-column>
            <el-table-column align="center" prop="region" label="地區"> 
              <template slot-scope = "{row,$index}" >
                  <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.region}}</span>
                  <el-select v-else v-model="row.region">
                      <el-option
                          v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value">
                      </el-option>
                  </el-select>
              </template>
              </el-table-column>
            <el-table-column align="center" prop="expiration" label="使用期限" width="145">
              <template slot-scope = "{row,$index}" >
                <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.expiration}}</span>
                <el-date-picker v-else value-format="yyyy-MM-dd" type="date" name="expiration" v-model="row.expiration" style="width: 135px;" ></el-date-picker>
              </template>
              </el-table-column>
            <el-table-column align="center" prop="user" label="負責人"> 
                <template slot-scope = "{$index,row}">
                  <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.user}}</span>
                  <el-autocomplete v-else v-model="row.user" :fetch-suggestions="querySearch_user" popper-append-to-body="false" placeholder="僅限一位負責人" />
                </template>
            </el-table-column>
            <el-table-column align="center" prop="contact" label="聯絡人" width="200"> 
              <template slot-scope = "{row,$index}" >
                <span v-if="row.operator=='刪除' || row.operator.includes('多筆')" >{{row.contact}}</span>
                <el-select v-else v-model="row.contact_display" @change="((item)=>{contact_selection_change(item, $index)})" filterable clearable multiple
                    :filter-method="contact_fliterer" @keyup.enter.native="contact_enter($index)" class = "contact-input" placeholder = "請輸入後按enter"> 
                    <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column align="center" prop="comment" label="備註"> 
              <template slot-scope = "{row,$index}" >
                  <span v-if="row.operator=='刪除'" >{{row.comment}}</span>
                  <i v-else-if="row.operator.includes('多筆')"  class="el-icon-tickets" style="cursor: pointer;" @click="open_detail(row)" />
                  <el-input v-else type="text" name="comment" v-model="row.comment" ></el-input>
              </template>
            </el-table-column>
            </el-table>
            <div v-if="tableData.length>20" style="position:absolute; right: 0px; width:21px; height:650px; background: rgb(241,241,241)">
              <el-slider 
                style="left: -8px; top: 60px;" 
                v-model="slider_position" 
                vertical height="579px" 
                :max="tableData.length"
                :min="20"
                :show-tooltip="false"
                @input="slider_input" 
              >
              </el-slider>
            </div>
          </div>

          <div style="text-align: end">
            <div style="display: inline; top: 3px; position: relative; font-size: 18px;">附件 :</div>
            <el-button style="font-size:20px; margin-right: 50px" type="text" @click="download">license-application.xlsx</el-button>
            <el-button style="width:150px;height:50px;display:inline;" @click="cancel" size = "medium" type="warning">取消申請</el-button>
            <el-button style="width:150px;height:50px;display:inline;" @click="back" size = "medium" type="warning">返回主頁</el-button>
            <el-button style="width:150px;height:50px;display:inline;" @click="test_and_dialog" size = "medium" type="warning">送出申請</el-button>
          </div>
      </div>

      <el-dialog :visible.sync="detail_dialog" width="1000px" class="submit_dialog">
        <span slot="title" style="font-size:20px;">
          {{detail_customer}} {{detail_sn}} {{detail_type}} 詳細資訊
        </span>
        <el-table :data="detail_data" height="650px">
          <el-table-column align="center" prop="product" label="產品"> </el-table-column>
          <el-table-column align="center" prop="module" label="模組"> </el-table-column>
          <el-table-column align="center" prop="version" label="版本"> </el-table-column>
          <el-table-column align="center" prop="count" label="數量"> </el-table-column>
          <el-table-column align="center" prop="type" label="類型"> </el-table-column>
          <el-table-column align="center" prop="region" label="地區"> </el-table-column>
          <el-table-column align="center" prop="expiration" label="使用期限"> </el-table-column>
        </el-table>
      </el-dialog>


      <el-dialog :visible.sync="submit_dialog" width="600px" class="submit_dialog">
        <el-form  label-width="80px" label-position="top" style="top: -30px; position: relative;">
          <el-form-item style="text-align: start;">
              <span style="font-weight: bold; font-size:25px">申請人</span><br>
              <el-autocomplete v-model="user[0]" :fetch-suggestions="querySearch_user" placeholder="請輸入申請人" ></el-autocomplete>
          </el-form-item>
          <el-form-item style="text-align: start;">
            <span style="font-weight: bold; font-size:25px">副本</span><br>
            <el-row><el-col :span="24">
              <el-select v-model="cc" filterable clearable multiple :filter-method="cc_fliterer" popper-class="cc-opt"
               @keyup.enter.native="cc_enter" style="width: 620px;" placeholder="請選擇副本或手動輸入後按Enter">
                  <el-option v-for="opt in cc_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
              </el-select>
            </el-col></el-row>
            
          </el-form-item>
          <el-form-item style="text-align: start;" prop="text">
            <span style="font-weight: bold; font-size:25px">申請原因</span><br>
            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 3}" name="sender" v-model="text"  ></el-input>
          </el-form-item>
          
          <el-form-item style="text-align: start;">
              <span style="font-weight: bold; font-size:25px">夾帶附件</span><br>
              
                  <el-upload
                  class="avatar-uploader"
                  action="111"
                  :http-request = "customUpload"
                  :on-remove="handleRemove"
                  :on-exceed="handleExceed"
                  :on-change="handleChange"
                  :before-upload="handleUpload"
                  accept=".png,.jpg,.docx,.xlsx,.xls,.pdf"
                  multiple
                  :limit="5"
                  :file-list="fileList">
                  <el-button size="small" type="warning" icon="el-icon-plus" style="position:relative; top:15px; left:110px;"></el-button>
                  <div slot="tip" class="el-upload__tip">Keypro申請單、正式&amp;永久申請單、訂單等...</div>
                  </el-upload>
              
          </el-form-item>
          <el-button @click="submit_dialog=false" type="warning">取消</el-button>
          <el-button @click="submit" type="warning">送出</el-button>
        </el-form>
      </el-dialog>
  </div>
</template>

<script>
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'handle',
  data: function() {
        return { 
            user:[],
            tableData:[],
            all_Data:[],
            nofilter_info_Data:[],
            info_data:[],
            compare_Data:[],//修改的對照表(原本的)
            compare_edit_Data:[],//修改的對照表(修改過的)row
            detail_dialog:false,
            detail_data:[],
            cc:[],
            text:'',
            fileList:[],//顯示以上傳列表
            fileList_check:[],
            isLoading:true,
            cc_opt:[],
            user_opt:[],
            region_opt:[],
            contact_opt:[],
            type_opt:[
              {label: '正式',value: '正式'},
              {label: '測試',value: '測試'},
              {label: '出貨',value: '出貨'},
              {label: '永久',value: '永久'}
            ],
            submit_dialog:false,
            deter_require:[],
            contact_fliter:[],
            contact_input:'',
            cc_fliter:[],
            cc_input:'',
            warning: false,
            warning_message: '',
            detail_customer:'',
            detail_sn:'',
            detail_type:'',
            product_map:{},
            option_map:{},
            module_map:{},
            region_map:{},
            table:null,
            scroll_position:0,
            slider_position:0,
        }
  },
   watch: {
   },
  created(){
    this.axios.get('/get_product_groups_info_data',{
      headers: {'Content-Encoding': 'gzip'}
    }).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      
      this.info_data = JSON.parse(JSON.stringify(response.data))['info_data']
      var product_map = new Map()
      var option_map = new Map()
      var module_map = new Map()
      var sn_dict = JSON.parse(JSON.stringify(response.data))['sn_dict']

      this.axios.get('/show_all',{
          headers: {'Content-Encoding': 'gzip'},
          params:{
              user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))
          }
      }).then(response => {
        this.all_Data = JSON.parse(JSON.stringify(response.data));
        
        // 判斷使用者是否有待申請資料
        var user_edit = false;
        for(let edit of this.all_Data['edit_data'])
          if(edit['user'] == this.user[0])
            user_edit = true;
        if(!user_edit){
          this.isLoading = false
          return
        }
      
        for(let product of this.all_Data['product_data'])
          product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
        for(let option of this.all_Data['option_data'])
          option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})
        
        this.all_Data['module_data'].forEach(item => module_map.set(item['mod_uid'],item['caption']))

        var cc_set = new Set();
        for(let user of this.all_Data['sn_data'])
          for(let user_email of user['user'].split(','))
              if (user_email.indexOf("@") != -1)
                cc_set.add(user_email)
        cc_set.forEach(item => this.cc_opt.push({value:item,label:item}))

        this.cc_fliter = this.cc_opt

        var user_set = new Set();
        for(let user of this.all_Data['sn_data'])
          for(let user_email of user['user'].split(','))
              user_set.add(user_email)

        for(let user of user_set)
          this.user_opt.push({value:user,label:user})
        

        var contact_set = new Set();
        for(let info of this.info_data)
          for(let contact of info['contact'].split(';'))
            contact_set.add(contact)


        for(let contact of contact_set)
          this.contact_opt.push({value:contact,label:contact});
        

        for (let region of this.all_Data['region_data'])
          this.region_opt.push({value:region['name'],label:region['name']});
        
      
        var order_form = JSON.parse(JSON.stringify(this.info_data))

        let customer_map = {}
        for (let cus of this.all_Data['customer_data'])
          customer_map[cus['customer_id']] = {'name': cus['name'], 'site': cus['site']}

        let region_map = {}
        for (let reg of this.all_Data['region_data'])
          region_map[reg['region_id']] = {'name': reg['name'], 'description': reg['description']}
      
        var i = 0
        for (let info of this.info_data){
            if (sn_dict[info['sn']] != undefined){
                let customer_name = customer_map[sn_dict[info['sn']]['sn_id']]['name']
                let customer_site = customer_map[sn_dict[info['sn']]['sn_id']]['site']
                if( customer_site != ''){
                  order_form[i] = Object.assign(order_form[i],{
                    'customer': customer_name + '|' + customer_site,
                    'user': sn_dict[info['sn']]['user'],
                    'info': [sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]
                  })
                }
                else{
                  order_form[i] = Object.assign(order_form[i],{
                    'customer': customer_name,
                    'user': sn_dict[info['sn']]['user'],
                    'info': [sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]
                  })
                }

                if(isNaN(sn_dict[info['sn']]['region']))  //判斷是否為數字
                  order_form[i] = Object.assign(order_form[i],{'region':sn_dict[info['sn']]['region']})
                else if(sn_dict[info['sn']]['region'] != '')
                  order_form[i] = Object.assign(order_form[i],{'region':region_map[parseInt(sn_dict[info['sn']]['region'],10)]['name']})
                else
                  order_form[i] = Object.assign(order_form[i],{'region':''})
            }
            
            if(option_map.get(info['func_uid']) != undefined){
              order_form[i] = Object.assign(order_form[i],{'caption':option_map.get(info['func_uid'])['category_id']})
              order_form[i]['module'] = option_map.get(info['func_uid'])['caption']
              order_form[i]['product'] = module_map.get( option_map.get(info['func_uid'])['product_name'] );
            }
            else if (product_map.get(info['func_uid']) != undefined){//db有錯
              order_form[i] = Object.assign(order_form[i],{'caption':product_map.get(info['func_uid'])['category_id']})
              order_form[i]['product'] = product_map.get(info['func_uid'])['caption'];//edit介面需要
              order_form[i]['module'] = ''
            }
            else{ //非預期錯誤
              order_form[i] = Object.assign(order_form[i],{'caption':''})
              order_form[i]['product'] = ''
              order_form[i]['module'] = ''
            }


            if(module_map.get(info['type']) != undefined)
              order_form[i]['type'] = module_map.get(info['type']);//edit介面需要
            
            i++
        }
        this.nofilter_info_Data = JSON.parse(JSON.stringify(order_form))
        
        
        for(let edit of this.all_Data['edit_data'])
          if(edit['user'] == this.user[0])//只給使用者他申請的資料
            this.tableData = JSON.parse(edit['data'])
   

        for(let data of this.tableData){
          // 必填項目顏色
          this.deter_require.push({'count':false, 'expiration':false, 'user':false, 'contact':false});
          // 多選聯絡人處理
          if(data['contact_display'] == '')
              data['contact_display'] = []
          else
              data['contact_display'] = data['contact'].split(';')

        }
        this.product_map = product_map
        this.option_map = option_map
        this.module_map = module_map
        this.region_map = region_map

        this.slider_position = this.tableData.length
        this.isLoading = false
      })
      
    })
  },
  mounted() {//避免上傳檔案 並刷新頁面後 殘留檔案在heroku上
    let _this = this
    window.onbeforeunload = function (e) {
    if (_this.$route.name == "handle") {
      var upload_file_name = [];
      for(let file of _this.fileList)
        upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name
      _this.axios.get("/F5_handle",{
      params:{
        upload_file_name:JSON.stringify(upload_file_name)
      }})
    } else {
      window.onbeforeunload = null
    }
  };

    /*監聽捲軸*/
    this.table = this.$refs.handletable.bodyWrapper;
			
    //瀏覽器兼容
    let userAgent = navigator.userAgent;
    let ff = userAgent.indexOf("Firefox") > -1;
    let down = false;
    let up = false;
    let self = this;
    if (ff) {
      this.table.addEventListener('DOMMouseScroll', (event) => {
        let detail = event.detail;
        up = detail < 0;
        down = detail > 0;
        if(up){
          if(self.scroll_position > 0)
            self.scroll_position -= 1
        }
        else if (down){
          if(self.scroll_position < self.tableData.length - 20)
            self.scroll_position += 1
        }
        self.slider_position = self.tableData.length - self.scroll_position
      });
    }
    else{
      this.table.addEventListener('mousewheel', (event) => {
        let wheel = event.deltaY;
        up = wheel < 0;
        down = wheel > 0;
        if(up){
          if(self.scroll_position > 0)
            self.scroll_position -= 1
        }
        else if (down){
          if(self.scroll_position < self.tableData.length - 20)
            self.scroll_position += 1
        }
        self.slider_position = self.tableData.length - self.scroll_position
      });
    }
  }, // end of mounted
  methods:{
    cc_fliterer(val){
      this.cc_input = val;
      if (val) {
          this.cc_fliter = this.cc_opt.filter((item) => {
          if (String(item['label']).split('@')[0].includes(val)) 
              return true
          })
      }
      else{
          this.cc_fliter = this.cc_opt
      }
    },
    contact_selection_change(selection, index){
        this.tableData[index].contact = selection.join(';')
    },
    contact_fliterer(val){
        this.contact_input = val;
        if (val) {
            this.contact_fliter = this.contact_opt.filter((item) => {
            if (String(item['label']).split('@')[0].includes(val)) 
                return true
            })
        }
        else{
            this.contact_fliter = this.contact_opt
        }
    },
    cc_enter(){
      this.cc.push(this.cc_input)
    },
    contact_enter(index){
        this.tableData[index]['contact_display'].push(this.contact_input)
        this.tableData[index]['contact'] = this.tableData[index]['contact_display'].join(';')
    },
    type_change(index){//根據type自動調整期限
      let tempDate = new Date;
      if(this.tableData[index].type == '正式'){//*當 B ==正式, 日期設定在隔年的 1/31
          tempDate.setMonth(tempDate.getMonth()+12);
          this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-01-31'
      }
      if(this.tableData[index].type == '測試'){//* 當 B ==測試, 以季為單位: 3/31、6/30、9/30、12/31，若時間少於 30 天, 直接進下一季
          let currentMonth = tempDate.getMonth() +1
            //隔年3/31
            if(currentMonth==12){
                tempDate.setMonth(tempDate.getMonth()+12);
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-03-31'
            }
            //今年3/31
            else if(currentMonth==1 || currentMonth==2)
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-03-31'
            //今年6/30
            else if(currentMonth==3 || currentMonth==4 || currentMonth==5)
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-06-30'
            //今年9/30
            else if(currentMonth==6 || currentMonth==7 || currentMonth==8)
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-09-30'
            //今年12/31
            else if(currentMonth==9 || currentMonth==10 || currentMonth==11)
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-12-31'
            else
                this.tableData[index].expiration = ""
      }
      if(this.tableData[index].type == '出貨'){//* 當 B ==出貨, 日期設定12/31
          this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-12-31' 
      }
      if(this.tableData[index].type == '永久')//* 當 B ==永久, 日期設定 2100年12月31日
          this.tableData[index].expiration = '2100-12-31'
    },
    handleUpload(file){//阻止檔案容量>20MB時 依然顯示清單問題
      var size = 0  
      for(let file_before of this.fileList_check)
        size += file_before.size;   
      const size_check = size / 1024 / 1024 < 20
      if(!size_check){
        this.$message.error('上傳總容量不得高於20MB!');
        return size_check
      }
    },
    handleChange(file,fileList){//上傳檔案時 在本地端下載上傳檔案 (阻止跑去後台載檔案)
      this.fileList_check = fileList
      var size = 0  
      for(let file_before of fileList)
        size += file_before.size;   
      const size_check = size / 1024 / 1024 < 20
      if(size_check){
        this.fileList = fileList
        let fd = new FormData()
        fd.append('file', file.raw)
        fd.append('name',file.name)
        fd.append('type', file.raw.type)
        let config = {
          headers:{"Content-Type":"application/octet-stream;charset=utf-8"}
        };
        const instance = this.axios.create({
          withCredentials:true
        });
        this.axios.post('/upload_on_local',fd)//,config)
      }
    },
    customUpload(file){//此function拿來覆蓋action 使upalod不自動上傳
    },
    handleExceed(files, fileList) {
        this.$message.warning('限制上傳5個文件以下');
    },
    handleRemove(file, fileList) {//remove檔案時 移除本地端下載的檔案
      this.fileList = fileList
      this.axios.get("/delete_upload_local",{
        params:{
          name: file.name
        }})
    },
    tranfer_xlsx(data) {//web下載 xlsx
      if (!data) {
        return
      }
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
    },
    download(){
      this.axios.get("/download",{//跑去後端下載資料庫內的資料(web下載)
        params:{
          user:JSON.stringify(this.user)
        },
        responseType: 'blob'
        }).then((response)=>{
          this.tranfer_xlsx(response.data)
          
        })
    },
    test_data(row, index){//修改資料的防呆
        let row_correct = true;
        if(row['contact'] == ''){
            this.deter_require[index]['contact'] = true;
            row_correct =  false;
        }
        if(row['user'] == ''){
            this.deter_require[index]['user'] = true;
            row_correct =  false;
        }
        
        if(row['count'] == null || row['count'] == ""){
            this.deter_require[index]['count'] = true;
            row_correct =  false;
        }
        let regex = /^[0-9]*$/;

        if(!regex.test(row['count'])){
            this.deter_require[index]['count'] = true;
            row_correct =  false;
        }

        if(row['expiration'] == null || row['expiration'] == ""){
            this.deter_require[index]['expiration'] = true;
            row_correct =  false;
        }
        return row_correct;
    },
    async test_and_dialog(){
      console.log("in test_and_dialog")
      if(this.tableData.length == 0){
        this.$alert('請送出至少一筆資料', '提示', {center: true, type: 'warning'})
        return false
      }
      let test_index = 0
      let all_correct = true
      //重置deter_require
      for(let i of this.deter_require)
          Object.keys(i).forEach((j)=>{i[j] = false})

      this.warning = false
      this.warning_message = ''
      
      for(let row of this.tableData){
          let row_correct = true;
          if (row['operator'] == "刪除" || row['operator'].includes("多筆"))
            row_correct = true;
          else
            row_correct = this.test_data(row, test_index);
          if(row_correct == false)
              all_correct = false;
          test_index += 1;
      }
      if(!all_correct){
          this.warning = true
          this.warning_message = '請確認資料完整性'
          return false
      }

      // 檢查相同KeyID不同負責人(不合法)
      let sn_user_dict = {}
      let diff_sn = []
      for(let row of this.tableData){
          if(row['operator'] == '刪除' || row['operator'].includes("多筆"))
            continue
          if(row['sn'] in sn_user_dict){
              if(!sn_user_dict[row['sn']].includes(row['user']))
                  sn_user_dict[row['sn']].push(row['user'])
          }
          else{
              sn_user_dict[row['sn']] = [row['user']]
          }
      }

      for(let sn in sn_user_dict)
          if(sn_user_dict[sn].length >= 2)
              diff_sn.push(sn)
          

      if(diff_sn.length){
          await this.$confirm('相同KeyID僅能對應至相同負責人'
              , '提示', {
              confirmButtonText: '確定',
              cancelButtonText: '取消',
              showClose: false,
              type: 'warning',
              center: true,
          }).catch(()=>{
          })

          let index = 0
          for(let table of this.tableData){
              if((table['operator'] != '刪除') && (!table['operator'].includes('多筆'))&& (diff_sn.includes(String(table['sn']))))
                this.deter_require[index]['user'] = true
              index += 1
          }
          this.warning = true
          this.warning_message = '相同KeyID僅能對應至相同負責人'
          return false
      }

      let table_index = 0
      let user_change = {}
      let user_change_index = []
      for(let row of this.tableData){
          for(let sn of this.all_Data['sn_data']){
              if((row['sn'] == sn['sn']) && (row['user'] != sn['user'])){
                  user_change[row['sn']] = {'old_user': sn['user'], 'new_user': row['user']}
                  user_change_index.push(table_index)
              }
          }
          table_index += 1
      }

      //檢查負責人變更
      if(Object.keys(user_change).length){
          let conflict_html = '<table style="border-collapse:collapse"  width="500px" border="1">\
                                  <tr>\
                                      <th width="100px">KeyID</th>\
                                      <th width="200px">原負責人</th>\
                                      <th width="200px">新負責人</th>\
                                  </tr>'
          for(let sn in user_change){
              conflict_html += `<tr><td>${sn}</td><td>${user_change[sn]['old_user']}</td><td>${user_change[sn]['new_user']}</td> </tr>`
          } 
          conflict_html += '</table>'

          await this.$confirm(conflict_html
              , '負責人變更，是否繼續?', {
              confirmButtonText: '確定',
              cancelButtonText: '取消',
              showClose: false,
              type: 'warning',
              center: true,
              dangerouslyUseHTMLString: true,
              customClass:'product-conflict'
          }).then(() => {
              
          }).catch(() => {
              for(let index of user_change_index)
                  this.deter_require[index]['user'] = true
              all_correct = false
          });
      }

      if(!all_correct){
          this.warning = true
          this.warning_message = '請檢查負責人'
          return true
      }

      // 都合法後統一處理cc
      this.tableData.forEach((row) => {
        for(let each_contact of row['contact'].split(';'))
          if (!this.cc.includes(each_contact))
            this.cc.push(each_contact)
      })
      
      this.submit_dialog = true;
    },
    submit:function(){
      // if(this.text.trim() == ""){
      //   this.$message({message:'請輸入申請原因', type:'error'});
      //   return false;
      // }
      this.$confirm('是否送出申請?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          for(let i = 0;i < this.cc.length; i++)
            if(this.cc[i] == ''){
              this.cc.splice(i,1);
              i--;
            }

          if(this.cc.length != 0){//防止內文email格式出錯
            for(let index in this.cc)
              if(this.cc[index].indexOf('@') == -1){
                this.$message({message:'副本請填入正確email格式', type:'error'});
                return;
              }
          }
          console.log("before upload_file_name")
          var upload_file_name = [];
          for(let file of this.fileList)
            upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name
          

          this.submit_dialog = false;
          this.isLoading  = true;
          console.log("before /handle_send isLoading==True")
          //--- 由於heroku http timeout 只有30秒, 需要分不同階段request ---//

          // 階段一: 把 edit 資料轉到 applicatio 並儲存在application table
          this.axios.post("/handle_send",{
            origin_data:this.nofilter_info_Data,
            edit_data: this.tableData,
            content: {'user':this.user[0],'cc':this.cc.join(';'),'text':this.text,'reply':''},//申請人 副本 內文 審核人回覆(check頁面才會用到)
            upload_file_name:upload_file_name,
            phase: 'transfer_edit_to_application',
            my_application_id: 0,
          }).then((response)=>{
              console.log("in /handle_send transfer_edit_to_application response"+JSON.stringify(response))
              console.log("in /handle_send transfer_edit_to_application response.data"+JSON.stringify(response.data))
              if(!String(response.data).includes('error')){
                var new_app_id = response.data
                // 階段二: 寄送審核通知信
                this.axios.post("/handle_send",{
                  origin_data:this.nofilter_info_Data,
                  edit_data: this.tableData,
                  content: {'user':this.user[0],'cc':this.cc.join(';'),'text':this.text,'reply':''},//申請人 副本 內文 審核人回覆(check頁面才會用到)
                  upload_file_name:upload_file_name,
                  phase: 'verify_email',
                  my_application_id: new_app_id,
                }).then((response)=>{
                    console.log("in /handle_send verify_email response"+JSON.stringify(response))
                    console.log("in /handle_send verify_email response.data"+JSON.stringify(response.data))
                    if(response.data=='verify_email success'){
                      // 階段三: 寄送申請確認信
                      this.axios.post("/handle_send",{
                        origin_data:this.nofilter_info_Data,
                        edit_data: this.tableData(),
                        content: {'user':this.user[0],'cc':this.cc.join(';'),'text':this.text,'reply':''},//申請人 副本 內文 審核人回覆(check頁面才會用到)
                        upload_file_name:upload_file_name,
                        phase: 'comfirm_email',
                        my_application_id: new_app_id,
                      }).then((response)=>{
                          console.log("in /handle_send comfirm_email response"+JSON.stringify(response))
                          console.log("in /handle_send comfirm_email response.data"+JSON.stringify(response.data))
                          if(response.data=='comfirm_email success'){
                            this.isLoading = false
                            this.$message({ showClose: true, message: '郵件傳送成功!', type: 'success' });
                            this.$router.push({name: 'Show_All'});
                          }
                          else{
                            console.log(response.data)
                            this.isLoading = false
                            this.$message({ showClose: true, message: '申請確認信傳送失敗!', type: 'error' });
                          }
                      }).catch(() => {
                        console.log('no response error')
                        this.$message({ showClose: true, message: '郵件傳送失敗!', type: 'error' });
                      });
                    }
                    else{
                      console.log(response.data)
                      this.isLoading = false
                      this.$message({ showClose: true, message: '審核通知信傳送失敗!', type: 'error' });
                    }
                }).catch(() => {
                  console.log('no response error')
                  this.isLoading = false
                  this.$message({ showClose: true, message: '郵件傳送失敗!', type: 'error' });
                });
              }
              else{
                console.log(response.data)
                this.isLoading = false
                this.$message({ showClose: true, message: '資料庫操作失敗!', type: 'error' });
              }
          }).catch(() => {
            console.log('no response error')
            this.isLoading = false
            this.$message({ showClose: true, message: '郵件傳送失敗!', type: 'error' });
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消送出申請'
          });    
        })      
    },
    back:function(){
      var upload_file_name = [];
      for(let file of this.fileList)
        upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name

      this.axios.get("/handle_back_ShowAll",{//跑去後端修改資料庫內的資料
        params:{
            user:JSON.stringify(this.user),
            upload_file_name:JSON.stringify(upload_file_name)
        }
        })
      this.$router.push({name: 'Show_All'});
    },
    cancel:function(){
      this.$confirm("是否需要取消此次申請(申請資料將刪除)"
          , '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          showClose: false,
          type: 'warning',
          center: true
      }).then(() => {
        this.axios.get("/handle_delete",{//跑去後端刪除資料庫內的資料
          params:{
              Row: JSON.stringify([]),
              user:JSON.stringify(this.user)
          }
        }).then((response)=>{
            let res = response.data;
            this.back();
        });
      }).catch(() => {
        return;
      })
      
    },
    deleterow:function(row, index){
      //刪除頁面上資料
      this.deter_require.splice(index,1);
      this.tableData.splice(index,1);
      
      let self = this;
      this.axios.post("/handle_delete",{//跑去後端刪除資料庫內的資料
        Row: self.tableData,
        user:self.user
      }).then((response)=>{
        let res = response.data;
      });
    },
    cell_color({row, column, rowIndex, columnIndex}){//若原來資料與修改後資料不依 則顯示紅色
      if(column.label == '客戶')
        if(row.customer != this.compare_edit_Data[0].customer)
          return 'warning-row';
      /*if(column.label == '更新日期')
        if(row.issued != this.compare_edit_Data[0].issued)
          return 'warning-row';*/
      if(column.label == 'KeyID')
        if(row.sn != this.compare_edit_Data[0].sn)
          return 'warning-row';
      if(column.label == '產品名稱')
        if(row.product != this.compare_edit_Data[0].product)
          return 'warning-row';
      if(column.label == '版本')
        if(row.version != this.compare_edit_Data[0].version)
          return 'warning-row';
      if(column.label == '類型')
        if(row.type != this.compare_edit_Data[0].type)
          return 'warning-row';
      if(column.label == '數量')
        if(row.count != this.compare_edit_Data[0].count)
          return 'warning-row';
      if(column.label == '使用期限')
        if(row.expiration != this.compare_edit_Data[0].expiration)
          return 'warning-row';
      if(column.label == '地區')
        if(row.region != this.compare_edit_Data[0].region)
          return 'warning-row';
      if(column.label == '備註')
        if(row.comment != this.compare_edit_Data[0].comment)
          return 'warning-row';
      if(column.label == '聯絡人')
        if(row.contact != this.compare_edit_Data[0].contact)
          return 'warning-row';
      if(column.label == '負責人')
        if(row.user != this.compare_edit_Data[0].user)
          return 'warning-row';
    },
    compare_row:function(row,index){
      //--------------製造修改的對照表--------------//
      this.compare_Data.length = 0;
      this.compare_edit_Data.length = 0;
      for(let origin_info of this.nofilter_info_Data)
        if(JSON.stringify(origin_info['info_id']) == JSON.stringify(row['info_id'])){
          this.compare_Data.push(origin_info);
          this.compare_edit_Data.push(row);
          }
    },
    setCellColor({row,column,rowIndex,columnIndex}){
        let column_map = {8:'count', 11:'expiration', 12:'user', 13:'contact'}
        if(this.deter_require[rowIndex][column_map[columnIndex]])
            return 'background: red;;border:solid 1px #EAEAEA';
        else
            return 'border: solid 1px #EAEAEA';
    },
    querySearch_cc(queryString, cb){
        var results = queryString ? this.cc_opt.filter(this.createFilter(queryString)) : this.cc_opt;
        if(results.length == 0){
            if(!queryString.includes('@')){
              results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
              results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
            }
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_user(queryString, cb){
        var results = queryString ? this.user_opt.filter(this.createFilter(queryString)) : this.user_opt;
        if(results.length == 0 && !queryString.includes('@')){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_contact(queryString, cb){
        var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
        if(results.length == 0 && !queryString.includes('@')){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
    createFilter(queryString) {//搜尋建議選項
        return (any) => {return (String(any.value).toLowerCase().split('@')[0].includes(String(queryString).toLowerCase()));
      };
    },
    open_detail(row){
      this.detail_data = [];
      var caption = ''
      var module = ''
      var product = ''

      for(let info of this.info_data){
        if(row['sn'] == info['sn']){
          if(this.option_map.get(info['func_uid']) != undefined){
            caption = this.option_map.get(info['func_uid'])['category_id']
            module = this.option_map.get(info['func_uid'])['caption']
            product = this.module_map.get(this.option_map.get(info['func_uid'])['product_name'])
          }
          else if (this.product_map.get(info['func_uid']) != undefined){
            caption = this.product_map.get(info['func_uid'])['category_id']
            module = ''
            product = this.product_map.get(info['func_uid'])['caption']
          }
          else{
            caption = ''
            module = ''
            product = info['func_uid']
          }

          this.detail_data.push({'caption':caption, 'product':product, 'module':module, 
            'version':info['version'], 'count': info['count'], 'type':this.module_map.get(info['type']),
            'region': this.region_map[parseInt(row['region'])]['name'], 'expiration':info['expiration']
          })
        }
      }
      
      this.detail_customer = row.customer
      this.detail_sn = row.sn
      this.detail_type = row.operator
      this.detail_dialog = true;
    },
    slider_input(val){
      this.scroll_position = this.tableData.length - val
    },
  }//end of method
}
</script>

