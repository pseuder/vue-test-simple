<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .el-button{
    font-size: 14px; 
    text-align:center;  
    vertical-align:middle; 
    margin-top: 2px;
  }
  .el-input {
    font-size: 14px; 
    margin-top: 10px;
    width: 90%;
  }
  .el-form-item{
    font-size: 14px;
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
  .apply_record_box{
    border-radius: 15px;
    height:280px;
    margin-bottom: 50px;
    background: navajowhite;
  }
  .product_list_box{
    border-radius: 15px;
    height:280px;
    background: burlywood;

  }
  .shadow_box{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  }
</style>


<style scoped>
  .header{
    width: 102%;
    position: relative;
    top: -60px;
    left: -8px;
    text-align: right;
    font-size: 20px;
    background-color: rgb(235, 209, 160);
  }
  .search-box{
    position: relative;
    width: 310px;
    height: 100%;
    background: wheat;
  }
  .search-box-item{
    margin: 15px;
    display: flex;
    margin: 15px -5px;
  }
  .search-box-item-font{
    width: 110px;
    text-align: right;
    margin: auto 10px;
    font-weight: bold;
  }
  .search-box-expiring{
    position: relative;
    left: -45px;
  }
  .search-box-expired{
    position: relative;
    left: -74px;
    margin-top: 20px;
  }
  .search-box-expiring /deep/ .el-checkbox__inner{
    width: 20px;
    height: 20px;
    margin-right: 14px;
  }
  .search-box-expired /deep/ .el-checkbox__inner{
    width: 20px;
    height: 20px;
    margin-right: 20px;
  }
  .search-drawer /deep/ .el-drawer.ltr{
    background: wheat;
    overflow-y: overlay;
    height: 100%;
  }
  .el-drawer__wrapper{
    width: 340px !important;
    top:60px !important;
  }
  .search-drawer /deep/ .modal{
    width: 340px;
  }
  .main-table /deep/ .exceed-row {
    background: #FE7F6E;
    color:#000;
    border: 1.5px solid silver
  }
  .main-table /deep/ .warning-row {
    background: #FFF063;
    color:#000;
    border: 1.5px solid silver
  }
  .main-table /deep/ .success-row {
    background: #FFF0D2;
    color:#000;
    border: 1.5px solid silver
  }
  .main-table /deep/ th, 
  .main-table /deep/ tr {
    background-color: #FFBE3F;
    color:#000;
    border: 1.5px solid silver
  }
  .el-table /deep/ .cell{
    word-break: break-word;
  }
</style>
<template>
  <div>
    <div>
      <el-header class="header">
        <div style="position:absolute;left:30px;top:3px;cursor:pointer;" @click="reload"> License Application Service</div>
        <div>
          <el-button-group class="mode-switch">
            <el-button type="warning" @click="mode_switch('product')" style="background: #ebd1a0; color: white; border-color: #e6a23c;">產品</el-button>
            <el-button type="warning" @click="mode_switch('KeyID')">SN</el-button>
          </el-button-group>
        </div>
        <el-popover trigger="hover" width="200" placement="bottom" :close-delay="delay_time">
          
          <div><span>成員名稱: {{user[0]}}</span></div>
          <div><span>-----------------------------------------</span></div>
          <div >
            <span>單頁筆數:<span>
            <el-select style="width:100px;" v-model="pagesize_display" size="small" @change="pagesize_change" @visible-change="select_change">
              <el-option key= '10' label="10" value="10"></el-option>
              <el-option key= '50' label="50" value="50"></el-option>
              <el-option key= 'all' label="all" value="all"></el-option>
            </el-select>
          </div>
          <div><el-button  @click="$router.push({name: 'admin', query:{}})"  type="primary" icon="el-icon-setting">後台管理</el-button></div>
          <div><el-button  @click="Logout"  icon="el-icon-switch-button" style="background:#F56C6C; color:#FFFFFF; width:117px;">登出</el-button></div>
         
          <el-button  class="memeber_button" slot="reference" icon="el-icon-s-custom"></el-button>
        </el-popover>
      </el-header>
      <div style="position:relative; top:-30px; font-size:20px;" align="right">
        <span style="background-color: #ffb7b7">紅色</span>代表過期、
        <span style="background-color: #FFFF30">黃色</span>代表一個月內過期
        <span style="margin-left: 60px;">Last update: {{update_time}}</span>
      </div>
    </div>

    <el-button v-show="search_drawer_btn" @click="drawer_open" type="warning" icon="el-icon-search" circle
      style="position: fixed; top: 80px; left: -20px; padding: 15px; font-size: 20px;"> </el-button>

    <el-drawer title="" :visible.sync="search_drawer" direction=ltr size=340 class="search-drawer" :show-close="false" @closed="search_drawer_btn=true"
      :modal-append-to-body="false" :modal="false" :with-header="false">
      <!-- 搜尋欄 -->
      <div class="search-box">
        <div style="left: 40px; bottom: -10px; position: relative;">
          <el-button type="warning"  icon="el-icon-s-open" @click="clear_filter">重置</el-button>
          <el-button type="warning"  icon="el-icon-search" @click="category_filter">搜尋</el-button>
        </div>

        <div class="search-box-item">
          <div class="search-box-item-font">客戶</div>
            <el-select v-model="customer_value" multiple  placeholder="客戶" filterable clearable @keyup.enter.native="customer_enter" 
              :filter-method="customer_fliterer" style="width:400px;">
              <el-option v-for="opt in customer_fliter"  :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-item">
          <div class="search-box-item-font">KeyID</div>
            <el-select v-model="KeyID_value" multiple  placeholder="KeyID" filterable clearable @keyup.enter.native="KeyID_enter" 
              :filter-method="KeyID_fliterer" style="width:400px;">
              <el-option v-for="opt in KeyID_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-item">  
          <div class="search-box-item-font">地區</div>
            <el-select v-model="region_value" multiple  placeholder="地區" filterable clearable @keyup.enter.native="region_enter" 
              :filter-method="region_fliterer" style="width:400px;">
              <el-option v-for="opt in region_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-item">  
          <div class="search-box-item-font">負責人</div>
            <el-select v-model="user_value" multiple  placeholder="負責人" filterable clearable @keyup.enter.native="user_enter" 
              :filter-method="user_fliterer" style="width:400px;">
              <el-option v-for="opt in user_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-item">
          <div class="search-box-item-font">到期日</div>
            <el-date-picker  value-format="yyyy-MM-dd" size="mini" v-model="expiration_value" type="daterange" 
            range-separator="_" start-placeholder="開始日期" end-placeholder="結束日期" style="width:345px; height:37px; margin-right: 25px; margin-top: 8px;" />
        </div>

        <div class="search-box-item">  
          <div class="search-box-item-font">備註1</div>
            <el-select v-model="note1_value" multiple  placeholder="備註1" filterable clearable @keyup.enter.native="note1_enter" 
              :filter-method="note1_fliterer" style="width:400px;">
              <el-option v-for="opt in note1_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-item">  
          <div class="search-box-item-font">備註2</div>
            <el-select v-model="note2_value" multiple  placeholder="備註2" filterable clearable @keyup.enter.native="note2_enter" 
              :filter-method="note2_fliterer" style="width:400px;">
              <el-option v-for="opt in note2_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        
        <div class="search-box-item">  
          <div class="search-box-item-font">備註3</div>
            <el-select v-model="note3_value" multiple  placeholder="備註3" filterable clearable @keyup.enter.native="note3_enter" 
              :filter-method="note3_fliterer" style="width:400px;">
              <el-option v-for="opt in note3_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        
        <div class="search-box-item">  
          <div class="search-box-item-font">備註4</div>
            <el-select v-model="note4_value" multiple  placeholder="備註4" filterable clearable @keyup.enter.native="note3_enter" 
              :filter-method="note3_fliterer" style="width:400px;">
              <el-option v-for="opt in note3_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>


        <div class="search-box-item">  
          <div class="search-box-item-font">備註5</div>
            <el-select v-model="note3_value" multiple  placeholder="備註5" filterable clearable @keyup.enter.native="note3_enter" 
              :filter-method="note3_fliterer" style="width:400px;">
              <el-option v-for="opt in note3_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>

        <div class="search-box-expiring">
          <el-checkbox v-model="expiring_check">
            <el-input v-model="expiring_days" placeholder="" style="width:55px"></el-input>
            <span style="font-weight: bold;">天內到期</span>
          </el-checkbox>
        </div>

        <div class="search-box-expired">
          <el-checkbox v-model="expired_check">
            <span style="font-weight: bold;">已過期</span>
          </el-checkbox>
        </div>
      </div>
    
        <el-button @click="drawer_close" type="warning" icon="el-icon-search" circle
          style="position: fixed; top: 80px; left: 290px; padding: 15px; font-size: 20px;"> 
        </el-button>
      
    </el-drawer>

    <div style="display:flex;">
      <div style="flex-basis:280px;" v-show="search_drawer"></div>
      <div style="margin: 0px auto; width:75%" id = "showtable">
        <div v-show="searched_data_num" style="color: red; font-size:20px; font-weight: bold;">已搜尋到{{searched_data_num}}筆資料</div>
        <el-table 
          ref="showtable" 
          :row-class-name="tableRowColor"
          :row-style="{height:0+'px'}"
          :cell-style="{border: 'solid 1px #EAEAEA'}"
          @sort-change='sortChange'
          @selection-change="handleSelectionChange"
          :header-cell-class-name="selection_column_style"
          :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)" 
          height= 650px
          border
          v-loading="enter_loading"
          class="main-table"
        >
        <!-- <el-table-column type="selection" align="center" prop="checked" label="" ></el-table-column> -->
        <el-table-column align="center"  prop="customer" label="客戶" sortable='custom'></el-table-column>
        <el-table-column align="center"  prop="sn" label="KeyID" sortable='custom'></el-table-column>
        <el-table-column align="center"  prop="region" label="區域" sortable='custom'></el-table-column>
        <el-table-column align="center"  prop="user" label="負責人" sortable='custom'> </el-table-column>
        <el-table-column align="center"  prop="expiration" label="到期日" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  prop="note1" label="備註1" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  prop="note2" label="備註2" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  prop="note3" label="備註3" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  prop="note4" label="備註4" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  prop="note5" label="備註5" sortable='custom' show-overflow-tooltip></el-table-column>
        <el-table-column align="center"  label="編輯備註" width="80">
          <template slot-scope="scope">
            <i size="mini" class="el-icon-edit" @click.stop="form.current_edit_data=scope.row; dialogFormVisible=true" 
              style="cursor: pointer;" />
          </template>
        </el-table-column>
        <!-- 跳視窗 -->
        <el-table-column align="center" width="48px" label="">
          <template slot-scope="scope">
          <i style="font-size:20px; cursor: pointer; z-index: 200; position: relative;" class="el-icon-arrow-right" 
            @click.stop = "detail_form(scope.row)"></i>
          </template>
        </el-table-column>
        </el-table>
      
      <div class="pagination">
        <el-pagination 
          background
          :current-page.sync="currentPage" 
          :page-size.sync="pagesize" 
          layout="prev, pager, next" 
          :total="tableData.length" >
        </el-pagination>
      </div>
      </div>
    </div>
    <div>
      <el-dialog  :visible.sync="detail" width="1500px" height="750px">
        <!-- KeyID申請紀錄 -->
        <div class="apply_record_box">
          <div style="font-size:25px;">{{detailForm.keyID}}申請紀錄</div>
          <el-table :data="detailForm.apply_record" style="width: 100%" class="fold shadow_box" :row-style="{height: '10px'}" height="250">
            <el-table-column type="expand">
              <template slot-scope="props">
                  <el-table :data="props.row.data">
                    <el-table-column prop="operator" label="操作" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="customer" label="客戶" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="sn" label="KeyID" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="product" label="產品" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="module" label="模組" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="version" label="版本" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="type" label="類型" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="count" label="數量" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="expiration" label="到期日期" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="region" label="地區" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="comment" label="備註" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="contact" label="聯絡人" show-overflow-tooltip></el-table-column>
                  </el-table>
              </template>
            </el-table-column>
            <el-table-column label="申請ID" prop="id"></el-table-column>
            <el-table-column label="申請日期" prop="date"></el-table-column>
            <el-table-column label="申請人" prop="applicant"></el-table-column>
            <el-table-column label="狀態" prop="status"></el-table-column>
            <el-table-column label="驗證時間" prop="verify_time"></el-table-column>
          </el-table>
        </div>
        
        <!-- KeyID產品清單 -->
        <div class="product_list_box">
          <div style="font-size:25px;">{{detailForm.keyID}}產品清單</div>
          <el-table :data="detailForm.product_list" style="width: 100%" class="fold shadow_box" :row-style="{height: '10px'}" height="250">
            <el-table-column label="客戶" prop="customer" show-overflow-tooltip> </el-table-column>
            <el-table-column label="KeyID" prop="sn" show-overflow-tooltip> </el-table-column>
            <el-table-column label="產品類別" prop="category" show-overflow-tooltip> </el-table-column>
            <el-table-column label="產品" prop="product" show-overflow-tooltip> </el-table-column>
            <el-table-column label="模組" prop="module" show-overflow-tooltip> </el-table-column>
            <el-table-column label="版本" prop="version" show-overflow-tooltip> </el-table-column>
            <el-table-column label="數量" prop="count" show-overflow-tooltip> </el-table-column>
            <el-table-column label="類型" prop="type" show-overflow-tooltip> </el-table-column>
            <el-table-column label="地區" prop="region" show-overflow-tooltip> </el-table-column>
            <el-table-column label="聯絡人" prop="contact" show-overflow-tooltip> </el-table-column>
            <el-table-column label="到期日" prop="expiration" show-overflow-tooltip> </el-table-column>
            <el-table-column label="備註" prop="comment" show-overflow-tooltip> </el-table-column>
          </el-table>
        </div>
      </el-dialog>


      <el-dialog title="修改備註" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="備註1"><el-input v-model="form.note1" :placeholder="form.current_edit_data.note1" ></el-input></el-form-item>
          <el-form-item label="備註2"><el-input v-model="form.note2" :placeholder="form.current_edit_data.note2" ></el-input></el-form-item>
          <el-form-item label="備註3"><el-input v-model="form.note3" :placeholder="form.current_edit_data.note3" ></el-input></el-form-item>
          <el-form-item label="備註4"><el-input v-model="form.note4" :placeholder="form.current_edit_data.note4" ></el-input></el-form-item>
          <el-form-item label="備註5"><el-input v-model="form.note5" :placeholder="form.current_edit_data.note5" ></el-input></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="dialogFormVisible = false; handleEdit()">確 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script>
