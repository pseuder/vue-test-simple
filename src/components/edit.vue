<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-table /deep/ .exceed-row {
    background: #FFF0D2;
}
.el-table /deep/ .warning-row {
    background: #FFF0D2;
}
.el-table /deep/ .success-row {
    background: #FFF0D2;
}
.el-table /deep/ th, 
.el-table /deep/ tr {
    background-color: #FFBE3F;
    color:#000;
    border: solid 1.5px #c0c0c0;
    font-size: 18px;
}
.el-table /deep/ .cell{
    word-break: break-word;
    display: contents;
}
.fade-enter,
.fade-leave-active{
    opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
#menu {
    position: fixed;
    top: 30%;
    right: 25px;
    z-index:120;
}
.OperatorButton:hover {
    font-size:30px;
}
.OperatorButton {
    cursor: pointer;
    font-size:25px;
    position:relative;
    bottom:20px;
    display:inline;
    border-radius: 10px;
    padding: 10px 10px;
    transition: all 0.4s;
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
}
.el-button{
    text-align:center;  
    vertical-align:middle; 
    margin-top: 2px;
}
.submit_button{
    position:relative;
    left: 37%;
    width:150px;
}
.el-input /deep/ .el-input__inner{
    overflow: auto;
}
.heading{
    font-size: 40px;
    color: #000;
    font-weight: bold;
    position: relative;
    top: -20px;
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
</style>
<style>
.el-notification {
    background-color: #fdf6ec;
    border-color: #faecd8;
    width:350px !important;
    left:40%;
}
.el-autocomplete-suggestion {
  width: auto!important;
}
</style>

<template>
    <div>
        <div id = "menu">
            <div><el-button class="OperatorButton"  type="warning" icon="el-icon-delete" @click="GoDelete" ></el-button></div>
            <div><el-button class="OperatorButton"  type="warning" icon="el-icon-timer" @click="Go_Edit_time" ></el-button></div>
        </div>

        <div>
            <el-header style="top:-60px; text-align: right; font-size:20px; position:relative; background-color:#EBD1A0 ; ">
                <div style="position:absolute; left:30px; top:3px; cursor:pointer;" @click="cancel">License Application Service</div>

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
        <div class="heading">修改</div>
        <div v-show="warning" style="color: red; font-size:20px; font-weight: bold;">{{warning_message}}</div>
        <div style="margin:0 auto; z-index: 110; width:1670px; width:90%">
            <el-table
            :row-class-name="tableRowColor"
            @selection-change="handleSelectionChange"
            ref="edittable"
            :data="tableData"
            :row-style="{height:0+'px'}"
            :cell-style="setCellColor"
            height= 650px>
            <el-table-column type="selection" align="center" prop="" label="編輯"  width="50"></el-table-column>
            <el-table-column align="center" width="65px" label=" ">
              <template slot-scope="scope">
                {{ scope.$index +1  }}
              </template>
            </el-table-column>
            <el-table-column align="center" prop="" label="操作"  width="80">
                <template slot-scope = "{$index,row}" >
                    <el-button  type="warning" circle icon="el-icon-refresh-right" @click="restore($index, row)" size = "mini"></el-button>
                </template>
            </el-table-column>
            
            <el-table-column align="center" prop="customer" label="客戶">
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="customer" v-model="row.customer" disabled ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="sn" label="KeyID" > 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="sn" v-model="row.sn"  disabled></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="product" label="產品" > 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="product" v-model="row.product"  disabled></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="module" label="模組" > 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="module" v-model="row.module"  disabled></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="version" label="版本" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="version" v-model="row.version" ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="count" label="數量" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="number" name="count" v-model="row.count"  @blur="all_column_change($index, 'count')"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="type" label="類型" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-select  v-model="row.type"  @change="type_change($index)">
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
            <el-table-column align="center" prop="region" label="地區" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-select  v-model="row.region" @change="all_column_change($index, 'region')">
                        <el-option
                            v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="expiration" label="使用期限" width="145"> 
                <template slot-scope = "{$index,row}">
                    <el-date-picker  type="date" value-format="yyyy-MM-dd" name="expiration" v-model="row.expiration" style="width:140px"  @blur="all_column_change($index, 'expiration')">
                    </el-date-picker>
                </template>
            </el-table-column>
            
            <el-table-column align="center" prop="user" label="負責人"> 
                <template slot-scope = "{$index,row}">
                    <el-autocomplete  v-model="row.user" :fetch-suggestions="querySearch_user" popper-append-to-body="false" @blur="all_column_change($index, 'user')" 
                    placeholder="僅限一位負責人" />
                </template>
            </el-table-column>
            <el-table-column align="center" prop="contact" label="聯絡人" width="200"> 
                <template slot-scope = "{$index,row}">
                    <el-select v-model="row.contact_display" @change="((item)=>{contact_selection_change(item, $index)})" filterable clearable multiple
                        :filter-method="contact_fliterer" @keyup.enter.native="contact_enter($index)" class = "contact-input" placeholder = "請輸入後按enter">
                        <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="comment" label="備註"> 
               <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="comment" v-model="row.comment" @blur="all_column_change($index, 'comment')"></el-input>
                </template>
            </el-table-column>
            
            </el-table>
        </div>
        <el-button class="submit_button" @click="cancel" size = "medium"  type="warning">取消</el-button>
        <el-button class="submit_button" @click="submit" size = "medium"  type="warning">修改</el-button>
    </div>
</template>

<script>

export default {
    name: 'edit',
    data: function() {
        return { 
            all_Data:{},//整個資料庫所有數據
            tableData:[],
            origin_Data:[],//原始整體資料(不被修改)
            checked_Data:[],//被勾選的資料
            user_opt:[],
            region_opt:[],
            caption_opt:[],
            product_opt:[],
            contact_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            deter_require:[],
            contact_fliter:[],
            contact_input:'',
            warning: false,
            warning_message: '',
        }
        
    },
    created(){
        this.user = JSON.parse(this.$route.query.user);//把user傳進來
        this.all_Data = JSON.parse(this.$route.query.all_Data);


        for (let caption of this.all_Data['product_data']){
            this.caption_opt.push({value:caption['caption'],label:caption['caption']});
        }
        for (let region of this.all_Data['region_data']){
            this.region_opt.push({value:region['name'],label:region['name']});
        }
        for (let contact of this.all_Data['user_data']){
            if(contact['email'].indexOf("@") > 0)
                this.contact_opt.push({value:contact['email'],label:contact['email']});
        }
        var user_set = new Set();
        for(let user of this.all_Data['sn_data'])
            for(let user_email of user['user'].split(','))
                user_set.add(user_email)

        for(let user of user_set){
            this.user_opt.push({value:user,label:user})
        }
        this.contact_fliter = this.contact_opt;
        var i = 0;
        let func_uid_Data = [];
        for(let check of JSON.parse(this.$route.query.checked_Data)){
            check = Object.assign(check,{'operator':'修改','index':i});//增加index讓 row中有index
            if(check['contact_display'] == '')
                check['contact_display'] = []
            else
                check['contact_display'] = check['contact'].split(';')
            func_uid_Data.push(check);
            i++;
        }
        for(let color of func_uid_Data){//新增color為判斷是否為更改資料
            color = Object.assign(color,{'color':0})
        }

        this.origin_Data = JSON.parse(JSON.stringify(func_uid_Data));
        this.tableData = JSON.parse(JSON.stringify(func_uid_Data));
   
        //必填項目顏色
        for(let i of this.tableData){
            this.deter_require.push({'count':false, 'expiration':false, 'user':false, 'contact':false});
        }
        
    },
    methods:{
    all_column_change(index, type){
        if(this.tableData.length >1){
        if(type == 'count'){
            if(this.origin_Data[index]['count'] != this.tableData[index]['count']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftNumber" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftNumber').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['count'] = that.tableData[index]['count'];
                    }
                    that.$notify.closeAll();
                })
            }
        }
        if(type == 'expiration'){
            if(this.origin_Data[index]['expiration'] != this.tableData[index]['expiration']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftExpiration" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftExpiration').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['expiration'] = that.tableData[index]['expiration'];
                    }
                    that.$notify.closeAll();
                })
            }
        }
        if(type == 'user'){
            if(this.origin_Data[index]['user'] != this.tableData[index]['user']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftUser" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftUser').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['user'] = that.tableData[index]['user'];
                    }
                    that.$notify.closeAll();
                })
            }
        }
        if(type == 'region'){
            if(this.origin_Data[index]['region'] != this.tableData[index]['region']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftRegion" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftRegion').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['region'] = that.tableData[index]['region'];
                    }
                    that.$notify.closeAll();
                })
            }
        }
        if(type == 'contact'){
            if(this.origin_Data[index]['contact'] != this.tableData[index]['contact']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftContact" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftContact').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['contact'] = that.tableData[index]['contact'];
                        that.contact_change(that.tableData[i]['contact'], i)
                    }
                    that.$notify.closeAll();
                })
            }
        }
        if(type == 'comment'){
            if(this.origin_Data[index]['comment'] != this.tableData[index]['comment']){
                this.$notify.closeAll();
                this.$notify({
                    dangerouslyUseHTMLString: true,
                    message: '<span style="font-size:18px; color: #606266;"><i class="el-icon-info"></i>是否套用至下面全部資料?</span>'+
                    '<button id="modiftComment" style="font-size:18px; border-radius: 8px; background-color:#ffbe3f; border: none; cursor: pointer; margin:0px 10px; color:black;">確定</button>'
                });

                let that = this;
                document.getElementById('modiftComment').addEventListener('click', function() {
                    for(let i=index+1; i<that.tableData.length; i++) {
                        that.tableData[i]['comment'] = that.tableData[index]['comment'];
                    }
                    that.$notify.closeAll();
                })
            }
        }
        }
    },
    Logout:function(){
      sessionStorage.clear();
      this.$router.push('/login');
    },
    GoDelete(){
        if(this.checked_Data.length == 0 || this.checked_Data[0] == undefined){
            this.$message({message: '請選取欲刪除的資料',type: 'warning'});
            return;
        }

        for(let i of this.checked_Data){
            for(let j in this.tableData){
                if(JSON.stringify(i) == JSON.stringify(this.tableData[j])){
                    this.tableData.splice(j,1);
                    this.origin_Data.splice(j,1);
                    this.deter_require.splice(j,1);
                }
            }
        }
    },
    Go_Edit_time(){
        if(this.checked_Data.length == 0 || this.checked_Data[0] == undefined){
        this.$message({message: '請選取欲修改時間的資料',type: 'warning'});
        return;
        }
        this.$prompt("請輸入到期日",'到期日修改',{
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            inputType:'date',
            inputPattern:/\d.\d.\d/,
            inputErrorMessage:'輸入日期不合法!'
        }).then(({ value }) => {
            for(let i of this.checked_Data){
                for(let j in this.tableData){
                    if(JSON.stringify(i) == JSON.stringify(this.tableData[j])){
                        this.tableData[j]['expiration'] = value;
                        break;
                    }
                }
            }
            this.$refs.edittable.clearSelection();
        })
        
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
    test_edit_add(row, index){//修改資料的防呆
        let row_correct = true;
        if(row['contact'] == ''){
            this.deter_require[index]['contact'] = true;
            row_correct =  false;
        }
        let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

        if(row['user'].search(emailRule) == -1){
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

        var customer_map = new Map()
        for(let customer of this.all_Data['customer_data']){
            if(customer['site'] != '')
                customer_map.set(customer['customer_id'],customer['name']+'|'+customer['site'])
            else
                customer_map.set(customer['customer_id'],customer['name'])
        }
        

        return row_correct;
    },
    contact_change(input, index){
        this.tableData[index].contact_display = input.split(';')
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
    contact_enter(index){
        this.tableData[index]['contact_display'].push(this.contact_input)
        this.tableData[index]['contact'] = this.tableData[index]['contact_display'].join(';')
    },
    //當select 有變化時執行 且val是所選row的所有資訊(type:array)//
    handleSelectionChange (val) {
        this.checked_Data = JSON.parse(JSON.stringify(val));
    },
    submit:async function(){//送出到編輯介面
        let test_index = 0
        let all_correct = true
        //重置deter_require
        for(let i of this.deter_require)
            Object.keys(i).forEach((j)=>{i[j] = false})
        
        this.warning = false
        this.warning_message = ''
        
        for(let row of this.tableData){
            let row_correct = true;
            row_correct = this.test_edit_add(row, test_index);
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
                if(diff_sn.includes(String(table['sn']))){
                    this.deter_require[index]['user'] = true
                }
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
    
                
        // for(let user_ch in user_change){
        //     await this.$confirm(`此ID:〈${String(user_ch)}〉原負責人為〈${user_change[user_ch][0]}〉將修改為〈${user_change[user_ch][1]}〉`
        //         , '提示', {
        //         confirmButtonText: '確定',
        //         cancelButtonText: '取消',
        //         showClose: false,
        //         type: 'warning',
        //         center: true
        //     }).catch(() => {
        //         all_correct = false;
        //     });
        // }

        // if(!all_correct)
        //     return false
        
        this.axios.post("/save_to_handle",{
            checked_Data: this.tableData,
            content:'none',
            user:this.user
        }).then(()=>{
            this.$confirm('', '下一步', {
                confirmButtonText: '送出申請',
                cancelButtonText: '返回主頁面',
                type: 'warning',
                center: true
            }).then(() => {
                this.$router.push({name: 'handle'});

            }).catch(() => {
                this.$router.push({name: 'Show_All'});
            });
        });
    
             
    },
    cancel:function(){
        this.$router.push({name: 'Show_All'});
    },
    restore:function(index, row){//回復成原本的資料列
        for(let i of Object.keys(this.origin_Data[index])){
            this.tableData[index][i] = this.origin_Data[index][i]
        }
    },
    datachange:function(){//跟原資料比較 若不一致 則color=1
        this.tableData = Object.assign([], this.tableData);//為了更新觸發watch
    },
    //------------------------列變色判斷------------------------------//
    tableRowColor({row, rowIndex}) {//被修改的資料->紅色
        if(this.tableData[rowIndex]['color'] == 1)
            return 'exceed-row';
        else
            return 'success-row';
    },
    //-------------------以下是el-input建議所需的function-------------------//
    querySearch_contact(queryString, cb){
        var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
        if(results.length == 0 && !queryString.includes('@')){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
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
    createFilter(queryString) {//搜尋建議選項
        return (any) => {
          return (String(any.value).toLowerCase().split('@')[0].includes(String(queryString).toLowerCase()));
        };
    },

    setCellColor({row,column,rowIndex,columnIndex}){
        let column_map = {8:'count', 11:'expiration', 12:'user', 13:'contact'}
        if(this.deter_require[rowIndex][column_map[columnIndex]])
            return 'background: red;;border:solid 1px #EAEAEA';
        else
            return 'border: solid 1px #EAEAEA';
    },


  }
}
</script>

