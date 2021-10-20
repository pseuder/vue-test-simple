<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-table /deep/ .exceed-row {
    background: #FE7F6E;
    color:#000;
    border: 1.5px solid silver
  }
  .el-table /deep/ .warning-row {
    background: #FFF063;
    color:#000;
    border: 1.5px solid silver
  }
  .el-table /deep/ .success-row {
    background: #FFF0D2;
    color:#000;
    border: 1.5px solid silver
  }
  .el-table /deep/ th, 
  .el-table /deep/ tr {
    background-color: #FFBE3F;
    color:#000;
    border: 1.5px solid silver
  }
  .el-table /deep/ .cell{
    word-break: break-word;
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
    z-index:111;
  }
  .menu-badge /deep/  .el-badge__content.is-fixed{
    top: -13px;
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
  .el-pagination.is-background /deep/ li,
  .el-pagination.is-background /deep/ .btn-prev,
  .el-pagination.is-background /deep/ .btn-next{
    background-color: #FFBE3F;
    color: black;
  }
  .el-pagination.is-background /deep/ li:not(.disabled).active{
    background-color: #8E6109;
    color: black;
  }
  .fold /deep/ th{
    background-color: #76AEE2;
    color:#000;
  }
  .fold /deep/ tr{
    background-color: white;
    color:#000;
  }
  .expand /deep/ th{
    background-color: #DDDDDD;
    color:#000;
  }
  .expand /deep/ tr{
    background-color: white;
    color:#000;
  }
  .expand /deep/ .cell{
    line-height: 15px;
  }
  .el-form-item /deep/ .el-form-item__content{
    line-height: 10px;
  }
  .search-box{
    position: relative;
    width: 310px;
    margin: auto 15px;
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
    overflow-y: auto;
  }
  .el-drawer__wrapper{
    width: 340px !important;
    top:60px !important;
  }
  .search-drawer /deep/ .modal{
    width: 340px;
  }
  .header{
    width: 102%;
    position: relative;
    top: -60px;
    left: -8px;
    text-align: right;
    font-size: 20px;
    background-color: rgb(235, 209, 160);
  }
</style>

<style>
.alert_class{
    position: relative;
    bottom: 165px;
  }append-to-body

.el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
  overflow: scroll!important;
}
.el-select-dropdown__list{
  margin: revert !important;
}
.mode-switch{
  right: 70px;
  bottom: 3px;
  position: relative;
}
.apply_record{
  border-radius: 15px;
  background: cornflowerblue;
}
.shadow_box{
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}
</style>


