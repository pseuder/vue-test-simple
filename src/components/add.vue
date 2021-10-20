<style scoped>
.none_delete_tag .el-tag.el-tag--info .el-tag__close{
  display: none;
}
.el-scrollbar__wrap {
    overflow-x: hidden;
}
.fade-enter,
.fade-leave-active{
    opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.el-select ::-webkit-scrollbar{
    display: none;
}
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
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
#menu {
    position: fixed;
    top: 30%;
    right: 25px;
    z-index:111;
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
.add_dialog /deep/ .el-dialog{
    background-color:#C4C4C4;
}
.func_uid-dialog /deep/ .el-dialog{
    background-color:#EBD1A0;
    width:1500px;
}
.submit_button{
    position:relative;
    left: 37%;
    width:150px;
}
.el-col{
    font-size: 18px;
    font-weight: bold;
    bottom: -10px;
    position: relative;
}
.el-col /deep/ .el-col-2{
    bottom: -10px;
    position: relative;
}
.product_tree{
    font-size: 20px;
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

<!-- popover的樣式需要放在全局style才有用 -->
<style>
.KeyID_popover {
    background:#EBD1A0 !important;
    border: none !important;
}
.product-conflict{
    width: 570px;
    height: 50%;
    overflow: auto;
}
</style>
<template>
    <div>
        <transition name="fade"><!--loading動畫-->
            <loading v-if="isLoading"></loading>
        </transition>

        <div>
            <!--product tree 產品選擇-->
            <!--
            <el-drawer
            title="產品選擇"
            :visible.sync="drawer"
            :with-header="false"
            size="20%">
            -->
            <el-dialog :visible.sync="drawer" class="func_uid-dialog">
                <!-- <el-button icon="el-icon-plus" @click="dialogVisible=true" type="warning" plain size="mini" v-show="this.lock[this.row_index]">產品群組</el-button> -->
                
                <span style="font-size: 20px; font-weight: 700; top: -20px; position: relative;">添加產品</span>
                <div style="display:flex" class="product_tree">
                    <div style="width:45%; margin: 0px auto;">
                        <span style="font-size: 20px; font-weight: 700;">產品/選項</span>
                        <el-tree
                            style="border-radius:4px; overflow-y:auto; height:400px;"
                            :data="tree_data"
                            :props="defaultProps"
                            node-key="id"
                            ref="tree"
                            @check="handleCheckChange"
                            :render-content="tag_for_tree"
                            show-checkbox>
                        </el-tree>
                    </div>

                
                    <div style="width:45%; margin: 0px auto;">
                        <span style="font-size: 18px; font-weight: 700;">已選擇({{tree_checked.length}})</span>
                        <el-tree
                            style="border-radius:4px; overflow-y:auto; height:400px;"
                            :data="tree_checked"
                            :props="defaultProps"
                            node-key="id"
                            :render-content="tag_for_tree"
                            >
                        </el-tree>
                    </div>

                    <el-dialog
                        title="產品群組(新增)"
                        :visible.sync="dialogVisible"
                        width="60%"
                        :append-to-body="true">
                        <el-scrollbar style="height: 350px">
                        <el-tree
                            style="position:relative;left:440px;width:400px;height:350px;"
                            :data="productgroup_tree"
                            :props="defaultProps"
                            accordion
                            node-key="id"
                            ref="product_group_tree"
                            @check="choose_product_group"
                            show-checkbox>
                        <span class="custom-tree-node" slot-scope="{ node, data }">
                            <span>{{ node.label }}</span>
                            <span>
                            <el-button
                                v-show="deter_product_group(node)==false && append_tree_lock==false && data['add'] != true"
                                type="text"
                                size="mini"
                                @click="() => append(node,data)">
                                加入此標籤
                            </el-button>
                            <el-button
                                v-show="data['add'] == true"
                                type="text"
                                size="mini"
                                @click="() => remove(node, data)">
                                重選標籤
                            </el-button>
                            <el-tag v-show="deter_product_group(node)=='group'" style="font-size:14px;height:22px;" type="success">G</el-tag>
                            </span>
                        </span>
                        </el-tree>
                        </el-scrollbar>
                        <div style="position:absolute;top:80px;">
                        <div style="position:relative;">名稱:<el-input v-model="product_dialog.caption" style="width:150px" placeholder="請輸入群組名稱"></el-input></div>
                        <div style="position:relative;">產品:<el-select ref="dialog_pro" class="none_delete_tag" v-model="product_dialog.product_list" filterable remote multiple style="width:300px;" @focus="make_blur('1')" placeholder="請輸入產品群組"></el-select></div><!--@remove-tag="interact_tree"-->
                        <div style="position:relative;">描述:<el-input v-model="product_dialog.description" style="width:200px" placeholder="請輸入描述"></el-input></div>
                        <div style="position:relative;">備註:<el-input v-model="product_dialog.remarks" style="width:200px" placeholder="請輸入備註"></el-input></div>
                        <span>
                            <el-button style="position:relative;left:30px;" type="danger" @click="cancel_product_group" plain>取消</el-button>
                            <el-button style="position:relative;left:40px;" type="primary" @click="store_product_group" plain>確定</el-button>
                        </span>

                        
                    </el-dialog>
                </div>
                <el-button @click="cancel_drawer" type="warning" size="medium" >取消</el-button>
                <el-button @click="check_drawer" type="warning" size="medium" >添加</el-button>
            </el-dialog>
        </div>

        <div id = "menu">
            <div><el-button v-if="checked_Data.length > 0" class="OperatorButton"  type="info" icon="el-icon-plus" disabled></el-button></div>
            <div><el-button v-if="checked_Data.length == 0" class="OperatorButton"  type="warning" icon="el-icon-plus" @click="GoAdd" ></el-button></div>
            <div><el-button class="OperatorButton"  type="warning" icon="el-icon-delete" @click="GoDelete" ></el-button></div>
        </div>
        <el-dialog :visible.sync="add_dialog" width="80%" class="add_dialog"  :before-close="handleClose" :show-close="false">
            <el-form :model="sub_row" label-width="80px" label-position="left">
                <el-form-item>
                    <div style="text-align: start;">
                        <el-col :span="2">客戶名</el-col>
                        <el-col :span="5">
                            <el-autocomplete style="width:95%; position: relative; top: -10px;"  size='small' v-model="input.name" 
                            :fetch-suggestions="querySearch_name" placeholder="請輸入客戶"></el-autocomplete>
                        </el-col>

                        <el-col :span="3" style="text-align: center;">客戶廠區(選填)</el-col>
                        <el-col :span="5">
                            <el-autocomplete style="width:95%; position: relative; top: -10px;" size='small' v-model="input.factory" 
                            :fetch-suggestions="querySearch_site" placeholder="請輸入廠區"></el-autocomplete>
                        </el-col>

                        <el-col :span="2" style="text-align: center;">業務地區</el-col>
                        <el-col :span="5">
                            <el-select style="width:95%; position: relative; top: -10px;"  size='small' v-model="sub_row.region" placeholder="業務地區">
                                <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-col>
                    </div>
                </el-form-item>
                <el-form-item>
                    <div style="text-align: start;">
                        <el-col :span="2">KeyID</el-col>
                        <div style="display:flex">
                            <el-select v-model="sub_row.sn_multi" filterable clearable multiple :filter-method="sn_fliterer"
                                @keyup.enter.native="subrow_sn_enter" style="width: 645px; bottom: 7px;" placeholder="請選擇KeyID或手動輸入後按Enter">
                                <el-option v-for="opt in sn_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                            </el-select>
                        
                            <div>
                                <el-popover placement="bottom" width="343" trigger="click" popper-class="KeyID_popover" ref="KeyID_pop">
                                    <div style="text-align: center; font-size: 18px;">添加多筆KeyID</div>
                                    <div style="display:flex">
                                    <div style="margin:10px">區間</div>
                                    <el-input style="width:140px" v-model.number="multi_KeyID_form.range_begin"></el-input>
                                    <div style="margin:10px">~</div>
                                    <el-input style="width:140px" v-model.number="multi_KeyID_form.range_end"></el-input>
                                    </div>
                                    <div style="dispaly:flex; text-align: end;">
                                        <el-button type="warning"  @click="$refs['KeyID_pop'].doClose()">取消</el-button>
                                        <el-button type="warning"  @click="add_multi_KeyID">添加</el-button>
                                    </div>
                                    <el-select v-model="sub_row.sn_multi" filterable clearable multiple :filter-method="sn_fliterer"
                                        @keyup.enter.native="subrow_sn_enter" style="width: 380px;" placeholder="請選擇KeyID或手動輸入後按Enter">
                                        <el-option v-for="opt in sn_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                                    </el-select>
                                    <div style="margin:10px"></div>
                                    <el-button  type="warning" slot="reference" style="left: -43px; position: relative;">添加多筆</el-button>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </el-form-item>
                <el-form-item>
                    <div style="text-align: start;">
                        <el-col :span="2">產品名稱</el-col>
                        <div style="display:flex">
                            <el-input  v-model="sub_row.func_uid" style="width: 580px; position: relative; top: -10px;" placeholder="請點選右邊「添加多筆」" readonly>
                            </el-input>
                            <el-button type="warning" @click="choose_func_uid()" style="left: 23px; position: relative; height: 38px;">添加多筆</el-button>
                        </div>
                    </div>
                </el-form-item>
                
                <el-form-item>
                    <div style="text-align: start;">
                        <el-col :span="2">類型</el-col>
                        <el-col :span="4">
                            <el-select size="small" v-model="sub_row.type" @change="subrow_type_change" style="width:95%; position: relative; top: -10px;" placeholder="類型">
                                <el-option v-for="item in type_opt" :key="item.value" :label="item.label" :value="item.value">
                                    <el-tooltip placement="right">
                                        <div v-if="item.value=='測試'" slot="content">測試 - 借用給客戶(3個月)<br>審核單位: 產品 BU<br>申請新的 key 須填寫領用單，行政查詢用</div>
                                        <div v-if="item.value=='出貨'" slot="content">出貨 - 尚未完全付完款項(6個月)<br>審核單位: 財會部<br>請提供訂單編號供行政查詢</div>
                                        <div v-if="item.value=='正式'" slot="content">正式 - 付完全部款項(隔年1月31日)<br>審核單位: 財會部<br>請提供訂單編號供行政查詢<br>系統會自動延期一年</div>
                                        <div v-if="item.value=='永久'" slot="content">台灣區需提供客戶切結書<br>目前試用電測付完尾款之客戶</div>
                                        <span style="color: #8492a6; font-size: 13px; padding:10px 55px">{{ item.value }}</span>
                                    </el-tooltip>
                                </el-option>
                            </el-select>
                        </el-col>

                        <el-col :span="2" style="text-align: center;">到期日</el-col>
                        <el-col :span="4">
                            <el-date-picker type="date" value-format="yyyy-MM-dd" name="expiration" 
                            v-model="sub_row.expiration" style="width:95%; position: relative; top: -10px;" placeholder="請輸入到期日"></el-date-picker>
                        </el-col>

                        <el-col :span="2" style="text-align: center;">數量</el-col>
                        <el-col :span="4"><el-input  v-model.number="sub_row.count" style="width: 95%; position: relative; top: -10px;" placeholder="請輸入數量"></el-input></el-col>

                        <el-col :span="2" style="text-align: center;">版本(選填)</el-col>
                        <el-col :span="4"><el-input  v-model="sub_row.version" style="width: 95%; position: relative; top: -10px;" placeholder="請輸入允許版本"></el-input></el-col>
                    </div>
                </el-form-item>
                <el-form-item >
                    <div style="text-align: start;">
                        <el-col :span="2">負責人</el-col>
                        <el-col :span="6">
                            <el-autocomplete  v-model="sub_row.user" style="width: 223px; position: relative; top: -10px;" 
                                :fetch-suggestions="querySearch_user" placeholder="請輸入負責人" ></el-autocomplete>
                        </el-col>
                    </div>
                </el-form-item>
                <el-form-item >
                    <div style="text-align: start;">
                        <el-col :span="2">聯絡人</el-col>
                        <div style="display:flex">
                            <el-select v-model="multi_contact_form.search_contact" @change="((item)=>{subrow_contact_selection_change(item)})" 
                                filterable clearable multiple :filter-method="contact_fliterer" @keyup.enter.native="subrow_contact_enter"
                                style="width: 647px; bottom: 7px;">
                                <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                            </el-select>
                        
                            <div>
                                <el-popover placement="bottom"  trigger="click" popper-class="KeyID_popover" ref="contact_pop">
                                    <div style="text-align: center; font-size: 18px;">添加多筆聯絡人</div>
                                    <div style="display:flex">
                                    <el-select v-model="multi_contact_form.search_contact" @change="((item)=>{subrow_contact_selection_change(item)})" 
                                        filterable clearable multiple :filter-method="contact_fliterer" @keyup.enter.native="subrow_contact_enter"
                                        class = "contact-input">
                                        <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                                    </el-select>
                                    </div>
                                    <el-button  type="warning" slot="reference" style="left: -43px; position: relative;">添加多筆</el-button>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </el-form-item>
                <el-form-item >
                    <div style="text-align: start;">
                        <el-col :span="2">備註(選填)</el-col>
                        <el-input  v-model="sub_row.comment" style="width: 582px; position: relative; top: -10px;" placeholder="請輸入備註"></el-input>
                    </div>
                </el-form-item>
            
            </el-form>
            <div style="position:relative; text-align:right">
                <el-button type="warning" @click="close_add_dialog">取消</el-button>
                <el-button type="warning" @click="subrow_add()">添加</el-button>
            </div>
        </el-dialog>
        <div>
            <el-header style="top:-60px; text-align: right; font-size:20px; position:relative; background-color:#EBD1A0 ; ">
                <div style="position:absolute;left:30px;top:3px; cursor:pointer;" @click="cancel">License Application Service</div>

                <el-popover trigger="hover" width="200" placement="bottom" :close-delay="delay_time">
                
                <div><span>成員名稱: {{user[0]}}</span></div>
                <div><span>-----------------------------------------</span></div>
                <div><el-button  @click="$router.push({name: 'admin', query:{}})"  type="primary" icon="el-icon-setting">後台管理</el-button></div>
                <div><el-button  @click="Logout"  icon="el-icon-switch-button" style="background:#F56C6C; color:#FFFFFF; width:117px;">登出</el-button></div>
                
                <el-button  class="memeber_button" slot="reference" icon="el-icon-s-custom"></el-button>
                </el-popover>
            </el-header>
        </div>

        <div class="heading">增加</div>
        <div v-show="warning" style="color: red; font-size:20px; font-weight: bold;">{{warning_message}}</div>
        <!-- 主要表格 -->
        <div style="position:relative; top:0px; margin:0 auto; z-index: 110; width:90%">
            <el-table
            @selection-change="handleSelectionChange"
            ref="addtable"
            :data="tableData"
            :row-style="{background: '#FFF0D2'}"
            :cell-style="setCellColor"
            height= 650px>
            <el-table-column type="selection" align="center" prop="" label="編輯" width=50></el-table-column>
            <el-table-column align="center"  label=" " width=70>
              <template slot-scope="scope">
                {{ scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column align="center" prop="" label="操作" width=80>
                <template slot-scope = "{$index,row}" >
                    <el-button  type="warning" circle icon="el-icon-refresh-right" @click="restore($index, row)" size = "mini"></el-button>
                </template>
            </el-table-column>
            
            <el-table-column align="center" prop="customer" label="客戶">
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="customer" v-model="row.customer"  ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="sn" label="KeyID"> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="number" name="sn" v-model="row.sn" ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="func_uid" label="產品" width=150> 
                <template slot-scope = "{$index,row}">
                    <el-input class="func_uid" type="text" name="product" v-model="row.product" style="width: 110px;" readonly></el-input>
                    <el-popover placement="bottom" width="260" trigger="click" :ref="`funcuid_popover-${$index}`">
                        <el-tree
                            style="border-radius:4px; min-height:290px; overflow-y:auto; max-height:400px;"
                            :data="single_choice_tree"
                            :props="defaultProps"
                            node-key="id"
                            :ref="`funcuid_tree-${$index}`"
                            :render-content="tag_for_tree"
                            check-on-click-node
                            @check="funcuid_click($index)"
                            show-checkbox>
                        </el-tree>

                        <el-button type="text" slot="reference"  icon="el-icon-edit-outline" style="font-size:15px;"></el-button>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="module" label="模組"> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="module" v-model="row.module" class="func_uid" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="version" label="版本" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="version" v-model="row.version" ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="count" label="數量" width=100> 
                <template slot-scope = "{$index,row}">
                    <el-input  type="number" name="count" v-model="row.count" ></el-input>
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
                    <el-select  v-model="row.region" >
                        <el-option
                            v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="expiration" label="使用期限" width=145> 
                <template slot-scope = "{$index,row}">
                    <el-date-picker  type="date" value-format="yyyy-MM-dd" name="expiration" v-model="row.expiration" style="width:135px"></el-date-picker>
                </template>
            </el-table-column>
            
            <el-table-column align="center" prop="user" label="負責人"> 
                <template slot-scope = "{$index,row}">
                    <div style="display: flex;">
                        <el-autocomplete  v-model="row.user" :fetch-suggestions="querySearch_user" popper-append-to-body="false" placeholder="僅限一位負責人" />
                    </div>
                </template>
            </el-table-column>
            
            <el-table-column align="center" prop="contact" label="聯絡人" width=200> 
                <template slot-scope = "{$index,row}">
                    <el-select v-model="row.contact_display" @change="((item)=>{contact_selection_change(item, $index)})" filterable clearable multiple
                        :filter-method="contact_fliterer" @keyup.enter.native="contact_enter($index)" class = "contact-input" placeholder = "請輸入後按enter">
                        <el-option v-for="opt in contact_fliter" :key="opt.value" :label="opt.label" :value="opt.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="comment" label="備註" > 
               <template slot-scope = "{$index,row}">
                    <el-input  type="text" name="comment" v-model="row.comment" ></el-input>
                </template>
            </el-table-column>
            
            </el-table>
        </div>
        <el-button class="submit_button" @click="cancel" size = "medium"  type="warning">取消</el-button>
        <el-button class="submit_button" @click="submit" size = "medium"  type="warning">添加</el-button>
    
    </div>
</template>
<script>
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'add',
  data: function() {
        return {
            product_groups_data:[],
            user:[],
            all_Data:{},//整個資料庫所有數據
            info_data:[],
            origin_Data:[],
            tableData:[],
            productgroup_tree:[],
            customer_site_opt:[],
            user_opt:[],
            customer_name_opt:[],
            region_opt:[],
            //caption_opt:[],
            func_uid_opt:[],
            sn_opt:[],
            contact_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            info_id:0,
            input:{//左上方input框使用的(為了將客戶拆解)
                name:'',
                factory:''
            },
            product_dialog:{
                caption:'',
                product_list:[],
                description:'',
                remarks:'',
                product_list_detail:[]
            },
            sub_row:{
                category: "",
                comment: "",
                contact: "",
                count: null,
                customer: "",
                expiration: "",
                func_uid: [],
                index: null,
                info: [],
                info_id: null,
                issued: "",
                operator: "",
                region: "",
                registration: "",
                sn: null,
                sn_multi:[],
                type: "",
                user: "",
                version: "",
                contact_display:[''],
                user_display:['']
            },
            multi_KeyID_form:{
                range_begin:'', 
                range_end:'',
                data:'',
            },
            multi_contact_form:{
                search_contact:'',
                data:'',
            },
            row_index:0,
            drawer: false,
            tree_data:[],
            origin_tree_data:[],
            dialogVisible:false,
            deter_require:[],
            append_tree_lock:false,//新增產品群組的lock
            register_append_node:[],//暫存新增產品群組data
            tree_node_count: 0,//key_id
            caption_to_product:[],//群組下對應所有產品
            tree_map:new Map(),
            optionSet:new Set(),
            isLoading:true,
            fight_data: [],
            add_dialog: false,
            tree_checked: [],
            user_region:"",
            checked_Data:[],
            product_map: new Map(),
            option_map: new Map(),
            module_map: new Map(),
            customer_map: new Map(),
            sn_dict: {},
            contact_input:'',
            contact_fliter:[],
            sn_input:[],
            sn_fliter:[],
            warning: false,
            warning_message:'',
        }
  },
  created(){
    this.axios.get('/get_product_groups_info_data',{
        headers: {'Content-Encoding': 'gzip'}
    }).then(response => {
    this.product_groups_data = JSON.parse(JSON.stringify(response.data))['product_groups'];//最新product_group資料

    this.info_data = JSON.parse(JSON.stringify(response.data))['info_data']
    
    this.axios.get('/show_all',{
        headers: {'Content-Encoding': 'gzip'},
        params:{
            user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))
        }
    }).then(response => {
        this.user = JSON.parse(sessionStorage.getItem('user'))
        this.all_Data = JSON.parse(JSON.stringify(response.data));
        //-----------------------處理nofilter_data(跟Show_all nofilter_data不一樣，add頁面的nofilter_data是整個info_data不關乎權限)
        this.product_map = new Map()
        this.option_map = new Map()
        this.module_map = new Map()
        this.sn_dict = JSON.parse(JSON.stringify(response.data))['sn_dict']
        for(let product of this.all_Data['product_data'])
            this.product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
        for(let option of this.all_Data['option_data'])
            this.option_map.set(option['option_name'],{'category_id':this.product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})
        for(let mod of this.all_Data['module_data'])
            this.module_map.set(mod['mod_uid'],mod['caption'])
        
        this.info_id = this.info_data.length;

        for(let sn of this.all_Data['sn_data'])
            this.sn_opt.push({value:sn['sn'],label:sn['sn']});
            
        var user_set = new Set();
        for(let user of this.all_Data['sn_data'])
            for(let user_email of user['user'].split(','))
                user_set.add(user_email)
        for(let user of user_set)
            this.user_opt.push({value:user,label:user})

        for (let region of this.all_Data['region_data'])
            this.region_opt.push({value:region['name'],label:region['name']});
            
        for (let contact of this.all_Data['user_data']){
            if(contact['user']==this.user[0]){
                for (let region of this.all_Data['region_data']){
                    if(region['region_id'] == contact['region'][1]){
                        this.user_region = region['name']
                        break;
                    }
                }
            } 
            this.contact_opt.push({value:contact['email'],label:contact['email']});
        }
        for (let customer of this.all_Data['customer_data']){
            let test_name = 0;
            let test_site = 0;
            for(let customer_name of this.customer_name_opt)
                if(customer_name['value'] == customer['name'])
                    test_name = 1
            for(let customer_site of this.customer_site_opt)
                if(customer_site['value'] == customer['site'])
                    test_site = 1
            if(test_name == 0)
                this.customer_name_opt.push({value:customer['name'],label:customer['name']})
            if(test_site == 0)
                this.customer_site_opt.push({value:customer['site'],label:customer['site']})
        }
        this.contact_fliter = this.contact_opt;
        this.sn_fliter = this.sn_opt;
        var checkData = JSON.parse(this.$route.query.checked_Data);
        if(checkData.length != 0){
            for (let add of checkData){
                add['contact_display'] = add['contact'].split(';');
            }
            for (let data of checkData){
                data['info_id'] = this.info_id;
                data = Object.assign(data,{'operator':'新增'});
                this.info_id++;
            }
            this.origin_Data = JSON.parse(JSON.stringify(checkData));
            this.tableData = JSON.parse(JSON.stringify(checkData));
        }
        //-----------------------處理樹狀數據(未加入自訂群組)---------------------//
        var captionSet = new Set();
        for(let caption of this.all_Data['product_data'])
            captionSet.add(caption['category_id'])
        for(let caption of captionSet){
            this.tree_data.push({'id':this.tree_node_count,'label':caption,'children':[]})
            this.tree_node_count++;
        }
        for(let product of this.all_Data['product_data'])
            for(let i = 0;i < this.tree_data.length; i++)
                if(this.tree_data[i]['label'] == product['category_id']){
                    this.tree_data[i]['children'].push({'id':this.tree_node_count,'label':product['caption'],'children':[],'category':product['category_id']})
                    this.tree_node_count++;
                }
        for(let i = 0; i < this.tree_data.length; i++)
            for(let j = 0; j < this.tree_data[i]['children'].length; j++)
                for(let product of this.all_Data['product_data'])
                    if(this.tree_data[i]['children'][j]['label'] == product['caption'])
                        for(let option of this.all_Data['option_data'])
                            if((product['product_name'] == option['product_name']) && !(option['caption'].includes("Agent ID"))){
                                this.tree_data[i]['children'][j]['children'].push({'id':this.tree_node_count,'label':option['caption'],'product_name':option['product_name'],'children':[],'category':option['product_name']})
                                this.tree_node_count++;
                            }
        this.origin_tree_data = JSON.parse(JSON.stringify(this.tree_data))
        //-------------------------caption對應product-------------------//
        for(let caption of captionSet){
            this.caption_to_product.push({'caption':caption,'product':[]})
            for(let pro of this.all_Data['product_data']){
                if(pro['category_id'] == this.caption_to_product[this.caption_to_product.length - 1]['caption'])
                    this.caption_to_product[this.caption_to_product.length - 1]['product'].push(pro['product_name'])
            }
        }

        for(let opt of this.all_Data['option_data'])
            this.optionSet.add(opt['product_name'])
        for(let opt of this.optionSet){
            this.caption_to_product.push({'caption':opt,'product':[]})
            for(let option of this.all_Data['option_data']){
                if(option['product_name'] == this.caption_to_product[this.caption_to_product.length - 1]['caption'])
                    this.caption_to_product[this.caption_to_product.length - 1]['product'].push(option['option_name'])
            }
            for(let i = 0; i < this.caption_to_product.length - 1; i++)
                if(this.caption_to_product[i]['product'].indexOf(this.caption_to_product[this.caption_to_product.length - 1]['caption']) != -1){
                    this.caption_to_product[i]['product'].splice(this.caption_to_product[i]['product'].indexOf(this.caption_to_product[this.caption_to_product.length - 1]['caption']),1)
                    for(let option of this.caption_to_product[this.caption_to_product.length - 1]['product'])
                        this.caption_to_product[i]['product'].push(option)
                }
        }
        for(let i = 0;i < this.caption_to_product.length; i++)
            for(let pro of this.all_Data['product_data']){
                if(this.caption_to_product[i]['caption'] == pro['product_name'])
                    this.caption_to_product[i]['caption'] = pro['caption']
            }

        //--------------------------caption所對應的tree-----------------------------//

        for(let tree of JSON.parse(JSON.stringify(this.tree_data)))
            if(tree.children.length != 0){
                this.tree_map.set(tree.label,tree)
                for(let c_tree of tree.children)
                    if(c_tree.children.length != 0)
                        this.tree_map.set(c_tree.label,c_tree)
            }
        
        //---------------------將自訂群組插入樹狀圖中(根據tag)----------------------//
        for(let pro_group of this.product_groups_data){//根據tag找到所對應的tree節點
            let temp = this.tree_data;
            for(let tag of JSON.parse(pro_group.tag))
                temp = temp[this.search_tree_index(temp,tag)]['children']

            temp.unshift({'id':this.tree_node_count++,'label':pro_group['caption'],'children':[]})
            let under_group = this.deter_group(this.caption_to_product,JSON.parse(pro_group['product_list']))

            let copy_pro_group = JSON.parse(pro_group['product_list']);
            for(let gro of under_group){
                let tree = this.tree_node_adjust(this.tree_map.get(gro),this.tree_node_count)
                temp[0]['children'].push(tree[0])
                this.tree_node_count = tree[1]
                for(let table of this.caption_to_product)
                    if(table['caption'] == gro){
                        for(let pro of table['product']){
                            let index = copy_pro_group.indexOf(pro);
                            if(index != -1)
                                copy_pro_group.splice(index,1)
                        }
                    }
            }

            for(let remainder_pro of copy_pro_group){//將預設群組內的產品去掉後 剩下的func_uid再額外插入自訂群組
                for(let opt of this.all_Data['option_data'])
                    if(opt['option_name'] == remainder_pro)
                        temp[0]['children'].push({'id':this.tree_node_count,'label':opt['caption'],'product_name':opt['product_name'],'children':[]})
                for(let pro of this.all_Data['product_data'])
                    if(pro['product_name'] == remainder_pro)
                        temp[0]['children'].push({'id':this.tree_node_count,'label':pro['caption'],'children':[]})
                this.tree_node_count++
            }
        }
        
        this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))
        this.isLoading = false
        if(this.tableData.length == 0)
                this.GoAdd();
        

        //必填項目顏色
        for(let i of this.tableData){
            this.deter_require.push({'customer':false, 'sn':false , 'product':false, 'count':false, 'expiration':false, 'user':false, 'contact':false});
        }
        
        //讓不能勾選的項目disabled
        this.single_choice_tree = JSON.parse(JSON.stringify(this.tree_data))
        function dfs(node){
            if(node['children'].length != 0){
                node['disabled'] = true
                for(let j of node['children']){
                    dfs(j);
                }
            }
        }
        for(let i of this.single_choice_tree)
            dfs(i);

    })
    
    })},
    watch:{
        input:{
            handler(newName, oldName) {//監測input是否改變 若改變則改變tableData customer
                if(this.input.factory != '')
                    this.sub_row.customer = this.input.name + '|' + this.input.factory
                else
                    this.sub_row.customer = this.input.name;
            },
            deep: true,
        },
        "sub_row.sn":{
            handler(newName, oldName) {//根據監測sn 帶入sn of user
                for(let sn of this.all_Data['sn_data'])//當你新增客戶 改了user 又把新增的庫戶改回來 此時需要把user還原
                    if(this.sub_row['sn'] == sn['sn'])
                        this.sub_row['user'] = sn['user'];
            },
            deep: true,
        },
    },
    methods:{
        funcuid_click(index) {
            let checked_nodes = this.$refs[`funcuid_tree-${index}`].getCheckedNodes();
            
            if(checked_nodes.length == 2){
                //父節點只有一個子節點
                if(checked_nodes[0].children.length == 1){
                    let node = checked_nodes[1]
                    if(node['product_name'] != undefined){
                        this.$confirm(`將更改為產品:〈${node['product_name']}〉模組:〈${node['label']}〉`
                            , '提示', {
                            confirmButtonText: '確定',
                            cancelButtonText: '取消',
                            showClose: false,
                            type: 'warning',
                            center: true
                        }).then(() => {
                            this.deter_require[index]['func_uid'] = false

                            this.tableData[index].product = node['product_name']
                            this.tableData[index].module = node['label']

                            //轉換func_uid
                            let my_func_uid = ""
                            if(this.tableData[index].module == ""){
                                for(let i of this.product_map){
                                    //for迴圈會將map轉成陣列
                                    if(i[1]['caption'] == this.tableData[index].product)
                                        my_func_uid = i[0]
                                }
                            }
                            else{
                                for(let i of this.option_map){
                                    //for迴圈會將map轉成陣列
                                    if(i[1]['product_name'] == this.tableData[index].product &&　
                                        i[1]['caption'] == this.tableData[index].module){
                                        my_func_uid = i[0]
                                    }
                                }
                            }
                            this.tableData[index].func_uid = my_func_uid

                            //category
                            this.tableData[index].category = this.product_map.get(my_func_uid)['category_id']


                            this.$refs[`funcuid_popover-${index}`].doClose()
                            this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                        }).catch(() => {
                            this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                            return false;
                        });
                    }
                    else{
                        this.$confirm(`將更改為產品:〈${node['label']}〉`
                            , '提示', {
                            confirmButtonText: '確定',
                            cancelButtonText: '取消',
                            showClose: false,
                            type: 'warning',
                            center: true
                        }).then(() => {
                            this.tableData[index].product = node['label']
                            this.tableData[index].module = ""

                            //轉換func_uid
                            let my_func_uid = ""
                            if(this.tableData[index].module == ""){
                                for(let i of this.product_map){
                                    //for迴圈會將map轉成陣列
                                    if(i[1]['caption'] == this.tableData[index].product)
                                        my_func_uid = i[0]
                                }
                            }
                            else{
                                for(let i of this.option_map){
                                    //for迴圈會將map轉成陣列
                                    if(i[1]['product_name'] == this.tableData[index].product &&　
                                        i[1]['caption'] == this.tableData[index].module){
                                        my_func_uid = i[0]
                                    }
                                }
                            }
                            this.tableData[index].func_uid = my_func_uid

                            //category
                            this.tableData[index].category = this.product_map.get(my_func_uid)['category_id']

                            this.$refs[`funcuid_popover-${index}`].doClose()
                            this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);

                            this.deter_require[index]['func_uid'] = false
                        }).catch(() => {
                            this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                            return false;
                        });
                    }
                }
            }
            else if(checked_nodes.length == 1){
                let node = checked_nodes[0]
                if(node['product_name'] != undefined){
                    this.$confirm(`將更改為產品:〈${node['product_name']}〉模組:〈${node['label']}〉`
                        , '提示', {
                        confirmButtonText: '確定',
                        cancelButtonText: '取消',
                        showClose: false,
                        type: 'warning',
                        center: true
                    }).then(() => {
                        this.deter_require[index]['func_uid'] = false

                        this.tableData[index].product = node['product_name']
                        this.tableData[index].module = node['label']

                        //轉換func_uid
                        let my_func_uid = ""
                        if(this.tableData[index].module == ""){
                            for(let i of this.product_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['caption'] == this.tableData[index].product)
                                    my_func_uid = i[0]
                            }
                        }
                        else{
                            for(let i of this.option_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['product_name'] == this.tableData[index].product &&　
                                    i[1]['caption'] == this.tableData[index].module){
                                    my_func_uid = i[0]
                                }
                            }
                        }
                        this.tableData[index].func_uid = my_func_uid

                        //category
                        this.tableData[index].category = this.product_map.get(my_func_uid)['category_id']
                        
                        this.$refs[`funcuid_popover-${index}`].doClose()
                        this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                    }).catch(() => {
                        this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                        return false;
                    });

                    
                }
                else{
                    this.$confirm(`將更改為產品:〈${node['label']}〉`
                        , '提示', {
                        confirmButtonText: '確定',
                        cancelButtonText: '取消',
                        showClose: false,
                        type: 'warning',
                        center: true
                    }).then(() => {
                        this.tableData[index].product = node['label']
                        this.tableData[index].module = ""

                        //轉換func_uid
                        let my_func_uid = ""
                        if(this.tableData[index].module == ""){
                            for(let i of this.product_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['caption'] == this.tableData[index].product)
                                    my_func_uid = i[0]
                            }
                        }
                        else{
                            for(let i of this.option_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['product_name'] == this.tableData[index].product &&　
                                    i[1]['caption'] == this.tableData[index].module){
                                    my_func_uid = i[0]
                                }
                            }
                        }
                        this.tableData[index].func_uid = my_func_uid

                        //category
                        this.tableData[index].category = this.product_map.get(my_func_uid)['category_id']
                        
                        this.$refs[`funcuid_popover-${index}`].doClose()
                        this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);

                        this.deter_require[index]['func_uid'] = false
                    }).catch(() => {
                        this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                        return;
                    });
                }
            }
            else{
                this.$refs[`funcuid_tree-${index}`].setCheckedKeys([]);
                return
            }
            
        },
        
        restore:function(index, row){//回復成原本的資料列
            for(let i of Object.keys(this.origin_Data[index]))
                this.tableData[index][i] = this.origin_Data[index][i]
        },
        handleSelectionChange (val) {
            this.checked_Data = JSON.parse(JSON.stringify(val));
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
        GoAdd(){
            //無勾選資料
            if(this.checked_Data.length == 0){
                this.input.name = "";
                this.input.factory  = "";
                this.sub_row['region'] = this.user_region;
                this.sub_row['sn'] = "";
                this.sub_row['sn_multi'] = [];
                this.sub_row['func_uid'] = "";
                this.sub_row['count'] = 1;
                this.sub_row['version'] = "";
                this.sub_row['user'] = this.user[2];
                this.sub_row['contact'] = this.user[2];
                this.sub_row['comment'] = "";
                this.sub_row['type'] = "測試";
                this.subrow_type_change();
                this.multi_contact_form.search_contact = [this.user[2]]
            }
            this.add_dialog = true;
        },
        close_add_dialog(){
            this.add_dialog=false;
            this.sub_row = {category: "",comment: "",contact: "",count: null,customer: "",
                expiration: "",func_uid: [],index: null,info: [],info_id: null,issued: "",sn_multi:[],
                operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
            this.input.name = ''
            this.input.factory = ''
        },
        subrow_contact_selection_change(selection){
            this.sub_row.contact = selection.join(';')
        },
        contact_selection_change(selection, index){
            this.tableData[index].contact = selection.join(';')
        },
        contact_change(input, index){
            this.tableData[index].contact_display = input.split(';')
        },
        contact_enter(index){
            this.tableData[index]['contact_display'].push(this.contact_input)
            this.tableData[index]['contact'] = this.tableData[index]['contact_display'].join(';')
        },
        subrow_contact_enter(){
            this.multi_contact_form.search_contact.push(this.contact_input)
            this.sub_row.contact = this.multi_contact_form.search_contact.join(';')
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
        sn_fliterer(val){
            this.sn_input = val;
            if (val) {
                this.sn_fliter = this.sn_opt.filter((item) => {
                    if (String(item['label']).includes(val)) 
                        return true
                })
            }
            else{
                this.sn_fliter = this.sn_opt
            }
        },
        subrow_sn_enter(){
            this.sub_row.sn_multi.push(this.sn_input)
        },
        add_multi_KeyID(){
                if(this.multi_KeyID_form.range_begin != '' && this.multi_KeyID_form.range_end == ''){
                    this.$message({message: '請輸入區間結束值',type: 'warning'});
                    return;
                }
                if(this.multi_KeyID_form.range_begin == '' && this.multi_KeyID_form.range_end != ''){
                    this.$message({message: '請輸入區間開始值',type: 'warning'});
                    return;
                }
                for(let KeyID=this.multi_KeyID_form.range_begin; KeyID<=this.multi_KeyID_form.range_end; KeyID++){
                    this.sub_row.sn_multi.push(KeyID)
                }
        },
        add_multi_contact(){
                this.sub_row['contact'] = this.multi_contact_form.data;
                this.$refs['contact_pop'].doClose()
        },
        //根據type自動調整期限
        type_change(index){
            let tempDate = new Date;
            if(this.tableData[index].type == '正式'){
                //正式, 日期設定在隔年的 1/30
                tempDate.setMonth(tempDate.getMonth()+12);
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-01-31'
            }
            if(this.tableData[index].type == '測試'){
                //測試, 以季為單位: 3/31、6/30、9/30、12/31，若時間少於 30 天, 直接進下一季
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
            if(this.tableData[index].type == '出貨'){
                //出貨, 日期設定12/31
                this.tableData[index].expiration = tempDate.toISOString().slice(0, 4) + '-12-31' 
            }
            if(this.tableData[index].type == '永久')//* 當 B ==永久, 日期設定 2100年12月31日
                this.tableData[index].expiration = '2100-12-31'
        },
      
        //add dialog根據type自動調整期限
        subrow_type_change(){
            let tempDate = new Date;
            switch (this.sub_row.type){
                case '正式':
                    //正式, 日期設定在隔年的 1/30
                    tempDate.setMonth(tempDate.getMonth()+12);
                    this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-01-31'
                    break;
                case '測試':
                    //測試, 以季為單位: 3/31、6/30、9/30、12/31，若時間少於 30 天, 直接進下一季
                    let currentMonth = tempDate.getMonth() +1
                    //隔年3/31
                    if(currentMonth==12){
                        tempDate.setMonth(tempDate.getMonth()+12);
                        this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-03-31'
                    }
                    //今年3/31
                    else if(currentMonth==1 || currentMonth==2)
                        this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-03-31'
                    //今年6/30
                    else if(currentMonth==3 || currentMonth==4 || currentMonth==5)
                        this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-06-30'
                    //今年9/30
                    else if(currentMonth==6 || currentMonth==7 || currentMonth==8)
                        this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-09-30'
                    //今年12/31
                    else if(currentMonth==9 || currentMonth==10 || currentMonth==11)
                        this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-12-31'
                    else
                        this.sub_row.expiration = ""
                    break;
                case '出貨':
                    //出貨, 日期設定12/31
                    this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-12-31' 
                    break;
                case '永久':
                    //永久, 日期設定 2100年12月31日
                    this.sub_row.expiration = '2100-12-31'  
                break;
            }
        },
        deter_group(caption_to_product,compare_product){//用caption_to_product判斷自訂群組底下有那些預設群組
            var group_record = []
            var copy = JSON.parse(JSON.stringify(compare_product))
            for(let table of caption_to_product){
                let test = 0
                for(let pro of table['product']){
                    if(copy.indexOf(pro) === -1){//若自訂群組沒有預設群組中一個產品 則直接break
                        test = 1
                        //copy = JSON.parse(JSON.stringify(compare_product))
                        break
                    }
                }
                if(test == 0){//若群組有該預設群組下所有產品 則將預設群組中所有產品從群組下移除
                    group_record.push(table['caption'])
                    for(let pro of table['product'])
                        copy.splice(copy.indexOf(pro),1)
                }
            }

            return group_record
        },
        store_product_group(){//儲存新增產品群組
            if (this.product_dialog.caption == '' || this.product_dialog.product_list.length == 0){
                this.$message.error('請將「產品群組」新增單，填寫完整');
                return
            }
            var temp = []
            for(let product of this.product_dialog.product_list_detail){//將caption換成product
                let test = 0
                let label_copy = product['label'].split('').reverse().join('').split('(') 
                if(this.optionSet.has(label_copy[0].replace(')','')))
                    product['label'] = product['label'].replace('('+label_copy[0].replace(')','')+')','')
                for(let opt of this.all_Data['option_data'])
                    if(product['label'] == opt['caption'] && product['category'] == opt['product_name']){
                        temp.push(opt['option_name'])
                        test = 1
                        break
                    }
                if(test == 0)
                    for(let pro of this.all_Data['product_data'])
                        if(product['label'] == pro['caption']){
                            temp.push(pro['product_name'])
                            break
                        }
            }

            for(let product_group of this.product_groups_data){//防止產品群組名稱or產品 重複
                if(product_group['caption'] == this.product_dialog.caption){
                    this.$message.error('產品名稱重複，請更改');
                    return
                }
                if(product_group.product_list == JSON.stringify(temp)){
                    this.$message.error('群組內產品與其他群組完全重複');
                    return
                }
            }
            if(this.append_tree_lock != true){
                this.$message.error('請選擇群組所在位置');
                return
            }
            this.product_dialog.product_list = JSON.parse(JSON.stringify(temp));
            var temp_local = []
            var temp = this.register_append_node[0]
            while(temp.label != undefined){
                temp_local.unshift(temp.label)
                temp = temp.parent;
            }

            this.axios.post("/save_to_product_group",{
                caption:this.product_dialog.caption,
                product_list:JSON.stringify(this.product_dialog.product_list),
                tag:JSON.stringify(temp_local),
                description:this.product_dialog.description,
                remarks:this.product_dialog.remarks
            }).then((response)=>{
                this.axios.get('/get_product_groups_info_data',{
                }).then(response => {
                this.product_groups_data = JSON.parse(JSON.stringify(response.data))['product_groups'];//最新product_group資料
                this.dialogVisible = false
                //------------------------把新增的product_groups重新insert tree一次---------------------//
                this.tree_data = JSON.parse(JSON.stringify(this.origin_tree_data))
                for(let pro_group of this.product_groups_data){//根據tag找到所對應的tree節點
                    let temp = this.tree_data;
                    for(let tag of JSON.parse(pro_group.tag))
                        temp = temp[this.search_tree_index(temp,tag)]['children']

                    temp.unshift({'id':this.tree_node_count++,'label':pro_group['caption'],'children':[]})
                    let under_group = this.deter_group(this.caption_to_product,JSON.parse(pro_group['product_list']))

                    let copy_pro_group = JSON.parse(pro_group['product_list']);
                    for(let gro of under_group){
                        let tree = this.tree_node_adjust(this.tree_map.get(gro),this.tree_node_count)
                        temp[0]['children'].push(tree[0])
                        this.tree_node_count = tree[1]
                        for(let table of this.caption_to_product)
                            if(table['caption'] == gro){
                                for(let pro of table['product']){
                                    let index = copy_pro_group.indexOf(pro);
                                    if(index != -1)
                                        copy_pro_group.splice(index,1)
                                }
                            }
                    }

                    for(let remainder_pro of copy_pro_group){//將預設群組內的產品去掉後 剩下的func_uid再額外插入自訂群組
                        for(let opt of this.all_Data['option_data'])
                            if(opt['option_name'] == remainder_pro)
                                temp[0]['children'].push({'id':this.tree_node_count,'product_name':opt['product_name'],'label':opt['caption'],'children':[]})
                        for(let pro of this.all_Data['product_data'])
                            if(pro['product_name'] == remainder_pro)
                                temp[0]['children'].push({'id':this.tree_node_count,'label':pro['caption'],'children':[]})
                        this.tree_node_count++
                    }
                }
                this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))
                this.product_dialog.caption = ''
                this.product_dialog.product_list = []
                this.product_dialog.description = ''
                this.product_dialog.remarks = ''
                this.product_dialog.product_list_detail = []
                })
            });
        },
        /*interact_tree(data){//el-select 刪除tag連動
            let temp_list = []

            for(let temp of this.$refs.product_group_tree.getCheckedNodes()){
                if(temp['children'].length == 0 && temp['label'] != data)
                    temp_list.push(temp)
            }
        this.$nextTick(() => {
            this.$refs.product_group_tree.setCheckedNodes([])
            this.$refs.product_group_tree.setCheckedNodes(temp_list)
            });
        },*/
        choose_func_uid(){//產品選擇
            this.drawer = true;
            this.product_group = []//將產品群組選擇初始化
        },
        cancel_drawer(){//取消tree選擇
            this.$nextTick(() => {this.$refs.tree.setCheckedKeys([])});//清空tree選擇
            this.drawer = false;
        },
        check_drawer(){//確認產品選擇
            this.sub_row.func_uid=[]
            
            var product_Set = new Set();//用set過濾 因有重複
            for(let node of this.$refs.tree.getCheckedNodes()){
                if(node['children'].length == 0 || node['children'] == undefined){
                    if(node['product_name'] != undefined)
                        product_Set.add(node['label']+'('+node['product_name']+')')
                    else
                        product_Set.add(node['label'])
                }
            }
            for(let product of product_Set)
                this.sub_row.func_uid.push(product)
            
            this.$nextTick(() => {this.$refs.tree.setCheckedKeys([])});//清空tree選擇
            this.drawer = false;
        },
        tree_node_adjust(tree,tree_node_count){//調整整個子樹的tree_node_count 
            let copy_tree = JSON.parse(JSON.stringify(tree))
            copy_tree.id = tree_node_count++;
            for(let c_tree of copy_tree.children){
                c_tree.id = tree_node_count++;
                for(let cc_tree of c_tree.children)
                    cc_tree.id = tree_node_count++;
            }
            return [copy_tree,tree_node_count]//[0]tree [1]node_count
        },
        cancel_product_group(){//初始化產品群組Dialog
            this.product_dialog.caption = ''
            this.product_dialog.product_list = []
            this.product_dialog.description=''
            this.product_dialog.remarks=''
            this.$nextTick(() => {this.$refs.product_group_tree.setCheckedKeys([])});//清空tree選擇
            this.dialogVisible = false;
        },
        remove(node, data) {//刪除新增節點
            this.append_tree_lock = false;
            const parent = node.parent;
            const children = parent.data.children || parent.data;
            const index = children.findIndex(d => d.id === data.id);
            children.splice(index, 1);
            this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))//初始化產品群組tree
            this.register_append_node = [];
        },
        append(node,data) {//新增群組節點
            if(this.product_dialog.caption == ''){
                this.$message.error('請填寫「群組名稱」，再選擇插入位置');
                return 
            }
            this.append_tree_lock = true;
            const newChild = {'label': this.product_dialog.caption, 'children': [], disabled:true,'add':true};
            if (!data.children) {
            this.$set(data, 'children', []);
            }
            data.children.push(newChild);
            this.register_append_node = [node];
        },
        tag_for_tree(h, { node, data, store }) {//產品群組在tree中 右邊有[群組]tag字樣
            for(let pro_group of this.product_groups_data){
                if(node.label == pro_group['caption'])
                    return ( <div> <span>{node.label}</span> <el-tag style="position:absolute;right:1px;font-size:14px;height:25px;"type="success">G</el-tag></div>)
                if(node.parent.label == pro_group['caption'])
                    if(node.data.children.length == 0 && node.data.product_name != undefined)
                        return ( <div> <span>{node.label}</span> <el-tag style="position:absolute;right:1px;font-size:14px;height:25px;"type="info">{node.data.product_name}</el-tag></div>)
            }
            return( <div> <span>{node.label}</span></div>) 
        },
        deter_product_group(node){//若是自訂群組則貼家G標籤 若是自訂群組下的product則不用
            for(let pro_group of this.product_groups_data)
            if(node.label == pro_group['caption'])
                return 'group'
            for(let pro_group of this.product_groups_data)
            if(node.parent.label == pro_group['caption'])
                return 'under_group'
            return false
        },
        choose_product_group(data,checked){//選擇product_group_tree時 同步帶入產品群組新增表單 
            var temp_product_list = []
            var temp_product_list_detail = []
            for(let product of this.$refs.product_group_tree.getCheckedNodes())
                if(product['children'].length == 0){
                    if(product['product_name']!= undefined){
                        temp_product_list.push(product['label']+'('+product['product_name']+')')
                        temp_product_list_detail.push({'label':product['label'],'category':product['category']})
                    }
                    else{
                        temp_product_list.push(product['label'])
                        temp_product_list_detail.push({'label':product['label'],'category':product['category']})
                    }
                }
            this.product_dialog.product_list = temp_product_list
            this.product_dialog.product_list_detail = temp_product_list_detail
        },
        handleCheckChange(data, checked){
            this.tree_checked = [];
            for(let node of this.$refs.tree.getCheckedNodes()){
                if(node['children'].length == 0 || node['children'] == undefined)
                    this.tree_checked.push(node)
            }
    
        },
        search_tree_index(array,SearchWord){//找自訂群組所對應tree的index
            for(let i = 0; i < array.length; i++)
                if(array[i]['label'] == SearchWord)
                    return i
            return -1
        },
        test_edit_add(row, index){//修改資料的防呆
            let row_correct = true;
            if(row['customer'] == ""){
                this.deter_require[index]['customer'] = true;
                row_correct =  false;
            }
            if(row['sn'] == null || row['sn'] == ""){
                this.deter_require[index]['sn'] = true;
                row_correct =  false;
            }
            
            if(row['contact'] == ''){
                this.deter_require[index]['contact'] = true;
                row_correct =  false;
            }
            if(row['user'] == ''){
                this.deter_require[index]['user'] = true;
                row_correct =  false;
            }

            let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
            if(row['user'].search(emailRule) == -1){
                this.$message({message: '請填寫有效信箱，且僅限一位負責人',type: 'warning'});
                this.deter_require[index]['user'] = true;
                return false;
            }
            
            if(row['count'] == null || row['count'] == ""){
                this.deter_require[index]['count'] = true;
                row_correct =  false;
            }
            

            if(row['expiration'] == null || row['expiration'] == ""){
                this.deter_require[index]['expiration'] = true;
                row_correct =  false;
            }

            return row_correct;
        },
        subrow_test_edit_add(){//新增表單加入時的防呆
            
            if(this.input.name == null || this.input.name == ""){
                this.$message({message: '客戶不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['user'] == null || this.sub_row['user'] == ""){
                this.$message({message: '負責人不可為空',type: 'warning'});
                return false;
            }
            let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
            if(this.sub_row['user'].search(emailRule) == -1){
                this.$message({message: '請填寫有效信箱，且僅限一位負責人',type: 'warning'});
                return false;
            }
            if(this.sub_row['contact_display'].length == 0){
                this.$message({message: '聯絡人不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['contact'].length == 0){
                this.$message({message: '聯絡人不可為空',type: 'warning'});
                return false;
            }
            for(let sub_row_sn of this.sub_row.sn_multi){
                if(sub_row_sn == null || sub_row_sn == ""){
                    this.$message({message: 'KeyID不可為空',type: 'warning'});
                    return false;
                }
                else if(!/^[\d;]+$/.test(sub_row_sn)){
                    this.$message({message: 'KeyID只可包含數字',type: 'warning'});
                    return false;
                }
            }
            if(this.sub_row['func_uid'] == null || this.sub_row['func_uid'] == ""){
                this.$message({message: '產品名稱不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['count'] == null || this.sub_row['count'] == ""){
                this.$message({message: '數量不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['expiration'] == null || this.sub_row['expiration'] == ""){
                this.$message({message: '到期日期不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['type'] == null || this.sub_row['type'] == ""){
                this.$message({message: '類型不可為空',type: 'warning'});
                return false;
            }
            if(this.sub_row['region'] == null || this.sub_row['region'] == ""){
                this.$message({message: '地區不可為空',type: 'warning'});
                return false;
            }
            
            return true;
        },
        submit:async function(){
            this.fight_data = []
            let table_index = 0
            
            let all_correct = true
            //重置deter_require
            for(let i of this.deter_require)
                Object.keys(i).forEach((j)=>{i[j] = false})
            this.warning = false
            this.warning_message = ''
            
            // 檢查資料完整性
            for(let row of this.tableData){
                let row_correct = true;
                row_correct = this.test_edit_add(row, table_index);
                if(row_correct == false)
                    all_correct = false;
                table_index += 1;
            }
            if(!all_correct){
                this.warning = true
                this.warning_message = '請確認資料完整性'
                return false
            }
            
            // 檢查相同KeyID不同客戶(不合法)
            let sn_customer_dict = {}
            let diff_sn = []
            for(let row of this.tableData){
                if(row['sn'] in sn_customer_dict){
                    if(!sn_customer_dict[row['sn']].includes(row['customer']))
                        sn_customer_dict[row['sn']].push(row['customer'])
                }
                else{
                    sn_customer_dict[row['sn']] = [row['customer']]
                }
            }

            for(let sn in sn_customer_dict){
                if(sn_customer_dict[sn].length >= 2){
                    diff_sn.push(sn)
                }
            }

            if(diff_sn.length){
                await this.$confirm('相同KeyID僅能對應至一組客戶'
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
                        this.deter_require[index]['customer'] = true
                    }
                    index += 1
                }
                this.warning = true
                this.warning_message = '相同KeyID僅能對應至一組客戶'
                return false
            }

            // 檢查相同KeyID不同負責人(不合法)
            let sn_user_dict = {}
            diff_sn = []
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
            

            // 檢查客戶變更
            var customer_map = new Map()
            for(let customer of this.all_Data['customer_data']){
                if(customer['site'] != '')
                    customer_map.set(customer['customer_id'],customer['name']+'|'+customer['site'])
                else
                    customer_map.set(customer['customer_id'],customer['name'])
            }
            
            let sn_change = {};
            let sn_change_index = []
            let user_change = {};
            let user_change_index = []

            table_index = 0
            for(let row of this.tableData){
                for(let sn of this.all_Data['sn_data']){
                    if((row['sn'] == sn['sn']) && (row['customer'] != customer_map.get(sn['sn_id']))){
                        sn_change[row['sn']] = {'old_customer': customer_map.get(sn['sn_id']), 'new_customer': row['customer']}
                        sn_change_index.push(table_index)
                    }
                    
                    if((row['sn'] == sn['sn']) &&  (row['customer'] == customer_map.get(sn['sn_id'])) && (row['user'] != sn['user'])){
                        user_change[row['sn']] = {'old_user': sn['user'], 'new_user': row['user']}
                        user_change_index.push(table_index)
                    }
                }
                table_index += 1
            }

            if(Object.keys(sn_change).length){
                let conflict_html = '<table style="border-collapse:collapse"  width="500px" border="1">\
                                        <tr>\
                                            <th width="100px">KeyID</th>\
                                            <th width="200px">原客戶</th>\
                                            <th width="200px">新客戶</th>\
                                        </tr>'
                for(let sn in sn_change)
                    conflict_html += `<tr><td>${sn}</td><td>${sn_change[sn]['old_customer']}</td><td>${sn_change[sn]['new_customer']}</td> </tr>`
                conflict_html += '</table>'


                await this.$confirm(conflict_html
                    , '客戶變更，是否刪除原有連結後新增?', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    showClose: false,
                    type: 'warning',
                    center: true,
                    dangerouslyUseHTMLString: true,
                    customClass:'product-conflict'
                }).then(() => {
                    for(let sn_ch in sn_change){
                        for(let show_all_info of this.info_data){
                            if(sn_ch == show_all_info['sn']){
                                delete show_all_info['info']
                                this.fight_data.push(show_all_info);
                            }
                        }
                    }
                }).catch(() => {
                    for(let table_index of sn_change_index)
                        this.deter_require[table_index]['customer'] = true
                    // 驅動表格刷新
                    this.$set(this.deter_require, this.deter_require)
                    
                    all_correct=false
                });
            }

            if(!all_correct){
                this.warning = true
                this.warning_message = '請檢查客戶衝突'
                return false;
            }

            // 檢查產品衝突
            let conflict_keyID = [];
            table_index = 0;
            for(let row of this.tableData){
                for(let info of this.all_Data['info_data'])
                if((row['type'] == this.module_map.get(info['type'])) && (row['sn'] == info['sn'])
                        && (row['func_uid'] == info['func_uid']) && (row['version'] == info['version'])){
                    conflict_keyID.push({'customer': row['customer'],'sn':row['sn'], 'func_uid': row['func_uid'], 'product': row['product'], 'module': row['module'], 'table_index': table_index})
                }
                table_index += 1;
            }

            if(conflict_keyID.length){
                let conflict_html = '<table style="border-collapse:collapse"  width="500px" border="1">\
                                        <tr>\
                                            <th width="100px">客戶</th>\
                                            <th width="100px">KeyID</th>\
                                            <th width="200px">產品</th>\
                                            <th width="200px">模組</th>\
                                        </tr>'
                for(let conflict of conflict_keyID)
                    conflict_html += `<tr><td>${conflict['customer']}</td><td>${conflict['sn']}</td><td>${conflict['product']}</td><td>${conflict['module']}</td> </tr>`
                conflict_html += '</table>'


                await this.$confirm(conflict_html
                    , '以下產品發生衝突，是否刪除原有資料後新增?', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    showClose: false,
                    type: 'warning',
                    center: true,
                    dangerouslyUseHTMLString: true,
                    customClass:'product-conflict'
                }).then(() => {
                    for(let conflict of conflict_keyID){
                        for(let info of this.info_data){
                            if(conflict['sn'] == info['sn'] && conflict['func_uid'] == info['func_uid']){
                                delete info['info']
                                this.fight_data.push(info)
                                break
                            }
                        }
                    }
                }).catch(() => {
                    for(let conflict of conflict_keyID){
                        let table_index = conflict['table_index']
                        this.deter_require[table_index]['func_uid'] = true
                        // 驅動表格刷新
                        this.$set(this.deter_require, this.deter_require)
                    }
                    all_correct=false
                });
            }
            
            // 點擊取消
            if(!all_correct){
                this.warning = true
                this.warning_message = '請檢查產品衝突'
                return true
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
            
            if(this.fight_data.length != 0){//若有新增內重複的資料就自動加一筆刪除(原本的)
                for (let fight of this.fight_data){
                    //增加產品、模組、類型方便確認頁面顯示
                    let module = ''
                    let product = ''
                    let product_name = ''
                    if(this.option_map.get(fight['func_uid']) != undefined){
                        module = this.option_map.get(fight['func_uid'])['caption']
                        product_name = this.option_map.get(fight['func_uid'])['product_name']
                        product = this.product_map.get(product_name)['caption'];
                    }
                    else if(this.product_map.get(fight['func_uid']) != undefined){
                        module=''
                        product = this.product_map.get(fight['func_uid'])['caption'];
                    }
                    else{
                        product = fight['func_uid']
                        module = ''
                    }
                    
                    if(this.module_map.get(fight['type']) != undefined)
                        fight['type'] = this.module_map.get(fight['type']);

                    fight = Object.assign(fight,{'operator':'刪除', 'product':product, 'module':module, 'region': "",
                                                    'user':this.sn_dict[fight['sn']]['user'], 'customer':""})

                    //region
                    for (let region of this.all_Data['region_data']){
                        if(region['region_id'] == this.sn_dict[fight['sn']]['region']){
                            fight['region'] = region['name']
                        }
                    }

                    // customer
                    for (let customer of this.all_Data['customer_data']){
                        if(customer['customer_id'] == this.sn_dict[fight['sn']]['sn_id']){
                            if(customer['site'] == "")
                                fight['customer'] = customer['name']
                            else
                                fight['customer'] = customer['name'] + " " + customer['site']
                            break;
                        }
                    }
                }
                
                this.axios.post("/save_to_handle",{
                    checked_Data:this.fight_data,
                    content:'資料庫衝突',
                    user:this.user
                }).then((response)=>{
                    this.axios.post("/save_to_handle",{//刪除後新增 必須擺在刪除then後 不然會衝突
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
                });
            }
            else{
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
            }
        },
        subrow_add:function(){//新增一行空數據
            if(this.sub_row['contact_display'].length > 1)
                for(let i = 0; i < this.sub_row['contact_display'].length; i++)//若聯絡人修改框中有框無值 則刪除此框
                    if(this.sub_row['contact_display'][i] == ''){
                        this.sub_row['contact_display'].splice(i,1);
                        i--;
                    }
            if(this.subrow_test_edit_add()){
                var tempDate = new Date;
                var today = tempDate.toISOString().slice(0, 10)
                this.sub_row.sn = String(this.sub_row.sn);
            
                for(let mulsn of this.sub_row.sn_multi){
                    for(let func_uid of this.sub_row.func_uid){
                        let product = "";
                        let module = "";
                        let my_func_uid = "";
                        let product_name = "";
                        let category = "";
                        if(func_uid.includes(")(")){
                            product_name = func_uid.split(")(")[1].split(")")[0]
                            module = func_uid.split(")(")[0]+")"
                            category = this.product_map.get(product_name)['category_id'];
                            product = this.product_map.get(product_name)['caption'];
                        }
                        else if(func_uid.includes("(")){
                            product_name = func_uid.split("(")[1].split(")")[0]
                            module = func_uid.split("(")[0]
                            category = this.product_map.get(product_name)['category_id'];
                            product = this.product_map.get(product_name)['caption'];
                        }
                        else{
                            product = func_uid
                            module = ""
                        }
                        
                        //轉換func_uid
                        if(module == ""){
                            for(let i of this.product_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['caption'] == product){
                                    my_func_uid = i[0]
                                    category = i[1]['category_id']
                                }
                            }
                        }
                        else{
                            for(let i of this.option_map){
                                //for迴圈會將map轉成陣列
                                if(i[1]['product_name'] == product_name &&　i[1]['caption'] == module){
                                    my_func_uid = i[0]
                                }
                            }
                        }
                        this.tableData.push({'info_id':this.info_id,'category':category,'comment':this.sub_row.comment,'contact':this.sub_row.contact,
                        'count':this.sub_row.count,'customer':this.sub_row.customer,'expiration':this.sub_row.expiration,
                        'func_uid':my_func_uid,'info':this.sub_row.info,'issued':today,'region':this.sub_row.region,
                        'registration':this.sub_row.registration,'sn':mulsn,'type':this.sub_row.type,'product':product,'module':module,
                        'user':this.sub_row.user,'version':this.sub_row.version,'operator':'新增','index':this.tableData.length,'contact_display':this.sub_row.contact.split(';')})
                        
                        this.origin_Data.push({'info_id':this.info_id,'category':category,'comment':this.sub_row.comment,'contact':this.sub_row.contact,
                        'count':this.sub_row.count,'customer':this.sub_row.customer,'expiration':this.sub_row.expiration,
                        'func_uid':my_func_uid,'info':this.sub_row.info,'issued':today,'region':this.sub_row.region,
                        'registration':this.sub_row.registration,'sn':mulsn,'type':this.sub_row.type,'product':product,'module':module,
                        'user':this.sub_row.user,'version':this.sub_row.version,'operator':'新增','index':this.tableData.length,'contact_display':this.sub_row.contact.split(';')})
                        
                        this.info_id++;
                        this.deter_require.push({'customer':false, 'sn':false , 'func_uid':false, 'count':false, 'expiration':false, 'user':false, 'contact':false});
                    }
                }
                this.close_add_dialog();
        
            }
        },
        cancel:function(){//退回主畫面
            this.$router.push({name: 'Show_All'});
        },
        //------------------------------建議選項-----------------------------//
        querySearch_sn(queryString, cb) {
            var results = queryString ? this.sn_opt.filter(this.createFilter(queryString)) : this.sn_opt;
            cb(results);// 調用 callback 返回建議列表的數據
        },
        querySearch_name(queryString, cb) {
            var results = queryString ? this.customer_name_opt.filter(this.createFilter(queryString)) : this.customer_name_opt;
            cb(results);// 調用 callback 返回建議列表的數據
        },
        querySearch_site(queryString, cb) {
            var results = queryString ? this.customer_site_opt.filter(this.createFilter(queryString)) : this.customer_site_opt;
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
        /*querySearch_region(queryString, cb) {
            var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
            cb(results);// 調用 callback 返回建議列表的數據
        },*/
        querySearch_contact(queryString, cb){
            var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
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
        make_blur(mode){//使el-select失焦
            if(mode == '1')
                this.$nextTick(()=>{this.$refs.dialog_pro.blur();})
            if(mode == '2')
                this.$nextTick(()=>{this.$refs.sub_row_pro.blur();})
        },
        setCellColor({row,column,rowIndex,columnIndex}){
            let column_map = {3:'customer', 4:'sn', 5:'func_uid', 8:'count', 11:'expiration', 12:'user', 13:'contact'}
            if(this.deter_require[rowIndex][column_map[columnIndex]])
                return 'background: red;border:solid 1px #EAEAEA';
            else
                return 'border: solid 1px #EAEAEA';
        },
        handleClose() {
            {}//避免點到旁邊導致消失
        },
    }
}
</script>