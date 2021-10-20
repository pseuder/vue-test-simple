<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#note{
    display:inline;
}
.input_no_border textarea.el-textarea__inner{
  border: 0px solid #dcdfe6;
  resize:none;
}
.el-textarea ::-webkit-scrollbar{
    display: none;
}
.el-notification {
  white-space:pre !important; 
  width:450px;
}
</style>
<style scoped>
.el-table{
  font-size: 18px !important;
}
.user-apply-form /deep/ .el-form-item__label{
  position: relative;
  top: 10px;
  font-size: 19px;
  width: 350px;
}
.el-tabs /deep/ .el-tabs__item{
  font-size: 18px;
}
.num-badge{
  border-radius: 10px;
  width: 20px;
  height: 20px;
  position: relative;
  top: 0px;
  right: -16px;
  line-height: 23px;
  background-color: rgb(245, 108, 108);
  color: #fff;
}
</style>
<template>
  <div>
      <transition name="fade"><!--loading動畫-->
        <loading v-if="isLoading"></loading>
      </transition>
      <div style="position: absolute; right: 12%; top: 18px;">
        
        <el-button style="margin-right: 25px; background-color:#EAEAEA; border-color:#EAEAEA; padding: 8px 11px; font-size: 18px;" 
          icon="el-icon-s-home" @click="$router.push({name: 'Show_All'})">主頁面</el-button>
        
        <el-link type="success"  icon="el-icon-s-custom" @click="$router.push({name: 'admin', query:{}})" style="font-size: 18px;">{{user[0]}}</el-link>
      </div>
      
      <el-tabs type="border-card" style="width:1300px; margin: 0px auto; height: 830px;" v-model="editableTabsValue">
      <el-tab-pane label="待審核資料" name="待審核資料" >
        <span slot="label" style="display:flex">
          待審核資料
          <div class="num-badge">{{app_Data_num}}</div>
        </span>
      <div style="width:1280px; margin:0 auto; top: -33px; position: relative;">
      <div style="position:relative;top:50px" align = "center">
        <el-table :data="app_Data" height= 650px>
        <el-table-column type="" align="center" prop="fake_id" label="順序編號" width="100"></el-table-column>
        <el-table-column type="" align="center" prop="" label="清除紀錄" width="130">
          <template slot-scope = "{row}" >
            <el-button type="danger" size="mini" @click.native="clear_data(row)" icon="el-icon-delete-solid" circle></el-button>
          </template>
        </el-table-column>
        <el-table-column align="left" prop="check" width="55">
        <template slot-scope = "{row,$index}">
          <el-checkbox v-model="check[$index]" @change="click_checkbox(check[$index],$index)" :disabled="disabled_checkbox(row)"></el-checkbox>
        </template>
        </el-table-column>
        <el-table-column type="" header-align="center" prop="validator"  :render-header="label_for_validator" width="300">
        <template align="left" slot-scope = "{row,$index}">
          審核群組:
          <template v-for="(item, index) in row.validator['verify_group']">
          <span style="color: #67C23A" v-if="row.validator['verify_check']['verify_group'][index] == true">{{item}}</span><!--條件通過-->
          <span style="color: #FF7575" v-if="row.validator['verify_check']['verify_group'][index] == false">{{item}}</span><!--條件未過-->
          <span v-if="(index+1) != row.validator['verify_group'].length">,</span>
          </template>
          <br>審核人數:
          <span style="color: #67C23A" v-if="row.validator['verify_check']['verify_num'] >= row.validator['verify_num']">{{row.validator['verify_num']}}</span><!--條件通過-->
          <span style="color: #FF7575" v-if="row.validator['verify_check']['verify_num'] < row.validator['verify_num']">{{row.validator['verify_num']}}</span><!--條件未過-->
        </template>
        </el-table-column>
        <el-table-column type=""align="center" prop="id" label="申請編號" width="100"></el-table-column>
        <el-table-column type=""align="center" prop="verify_status" label="審核狀態" width="120">
        <template slot-scope = "{row,$index}" >
        <span v-show="row.verify_status==1" style="color: #67C23A">已審核</span>
        <span v-show="row.verify_status==0" style="color: #FF7575">尚未審核</span>
        </template>
        </el-table-column>
        <el-table-column type=""align="center" prop="applicant" label="申請人" width="100"></el-table-column>
        <el-table-column type=""align="center" prop="date" label="申請日期" width="180"></el-table-column>
        <el-table-column type=""align="center" prop="" label="編輯" width="150">
          <template slot-scope = "{row,$index}" ><!--此時row是app_data-->
            <el-button type="text" @click="open_dialog(row,$index)">查看資料</el-button>
            <el-dialog width='95%' title="申請內容" :visible.sync="dialogTableVisible[$index]">
              <div style="display:flex; font-size: 18px;">
                <div style="width:33%">
                  <!-- 申請人 -->
                  <div style="display:flex">
                    <div style="text-align: end; width:40%; margin-right: 25px; bottom: -3px; position: relative;"> 申請人 :</div>
                    <div style="text-align: start;">
                      <el-input class="input_no_border" type="textarea" :autosize="{ minRows: 1, maxRows: 1}" name="sender" v-model="content['user']" readonly 
                        style="width:150px;" />
                    </div>
                  </div>
                  <!-- 副本 -->
                  <div style="display:flex">
                    <div style="text-align: end; width:40%; margin-right: 25px; bottom: -9px; position: relative;"> 副本 :</div>
                    <div style="text-align: start;  width:55%">
                      <template  v-for="(item, index) in cc">
                        <el-autocomplete v-model="cc[index]"  :fetch-suggestions="querySearch_cc" placeholder="請輸入副本" ></el-autocomplete>
                        <el-button v-show="index != 0" type="text" icon="el-icon-error"  @click="remove_cc(index)"></el-button>
                      </template>
                      <el-button type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="add_cc()"></el-button>
                    </div>
                  </div>
                  <!-- 附件下載 -->
                  <div style="display:flex">
                    <div style="text-align: end; width:40%; margin-right: 25px; bottom: -9px; position: relative;"> 附件下載 :</div>
                    <div style="text-align: start;">
                      <el-button style="" type="text" @click="download_check(row,$index)">license-application.xlsx</el-button>
                    </div>
                  </div>
                  <!-- 申請內文 -->
                  <div style="display:flex">
                    <div style="text-align: end; width:40%; margin-right: 25px; bottom: 2px; position: relative;"> 申請內文 :</div>
                    <div style="text-align: start;">
                     <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="content['text']" readonly 
                      :disabled="true" style="width:250px;" />
                    </div>
                  </div>
                </div>

                <div style="width:33%">
                  <!-- 審核者回覆 -->
                  <div style="display:flex">
                    <div style="text-align: end; width:20%; margin-right: 25px; bottom: 2px; position: relative;"> 審核者回覆 :</div>
                    <div style="text-align: start;">
                     <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="content['reply']" 
                        style="width:400px;" />
                    </div>
                  </div>
                </div>
                
                <div style="width:33%; top: -22px; position: relative;">
                  <!-- 統計紀錄 -->
                  <div> 申請紀錄統計(總共{{tableData.length}}筆)</div>
                  <div style="height: 180px; width: auto; overflow: auto; border: 1px solid #dcdfe6; border-radius: 4px; margin: 0px auto;text-align: right;">
                    <div v-html="data_statistics_text" style="font-size: 20px; position: relative; left: -15px;"></div>
                  </div>
                </div>
              </div>

              <div style="text-align: start">
                <el-button style="background-color:#67C23A; border-color:#67C23A; padding: 8px 11px; color: #ffffff;" 
                  icon="el-icon-check" @click="all_approve"></el-button>
                <el-button style="background-color:#F56C6C; border-color:#F56C6C; padding: 8px 11px; color: #ffffff;" 
                  icon="el-icon-close" @click="all_reject"></el-button>
                <el-button style="background-color:#909399; border-color:#909399; padding: 8px 11px; color: #ffffff;" 
                  icon="el-icon-refresh-right" @click="all_clear"></el-button>
              </div>

              <div>
                <el-table :data="tableData" height="400px">
                  <el-table-column align="center" prop="customer" label="審核"  width="100px" >
                    <template slot-scope = "{row,$index}" ><!--此時row是app_data['data']-->
                      <el-radio-group :ref="`radio-${$index}`" :fill="radio[$index] == '√'? '#67C23A':'#F56C6C'" v-model="radio[$index]" @change="verify_change(row,$index)" size="mini">
                        <el-radio-button label="√"></el-radio-button>
                        <el-radio-button label="×" ></el-radio-button>
                      </el-radio-group>
                    </template>
                  </el-table-column>
                  <el-table-column type=""align="center" prop="" label="編輯" width="100">
                    <template slot-scope = "{row,$index}" >
                    <el-row>
                      <el-button type="primary" size="mini"@click.native="handleCheck($index, row)"  v-if="showEdit[$index]"icon="el-icon-check" circle></el-button>
                      <el-button type="danger"  style="position:relative;right:5px;" size="mini"@click.native="handelRestore($index, row)"  v-if="showEdit[$index]"icon="el-icon-close" circle></el-button>
                      <el-button type="primary" size="mini"@click.native="handleEdit($index, row)"  v-if="!showEdit[$index]"icon="el-icon-edit" circle></el-button>
                      <el-popover ref="popover" width="950px" trigger="hover" placement="top-start" offset="300">
                        <el-table :cell-class-name="cell_color" :data="compare_Data" >
                        <el-table-column width="100px" prop="customer" label="客戶"></el-table-column>
                        <el-table-column width="130px" prop="issued" label="更新日期"></el-table-column>
                        <el-table-column width="70px" prop="sn" label="KeyID"></el-table-column>
                        <el-table-column width="140px" prop="func_uid" label="產品名稱"></el-table-column>
                        <el-table-column width="70px" prop="version" label="版本"></el-table-column>
                        <el-table-column width="70px" prop="type" label="類型"></el-table-column>
                        <el-table-column width="70px" prop="count" label="數量"></el-table-column>
                        <el-table-column width="130px" prop="expiration" label="到期日期"></el-table-column>
                        <el-table-column width="70px" prop="region" label="地區"></el-table-column>
                        <el-table-column width="140px" prop="comment" label="備註"></el-table-column>
                        <el-table-column width="150px" prop="contact" label="聯絡人"></el-table-column>
                        </el-table>
                        <el-button type="info " size="mini" slot="reference" @mouseenter.native="compare_row(row,$index)" v-show="row.operator=='修改'" icon="el-icon-view" circle></el-button>
                      </el-popover>
                    </el-row>
                    </template>
                  </el-table-column>
                  <el-table-column align="center" prop="operator" label="操作" width="100"></el-table-column>
                  <el-table-column align="center" prop="customer" label="客戶" width="100">
                    <template slot-scope = "{row,$index}" >
                      <el-autocomplete  v-if="showEdit[$index]" style="width: 70px"  size='small' name="customer" v-model="row.customer"
                          :fetch-suggestions="querySearch_customer"></el-autocomplete>
                      <!--<el-input v-if="showEdit[$index]" type="text" name="customer" v-model="row.customer" style="width: 110px"></el-input>-->
                      <span v-if="!showEdit[$index]">{{row.customer}}</span>
                    </template>
                  </el-table-column>
                  <el-table-column align="center" prop="issued" label="更新日期" width="160">
                    <template slot-scope = "{row,$index}" >
                      <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="issued" v-model="row.issued" style="width: 135px;"></el-date-picker>
                      <span v-if="!showEdit[$index]">{{row.issued}}</span>
                    </template>
                  </el-table-column>
                  <el-table-column align="center" prop="sn" label="KeyID" width="100px">
                  <template slot-scope = "{row,$index}" >
                      <el-input v-if="showEdit[$index]" type="text" name="sn" v-model="row.sn" style="width: 90px"></el-input>
                      <span v-if="!showEdit[$index]">{{row.sn}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="product" label="產品">
                  <template slot-scope = "{row,$index}" >
                      <el-autocomplete  v-if="showEdit[$index]" size='small' name="func_uid" v-model="row.product"
                          :fetch-suggestions="querySearch_func_uid"></el-autocomplete>
                      <span v-if="!showEdit[$index]">{{row.product}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="product" label="模組">
                  <template slot-scope = "{row,$index}" >
                      <span >{{row.module}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="version" label="版本" width="100px">
                  <template slot-scope = "{row,$index}" >
                      <el-input v-if="showEdit[$index]" type="text" name="version" v-model="row.version" style="width: 70px"></el-input>
                      <span v-if="!showEdit[$index]">{{row.version}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="type" label="類型" width="110px" >
                  <template slot-scope = "{row,$index}" >
                      <el-autocomplete  v-if="showEdit[$index]" style="width:80px"  size='small' name="type" v-model="row.type"
                          :fetch-suggestions="querySearch_type"></el-autocomplete>
                      <!--<el-input v-if="showEdit[$index]" type="text" name="type" v-model="row.type" style="width: 60px"></el-input>-->
                      <span v-if="!showEdit[$index]">{{row.type}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="count" label="數量" width="100px">
                  <template slot-scope = "{row,$index}" >
                      <el-input v-if="showEdit[$index]" type="text" name="count" v-model="row.count" style="width: 50px"></el-input>
                      <span v-if="!showEdit[$index]">{{row.count}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="expiration" label="到期日期" width="160px">
                  <template slot-scope = "{row,$index}" >
                    <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="expiration" v-model="row.expiration" style="width: 135px;"></el-date-picker>
                    <span v-if="!showEdit[$index]">{{row.expiration}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="region" label="地區" width="110px" >
                  <template slot-scope = "{row,$index}" >
                    <el-autocomplete  v-if="showEdit[$index]" style="width:80px"  size='small' name="region" v-model="row.region"
                      :fetch-suggestions="querySearch_region"></el-autocomplete>
                    <!--<el-input v-if="showEdit[$index]" type="text" name="region" v-model="row.region" style="width: 60px"></el-input>-->
                    <span v-if="!showEdit[$index]">{{row.region}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="comment" label="備註">
                  <template slot-scope = "{row,$index}" >
                    <el-input v-if="showEdit[$index]" type="text" name="comment" v-model="row.comment" style="width: 110px"></el-input>
                    <span v-if="!showEdit[$index]">{{row.comment}}</span>
                  </template>
                  </el-table-column>
                  <el-table-column align="center" prop="contact" label="聯絡人" :width="max_contact_length * 10 + 30">
                  <template slot-scope = "{row,$index}">
                    <el-input v-if="showEdit[$index]" type="text" name="contact" v-model="row.contact" style="width: 170px"></el-input>
                    <span v-if="!showEdit[$index]">{{row.contact}}</span>
                  </template>
                  </el-table-column>
                </el-table>
              </div>
              <div>
                <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="dialog_cancel(row,$index)" size = "medium" >取消</el-button>
                <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="dialog_check(row,$index)" size = "medium" >確認</el-button>
              </div>
            </el-dialog>
          </template>
        </el-table-column>
        </el-table>
      </div>
      </div>
      <div style="position:relative;top:50px">
        <el-button round = "true" style="position:fixed; width:150px; height:50px; left: 47%;" @click="submit()">送出</el-button>
      </div>
    </el-tab-pane>

    <el-tab-pane label="使用者申請"  name="使用者申請">
      <span slot="label" style="display:flex">
        使用者申請
        <div class="num-badge">{{new_user_num}}</div>
      </span>
      <el-table :data="new_user_tableData">
        <el-table-column prop="user" label="使用者" align="center"></el-table-column>
        <el-table-column prop="password" label="密碼" align="center"></el-table-column>
        <el-table-column prop="email" label="信箱" align="center"></el-table-column>
        <el-table-column prop="region" label="地區" align="center"></el-table-column>
        <el-table-column prop="record" label="確認申請資訊" align="center">
          <template slot-scope = "{row,$index}" >
            <el-button type="primary" icon="el-icon-s-claim" size="small" circle @click="confirm(row)"></el-button>
            <el-dialog title="申請資訊" :visible.sync="new_user_dialog">
              <el-form :model="form">
                <el-form-item prop="user" label="使用者" class="user-apply-form">
                  <el-input v-model="form.user" style="width:32%; display: table; left: 60px;" placeholder="請輸入使用者名稱"></el-input>
                </el-form-item>
                <el-form-item prop="password" label="密碼" class="user-apply-form">
                  <el-input v-model="form.password" style="width:32%; display: table; left: 60px;" placeholder="請輸入密碼"></el-input>
                </el-form-item>
                <el-form-item prop="email" label="信箱" class="user-apply-form">
                  <el-input v-model="form.email" style="width:32%; display: table; left: 60px;" placeholder="請輸入信箱"></el-input>
                </el-form-item>
                <el-form-item prop="groups" label="群組(可多選)" class="user-apply-form">
                  <el-select v-model="form.groups" style="width:35%; display: table; left: 60px;" multiple placeholder="請輸入群組">
                    <el-option v-for="item in groups_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item prop="region" label="區域" class="user-apply-form">
                  <el-select v-model="form.myregion" style="width:35%; display: table; left: 60px;" placeholder="請輸入區域">
                      <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item prop="description" label="描述(選填)" class="user-apply-form">
                  <el-input v-model="form.description" style="width:32%; display: table; left: 60px;" placeholder="請輸入描述"></el-input>
                </el-form-item>
              </el-form>
              <div slot="footer" style="margin-right: 215px;">
                  <el-button type="warning" @click="deny" plain>否決</el-button>
                  <el-button type="danger" @click="new_user_dialog=false" plain>取消</el-button>
                  <el-button type="primary" @click="new_user_submit" plain>確定</el-button>
              </div>
            </el-dialog>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>

    <el-tab-pane label="審核紀錄" name="審核紀錄" >
      <div style="width:1280px; margin:0 auto; top: -33px; position: relative;">
      <div style="position:relative;top:50px"align = "center">
        <el-table
        :data="history_app_Data"
        height= 650px
        >
        <el-table-column type=""align="center" prop="id" label="申請編號" sortable></el-table-column>
        <el-table-column type="" align="center" prop="" label="清除紀錄" >
          <template slot-scope = "{row}" >
            <el-button type="danger" size="mini" @click.native="clear_data(row)" icon="el-icon-delete-solid" circle></el-button>
          </template>
        </el-table-column>
        <el-table-column type=""align="center" prop="status" label="審核狀態" >
        </el-table-column>
        <el-table-column type=""align="center" prop="applicant" label="申請人"></el-table-column>
        <el-table-column type=""align="center" prop="verify_time" label="審核日期"></el-table-column>
        <el-table-column type=""align="center" prop="" label="重新審核" >
          <template slot-scope = "{row,$index}" ><!--此時row是app_data-->
            <el-button type="text" @click="open_dialog_history(row,$index)">查看資料</el-button>
            
          </template>
        </el-table-column>
        </el-table>
      </div>
        <el-dialog width='95%' title="申請內容" :visible.sync="history_dialog">
            <div style="display:flex; font-size: 18px;">
              <div style="width:33%">
                <!-- 申請人 -->
                <div style="display:flex">
                  <div style="text-align: end; width:40%; margin-right: 25px; bottom: -3px; position: relative;"> 申請人 :</div>
                  <div style="text-align: start;">
                    <el-input class="input_no_border" type="textarea" :autosize="{ minRows: 1, maxRows: 1}" name="sender" v-model="history_content['user']" readonly 
                      style="width:150px;" />
                  </div>
                </div>
                <!-- 副本 -->
                <div style="display:flex">
                  <div style="text-align: end; width:40%; margin-right: 25px; bottom: -9px; position: relative;"> 副本 :</div>
                  <div style="text-align: start;  width:55%">
                    <template  v-for="(item, index) in history_cc">
                      <el-autocomplete v-model="history_cc[index]"  :fetch-suggestions="querySearch_cc" placeholder="請輸入副本" ></el-autocomplete>
                      <el-button v-show="index != 0" type="text" icon="el-icon-error"  @click="history_remove_cc(index)"></el-button>
                    </template>
                    <el-button type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="history_add_cc()"></el-button>
                  </div>
                </div>
                <!-- 附件下載 -->
                <div style="display:flex">
                  <div style="text-align: end; width:40%; margin-right: 25px; bottom: -9px; position: relative;"> 附件下載 :</div>
                  <div style="text-align: start;">
                    <el-button style="" type="text" @click="download_check(row,$index)">license-application.xlsx</el-button>
                  </div>
                </div>
                <!-- 申請內文 -->
                <div style="display:flex">
                  <div style="text-align: end; width:40%; margin-right: 25px; bottom: 2px; position: relative;"> 申請內文 :</div>
                  <div style="text-align: start;">
                    <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="history_content['text']" readonly 
                    :disabled="true" style="width:250px;" />
                  </div>
                </div>
              </div>

              <div style="width:33%">
                <!-- 審核者回覆 -->
                <div style="display:flex">
                  <div style="text-align: end; width:20%; margin-right: 25px; bottom: 2px; position: relative;"> 審核者回覆 :</div>
                  <div style="text-align: start;">
                    <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="history_content['reply']" 
                      style="width:400px;" />
                  </div>
                </div>
              </div>
              
              <div style="width:33%; top: -22px; position: relative;">
                <!-- 統計紀錄 -->
                <div> 申請紀錄統計(總共{{history_tableData.length}}筆)</div>
                <div style="height: 180px; width: auto; overflow: auto; border: 1px solid #dcdfe6; border-radius: 4px; margin: 0px auto;text-align: right;">
                  <p v-html="his_data_statistics_text" style="font-size: 20px; margin: 0px 50px;"></p>
                </div>
              </div>
            </div>

            <div style="text-align: start">
              <el-button style="background-color:#67C23A; border-color:#67C23A; padding: 8px 11px; color: #ffffff;" 
                icon="el-icon-check" @click="history_all_approve"></el-button>
              <el-button style="background-color:#F56C6C; border-color:#F56C6C; padding: 8px 11px; color: #ffffff;" 
                icon="el-icon-close" @click="history_all_reject"></el-button>
              <el-button style="background-color:#909399; border-color:#909399; padding: 8px 11px; color: #ffffff;" 
                icon="el-icon-refresh-right" @click="history_all_clear"></el-button>
            </div>

            <el-table :data="history_tableData" height="400px">
              <el-table-column align="center" width="120px" prop="customer" label="審核">
                <template slot-scope = "{row}" ><!--此時row是app_data['data']-->
                  <el-radio-group  :fill="row['verify'] == '√'? '#67C23A':'#F56C6C'" v-model="row['verify']" size="mini">
                    <el-radio-button label="√"></el-radio-button>
                    <el-radio-button label="×" ></el-radio-button>
                  </el-radio-group>
                </template>
              </el-table-column>
              <el-table-column width="100px" prop="operator" label="操作"></el-table-column>
              <el-table-column align="center" width="140px" prop="customer" label="客戶"></el-table-column>
              <el-table-column align="center" width="165px" prop="issued" label="更新日期"></el-table-column>
              <el-table-column align="center" width="120px" prop="sn" label="KeyID"></el-table-column>
              <el-table-column align="center" width="210px" prop="product" label="產品"></el-table-column>
              <el-table-column align="center" width="210px" prop="module" label="模組"></el-table-column>
              <el-table-column align="center" width="100px" prop="version" label="版本"></el-table-column>
              <el-table-column align="center" width="110px" prop="type" label="類型"></el-table-column>
              <el-table-column align="center" width="80px" prop="count" label="數量"></el-table-column>
              <el-table-column align="center" width="165px" prop="expiration" label="到期日期"></el-table-column>
              <el-table-column align="center" width="110px" prop="region" label="地區"></el-table-column>
              <el-table-column align="center" width="140px" prop="comment" label="備註"></el-table-column>
              <el-table-column align="center" prop="contact" label="聯絡人" :width="his_max_contact_length * 10 + 30">
            </el-table>

            <div>
              <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="history_dialog=false" size = "medium" >取消</el-button>
              <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="history_dialog_check" size = "medium" >重新送出</el-button>
            </div>
          </el-dialog>
      </div>
    </el-tab-pane>

    </el-tabs>

      
  </div>
</template>

<script>
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'check',
  data: function() {
        return { 
            isLoading:false,
            origin_tableData:[],//修改前的tableData
            tableData:[],
            all_Data:[],
            app_Data:[],//all_Data['appliection_data']
            app_Data_num:0,
            dialogTableVisible:[],//dialog開關
            showEdit:[],//false:不可編輯 true:可編輯
            nofilter_info_Data:[],
            compare_Data:[],
            compare_edit_Data:[],
            radio:[],
            content:{},
            user:[],
            customer_opt:[],
            region_opt:[],
            func_uid_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            cc:[''],
            cc_opt:[],
            check:[],
            region_data:[],
            new_user_tableData:[],
            new_user_num:0,
            group_data:[],
            groups_opt:[],
            form:{
              id:0,//edit才用的到
              user:'',
              password:'',
              email:'',
              groups:[],
              region:'',
              myregion:'',
              record:'',
              description:'',
              admin_mail:'',
              inspector:'',
            },
            new_user_dialog:false,
            editableTabsValue:'',
            history_app_Data:[],
            history_tableData:[],
            history_content:{},
            history_cc:[],
            history_origin_tableData:[],
            history_dialog:false,
            history_row:[],
            data_statistics_text:'',
            his_data_statistics_text:'',
            max_contact_length:0,
            his_max_contact_length:0,
            multi_expand_map: {},
            multi_delete_map: {},
        }
  },
  created(){
    this.isLoading = true
    this.axios.get('/check/' + this.$route.params.verifyname,{
      headers: {'Content-Encoding': 'gzip'}
      }).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))
      this.all_data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
      this.app_Data = JSON.parse(JSON.stringify(response.data['application_data']));
      this.history_app_Data = JSON.parse(JSON.stringify(response.data['history_application_data']));
      for(let app of this.app_Data)
        this.check.push(false)
      var module_map = new Map()
      for (let func_uid of this.all_data['module_data']){
        this.func_uid_opt.push({value:func_uid['caption'],label:func_uid['caption']});
        module_map.set(func_uid['mod_uid'],func_uid['caption'])
      }
      this.region_data = JSON.parse(JSON.stringify(this.all_data['region_data']));
      for (let region of this.all_data['region_data'])
        this.region_opt.push({value:region['name'],label:region['name']});

      var cc_set = new Set();
      for(let user of this.all_data['sn_data'])
        for(let user_email of user['user'].split(','))
            cc_set.add(user_email)
      for(let user of cc_set)
        this.cc_opt.push({value:user,label:user})

      for (let customer of this.all_data['customer_data'])
        this.customer_opt.push({value:customer['name']+'|'+customer['site'],label:customer['name']+'|'+customer['site']})
      var i = 1
      for(let app of this.app_Data){
        app = Object.assign(app,{'fake_id':i,'verify_status':1,'check':false})//0:尚未審核 1:已審核
        i++
      }
      for(let app of this.app_Data){
        let test = 0
        app['data'] = JSON.parse(app['data'])
        app['validator'] = JSON.parse(app['validator'])
        for(let data of app['data']){
          if(data.verify == undefined && data.reason == undefined){
            data = Object.assign(data,{'verify':'','reason':null})
            test = 1
          }
          if(data.verify == '')
            test = 1
        }
        if(test == 1)
          app['verify_status'] = 0
        app['data'] = JSON.stringify(app['data'])
      }
      for(var i = 0; i < this.app_Data.length; i++){
        this.dialogTableVisible.push(false);
      }
      var order_form = JSON.parse(JSON.stringify(this.all_data['info_data']));//複製一個完全獨立的info 深複製
      var i = 0
      var sn_dict = response.data['sn_dict']
      var product_map = new Map()
      var option_map = new Map()
      for(let product of response.data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of response.data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})

      let customer_map = {}
      for (let cus of this.all_data['customer_data'])
        customer_map[cus['customer_id']] = {'name': cus['name'], 'site': cus['site']}
      
      let region_map = {}
      for (let reg of this.all_data['region_data'])
        region_map[reg['region_id']] = {'name': reg['name'], 'description': reg['description']}
      
      var i = 0
      for (let info of this.all_data['info_data']){
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
      this.nofilter_info_Data = JSON.parse(JSON.stringify(order_form));//複製一個完全獨立的info(未過濾) 深複製
      
      for (let info of this.nofilter_info_Data){//當聯絡人超過兩人時的nofilter email簡化
      if(info['contact'].split(',').length > 1){
        info['contact'] = info['contact'].split(',')
        for(let i = 0; i < info['contact'].length; i++){
          for(let user of this.all_data['user_data'])
            if(info['contact'][i] == user['email']){
              info['contact'][i] = user['user']
            }
        }
        info['contact'] = info['contact'].join()
      }
      }

      this.app_Data_num = this.app_Data.length
      
      this.group_data = JSON.parse(JSON.stringify(this.all_data['group_data']));
      for (let group of this.group_data)
        this.groups_opt.push({'value':group.caption,'label':group.caption});

      for(let user of this.all_data['user_data'])
          for(let group of user['groups'])
              if(group == '1')
                  this.form.admin_mail += `${user['email']};`;
      
      for(let userdata of this.all_data['user_data']){
        if (userdata['description'] == 'to be confirmed'){
          let record = JSON.parse(userdata['record']);
          this.new_user_tableData.push({id:userdata['user_id'], user:record['user'], password:record['password'], email:record['email'], region:record['region']});
          this.new_user_num += 1
        }
      }

      // 處理歷史紀錄
      for(let his_app of this.history_app_Data){
        his_app['verify_time'] = his_app['verify_time'].replaceAll('"','')
      }

      // 排序審核時間
      this.history_app_Data.sort(function(a,b){
        // 將沒有審核時間的資料排在最下方
        if(a.verify_time == '')
          return new Date(b.verify_time) - new Date('0001-01-01')
        else if(b.verify_time == '')
          return new Date('0001-01-01') - new Date(a.verify_time)
        else
          return new Date(b.verify_time) - new Date(a.verify_time)
      });
      
      if(this.$route.query.checked_mode == "new_user")
        this.editableTabsValue = "使用者申請"
      else
        this.editableTabsValue = "待審核資料"

      this.isLoading = false
    })
  },
  methods:{
    click_checkbox(check,index){
      this.$set(this.app_Data[index],'check',check)
    },
    cc_location(index,mode){
      if(mode == 'input'){
        var top = (80 + index * 45)
        return ("width:200px;position:absolute;right:200px;top:" + String(top)+"px")
      }
      else if(mode == 'button'){
        var top = (63 + index * 45)
        return ("color:#F56C6C;font-size:15px;position:absolute;right:192px;top:"+String(top)+'px')
      }
    },
    add_cc(){//上方聯絡人修改框增加
        this.cc.push('');
    },
    history_add_cc(){
      this.history_cc.push('');
    },
    remove_cc(index){//上方聯絡人修改框減少
      this.cc.splice(index,1);
    },
    history_remove_cc(index){//上方聯絡人修改框減少
      this.history_cc.splice(index,1);
    },
    tranfer_xlsx(data) {//web下載 xlsx
      if (!data) {
        return
      }
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'verify-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
    },
    download_check(row,index){
      this.axios({
          method: 'post', // 请求方式
          url: '/download_check',
          data: {
            data:row
          }, // 请求参数
          responseType: 'blob' // 服务器返回的数据类型
        }).then((response)=>{
          this.tranfer_xlsx(response.data)
        })
    },
    clear_data(row){
      this.$confirm('是否要清除申請?(不可復原)', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
      }).then(() => {
        this.axios.post("/del_application",{
            rowid: row['id']
        }).then(()=>{
          this.$message({message: '刪除成功', type: 'success'});
          location.reload();
        })

      }).catch(()=>{
        this.$message({message: '取消刪除', type: 'info'});
      })

    },
    submit(){
      var pass_app_Data = []//只儲存已通過的資料
      for(let app of this.app_Data)
        if(app['check'] == true)
          pass_app_Data.push(app)
      
      if(pass_app_Data.length == 0){
        this.$message({message: '尚未勾選已審核資料', type: 'error'});
        return;
      }
      this.$confirm('是否確定送出審核?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.isLoading = true;
          this.axios.post("/check_verify",{
                verify_Data:pass_app_Data,
                user:this.user,
                status:'',
            }).then((response)=>{
                this.isLoading = false;
                this.$message({type: 'success', message: '審核成功!'});

                this.axios.get('/check/' + this.user[0],{
                  headers: {'Content-Encoding': 'gzip'}
                }).then(response => {
                    var app_Data = JSON.parse(JSON.stringify(response.data['application_data']));
                    if(app_Data.length)
                      location.reload();
                    else
                      this.$router.push({name: 'Show_All'});
                })
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消送出審核'
          });          
        });
    },
    verify_change(row,index){//二級參數無法直接渲染視圖 顧透過change來給row.verify值
      this.$set(this.tableData[index],'verify',this.radio[index]);
      if(this.radio[index] == '×'){
        var comment = prompt("請輸入審核原因：\n");
        row.reason = comment;
      }
    },
    dialog_check:function(row,index){//把dialog修改的資料儲存在row['data']
      for(var i = 0; i < this.showEdit.length; i++)
        if(this.showEdit[i] == true){
          this.$message({message: '請先將確認修改資料√', type: 'error'});
          return;
        }
        this.app_Data[index]['verify_status'] = 1
        this.app_Data[index]['check'] = true
        this.$set(this.check,index,true)
        for(let data of this.tableData)
          if(data.verify == ''){
            this.app_Data[index]['verify_status'] = 0
            this.app_Data[index]['check'] = false
            this.$set(this.check,index,false)
          }
      row['data'] = JSON.stringify(this.tableData);
      this.content['cc'] = this.cc.join();
      row['content'] = JSON.stringify(this.content);
      this.$set(this.dialogTableVisible,index,false);
          this.axios.post("/dialog_check",{
                check_data:this.app_Data[index],
                user:this.user
            }).then((response)=>{
              this.$confirm('', '提示', {
                  confirmButtonText: '寄出審核結果',
                  cancelButtonText: '返回審核主頁',
                  showClose: false,
                  type: 'warning',
                  center: true
              }).then(() => {
                  this.isLoading = true;
                  this.axios.post("/check_verify",{
                        verify_Data:[response.data],
                        user:this.user,
                        status:'',
                    }).then((response)=>{
                        this.isLoading = false;
                        this.$message({type: 'success', message: '審核成功!'});
                        this.axios.get('/check/' + this.user[0],{
                          headers: {'Content-Encoding': 'gzip'}
                        }).then(response => {
                            var app_Data = JSON.parse(JSON.stringify(response.data['application_data']));
                            if(app_Data.length)
                              location.reload();
                            else
                              this.$router.push({name: 'Show_All'});
                        })
                    });
              }).catch(() => {
                  location.reload();
              });

            });
    },
    history_dialog_check:function(){
      for(let h_tableData of  this.history_tableData){
        if(h_tableData['verify'] != "×" && h_tableData['verify'] != "√"){
          this.$confirm('請先確認所有審核按鈕', '提示', {
            showClose: false,
            type: 'warning',
            center: true
          })
          return
        }
      }
      this.history_row['data'] = JSON.stringify(this.history_tableData);
      this.history_content['cc'] = this.history_cc.join()
      this.history_row['content'] = JSON.stringify(this.history_content);
      this.history_row['validator'] = JSON.parse(this.history_row['validator'])
      this.axios.post("/dialog_check",{
          check_data:this.history_row,
          user:this.user
      }).then((response)=>{
        this.isLoading = true;
        this.axios.post("/check_verify",{
            verify_Data:[response.data],
            user:this.user,
            status:'resend',
        }).then((response)=>{
            this.isLoading = false;
            this.$message({type: 'success', message: '審核成功!'});
            location.reload();
        });
      }).catch(() => {

      });

    },
    open_dialog:function(row,index){
      var temp_tableData = JSON.parse(row['data']);//temp_tableData就是當前你點查看資料時的row的data(已轉成array)
      this.content = JSON.parse(row['content'])
      this.cc = this.content['cc'].split(',')
      this.showEdit.length = 0;//重置開關
      this.radio.length = 0;
      this.max_contact_length = 0;
      

      // 資料筆數統計
      let data_statistics = {}
      this.data_statistics_text = ''
      for(let data of temp_tableData){
          if (data_statistics[data['customer']] == undefined )
              data_statistics[data['customer']] = {'id_list':[], 'data_num':0, 'add_num':0, 'mod_num':0, 'del_num':0}
          data_statistics[data['customer']]['data_num'] += 1
          if(!data_statistics[data['customer']]['id_list'].includes(data['sn']))
              data_statistics[data['customer']]['id_list'].push(data['sn'])
          if (data['operator'] == '新增')
              data_statistics[data['customer']]['add_num'] += 1
          if (data['operator'] == '修改' || data['operator'] == '多筆展延')
              data_statistics[data['customer']]['mod_num'] += 1
          if (data['operator'] == '刪除' || data['operator'] == '多筆刪除')
              data_statistics[data['customer']]['del_num'] += 1
      }
      for (let customer in data_statistics){
          let id_num = data_statistics[customer]['id_list'].length
          let data_num = data_statistics[customer]['data_num']
          let add_num = data_statistics[customer]['add_num']
          let mod_num = data_statistics[customer]['mod_num']
          let del_num = data_statistics[customer]['del_num']
          this.data_statistics_text += `${customer} 申請 ${id_num}筆id, 共 ${data_num}筆資料(新增: ${add_num}, 修改: ${mod_num}, 刪除 ${del_num}) <br>`
      }

      var multiple_expand_data = []
      var multiple_delete_data = []
      for(let temp_table of temp_tableData){
        if(temp_table.operation_type == 'multiple_expand')
          multiple_expand_data.push(temp_table)
        else if(temp_table.operation_type == 'multiple_delete')
          multiple_delete_data.push(temp_table)
        else
          this.tableData.push(temp_table)
      }

      var multi_expand_map = {}
      for(let multi_data of multiple_expand_data){
        if(multi_data['sn'] in multi_expand_map)
          multi_expand_map[multi_data['sn']].push(multi_data)
        else
          multi_expand_map[multi_data['sn']] = [multi_data]
      }

      var multi_delete_map = {}
      for(let multi_data of multiple_delete_data){
        if(multi_data['sn'] in multi_delete_map)
          multi_delete_map[multi_data['sn']].push(multi_data)
        else
          multi_delete_map[multi_data['sn']] = [multi_data]
      }

      for(let sn in multi_expand_map){
        this.tableData.push({'operator': '多筆展延', 'customer': multi_expand_map[sn][0].customer, 'sn': multi_expand_map[sn][0].sn, 
          'count': multi_expand_map[sn].length, 'user': multi_expand_map[sn][0].user, 'contact': multi_expand_map[sn][0].contact, 'verify':'', 'reason':''})
      }

      for(let sn in multi_delete_map){
        this.tableData.push({'operator': '多筆刪除', 'customer': multi_delete_map[sn][0].customer, 'sn': multi_delete_map[sn][0].sn, 
          'count': multi_delete_map[sn].length, 'user': multi_delete_map[sn][0].user, 'contact': multi_delete_map[sn][0].contact, 'verify':'', 'reason':''})
      }
      this.multi_expand_map = multi_expand_map
      this.multi_delete_map = multi_delete_map


      this.origin_tableData = JSON.parse(JSON.stringify(this.tableData));
      for(let i = 0; i < this.tableData.length; i++){//showEdit&radio的數量=temp_tableData[data]數量 
        this.showEdit.push(false);//showEdit:編輯修改的開關
        this.radio.push('');//勾選勾叉的開關
      }
      
      var i = 0;
      for(let data of this.tableData){//verify用來儲存審核是否通過
          this.radio[i] = data.verify;
        i++
        if(data['contact'].length > this.max_contact_length)
          this.max_contact_length = data['contact'].length
      }

      this.dialogTableVisible[index]=true;
    },
    open_dialog_history:function(row,index){
      this.his_max_contact_length = 0;
      this.history_tableData = JSON.parse(row['data']);
      this.history_content = JSON.parse(row['content'])
      this.history_cc = this.history_content['cc'].split(',')
      this.history_origin_tableData = JSON.parse(JSON.stringify(this.history_tableData));
      this.history_row = row
      // 資料筆數統計
      let his_data_statistics = {}
      this.his_data_statistics_text = ''
      for(let data of this.history_tableData){
        if (his_data_statistics[data['customer']] == undefined )
            his_data_statistics[data['customer']] = {'id_list':[], 'data_num':0, 'add_num':0, 'mod_num':0, 'del_num':0}
        his_data_statistics[data['customer']]['data_num'] += 1
        if(!his_data_statistics[data['customer']]['id_list'].includes(data['sn']))
            his_data_statistics[data['customer']]['id_list'].push(data['sn'])
        if (data['operator'] == '新增')
            his_data_statistics[data['customer']]['add_num'] += 1
        if (data['operator'] == '修改')
            his_data_statistics[data['customer']]['mod_num'] += 1
        if (data['operator'] == '刪除')
            his_data_statistics[data['customer']]['del_num'] += 1

        if(data['contact'].length > this.his_max_contact_length)
          this.his_max_contact_length = data['contact'].length
      }
      for (let customer in his_data_statistics){
        let id_num = his_data_statistics[customer]['id_list'].length
        let data_num = his_data_statistics[customer]['data_num']
        let add_num = his_data_statistics[customer]['add_num']
        let mod_num = his_data_statistics[customer]['mod_num']
        let del_num = his_data_statistics[customer]['del_num']
        this.his_data_statistics_text += `${customer} 申請 ${id_num}筆id, 共 ${data_num}筆資料(新增: ${add_num}, 修改: ${mod_num}, 刪除 ${del_num}) <br>`
      }

      this.history_dialog = true;
    },
    dialog_cancel:function(row,index){//關閉dialog
      this.$set(this.dialogTableVisible,index,false)
      this.cc=[''];
    },
    handleEdit(index, row) {//修改tableData資料
      this.$set(this.showEdit,index,true)
    },
    /*deleterow(row){//刪除tableData單列資料
      for(var i = 0; i < this.tableData.length; i++)
        if(JSON.stringify(row) == JSON.stringify(this.tableData[i])){
          this.tableData.splice(i,1);
          this.origin_tableData.splice(i,1);
        }
    },*/
    handleCheck(index,row){
      var test = 0;
      for(let info of this.nofilter_info_Data)//比對是否有衝突
        if(this.tableData[index]['sn'] != this.origin_tableData[index]['sn'] || 
            this.tableData[index]['type'] != this.origin_tableData[index]['type'] || 
            this.tableData[index]['func_uid'] != this.origin_tableData[index]['func_uid'])
          if(this.tableData[index]['sn'] == info['sn'] && this.tableData[index]['type'] == info['type'] && this.tableData[index]['func_uid'] == info['func_uid']){
            var msg = '修改資料'+ '\nKeyID:' + this.tableData[index]['sn'] +'\n類型:' + this.tableData[index]['type'] +'\n產品名稱:' + this.tableData[index]['func_uid'] + '\n已有重複資料';
            //this.$message({message: msg, type: 'error'});
            this.$notify.error({
              title: '修改通知',
              message: msg,
              duration: 0
            });
            this.tableData[index] = JSON.parse(JSON.stringify(this.origin_tableData[index]));
            this.$set(this.showEdit,index,false)
            test = 1;
          }
      if(test == 0){
      this.origin_tableData[index] = this.tableData[index];
      this.$set(this.showEdit,index,false)
      }
    },
    handelRestore(index, row){
      this.tableData[index] = JSON.parse(JSON.stringify(this.origin_tableData[index]));
      this.$set(this.showEdit,index,false)
    },
    compare_row(row,index){//此時row是app_data['data']
      //--------------製造修改的對照表--------------//
      for(let origin_info of this.nofilter_info_Data)
        if(JSON.stringify(origin_info['info_id']) == JSON.stringify(row['info_id'])){
          this.$set(this.compare_Data,0,origin_info)
          this.$set(this.compare_edit_Data,0,row)
          }
    },
    cell_color({row, column, rowIndex, columnIndex}){//若原來資料與修改後資料不依 則顯示紅色
      if(column.label == '客戶')
        if(row.customer != this.compare_edit_Data[0].customer)
          return 'warning-row';
      if(column.label == '更新日期')
        if(row.issued != this.compare_edit_Data[0].issued)
          return 'warning-row';
      if(column.label == 'KeyID')
        if(row.sn != this.compare_edit_Data[0].sn)
          return 'warning-row';
      if(column.label == '產品名稱')
        if(row.func_uid != this.compare_edit_Data[0].func_uid)
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
      if(column.label == '到期日期')
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
    },
    querySearch_customer(queryString, cb) {
      var results = queryString ? this.customer_opt.filter(this.createFilter(queryString)) : this.customer_opt;
      cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_func_uid(queryString, cb) {
        var results = queryString ? this.func_uid_opt.filter(this.createFilter(queryString)) : this.func_uid_opt;
        cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_type(queryString, cb) {
      var results = queryString ? this.type_opt.filter(this.createFilter(queryString)) : this.type_opt;
      cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_region(queryString, cb) {
      var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
      cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_cc(queryString, cb){
        var results = queryString ? this.cc_opt.filter(this.createFilter(queryString)) : this.cc_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
    createFilter(queryString) {//搜尋建議選項
      return (any) => {
        return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    label_for_validator(h, {column}){//validator的Label
      return(<span>審核條件<br></br>(<span style="color:black;background-color: #ffb7b7">紅色</span>為缺少條件，
      <span style="color:black;background-color:#67C23A">綠色</span>為已滿足條件)</span>)
    },
    disabled_checkbox(row){
      if(row.verify_status==0)
        return true
      if(row.validator['verify_check']['verify_group'].indexOf(true) == -1)
        return true
      
      if(row.validator['verify_check']['verify_num'] < row.validator['verify_num'])
        return true

      return false
    },
    all_approve(){
      this.radio.fill('√');
      this.tableData.forEach(i => i['verify'] = '√')
      //單純改值無法即時觸發變化，需手動調整
      for(let i in this.tableData){
        this.$refs[`radio-${i}`].value = '√'
        this.$refs[`radio-${i}`].fill = '#67C23A'
      }
      
    },
    history_all_approve(){
      this.history_tableData.forEach(i => i['verify'] = '√')
    },
    all_reject(){
      var comment = prompt("請輸入審核原因：\n");
      this.radio.fill('×');
      this.tableData.forEach(i => {i['verify'] = '×'; i['reason'] = comment})
      for(let i in this.tableData){
        this.$refs[`radio-${i}`].value = '×'
        this.$refs[`radio-${i}`].fill = '#F56C6C'
      }
    },
    history_all_reject(){
      var comment = prompt("請輸入審核原因：\n");
      this.history_tableData.forEach(i => {i['verify'] = '×'; i['reason'] = comment})
    },
    all_clear(){
      this.radio.fill('');
      this.tableData.forEach(i => {i['verify'] = ''; i['reason'] = ''})
      for(let i in this.tableData){
        this.$refs[`radio-${i}`].value = ''
        this.$refs[`radio-${i}`].fill = '#fff'
      }
    },
    history_all_clear(){
      this.history_tableData.forEach(i => {i['verify'] = ''; i['reason'] = ''})
    },
    confirm(row_data){
      this.new_user_dialog = true;
      this.form.id = row_data['id'];
      this.form.user = row_data['user'];
      this.form.password = row_data['password'];
      this.form.email = row_data['email'];
      this.form.region = row_data['region'];
      this.form.myregion = row_data['region'];
    },
    new_user_submit(){
      this.form.inspector = this.user;
      if(this.form.user == '' || this.form.password == ''|| this.form.email == ''){
            this.$message({message: '請填入群組名稱及群組類別及信箱', type: 'error'});
            return;
        }
      if(this.form.email.split('@')[1] == undefined){
          this.$message({message:'請填入正確email格式', type:'error'});
          return;
      }
      
      this.form.groups = JSON.stringify(this.form.groups).replace('["','').replace('"]','').replace(/","/g,',');
      this.form.record = "";

      //將群組名稱轉成數字代號
      if(this.form.groups != '[]'){
          this.form.groups = this.form.groups.split(',');
          for(var i = 0; i < this.form.groups.length; i++){
              for(let group of this.group_data)
                  if(this.form.groups[i] == group['caption'])
                      this.form.groups[i] = group['group_id']
          }
          this.form.groups = JSON.stringify(this.form.groups);
      }
      else
        this.form.groups = '';
      
      //將區域名稱轉成數字代號
      if(this.form.myregion != ''){
        for(let region of this.region_data)
            if(this.form.myregion == region['name'])
                this.form.region = region['region_id']
          this.form.region = '[' + JSON.stringify(this.form.region) + ']';
      }
      else
        this.form.region = '';

      
      this.axios.post("/operator_user",{
          params:{
              form: JSON.stringify(this.form),
              operator:'edit'
          }
          }).then((response)=>{
              this.axios.post("/send_signup_success_email",{
                  origin_data: this.form
              }).then((response)=>{
                  if(response.data=='郵件傳送成功!'){
                      this.$message({type: 'success', message: '已傳送帳號確認通知!'});
                      location.reload();
                  }
                  else{
                    this.$message({type: 'success', message: '帳號申請失敗!'});
                  }
              });
          });
    },
    deny(){
      this.$confirm('否決此帳號申請?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.get("/operator_user",{
          params:{
            user_name: JSON.stringify(this.form.user),
            operator:'delete'
          }
        }).then((response)=>{
          location.reload();
        });
      }).catch(() => {
        this.$message({type: 'info', message: '已取消'});          
      });
    },
  }
}
</script>