<template>
  <div>
    <transition name="fade"><!--loading動畫-->
      <loading v-if="isLoading"></loading>
    </transition>
    <div id = "menu">
      <div>
        <el-badge :value="num_check" v-show=deter_check class="menu-badge">
          <el-tooltip placement="left" effect="light">
            <div slot="content"><span style="font-weight: bold; font-size:15px">審核資料</span><br>有{{num_check}}筆資料待審核</div>
            <el-button v-show=deter_check class="OperatorButton"  type="warning" icon="el-icon-s-check" @click="GoCheck" />
          </el-tooltip>
        </el-badge>
      </div>
      <div>
        <el-badge :value="num_handle" class="menu-badge">
          <el-tooltip placement="left" effect="light">
            <div slot="content" style="font-weight: bold; font-size:15px">送出申請</div>
            <el-button class="OperatorButton" type="warning" icon="el-icon-s-promotion" @click="GoHandle" />
          </el-tooltip>
        </el-badge>
      </div>
      <div>
        <el-tooltip placement="left" effect="light">
          <div slot="content" style="font-weight: bold; font-size:15px">新增</div>
          <el-button class="OperatorButton"  type="warning" icon="el-icon-plus" @click="GoAdd" />
        </el-tooltip>
      </div>
      <div>
        <el-tooltip placement="left" effect="light">
          <div slot="content" style="font-weight: bold; font-size:15px">修改</div>
          <el-button class="OperatorButton"  type="warning" icon="el-icon-edit" @click="GoEdit" />
        </el-tooltip>
      </div>
      <div>
        <el-tooltip placement="left" effect="light">
          <div slot="content" style="font-weight: bold; font-size:15px">刪除</div>
          <el-button class="OperatorButton"  type="warning" icon="el-icon-delete" @click="GoDelete" />
        </el-tooltip>
      </div>
      <div>
        <el-tooltip placement="left" effect="light">
          <div slot="content" style="font-weight: bold; font-size:15px">多筆展延</div>
          <el-button class="OperatorButton"  type="warning" icon="el-icon-timer" @click="Go_Edit_time" />
        </el-tooltip>
      </div>
      <div>
        <el-tooltip placement="left" effect="light">
          <div slot="content" style="font-weight: bold; font-size:15px">資料下載</div>
          <el-button class="OperatorButton"  type="warning" icon="el-icon-download" @click="click_download" />
        </el-tooltip>
      </div>
    </div>

    <div>
      <el-header class="header">
        <div style="position:absolute;left:30px;top:3px;cursor:pointer;" @click="reload"> License Application Service</div>
        <div>
          <el-button-group class="mode-switch">
            <el-button type="warning" @click="mode_switch('product')">產品</el-button>
            <el-button type="warning" @click="mode_switch('KeyID')" style="background: #ebd1a0; color: white; border-color: #e6a23c;">SN</el-button>
          </el-button-group>
        </div>
        <el-popover trigger="hover" width="200" placement="bottom" :close-delay="delay_time">
          
          <div><span>成員名稱: {{user[0]}}</span></div>
          <div><span>-----------------------------------------</span></div>
          <div >
            <span>單頁筆數: <span>
            <el-select style="width:80px;" v-model="pagesize" size="small" @change="pagesize_change"  @visible-change="select_change" placeholder="請選擇">
              <el-option key= '10' label="10" value='10'></el-option>
              <el-option key= '20' label="20" value='20'></el-option>
              <el-option key= '50' label="50" value='50'></el-option>
              <el-option key= '100' label="100" value='100'></el-option>
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
          <div class="search-box-item-font">產品類別</div>
          
            <el-select v-model="category_value" multiple  placeholder="產品類別" filterable clearable  @keyup.enter.native="category_enter" 
              :filter-method="category_fliterer" style="width:400px;">
              <el-option v-for="opt in category_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>
        
        <div class="search-box-item">
          <div class="search-box-item-font">產品</div>
            <el-select v-model="product_value" multiple placeholder="產品" filterable clearable @keyup.enter.native="product_enter" 
              :filter-method="product_fliterer" style="width:400px;">
              <el-option v-for="opt in product_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>
        
        <div class="search-box-item">
          <div class="search-box-item-font">模組</div>
            <el-select v-model="module_value" multiple  placeholder="模組" filterable clearable @keyup.enter.native="module_enter" 
              :filter-method="module_fliterer" style="width:400px;">
              <el-option v-for="opt in module_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>
        
        <!-- <div class="search-box-item">
          <div class="search-box-item-font">版本</div>
          <el-badge style="position:absolute; left: 8px;" :value="version_value.length" v-if="version_value.length"></el-badge>
          <el-popover placement="bottom"  trigger="click">
            <el-select v-model="version_value" multiple placeholder="版本" filterable clearable @keyup.enter.native="version_enter" 
              :filter-method="version_fliterer" >
              <el-option v-for="opt in version_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
            <el-button class="search_button" icon="el-icon-search" circle slot="reference" size='mini'  @click.stop></el-button>
          </el-popover>
        </div> -->
        
              

        <!-- <div class="search-box-item">
          <div class="search-box-item-font">數量</div>
            <el-select v-model="count_value" multiple  placeholder="數量" filterable clearable @keyup.enter.native="count_enter" 
              :filter-method="count_fliterer" style="width:400px;">
              <el-option v-for="opt in count_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
        </div>  -->

        <div class="search-box-item"> 
          <div class="search-box-item-font">類型</div>
            <el-select v-model="type_value" multiple  placeholder="類型" filterable clearable @keyup.enter.native="type_enter" 
              :filter-method="type_fliterer" style="width:400px;">
              <el-option v-for="opt in type_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
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
          <div class="search-box-item-font">聯絡人</div>
            <el-select v-model="contact_value" multiple  placeholder="聯絡人" filterable clearable @keyup.enter.native="contact_enter" 
              :filter-method="contact_fliterer" style="width:400px;">
              <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
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

        <div class="search-box-item">
          <div class="search-box-item-font">到期日</div>
            <el-date-picker  value-format="yyyy-MM-dd" size="mini" v-model="expiration_value" type="daterange" 
            range-separator="_" start-placeholder="開始日期" end-placeholder="結束日期" style="width:345px; height:37px; margin-right: 25px; margin-top: 8px;" />
        </div>

        <div class="search-box-item">
          <div class="search-box-item-font">更新日期</div>
            <el-date-picker value-format="yyyy-MM-dd" size="mini" v-model="issued_value" type="daterange" 
            range-separator="_" start-placeholder="開始日期" end-placeholder="結束日期" style="width:345px; height:40px; margin-right: 25px; margin-top: 8px;" />
        </div>

        
      </div>
      
        <el-button @click="drawer_close" type="warning" icon="el-icon-search" circle
          style="position: fixed; top: 80px; left: 319px; padding: 15px; font-size: 20px;"> 
        </el-button>
      
    </el-drawer>
    
    <div style="display:flex;">
    <!-- 主要表格 -->
    <div style="flex-basis:280px;" v-show="search_drawer"></div>
    <div style="margin: 0px auto; width:75%" id = "showtable">
        <div v-show="searched_data_num" style="color: red; font-size:20px; font-weight: bold;">已搜尋到{{searched_data_num}}筆資料</div>
          <el-table
            ref="showtable"
            @row-click='rowclick'
            :row-class-name="tableRowColor"
            :row-style="{height:0+'px'}"
            :cell-style="{border: 'solid 1px #EAEAEA'}"
            @sort-change='sortChange'
            @selection-change="handleSelectionChange"
            :header-cell-class-name="selection_column_style"
            :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            height= 650px
            border
            row-key="info_id"
          >
            <!-- index -->
            <el-table-column align="center"  label=" " width=50>
              <template slot-scope="scope">
                {{ ((currentPage-1) * 50) + (scope.row['index'] + 1) }}
              </template>
            </el-table-column>
            <!-- check box -->
            <el-table-column type="selection" align="center" width=50 :reserve-selection="true"></el-table-column>
            <!-- 客戶 -->
            <el-table-column align="center" sortable='custom' prop="customer" label="客戶"></el-table-column>
            <!-- KeyID -->
            <el-table-column align="center" sortable='custom' prop="sn" label="KeyID" min-width=100></el-table-column>
            <!-- 產品類別 -->
            <el-table-column align="center" sortable='custom' prop="category" label="產品類別" min-width=100></el-table-column>
            <!-- 產品 -->
            <el-table-column align="center" sortable='custom' prop="product" label="產品" ></el-table-column>
            <!-- 模組 -->
            <el-table-column align="center" sortable='custom' prop="module" label="模組" ></el-table-column>
            <!-- 版本 -->
            <!-- <el-table-column align="center" sortable='custom' prop="version" label="版本" width="130px"></el-table-column> -->
            <!-- 更新日期 -->
            <el-table-column align="center" sortable='custom' prop="issued" label="更新日期" min-width=100></el-table-column>
            <!-- 到期日 -->
            <el-table-column align="center" sortable='custom' prop="expiration" label="到期日" min-width=100></el-table-column>
            <!-- 數量 -->
            <el-table-column align="center" sortable='custom' prop="count" label="數量" ></el-table-column>
            <!-- 類型 -->
            <el-table-column align="center" sortable='custom' prop="type" label="類型" ></el-table-column>
            <!-- 地區 -->
            <el-table-column align="center" sortable='custom' prop="region" label="地區" ></el-table-column>
            <!-- 聯絡人 -->
            <el-table-column align="center" sortable='custom' prop="contact_display" label="聯絡人" min-width=100></el-table-column>
            <!-- 備註 -->
            <el-table-column align="center" sortable='custom' prop="comment" label="備註" show-overflow-tooltip></el-table-column>
            <!-- 跳視窗 qwe-->
            <el-table-column align="center"  label="" width=50>
              <template slot-scope="scope">
              <i style="font-size:20px; cursor: pointer; z-index: 200; position: relative;" class="el-icon-arrow-right"  @click.stop = "detail_form(scope.row)"></i>
              
              </template>
            </el-table-column>
          </el-table>
        
        <div class="pagination"><!--對頁面做分頁 當當前頁改變時改變tableData 補充:sync是雙向綁定-->
          <el-pagination 
            background
            @current-change="handleCurrentChange" 
            :current-page.sync="currentPage" 
            :page-size.sync="pagesize" 
            layout="prev, pager, next" 
            :total="tableData.length" >
          </el-pagination>
        </div>
    </div>
    </div>
    <!-- 此產品申請紀錄 -->
    <el-dialog  :visible.sync="detail" width="80%" append-to-body="true">
      <div style="height:580px">
        <div style="font-size:25px;">{{form.form_customer}}    {{form.form_KeyID}}申請紀錄</div>
        <el-table :data="form.form_data.fold" style="width: 100%" class="fold" :row-style="{height: '10px'}" height="500">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-table :data="form.form_data.expand[props.$index]" border class="expand" :cell-style="{height:'20px'}" >
                <el-table-column prop="申請類別" label="申請類別" width="100">
                  <template slot-scope="scope">
                    <span v-if="scope.row['申請類別'] == '修改'">{{scope.row['申請類別']}}</span>
                    <span v-else-if="form.form_data.expand[props.$index][0]['申請類別'] !=  scope.row['申請類別']" style="color:red">{{scope.row['申請類別']}}</span>
                    <span v-else>{{scope.row['申請類別']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="產品類別" label="產品類別">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['產品類別'] !=  scope.row['產品類別']" style="color:red">{{scope.row['產品類別']}}</span>
                    <span v-else>{{scope.row['產品類別']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="產品" label="產品">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['產品'] !=  scope.row['產品']" style="color:red">{{scope.row['產品']}}</span>
                    <span v-else>{{scope.row['產品']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="模組/功能" label="模組/功能">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['模組/功能'] !=  scope.row['模組/功能']" style="color:red">{{scope.row['模組/功能']}}</span>
                    <span v-else>{{scope.row['模組/功能']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="版本" label="版本">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['版本'] !=  scope.row['版本']" style="color:red">{{scope.row['版本']}}</span>
                    <span v-else>{{scope.row['版本']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="數量" label="數量" width="100">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['數量'] !=  scope.row['數量']" style="color:red">{{scope.row['數量']}}</span>
                    <span v-else>{{scope.row['數量']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="類型" label="類型" width="100">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['類型'] !=  scope.row['類型']" style="color:red">{{scope.row['類型']}}</span>
                    <span v-else>{{scope.row['類型']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="聯絡人" label="聯絡人">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['聯絡人'] !=  scope.row['聯絡人']" style="color:red">{{scope.row['聯絡人']}}</span>
                    <span v-else>{{scope.row['聯絡人']}}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="使用期限" label="使用期限" width="120">
                  <template slot-scope="scope">
                    <span v-if="form.form_data.expand[props.$index][0]['使用期限'] !=  scope.row['使用期限']" style="color:red">{{scope.row['使用期限']}}</span>
                    <span v-else>{{scope.row['使用期限']}}</span>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column label="ID" prop="ID"></el-table-column>
          <el-table-column label="申請日期" prop="申請日期"></el-table-column>
          <el-table-column label="申請人" prop="申請人"></el-table-column>
          <el-table-column label="類型類別" prop="類型類別"></el-table-column>
          <el-table-column label="審核人" prop="審核人"></el-table-column>
        </el-table>
        <div style="text-align: right">
          <el-button type="primary" size="small" round plain @click="click_apply_record">查看完整申請</el-button>
        </div>
      </div>
    </el-dialog>

    <!-- KeyID完整申請紀錄 -->
    <el-dialog :visible.sync="apply_record_dialog" width="75%" append-to-body="true">
      <div class="apply_record">
        <div style="font-size:25px; text-align:center; color:black">{{form.form_KeyID}}完整申請紀錄</div>
        <el-table :data="form.apply_record" style="width: 100%" class="fold shadow_box" :row-style="{height: '10px'}" height="400">
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
                  <el-table-column prop="contact" label="聯絡人"></el-table-column>
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
    </el-dialog>

    <!-- 多筆KeyID操作-->
    <el-dialog  :visible.sync="multi_keyID_dialog" width="55%" :close-on-click-modal="false" style="margin-top: 2vh;">
      <div style="font-size: 25px; font-weight: 600; padding: 5px; top: -20px; position: relative;">多筆id{{multi_keyID_mode}}</div>
      <div style="font-size: 20px; font-weight: 600; padding: 5px; text-align: left;">notice:如果id下有多個產品會一併{{multi_keyID_mode}}</div>
      <div style="font-size: 20px; font-weight: 600; padding: 5px; text-align: left;">ex: 2000001;2000002;2000003</div>
      <div style="font-size: 18px; font-weight: 600; padding: 5px; color: red;"><span>{{error_message.digital_error}}</span></div>
      <div style="font-size: 18px; font-weight: 600; padding: 5px; color: red;"><span>{{error_message.type_error}}</span></div>
      <div style="font-size: 18px; font-weight: 600; padding: 5px; color: red;"><span>{{error_message.exist_error}}</span></div>
      <el-input type="textarea" v-model="multi_keyID_text" style="display:none"></el-input>
      <textarea id="multi_keyID_textarea" rows="15" cols="110" placeholder="只允許 7 碼數字，且使用;區隔" style="width: 100%; font-size: 18px;"></textarea>
      <el-button @click="multi_keyID_dialog = false">取消</el-button>
      <el-button @click="multi_keyID_dialog_click">確定</el-button>
    </el-dialog>

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
// 將全型轉半形
function toHalf(chars) {
    var ascii = '';
    for(var i=0, l=chars.length; i<l; i++) {
        var c = chars[i].charCodeAt(0);
        //只針對半形去轉換
        if (c >= 0xFF00 && c <= 0xFFEF) {
            c = 0xFF & (c + 0x20);
        }
        ascii += String.fromCharCode(c);
    }
    return ascii;
}
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'Show_All',
  data () {
    return {
      all_Data:{},//整個資料庫的數據
      tableData: [],//要顯示的tabledata
      origin_Data:[],//原始的tableData
      filter_Data:[],//分頁後的tableData
      sort_Data:[],//做完搜尋的Data 之後拿sort來做排序 同時也是最完整最終的Data
      checked_Data:[],//勾選row的資料
      application_data:[],
      currentPage: 1, //默認當前頁為1
      pagesize: 10, //每頁顯示數量
      user:[],
      TabsValue: '1',//default <all>
      Tabs:[],
      //篩選欄位建議選項及選中值
      customer_opt:[],
      customer_value:'',
      customer_fliter:[],
      customer_input:"",
      customer_dict:{},
      issued_opt:[],
      issued_value:null,
      KeyID_opt:[],
      KeyID_value:'',
      KeyID_fliter:[],
      KeyID_input:"",
      product_opt:[],
      product_value:'',
      product_fliter:[],
      product_input:"",
      contact_opt:[],
      contact_value:'',
      contact_fliter:[],
      contact_input:"",
      expiration_opt:[],
      expiration_value:null,
      count_opt:[],
      count_value:'',
      count_fliter:[],
      count_input:"",
      region_opt:[],
      region_value:'',
      region_fliter:[],
      region_input:"",
      type_opt:[],
      type_value:'',
      type_fliter:[],
      type_input:"",
      category_opt:[],
      category_value:'',
      category_fliter:[],
      category_input:"",
      module_opt:[],
      module_value:'',
      module_fliter:[],
      module_input:"",
      version_opt:[],
      version_value:'',
      version_fliter:[],
      version_input:"",
      expiring_days:30,
      expiring_check:false,
      expired_check:false,
      num_handle:0,
      num_check:0,
      all_checked:false,
      mode:'產品',//顯示模式
      update_time:'',//push heroku的時間
      git_push_time:'',//git push 時間
      deter_download:false,//判斷是否有download excel權限
      deter_check:false,
      isLoading:true,
      select_out:false,
      detail:false,
      search_drawer:false,
      search_drawer_btn:true,
      apply_record_dialog: false,
      apply_record_map: {},
      download_format:'',
      download_data:[],
      keypro_application_time:"",
      official_application_time:"",
      license_time:"",
      form:{
        form_customer:"",
        form_KeyID:"",
        form_data:{
          fold:[],
          expand:[],
        },
        apply_record: []
      },
      info_keyID: [],
      multi_keyID_dialog:false,
      multi_keyID_text:'',
      multi_keyID_mode: '',
      error_message:{
        digital_error:'',
        type_error:'',
        exist_error:'',
      },
      searched_data_num:0,
      customer_dict:{},
      sn_dict:{},
    }
  },
  created () {//創建原始資料
    //檢查是否有未送出資料
    if (sessionStorage.getItem('first_time_login') == 'yes'){
      this.axios.get('/get_editing_num',{
        params:{
            user:JSON.parse(sessionStorage.getItem('user'))[0]
        }
      }).then(response => {
        sessionStorage.setItem('first_time_login', 'no');
        if(response.data != 0){
          this.$confirm(`尚有 ${response.data} 筆資料未送出, 是否前往確認 ?`, '提示', {
              confirmButtonText: '是(前往查看)',
              cancelButtonText: '否(刪除申請資料)',
              type: 'warning',
              center: true,
              closeOnClickModal: false,
              showClose: false,
          }).then(() => {
              this.$router.push({name: 'handle'})
          }).catch(() => {
              this.axios.get("/handle_delete",{
                params:{
                    Row: JSON.stringify([]),
                    user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))
                }
              }).then((response)=>{
                location.reload()
              });
          })
        }
        else{
          location.reload()
        }
      })
    }
    else{
      this.axios.get('/show_all',{
        headers: {'Content-Encoding': 'gzip'},
        params:{
                user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))//為了讓後端 傳出來的edit table資料只限於當前使用者的
            }
      }).then(response => {
      //-----------------------------建議選項處理------------------------------//
      if(sessionStorage['authority'] != undefined)
        if(JSON.parse(sessionStorage.getItem('authority')).includes('下載權限'))
          this.deter_download = true

      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
      this.application_data = this.all_Data['application_data']
      this.update_time = this.all_Data['update_time']
      this.git_push_time = this.all_Data['git_push_time']
      
      //handle的資料筆數
      this.axios.get('/get_editing_num',{
        params:{
          user:this.user[0]
        }
      }).then(response => {
          this.num_handle = response.data
      })

      for (let customer of response.data['customer_data']){
        if(customer['site'] != '')
          this.customer_opt.push({value:(customer['name'] + '|' + customer['site']),label:(customer['name'] + '|' + customer['site'])});
        else
          this.customer_opt.push({value:customer['name'],label:customer['name']});

        this.customer_dict[customer['customer_id']] = {'name': customer['name'], 'site': customer['site']}
      }
      var temp_info_func_uid = [];
      var countSet = new Set();//用set過濾 因有重複
      var contactSet = new Set();//用set過濾 因有重複
      var issuedSet = new Set();//用set過濾 因有重複
      var expirationSet = new Set();//用set過濾 因有重複
      var typeSet = new Set();//用set過濾 因有重複
      var module_map = new Map()
      response.data['module_data'].forEach(item => module_map.set(item['mod_uid'],item['caption']))
      for (let info of response.data['info_data']){
        var copy = info['contact'];
        var copy_part = copy.split(',');
        for(let part of copy_part)
          contactSet.add(part.split('@')[0]);
        countSet.add(info['count'])
        temp_info_func_uid.push(info['func_uid'])
        issuedSet.add(info['issued'])
        expirationSet.add(info['expiration'])
        if(module_map.get(info['type'])!=undefined)
          typeSet.add(module_map.get(info['type']))
        if(this.version_opt.map(x => x.value).indexOf(info['version']) < 0)
          this.version_opt.push({value:info['version'],label:info['version']})
      }
      contactSet.forEach(item => this.contact_opt.push({value:item,label:item}))
      response.data['sn_data'].forEach(item => this.KeyID_opt.push({value:item['sn'],label:item['sn']}))
      countSet.forEach(item => this.count_opt.push({value:item,label:item}))
      response.data['region_data'].forEach(item => this.region_opt.push({value:item['name'],label:item['name']}))
      var product_set = new Set()
      var module_set = new Set()
      for (let product of response.data['product_data']){
        if(temp_info_func_uid.includes(product['product_name']))//把測試新增修改刪除(建議)去掉
          product_set.add(product['caption']);
        if(this.category_opt.map(x => x.value).indexOf(product['category_id']) < 0)
          this.category_opt.push({value:product['category_id'],label:product['category_id']})
      }
      for(let option of response.data['option_data']){
        if(temp_info_func_uid.includes(option['option_name']))
          product_set.add(option['caption']);
        module_set.add(option['product_name']);
      }
      
      
      issuedSet.forEach(item => this.issued_opt.push({value:item,label:item}))
      expirationSet.forEach(item => this.expiration_opt.push({value:item,label:item}))
      typeSet.forEach(item => this.type_opt.push({value:item,label:item}))
      //---------------------------處理tableData關聯資料統整-------------------------//
      var order_form = JSON.parse(JSON.stringify(response.data.info_data));//複製一個完全獨立的info 深複製
      var sn_dict = response.data['sn_dict']
      var i = 0
      var product_map = new Map()
      var option_map = new Map()
      for(let product of response.data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of response.data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})
      let region_map = {}
      for (let reg of response.data['region_data'])
        region_map[reg['region_id']] = {'name': reg['name'], 'description': reg['description']}
      
      for (let info of response.data['info_data']){
        if (sn_dict[info['sn']] != undefined){
          if(this.customer_dict[sn_dict[info['sn']]['sn_id']]['site'] != ''){//若客戶site=''
            order_form[i] = Object.assign(order_form[i], 
            {
            'customer':this.customer_dict[sn_dict[info['sn']]['sn_id']]['name'] + '|' + this.customer_dict[sn_dict[info['sn']]['sn_id']]['site'],
            'user':sn_dict[info['sn']]['user'],
            'info':[sn_dict[info['sn']]['note1'], sn_dict[info['sn']]['note2'], sn_dict[info['sn']]['note3'], sn_dict[info['sn']]['note4'], sn_dict[info['sn']]['note5']],
            'version':info['version'],
            'info':info['info']
            })
          }
          else//若客戶site!='' 則客戶name|site
            order_form[i] = Object.assign(order_form[i],
            {
            'customer':this.customer_dict[sn_dict[info['sn']]['sn_id']]['name'] ,
            'user':sn_dict[info['sn']]['user'],
            'info':[sn_dict[info['sn']]['note1'], sn_dict[info['sn']]['note2'], sn_dict[info['sn']]['note3'], sn_dict[info['sn']]['note4'], sn_dict[info['sn']]['note5']],
            'version':info['version'],
            'info':info['info']
            })
          if(isNaN(sn_dict[info['sn']]['region']))  //判斷是否為數字
            order_form[i] = Object.assign(order_form[i],{'region':sn_dict[info['sn']]['region']})
          else if(sn_dict[info['sn']]['region'] != '')
            order_form[i] = Object.assign(order_form[i],{'region':region_map[parseInt(sn_dict[info['sn']]['region'],10)]['name']})
          else
            order_form[i] = Object.assign(order_form[i],{'region':''})
          }
        
        //func_uid在option內
        if(option_map.get(info['func_uid']) != undefined){
          order_form[i] = Object.assign(order_form[i],
          {
            'category':option_map.get(info['func_uid'])['category_id'], 
            'module' :option_map.get(info['func_uid'])['caption']
          });
          //模組
          let module_name = option_map.get(info['func_uid'])['caption'];
          if(this.module_opt.map(x => x.value).indexOf(module_name) < 0)
            this.module_opt.push({value:module_name, label:module_name});
          //產品
          order_form[i]['product'] = option_map.get(info['func_uid'])['product_name'];
          if(product_map.get(order_form[i]['product']) != undefined)
            order_form[i]['product'] = product_map.get(order_form[i]['product'])['caption'];
          
          let product_name = order_form[i]['product'];
          if(this.product_opt.map(x => x.value).indexOf(product_name) < 0)
            this.product_opt.push({value:product_name, label:product_name});
        }
        //func_uid在product內
        else if(product_map.get(info['func_uid']) != undefined){
          order_form[i] = Object.assign(order_form[i],
          {
            'category':product_map.get(info['func_uid'])['category_id'],
            'module' :''
          })
          //產品
          order_form[i]['product'] = product_map.get(info['func_uid'])['caption'];
          let product_name = order_form[i]['product'];
          if(this.product_opt.map(x => x.value).indexOf(product_name) < 0)
            this.product_opt.push({value:product_name, label:product_name});
        }
        else{
          order_form[i] = Object.assign(order_form[i],
          {
            'category':'',
            'module' :''
          })
          order_form[i]['product'] = info['func_uid']
        }
        //類型
        if(module_map.get(info['type']) != undefined)
          order_form[i]['type'] = module_map.get(info['type']);
        
        i++
        if(!this.info_keyID.includes(info['sn']))
          this.info_keyID.push(info['sn'])
      }
    //--------------------------根據日期將資料上色分類----------------------//
    if(order_form.length != 0)
      order_form = ascending_order(order_form,'expiration')//綠黃紅

    var tempDate = new Date;
    tempDate.setHours(tempDate.getHours());
    var today = tempDate.toISOString().slice(0, 10)
    tempDate.setMonth(tempDate.getMonth()+1);
    var oneMonthLater = tempDate.toISOString().slice(0, 10)

    var yellow_order_form = order_form.filter(item => (item['expiration'] < oneMonthLater && item['expiration'] > today))
    order_form = order_form.filter(item=>(item['expiration'] >= oneMonthLater || item['expiration'] <= today))//調整初始數據順序 綠黃紅->黃綠紅
    for(let order of yellow_order_form)
      order_form.unshift(order)
    //-----------------------聯絡人細節省略處理------------------------//
    for(let order of order_form){//若info聯絡人在user中有對應到email 則去除尾段email address
        order = Object.assign(order,{'contact_display':order['contact']})
        order = Object.assign(order,{'user_display':order['user']})//新增編輯頁面需要負責人欄位
    }


    //建議選項排序
    this.count_opt = this.count_opt.sort(function(a,b){return a.value>b.value?1:-1;});
    
    //賦予Tabs
    this.Tabs.push({label: '總表',name: '1'});
    this.Tabs.push({label: '一個月內過期',name: '一個月內過期'});
    for (let category of this.category_opt)
      this.Tabs.push({label: category.value,name:category.value});
    this.Tabs.push({label: '已過期',name: '已過期'});
    
    //動態調整tab寬度
    let tab_width = 1413 / this.Tabs.length;
    document.documentElement.style.setProperty('--tabwidth', `${tab_width}px`);
    
    //取得keypro領用申請單更新時間
    this.axios.post("/get_file_update_time",{
      path:'public/static/keypro_application.docx',
    }).then((response)=>{
      this.keypro_application_time = response.data;
    })

    //取得申請永久正式key表格更新時間
    this.axios.post("/get_file_update_time",{
      path:'public/static/official_application.xls',
    }).then((response)=>{
      this.official_application_time = response.data;
    })

    //取得license更新時間
    this.axios.post("/get_file_update_time",{
      path:'public/static/license',
    }).then((response)=>{
      this.license_time = response.data;
    })

    
    
    //取得待審核數量
    for(let app of this.application_data)
      if(app['status'] == 'wait_for_verification')
        this.num_check += 1
    
    //取得使用者申請數量
    for(let user of this.all_Data['user_data'])
      if(user['description'] == 'to be confirmed')
        this.num_check += 1


    //取得審核權限
    for(let users of this.all_Data['user_data']){
      if(users['user'] == this.user[0]){
        //審核-產品:5； 審核-財務:6
        if(users['groups'].includes(5) || users['groups'].includes(6))
          this.deter_check = true;
        break;
      }
    }

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

    this.origin_Data = order_form
    this.tableData = order_form
    this.filter_Data = order_form;
    this.sort_Data = order_form;
    this.sn_dict = sn_dict;
    this.customer_dict = response.data['customer_dict']
    
    
    var user_setting = JSON.parse(this.all_Data['user_data'].filter(item => (item['user'] == this.user[0]))[0]['setting'])//處理使用者設定
    if(user_setting['pagesize'] == 'all')
      this.pagesize = 100
    else
      this.pagesize = user_setting['pagesize']
    this.customer_fliter = this.customer_opt;
    this.KeyID_fliter = this.KeyID_opt;
    this.category_fliter = this.category_opt;
    this.product_fliter = this.product_opt;
    this.module_fliter = this.module_opt;
    this.version_fliter = this.version_opt;
    this.count_fliter = this.count_opt;
    this.type_fliter = this.type_opt;
    this.region_fliter = this.region_opt;
    this.contact_fliter = this.contact_opt;

    //-----------------------存留過濾條件處理------------------------//
    let sessionStorage_fliter = JSON.parse(sessionStorage.getItem('fliter'))
    if(sessionStorage_fliter){
      if(sessionStorage_fliter['customer_value']) this.customer_value = sessionStorage_fliter['customer_value']
      if(sessionStorage_fliter['KeyID_value']) this.KeyID_value = sessionStorage_fliter['KeyID_value']
      if(sessionStorage_fliter['category_value']) this.category_value = sessionStorage_fliter['category_value']
      if(sessionStorage_fliter['product_value']) this.product_value = sessionStorage_fliter['product_value']
      if(sessionStorage_fliter['module_value']) this.module_value = sessionStorage_fliter['module_value']
      if(sessionStorage_fliter['version_value']) this.version_value = sessionStorage_fliter['version_value']
      if(sessionStorage_fliter['issued_value']) this.issued_value = sessionStorage_fliter['issued_value']
      if(sessionStorage_fliter['count_value']) this.count_value = sessionStorage_fliter['count_value']
      if(sessionStorage_fliter['type_value']) this.type_value = sessionStorage_fliter['type_value']
      if(sessionStorage_fliter['region_value']) this.region_value = sessionStorage_fliter['region_value']
      if(sessionStorage_fliter['contact_value']) this.contact_value = sessionStorage_fliter['contact_value']
      if(sessionStorage_fliter['expiration_value']) this.expiration_value = sessionStorage_fliter['expiration_value']
      if(sessionStorage_fliter['expiring_days']) this.expiring_days = sessionStorage_fliter['expiring_days']
      if(sessionStorage_fliter['expiring_check']) this.expiring_check = sessionStorage_fliter['expiring_check']
      if(sessionStorage_fliter['expired_check']) this.expired_check = sessionStorage_fliter['expired_check']
      if(sessionStorage_fliter!= undefined || JSON.stringify(sessionStorage_fliter)!=JSON.stringify({}))
        this.category_filter()
    }
    
    if(user_setting['mode'] != 'product')
      this.$router.push({name: 'KeyID'});

    this.search_drawer = true;
    this.isLoading = false;
    })
    }
  },
  methods: {
    click_apply_record(){
      this.form.apply_record = []
      let inner_data = {}
      let sn = this.form.form_KeyID
      if(this.apply_record_map[sn] != undefined) {
        // 處理展開所需資料
        for(let map of this.apply_record_map[sn]){
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
        for(let map of this.apply_record_map[sn]){
          if(id_list.includes(map['id']))
            continue
          this.form.apply_record.push({'id':map['id'], 'date':map['date'], 'applicant':map['applicant'], 'status':map['status'], 
          'verify_time':map['verify_time'], 'data': inner_data[map['id']]})
          id_list.push(map['id'])
        }
      }
      this.apply_record_dialog = true
    },
    /*---搜尋欄---*/
    drawer_open(){
      this.search_drawer = true
      this.search_drawer_btn = false
      document.getElementById('showtable').style.width = '75%'
    },
    drawer_close(){
      this.search_drawer = false
      document.getElementById('showtable').style.width = '85%'
    },
    contact_enter(){
      this.contact_value.push(this.contact_input)
      this.contact_input = ''
    },
    contact_fliterer(val){
      if (val) {
        this.contact_input = val;
        this.contact_fliter = this.contact_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    region_enter(){
      this.region_value.push(this.region_input)
      this.region_input = ''
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
    type_enter(){
      this.type_value.push(this.type_input)
      this.type_input = ''
    },
    type_fliterer(val){
      if (val) {
        this.type_input = val;
        this.type_fliter = this.type_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    count_enter(){
      this.count_value.push(this.count_input)
      this.count_input = ''
    },
    count_fliterer(val){
      if (val) {
        this.count_input = val;
        this.count_fliter = this.count_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    version_enter(){
      this.version_value.push(this.version_input)
      this.version_input = ''
    },
    version_fliterer(val){
      if (val) {
        this.version_input = val;
        this.version_fliter = this.version_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    module_enter(){
      this.module_value.push(this.module_input)
      this.module_input = ''
    },
    module_fliterer(val){
      if (val) {
        this.module_input = val;
        this.module_fliter = this.module_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    product_enter(){
      this.product_value.push(this.product_input)
      this.product_input = ''
    },
    product_fliterer(val){
      if (val) {
        this.product_input = val;
        this.product_fliter = this.product_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    category_enter(){
      this.category_value.push(this.category_input)
      this.category_input = ''
    },
    category_fliterer(val){
      if (val) {
        this.category_input = val;
        this.category_fliter = this.category_opt.filter((item) => {
          if (!!~String(item['label']).indexOf(val)) 
            return true
        })
      }
    },
    customer_enter(){
      this.customer_value.push(this.customer_input)
      this.customer_input = ''
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
    KeyID_enter(){
      this.KeyID_value.push(this.KeyID_input)
      this.KeyID_input = ''
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
    select_change(){
      this.select_out = !this.select_out;
    },
    pagesize_change(){//變更單頁筆數時 去DB更改User[setting]
      let self = this;
      if(self.pagesize == 'all'){
        self.pagesize = self.tableData.length
        self.axios.post("/save_to_user_setting",{
          source:'product',
          user:self.user[0],
          mode:'product',
          pagesize:'all'
        })
      }
      else{
        self.axios.post("/save_to_user_setting",{
          source:'product',
          user:self.user[0],
          mode:'product',
          pagesize:parseInt(self.pagesize)
        })
      }
    },
    mode_switch(mode){//模式切換時觸發 更改DB User[setting]
      let self = this;
      if(mode == "KeyID"){
        this.axios.post("/save_to_user_setting",{
          source:'product',
          user:self.user[0],
          mode:mode,
          pagesize:self.pagesize
        }).then(response => {
          self.$router.push({name: 'KeyID'});
        })
      }
    },
    all_check(){//自製的全選框被觸發時
      if(this.all_checked == true)
        this.$refs.showtable.toggleAllSelection()
      else 
        this.$refs.showtable.clearSelection()
    },
    selection_column_style:function(row){//將header 全選框隱藏 因為排版問題只能自己做一個自製全選框 
      if(row.columnIndex == 0)
        return 'selection_style'
    },
    Logout:function(){
      sessionStorage.clear();
      this.$router.push('/login');
    },
    GoCheck:function(){//編輯頁面
      this.$router.push({path: `/check/${this.user[0]}`});
    },
    GoHandle:function(){//編輯頁面
      this.$router.push({name: 'handle'});
    },
    GoAdd:function(){//新增頁面
      this.checked_Data.forEach((item)=> delete item['info'])
      this.$router.push({name: 'add', query:{checked_Data: JSON.stringify(this.checked_Data)}});
    },
    GoEdit:function(){//修改頁面
      if(this.checked_Data[0] == undefined){
        this.$alert('請選取欲修改的資料', '', {center: true, type: 'warning'});
        return;
      }//也可以用this.$router.push(name:'',params:{})傳參數 但要設置路由
      delete this.all_Data['info_data']//edit頁面用不到 節省傳輸時間
      this.checked_Data.forEach((item)=> delete item['info'])
      this.$router.push({name: 'edit', query:{user:JSON.stringify(this.user),checked_Data: JSON.stringify(this.checked_Data),all_Data: JSON.stringify(this.all_Data)}});
    },
    Go_Edit_time:function(){//延展到期日
      if(this.checked_Data[0] == undefined){
        this.multi_keyID_mode = '展延'
        this.error_message.digital_error = ''
        this.error_message.type_error = ''
        this.error_message.exist_error = ''
        this.multi_keyID_dialog = true
      }
      else{
        this.$prompt("請輸入到期日",'到期日修改',{
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          inputType:'date',
          inputPattern:/\d.\d.\d/,
          inputErrorMessage:'輸入日期不合法!'
        }).then(({ value }) => {
          for(let check of this.checked_Data){//
            check = Object.assign(check,{'operator':'修改'})
            check = Object.assign(check,{'expiration':value})
            delete check['info']
          }

          this.axios.post("/save_to_handle",{
            checked_Data:this.checked_Data,
            content:'延展到期日',
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
                  location.reload();
              });
          })
        }).catch(() => {
          this.$message({type: 'info', message: '已取消修改'});
        });
      }
    },
    multi_keyID_dialog_click(){
      this.multi_keyID_text = document.getElementById('multi_keyID_textarea').value
      if(this.multi_keyID_text == undefined ||  this.multi_keyID_text == null)
        return
      
      this.multi_keyID_error_message = ''
      var valid_keyIDs = []
      var digital_error_keyIDs = []
      var type_error_keyIDs = []
      var exist_error_keyIDs = []
      this.error_message.digital_error = ''
      this.error_message.type_error = ''
      this.error_message.exist_error = ''
      let regex = /^[0-9]*$/;
      // 將全型轉半形
      let input_text = toHalf(this.multi_keyID_text)
      if(input_text.trim().length == 0)
        return

      // 檢查合法性
      for(let input of input_text.split(';')){
        if(input.trim() == '')
          continue

        if (input.trim().length != 7)
          digital_error_keyIDs.push(input.trim())
        else if(!regex.test(input.trim()))
          type_error_keyIDs.push(input.trim())
        else if(!this.info_keyID.includes(Number(input.trim())))
          exist_error_keyIDs.push(input.trim())
        else
          valid_keyIDs.push(input.trim())
      }

      // 錯誤訊息
      if(digital_error_keyIDs.length)
        this.error_message.digital_error = `錯誤 - 只允許 7 碼數字：${digital_error_keyIDs.join('、')}`
      if(type_error_keyIDs.length)
        this.error_message.type_error = `錯誤 - 只允許數字和 ;：${type_error_keyIDs.join('、')}`
      if(exist_error_keyIDs.length)
        this.error_message.exist_error = `錯誤 - 以下id不存在：${exist_error_keyIDs.join('、')}`
      // 驅動錯誤訊息顯示
      this.multi_keyID_text += ' '
      this.multi_keyID_text = this.multi_keyID_text.substring(0, this.multi_keyID_text.length - 1)

      // 輸入都合法
      if(!digital_error_keyIDs.length && !type_error_keyIDs.length && !exist_error_keyIDs.length){
        if(this.multi_keyID_mode == '展延'){
          this.$prompt("請輸入到期日",'到期日修改',{
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            inputType:'date',
            inputPattern:/\d.\d.\d/,
            inputErrorMessage:'輸入日期不合法!'
          }).then(({ value }) => {
            let multi_sn_data = []
            for(let keyID of valid_keyIDs){
              let data = {}
              let user = this.sn_dict[keyID]['user']
              let sn_id = this.sn_dict[keyID]['sn_id']
              let region = this.sn_dict[keyID]['region']
              let customer_site = this.customer_dict[sn_id]['site']
              let customer = this.customer_dict[sn_id]['name']
              if(customer_site != '')
                customer += `|${customer_site}`
              data = Object.assign(data,{'sn':keyID})
              data = Object.assign(data,{'operator':'多筆延展'})
              data = Object.assign(data,{'user':user})
              data = Object.assign(data,{'customer':customer})
              data = Object.assign(data,{'expiration':value})
              data = Object.assign(data,{'region':region})
              data = Object.assign(data,{'count':''})
              data = Object.assign(data,{'contact':''})
              data = Object.assign(data,{'operation_type':'multiple_expand'})
              multi_sn_data.push(data)
            }
            this.axios.post("/save_to_handle",{
              checked_Data: multi_sn_data,
              content:'延展到期日',
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
                    location.reload();
                });
            })
          }).catch(() => {
            this.$message({type: 'info', message: '已取消修改'});
          })
        }
        else if (this.multi_keyID_mode == '刪除'){
          let multi_sn_data = []
          for(let keyID of valid_keyIDs){
            let data = {}
            let user = this.sn_dict[keyID]['user']
            let sn_id = this.sn_dict[keyID]['sn_id']
            let region = this.sn_dict[keyID]['region']
            let customer_site = this.customer_dict[sn_id]['site']
            let customer = this.customer_dict[sn_id]['name']
            if(customer_site != '')
              customer += `|${customer_site}`
            data = Object.assign(data,{'sn':keyID})
            data = Object.assign(data,{'operator':'多筆刪除'})
            data = Object.assign(data,{'user':user})
            data = Object.assign(data,{'customer':customer})
            data = Object.assign(data,{'region':region})
            data = Object.assign(data,{'count':''})
            data = Object.assign(data,{'expiration':''})
            data = Object.assign(data,{'contact':''})
            data = Object.assign(data,{'operation_type':'multiple_delete'})
            multi_sn_data.push(data)
          }
          this.axios.post("/save_to_handle",{
            checked_Data: multi_sn_data,
            content:'',
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
                  location.reload();
              });
          })
        }
      }
         
    },
    GoDownload:function(){//下載勾選資料
      var data_download = [];
      var i = 0;
      for(let check of this.download_data){
        data_download.push(check);
        data_download[i] = Object.assign(data_download[i],{'operator':'下載'});//增加index讓 row中有index
        i++;
      }
      if(this.download_format == 'excel'){  //excel
        this.axios({
          method: 'post', // 请求方式
          url: '/download_show',
          data: {
            format: 'excel',
            user:this.user,
            data:data_download,
          }, // 请求参数
          responseType: 'blob' // 服务器返回的数据类型
        }).then((response)=>{
            this.tranfer_xlsx(response.data)
        })
      }
      else if(this.download_format == 'csv'){   //csv
        this.axios({
          method: 'post', // 请求方式
          url: '/download_show',
          data: {
            format: 'csv',
            user:this.user,
            data:data_download,
          }, 
        }).then((response)=>{
            this.tranfer_csv(response.data)
        })
      }
      else if(this.download_format == 'json'){   //json
        this.axios({
          method: 'post', // 请求方式
          url: '/download_show',
          data: {
            format: 'json',
            user:this.user,
            data:data_download,
          }, 
        }).then((response)=>{
            this.tranfer_json(response.data)
        })
      }
    },
    GoDelete: function(){//刪除頁面
      if(this.checked_Data[0] == undefined){
        this.multi_keyID_mode = '刪除'
        this.error_message.digital_error = ''
        this.error_message.type_error = ''
        this.error_message.exist_error = ''
        this.multi_keyID_dialog = true
      }
      //刪除原因，暫無用處
      // var comment = prompt("請填寫刪除原因: (ex: 客戶測試結束、損壞)");
      // if(comment == null)//當使用者按cancel時
      //   return;
      // else if(comment == ''){
      //   alert('請填寫原因');
      //   return;
      // }
      else{
        this.$confirm('確定要刪除嗎?', '提示', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning',
            center: true
        }).then(() => {
          for(let check of this.checked_Data){
            check = Object.assign(check,{'operator':'刪除'})
            delete check['info']
          }
          
          this.axios.post("/save_to_handle",{
                checked_Data:this.checked_Data,
                content:"",
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
                  location.reload();
              });
          });

        }).catch(() => {
            this.$message({type: 'info',message: '已取消刪除'});
        });
      }
    },
    rowclick(row, event, column){//點選列時也可以觸發勾選框
      if(event['label'] != '')
        this.$refs.showtable.toggleRowSelection(row);
    },
    handleSelectionChange (val) {//當select 有變化時執行 且val是所選row的所有資訊(type:array)
      this.checked_Data = JSON.parse(JSON.stringify(val));
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
    clear_filter:function(){
      this.customer_value = []
      this.issued_value = null
      this.KeyID_value = []
      this.product_value = []
      this.contact_value = []
      this.expiration_value = null
      this.count_value = []
      this.region_value = []
      this.type_value = []
      this.category_value = []
      this.module_value = []
      this.version_value = []
      this.expiring_check = false
      this.expired_check = false
      this.category_filter()
      sessionStorage.setItem('fliter', JSON.stringify({}));
    },
    category_filter: function(){//對product分頁底下的tableData做過濾2
      if(this.expiring_check){
        if((!Number.isInteger(Number.parseInt(this.expiring_days))) || (Number.parseInt(this.expiring_days)<0)){
          this.$alert("到期日請輸入正整數!", "提示", {type: 'warning', center: true})
          return
        }
      }

      sessionStorage.setItem('fliter', JSON.stringify({
        'customer_value':this.customer_value,
        'KeyID_value':this.KeyID_value,
        'category_value':this.category_value,
        'product_value':this.product_value,
        'module_value':this.module_value,
        'version_value':this.version_value,
        'count_value':this.count_value,
        'type_value':this.type_value,
        'region_value':this.region_value,
        'contact_value':this.contact_value,
        'expiring_days':this.expiring_days,
        'expiring_check':this.expiring_check,
        'expired_check':this.expired_check,
        'expiration_value':this.expiration_value,
        'issued_value':this.issued_value,
      }));
      for(let i in  this.KeyID_value)
        this.KeyID_value[i] = parseInt(this.KeyID_value[i])
      for(let i in  this.count_value)
        this.count_value[i] = parseInt(this.count_value[i])

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

      function contactFilter(array, contact_value) {
        let filterArr = []
        for(let arr of array){
          for(let cont of contact_value){
            if(!!~arr['contact_display'].indexOf(cont)){
              filterArr.push(arr);
              break;
            }
          }
        }
        return filterArr;
      }
 
      var copy_data = [];
      var no_filter = false
      //都沒選
      if(!(this.customer_value).length && 
          !(this.KeyID_value).length && 
          !(this.category_value).length && 
          !(this.product_value).length &&
          !(this.module_value).length &&
          !(this.version_value).length &&
          (this.issued_value == null) &&
          !(this.count_value).length && 
          !(this.type_value).length && 
          !(this.region_value).length &&
          !(this.contact_value).length &&
          (this.expiration_value == null)
        ){ 
        copy_data = this.filter_Data; 
        no_filter = true
      }
      //有選
      else{ 
        var filters = {}
        var contact_filters = {};
        filters['customer'] =  this.customer_value;
        filters['sn'] = this.KeyID_value;
        filters['category'] = this.category_value;
        filters['product'] = this.product_value;
        filters['module'] = this.module_value;
        filters['version'] = this.version_value;
        filters['count'] = this.count_value;
        filters['type'] = this.type_value;
        filters['region'] = this.region_value;
        copy_data = multiFilter(this.filter_Data,filters);
        if(this.contact_value.length)
          copy_data = contactFilter(copy_data, this.contact_value);
      }
          
      if(this.expiration_value == null && this.issued_value == null){
      }
      else if(this.expiration_value == null){
        copy_data = copy_data.filter(x => (this.issued_value[0] <= x['issued'] && x['issued'] <= this.issued_value[1]))
      }
      else if(this.issued_value == null){
        copy_data = copy_data.filter(x => (this.expiration_value[0] <= x['expiration'] && x['expiration'] <= this.expiration_value[1]))
      }
      else{
        copy_data = copy_data.filter(x => (this.issued_value[0] <= x['issued'] && x['issued'] <= this.issued_value[1]
                                          && this.expiration_value[0] <= x['expiration'] && x['expiration'] <= this.expiration_value[1]))
      }
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
    tabClick(tab, event) {//當點擊標籤頁時1
      this.currentPage = 1;
      this.all_checked = false;//自製全選框連動
      this.customer_value = '';
      this.KeyID_value = '';
      this.category_value = '';
      this.product_value = '';
      this.module_value = '';
      this.version_value = '';
      this.count_value = '';
      this.type_value = '';
      this.region_value = '';
      this.contact_value = '';
      this.issued_value = null;
      this.expiration_value = null;

      if(tab.label == '總表'){//如果是all就顯示原tableData
        this.tableData = this.origin_Data;
        this.filter_Data = this.origin_Data;
        this.sort_Data = this.origin_Data;
      }
      else if(tab.label == '一個月內過期'){
        var tempDate = new Date;
        
        tempDate.setHours(tempDate.getHours());
        var today = tempDate.toISOString().slice(0, 10)

        tempDate.setMonth(tempDate.getMonth()+1);
        var oneMonthLater = tempDate.toISOString().slice(0, 10)
        this.filter_Data = this.origin_Data.filter(item=> item['expiration'] < oneMonthLater)//濾掉綠色
        this.filter_Data = this.filter_Data.filter(item=> item['expiration'] > today)//濾掉紅色
        this.tableData = this.filter_Data;
        this.sort_Data = this.filter_Data;
      }
      else if(tab.label == '已過期'){
        var tempDate = new Date;
        tempDate.setHours(tempDate.getHours());
        var today = tempDate.toISOString().slice(0, 10)
        this.filter_Data = this.filter_Data.filter(item=> item['expiration'] < today)//留下紅色
        this.tableData = this.filter_Data;
        this.sort_Data = this.filter_Data;
      }
      else{
        var copy_data = []
        this.filter_Data = this.origin_Data.filter(item=> item['category'] == tab.label)
        this.tableData = this.filter_Data;
        this.sort_Data = this.filter_Data;
      }
    },
    tableRowColor({row, rowIndex}) {//比較當前與過期時間來顯示顏色
        var Index = rowIndex + (this.currentPage - 1) * this.pagesize;//分頁問題 當換到當前分頁時顏色才會顯現正確
        row.index = rowIndex;//把每一行的index放入row 為了給rowclick用
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
    handleCurrentChange: function(currentPage) {//點擊第幾頁
        this.currentPage = currentPage;
        this.all_checked = false;//自製全選框初始化
    },
    //web下載 xlsx
    tranfer_xlsx(data) {
      if(!data)
        return
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    //web下載 csv
    tranfer_csv(data) {
      if(!data) return
      let csv_data = data.join('\n');
      csv_data = new Blob([`\ufeff${csv_data}`], {type: "data:text/csv;charset=utf-8,%EF%BB%BF"})
      let url = window.URL.createObjectURL(csv_data)
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.csv')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    //web下載 json
    tranfer_json(data) {
      if(!data) return
      let json_data = new Blob([JSON.stringify(data)], {type: 'application/json'})
      let url = window.URL.createObjectURL(json_data)
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.json')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    // 點擊>按鈕
    detail_form(row){
      this.form.form_data.fold = []
      this.form.form_data.expand = []
      this.form.form_customer = row['customer']
      this.form.form_KeyID = row['sn']
      if(row['info'] != ''){
        let row_info = eval(row['info']);
        for(let i of row_info){
          if(i.length == 1){
            this.form.form_data.fold.push(i[0]);
            this.form.form_data.expand.push(i);
          }
          else if(i.length == 2){
            this.form.form_data.fold.push(i[1]);
            this.form.form_data.expand.push(i)
          }

        }
      }
      
      this.detail=true;
    },
    
    click_download(){
      this.download_data = this.checked_Data;
      if(this.checked_Data.length >0){
        this.$alert(
            '<input type="radio" id="excel" name="downloadType" value="excel" checked><label for="excel" style="margin-right: 100px;">excel</label>'+
            '<input type="radio" id="csv" name="downloadType" value="csv"><label for="csv" style="margin-right: 100px;">csv</label>'+
            '<input type="radio" id="json" name="downloadType" value="json"><label for="json">json</label>'+
            '<br><br><br>-----------------------------------------------------------------------------------<br>其他文件<br>'+
            '<div style="position:relative; top:10px"><a href="/static/keypro_application.docx" download="keypro領用申請單.docx"><i class="el-icon-paperclip"></i>keypro領用申請單</a>'+
            `<span style="position:relative; right:-74px;">更新日期：${this.keypro_application_time}</span></div>`+
            
            '<div style="position:relative; top:20px"><a href="/static/official_application.xls" download="申請永久正式key表格.xls"><i class="el-icon-paperclip"></i>申請永久正式key表格</a>'+
            `<span style="position:relative; right:-50px;">更新日期：${this.official_application_time}</span></div>`+

            '<div style="position:relative; top:30px"><a href="/static/license" download="license"><i class="el-icon-paperclip"></i>license</a>'+
            `<span style="position:relative; right:-143px;">更新日期：${this.license_time}</span></div>`,
            '請選擇下載格式', {
            dangerouslyUseHTMLString: true, confirmButtonClass:"alert_class"
        }).then((response)=>{
              if(document.getElementById("excel").checked){
                this.download_format = "excel";
              }
              else if(document.getElementById("csv").checked){
                this.download_format = "csv";
              }
              else if(document.getElementById("json").checked){
              this.download_format = "json";
              }
              this.$message({type: 'success', message: '開始下載'});
              this.GoDownload();
          }).catch(() => {
              this.$message({type: 'info', message: '取消下載'});
          })
      }
      else{

        this.$alert(
            '<div style="position:relative; top:10px"><a href="/static/keypro_application.docx" download="keypro領用申請單.docx"><i class="el-icon-paperclip"></i>keypro領用申請單</a>'+
            `<span style="position:relative; right:-74px;">更新日期：${this.keypro_application_time}</span></div>`+
            
            '<div style="position:relative; top:20px"><a href="/static/official_application.xls" download="申請永久正式key表格.xls"><i class="el-icon-paperclip"></i>申請永久正式key表格</a>'+
            `<span style="position:relative; right:-50px;">更新日期：${this.official_application_time}</span></div>`+

            '<div style="position:relative; top:30px"><a href="/static/license" download="license"><i class="el-icon-paperclip"></i>license</a>'+
            `<span style="position:relative; right:-143px;">更新日期：${this.license_time}</span></div><br>`,
            "其他文件",
            {dangerouslyUseHTMLString: true}
        )
      
      }
    },
    reload(){
      location.reload();
    },
 
  },
  computed:{
    delay_time: function(){
      return this.select_out * 10000;
    }
  }
}
</script>