//合併排序法
function merge(left, right,name){
  const result = [];
  let leftIndex = 0;
  let rightIndex = 0;
  while(leftIndex < left.length && 
        rightIndex < right.length){
     if(left[leftIndex][name] > right[rightIndex][name]){
       result.push(left[leftIndex]);
       leftIndex++;
     } else{
       result.push(right[rightIndex]);
       rightIndex++
    }
  }  
  return result.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));
}

//升序排序
function ascending_order(initial_Data,name){
  if (initial_Data.length === 1) {
    return initial_Data
  }
  // 將陣列切成左右
  const length = initial_Data.length;
  const middle = Math.floor(length / 2)
  const left = initial_Data.slice(0, middle) 
  const right = initial_Data.slice(middle)

  return merge(
    ascending_order(left,name),
    ascending_order(right,name),
    name
  )
}

export default {
  name: 'KeyID',
  data () {
    return {
      all_Data:{},//整個資料庫的數據
      user_setting:{},
      tableData: [],//要顯示的tabledata
      customer_data:[],
      region_data:[],
      origin_data:[],
      filter_Data:[],
      sort_Data:[],
      application_data:[],
      apply_record_map:{},
      info_data:[],
      product_list_map:{},
      user:[],
      checked_Data:[],//勾選row的資料
      //篩選欄位建議選項及選中值
      mode:'KeyID',//顯示模式
      update_time:'',//push heroku的時間
      pagesize_display:'',
      pagesize:50,
      currentPage: 1,
      select_out:false,
      dialogFormVisible: false,
      detail:false,
      form:{
        current_edit_data:'',
        note1:'',
        note2:'',
        note3:'',
        note4:'',
        note5:'',
      },
      detailForm:{
        keyID:'',
        apply_record:[],
        product_list:[],
      },
      //篩選欄位建議選項及選中值
      customer_opt:[],
      customer_value:'',
      customer_fliter:[],
      customer_input:"",
      customer_dict:{},
      KeyID_opt:[],
      KeyID_value:'',
      KeyID_fliter:[],
      KeyID_input:"",
      region_opt:[],
      region_value:'',
      region_fliter:[],
      region_input:"",
      user_opt:[],
      user_value:'',
      user_fliter:[],
      user_input:"",
      expiration_opt:[],
      expiration_value:null,
      expiring_days:30,
      expiring_check:false,
      expired_check:false,
      note1_opt:[],
      note1_value:'',
      note1_fliter:[],
      note1_input:"",
      note2_opt:[],
      note2_value:'',
      note2_fliter:[],
      note2_input:"",
      note3_opt:[],
      note3_value:'',
      note3_fliter:[],
      note3_input:"",
      note4_opt:[],
      note4_value:'',
      note4_fliter:[],
      note4_input:"",
      note5_opt:[],
      note5_value:'',
      note5_fliter:[],
      note5_input:"",
      enter_loading:true,
      search_drawer:false,
      search_drawer_btn:true,
      searched_data_num:0,
    }
  },
  created () {//創建原始資料
    this.axios.get('/KeyID',{
      params:{
         user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))
      }
    }).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
      this.user_setting = JSON.parse(JSON.stringify(this.all_Data['user_setting']))
      this.customer_data = JSON.parse(JSON.stringify(this.all_Data['customer_data']))
      this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']))
      this.tableData = JSON.parse(JSON.stringify(this.all_Data['sn_data']))
      this.application_data = JSON.parse(JSON.stringify(this.all_Data['application_data']))
      this.info_data = JSON.parse(JSON.stringify(this.all_Data['info_data']))
      this.update_time = this.all_Data['update_time']
      var customer_name_mapping = {}
      for(let customer of this.customer_data){
        customer_name_mapping[customer['customer_id']] = customer['name']
        if (customer['site'] != "")
          customer_name_mapping[customer['customer_id']] += `(${customer['site']})`
        
        if(customer['site'] != '')
          this.customer_opt.push({value:(customer['name'] + '|' + customer['site']),label:(customer['name'] + '|' + customer['site'])});
        else
          this.customer_opt.push({value:customer['name'],label:customer['name']});

        this.customer_dict[customer['customer_id']] = {'name': customer['name'], 'site': customer['site']}
      }
      var region_name_mapping = {}
      for(let region of this.region_data){
        region_name_mapping[region['region_id']] = region['name']
        this.region_opt.push({value:region['name'],label:region['name']})
      }
      var userSet = new Set();
      var note1Set = new Set();
      var note2Set = new Set();
      var note3Set = new Set();
      var note4Set = new Set();
      var note5Set = new Set();
      for(let data of this.tableData){
        data['customer'] = customer_name_mapping[data['sn_id']]
        data['region'] = region_name_mapping[data['region']]
        this.KeyID_opt.push({value:data['sn'],label:data['sn']})
        
        //多位user
        // if(data['user'].includes(";"))
        //   data['user'].split(";").forEach(item => userSet.add(item))
        // else if(data['user'].includes(","))
        //   data['user'].split(",").forEach(item => userSet.add(item))
        // else if(data['user'] != '')
        //   userSet.add(data['user'])
        if(data['user'] != '')
          userSet.add(data['user'])
        if(data['note1'] != '')
          note1Set.add(data['note1'])
        if(data['note2'] != '')
          note2Set.add(data['note2'])
        if(data['note3'] != '')
          note3Set.add(data['note3'])
        if(data['note4'] != '')
          note4Set.add(data['note4'])
        if(data['note5'] != '')
          note5Set.add(data['note5'])
      }

      // 建議選項處理
      userSet.forEach(item => this.user_opt.push({value:item,label:item}))
      note1Set.forEach(item => this.note1_opt.push({value:item,label:item}))
      note2Set.forEach(item => this.note2_opt.push({value:item,label:item}))
      note3Set.forEach(item => this.note3_opt.push({value:item,label:item}))
      note4Set.forEach(item => this.note4_opt.push({value:item,label:item}))
      note5Set.forEach(item => this.note5_opt.push({value:item,label:item}))
      this.customer_fliter = this.customer_opt;
      this.KeyID_fliter = this.KeyID_opt;
      this.region_fliter = this.region_opt;
      this.user_fliter = this.user_opt;
      this.note1_fliter = this.note1_opt;
      this.note2_fliter = this.note2_opt;
      this.note3_fliter = this.note3_opt;
      this.note4_fliter = this.note4_opt;
      this.note5_fliter = this.note5_opt;

      

      //-----------------------申請紀錄處理------------------------//
      for(let app of this.application_data){
        for(let data of JSON.parse(app['data'])){
          if(data['sn'] in this.apply_record_map){
            this.apply_record_map[data['sn']].push({'id':app['id'], 'date':app['date'], 'applicant':app['applicant'], 'status':app['status'], 
              'verify_time':app['verify_time'].replaceAll('"',''),'operator':data['operator'], 'customer':data['customer'], 'sn': data['sn'], 
              'product':data['product'], 'module':data['module'], 'version':data['version'], 'type': data['type'], 'count':data['count'], 
              'expiration':data['expiration'], 'region': data['region'], 'comment':data['comment'], 'contact':data['contact']
            })
          }
          else{
            this.apply_record_map[data['sn']] = [{'id':app['id'], 'date':app['date'], 'applicant':app['applicant'], 'status':app['status'], 
              'verify_time':app['verify_time'].replaceAll('"',''), 'operator':data['operator'], 'customer':data['customer'], 'sn': data['sn'], 
              'product':data['product'], 'module':data['module'], 'version':data['version'], 'type': data['type'], 'count':data['count'], 
              'expiration':data['expiration'], 'region': data['region'], 'comment':data['comment'], 'contact':data['contact']
            }]
          }
        }
      }
      //-----------------------產品清單處理------------------------//
      for(let info of this.info_data){
        if(info['sn'] in this.product_list_map){
          this.product_list_map[info['sn']].push({'sn':info['sn'], 'customer':info['customer'],'category':info['category'], 'product':info['product'],
            'module':info['module'], 'version':info['version'], 'count': info['count'], 'type': info['type'], 'region':info['region'],
            'contact':info['contact'], 'expiration':info['expiration'], 'comment':info['comment']
          })
        }
        else{
          this.product_list_map[info['sn']] = [{'sn':info['sn'], 'customer':info['customer'],'category':info['category'], 'product':info['product'],
          'module':info['module'], 'version':info['version'], 'count': info['count'], 'type': info['type'], 'region':info['region'],
          'contact':info['contact'], 'expiration':info['expiration'], 'comment':info['comment']}]
        }
      }
      // 找出最近的到期日
      for(let row of this.tableData){
        let expiration_obj = {}
        for(let product of this.product_list_map[row['sn']]){
          var product_date = new Date(product['expiration'])
          var today = new Date()
          var secondToDay = 1000 * 60 * 60 * 24
          var days = parseInt(Math.abs( product_date - today ) / secondToDay)
          expiration_obj[days] = product['expiration']
        }
        let arr = Object.keys( expiration_obj ).map(function ( key ) { return key; });
        let recently_day = Math.min.apply( null, arr );
        row = Object.assign(row, {'expiration': expiration_obj[recently_day]})
      }

      this.filter_Data = JSON.parse(JSON.stringify(this.tableData))
      this.sort_Data = JSON.parse(JSON.stringify(this.tableData))

      if(this.user_setting['pagesize'] == 'all'){
        this.pagesize = this.tableData.length
        this.pagesize_display = 'all'
      }
      else{
        this.pagesize = this.user_setting['pagesize']
        this.pagesize_display = this.user_setting['pagesize']
      }

    //-----------------------存留過濾條件處理------------------------//
    let sessionStorage_fliter = JSON.parse(sessionStorage.getItem('sn_fliter'))
    if(sessionStorage_fliter){
      if(sessionStorage_fliter['customer_value']) this.customer_value = sessionStorage_fliter['customer_value']
      if(sessionStorage_fliter['KeyID_value']) this.KeyID_value = sessionStorage_fliter['KeyID_value']
      if(sessionStorage_fliter['region_value']) this.region_value = sessionStorage_fliter['region_value']
      if(sessionStorage_fliter['user_value']) this.user_value = sessionStorage_fliter['user_value']
      if(sessionStorage_fliter['expiration_value']) this.expiration_value = sessionStorage_fliter['expiration_value']
      if(sessionStorage_fliter['note1_value']) this.note1_value = sessionStorage_fliter['note1_value']
      if(sessionStorage_fliter['note2_value']) this.note2_value = sessionStorage_fliter['note2_value']
      if(sessionStorage_fliter['note3_value']) this.note3_value = sessionStorage_fliter['note3_value']
      if(sessionStorage_fliter['note4_value']) this.note4_value = sessionStorage_fliter['note4_value']
      if(sessionStorage_fliter['note5_value']) this.note5_value = sessionStorage_fliter['note5_value']
      if(sessionStorage_fliter['expiring_days']) this.expiring_days = sessionStorage_fliter['expiring_days']
      if(sessionStorage_fliter['expiring_check']) this.expiring_check = sessionStorage_fliter['expiring_check']
      if(sessionStorage_fliter['expired_check']) this.expired_check = sessionStorage_fliter['expired_check']
      if(sessionStorage_fliter!= undefined || JSON.stringify(sessionStorage_fliter)!=JSON.stringify({}))
        this.category_filter()
    }

      this.search_drawer = true;
      this.enter_loading = false
    })
  },
  methods: {
    select_change(){
      this.select_out = !this.select_out;
    },
    mode_switch(mode){
      if(mode == "product"){
        let save_pagesize
        if(this.pagesize_display == 'all')
          save_pagesize ='all'
        else
          save_pagesize = parseInt(this.pagesize_display)
        this.axios.post("/save_to_user_setting",{
          source:'KeyID',
          user:this.user,
          mode:mode,
          pagesize:save_pagesize
        }).then(response => {
          this.$router.push({name: 'Show_All'});
        })
      }
    },
    pagesize_change(){
      if(this.pagesize_display == 'all'){
        this.pagesize = this.tableData.length
        this.axios.post("/save_to_user_setting",{
          source:'KeyID',
          user:this.user,
          mode:this.mode,
          pagesize:'all'
        })
      }
      else{
        this.pagesize = parseInt(this.pagesize_display)
        this.axios.post("/save_to_user_setting",{
          source:'KeyID',
          user:this.user,
          mode:this.mode,
          pagesize:parseInt(this.pagesize)
        })
      }
    },
    Logout:function(){
      sessionStorage.clear();
      this.$router.push('/login');
    },
    handleSelectionChange (val) {//當select 有變化時執行 且val是所選row的所有資訊(type:array)
      this.checked_Data = JSON.parse(JSON.stringify(val));
    },
    handleEdit() {
        if (this.form.note1 == "" && this.form.note2 == "" && this.form.note3 == "" && this.form.note4 == "" && this.form.note5 == "")
          return;

        var today = new Date();
        let hour = today.getHours().toString();
        let minute = today.getMinutes().toString();
        hour = hour.length < 2 ? '0' + hour : hour
        minute = minute.length < 2 ? '0' + minute : minute
        var currentDateTime =`${today.getFullYear()}/${today.getMonth()+1}/${today.getDate()} ${hour}:${minute}`;
        var mynote = this.form.current_edit_data;
        mynote['record'] = `${currentDateTime} (${this.user[0]})`;
        if (this.form.note1!="")  mynote['note1'] = this.form.note1;
        if (this.form.note2!="")  mynote['note2'] = this.form.note2;
        if (this.form.note3!="")  mynote['note3'] = this.form.note3;
        if (this.form.note4!="")  mynote['note4'] = this.form.note4;
        if (this.form.note5!="")  mynote['note5'] = this.form.note5;

        this.axios.post("/save_to_sn",{
            newNotes: mynote,
        }).then((response)=>{
            this.form.note1='';
            this.form.note2='';
            this.form.note3='';
            this.form.note4='';
            this.form.note5='';
            //location.reload();
        })
    },
    detail_form(row){
      this.detailForm.keyID = row['sn']
      this.detailForm.product_list = this.product_list_map[row['sn']]
      this.detailForm.apply_record = []
      let inner_data = {}
      if(this.apply_record_map[row['sn']] != undefined) {
        // 處理展開所需資料
        for(let map of this.apply_record_map[row['sn']]){
          if(map['id'] in inner_data){
            inner_data[map['id']].push({'operator':map['operator'], 'customer':map['customer'], 'sn': map['sn'], 'product':map['product'], 
              'module':map['module'], 'version':map['version'], 'type': map['type'], 'count':map['count'], 'expiration':map['expiration'], 
              'region': map['region'], 'comment':map['comment'], 'contact':map['contact']})
          }
          else{
            inner_data[map['id']] = [{'operator':map['operator'], 'customer':map['customer'], 'sn': map['sn'], 'product':map['product'], 
              'module':map['module'], 'version':map['version'], 'type': map['type'], 'count':map['count'], 'expiration':map['expiration'], 
              'region': map['region'], 'comment':map['comment'], 'contact':map['contact']}]
          }
        }

        let id_list = []
        for(let map of this.apply_record_map[row['sn']]){
          if(id_list.includes(map['id']))
            continue
          this.detailForm.apply_record.push({'id':map['id'], 'date':map['date'], 'applicant':map['applicant'], 'status':map['status'], 
          'verify_time':map['verify_time'], 'data': inner_data[map['id']]})
          id_list.push(map['id'])
        }
      }
      this.detail = true
    },
    customer_enter(){
      this.customer_value.push(this.customer_input)
      this.category_filter();
    },
    customer_fliterer(val){
      if (val) {
        this.customer_input = val;
        this.customer_fliter = this.customer_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    KeyID_fliterer(val){
      if (val) {
        this.KeyID_input = val;
        this.KeyID_fliter = this.KeyID_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    region_fliterer(val){
      if (val) {
        this.region_input = val;
        this.region_fliter = this.region_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    user_fliterer(val){
      if (val) {
        this.user_input = val;
        this.user_fliter = this.user_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    note1_fliterer(val){
      if (val) {
        this.note1_input = val;
        this.note1_fliter = this.note1_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    note2_fliterer(val){
      if (val) {
        this.note2_input = val;
        this.note2_fliter = this.note2_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    note3_fliterer(val){
      if (val) {
        this.note3_input = val;
        this.note3_fliter = this.note3_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    note4_fliterer(val){
      if (val) {
        this.note4_input = val;
        this.note4_fliter = this.note4_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    note5_fliterer(val){
      if (val) {
        this.note5_input = val;
        this.note5_fliter = this.note5_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    category_filter: function(){
      if(this.expiring_check){
        if((!Number.isInteger(Number.parseInt(this.expiring_days))) || (Number.parseInt(this.expiring_days)<0)){
          this.$alert("到期日請輸入正整數!", "提示", {type: 'warning', center: true})
          return
        }
      }
      var test = {
        'customer_value':this.customer_value,
        'KeyID_value':this.KeyID_value,
        'region_value':this.region_value,
        'user_value':this.user_value,
        'expiration_value':this.expiration_value,
        'note1_value':this.note1_value,
        'note2_value':this.note2_value,
        'note3_value':this.note3_value,
        'note4_value':this.note4_value,
        'note5_value':this.note5_value,
        'expiring_days':this.expiring_days,
        'expiring_check':this.expiring_check,
        'expired_check':this.expired_check,
      }
      sessionStorage.setItem('sn_fliter', JSON.stringify({
        'customer_value':this.customer_value,
        'KeyID_value':this.KeyID_value,
        'region_value':this.region_value,
        'user_value':this.user_value,
        'expiration_value':this.expiration_value,
        'note1_value':this.note1_value,
        'note2_value':this.note2_value,
        'note3_value':this.note3_value,
        'note4_value':this.note4_value,
        'note5_value':this.note5_value,
        'expiring_days':this.expiring_days,
        'expiring_check':this.expiring_check,
        'expired_check':this.expired_check,
      }));

      // 手動輸入的KeyID為字串，需轉成數字
      for(let i in  this.KeyID_value)
        this.KeyID_value[i] = parseInt(this.KeyID_value[i])
      //多條件篩選
      function multiFilter(array, filters) {
        const filterKeys = Object.keys(filters)
        return array.filter((item) => {
          return filterKeys.every(key => {
            // 防止意外錯誤
            if(filters[key].includes(undefined) || filters[key].includes(NaN) || filters[key].includes(null))
              return true
            else if(!filters[key].length) 
              return true
            else{
              for(let key_item of filters[key]){
                if(String(item[key]).includes(key_item))
                  return true
              }
              return false
            }
          })
        })
      }

      var copy_data = [];
      var no_filter = false
      //都沒選
      if(!(this.customer_value).length && 
        !(this.KeyID_value).length && 
        !(this.region_value).length &&
        !(this.user_value).length &&
        (this.expiration_value == null)&&
        !(this.note1_value).length &&
        !(this.note2_value).length &&
        !(this.note3_value).length &&
        !(this.note4_value).length &&
        !(this.note5_value).length )
      { 
        copy_data = this.filter_Data;
        no_filter = true
      }
      //有選
      else{ 
        var filters = {}
        filters['customer'] =  this.customer_value;
        filters['sn'] = this.KeyID_value;
        filters['region'] = this.region_value;
        filters['user'] = this.user_value;
        filters['note1'] = this.note1_value;
        filters['note2'] = this.note2_value;
        filters['note3'] = this.note3_value;
        filters['note4'] = this.note4_value;
        filters['note5'] = this.note5_value;
        copy_data = multiFilter(this.filter_Data,filters);
      }
        
      if(this.expiration_value)
        copy_data = copy_data.filter(x => (this.expiration_value[0] <= x['expiration'] && x['expiration'] <= this.expiration_value[1]))
      
      let convert_day = 1000 * 60 * 60 * 24
      if(this.expiring_check &&　this.expired_check){
        copy_data = copy_data.filter(x => 
          (this.expiring_days >= parseInt((new Date(x['expiration']) - new Date()) / convert_day, 10))
        )
      }
      else if(this.expiring_check){
        copy_data = copy_data.filter(x => 
          (this.expiring_days >= parseInt((new Date(x['expiration']) - new Date()) / convert_day, 10))
          && (0 <= parseInt((new Date(x['expiration']) - new Date()) / convert_day, 10))
        )
      }
      else if(this.expired_check){
        copy_data = copy_data.filter(x => 
          (0 > parseInt((new Date(x['expiration']) - new Date()) / convert_day, 10))
        )
      }

      this.sort_Data = JSON.parse(JSON.stringify(copy_data))
      this.tableData = this.sort_Data;
      if(no_filter)
        this.searched_data_num = 0
      else
        this.searched_data_num = this.tableData.length
    },
    sortChange: function(column){
      var initial_Data = JSON.parse(JSON.stringify(this.sort_Data));
      if(initial_Data.length == 0)  return;
      var order_Data = ascending_order(initial_Data,column.prop);
      if(column.order == 'ascending')
        this.tableData = order_Data;
      else if(column.order == 'descending')
        this.tableData = order_Data.reverse();
      else
        this.tableData = this.sort_Data;
    },
    customer_enter(){
      this.customer_value.push(this.customer_input)
    },
    KeyID_enter(){
      this.KeyID_value.push(this.KeyID_input)
    },
    region_enter(){
      this.region_value.push(this.region_input)
    },
    user_enter(){
      this.user_value.push(this.user_input)
    },
    note1_enter(){
      this.note1_value.push(this.note1_input)
    },
    note2_enter(){
      this.note2_value.push(this.note2_input)
    },
    note3_enter(){
      this.note3_value.push(this.note3_input)
    },
    note4_enter(){
      this.note4_value.push(this.note4_input)
    },
    note5_enter(){
      this.note5_value.push(this.note5_input)
    },
     drawer_open(){
      this.search_drawer = true
      this.search_drawer_btn = false
      document.getElementById('showtable').style.width = '75%'
    },
    drawer_close(){
      this.search_drawer = false
      document.getElementById('showtable').style.width = '85%'
    },
    clear_filter(){
      this.customer_value = []
      this.KeyID_value = []
      this.region_value = []
      this.user_value = []
      this.expiration_value = null
      this.note1_value = []
      this.note2_value = []
      this.note3_value = []
      this.note4_value = []
      this.note5_value = []
      this.expiring_check = false
      this.expired_check = false
      this.category_filter()
      sessionStorage.setItem('sn_fliter', JSON.stringify({}));
    },
    reload(){
      location.reload();
    },
    tableRowColor({row, rowIndex}) {
      var Index = rowIndex + (this.currentPage - 1) * this.pagesize;
      row.index = rowIndex;
      var tempDate = new Date;
      
      tempDate.setHours(tempDate.getHours());
      var today = tempDate.toISOString().slice(0, 10)
      
      tempDate.setMonth(tempDate.getMonth()+1);
      var oneMonthLater = tempDate.toISOString().slice(0, 10)
      
      var order_expiration = this.tableData[Index]['expiration'];
      
      if (order_expiration < today){
          return 'exceed-row';
      }
      else if (order_expiration < oneMonthLater) {
          return 'warning-row';
      }
      return 'success-row';
    },
    selection_column_style:function(row){
      if(row.columnIndex == 0)
        return 'selection_style'
    },
  },
  computed:{
    delay_time: function(){
      return this.select_out * 10000;
    }
  }
}
</script>


