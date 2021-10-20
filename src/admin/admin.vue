<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
  
  .el-aside {
    color: #333;
  }

  .apply_num_box{
    border-radius: 15px;
    width: 260px;
    height:240px;
    margin-right: 15px;
    background: paleturquoise;
  }
  .verifying_box{
    border-radius: 15px;
    width: 85%; 
    height:247px;
    background: #89DFDF;
  }
  .expire_box{
    border-radius: 15px;
    height:258px;
    margin-bottom: 40px;
    background: #00CED4;
  }
  .applied_box{
    border-radius: 15px;
    height:250px;
    background: #00CEDE;

  }
  .shadow_box{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  }
  .expiration_7{
    color: #409eff;
    border-color: #c6e2ff;
    background-color: #ecf5ff;
    width: 30px
  }

</style>

<template>
  <div>
    <el-container>
    <Aside></Aside>
    <el-main>
      <div style="display: flex; margin-bottom: 20px; height: 265px;">
        <div class="apply_num_box shadow_box">
          <div style="margin: 55px 20px; font-weight: 700; font-size: 20px;">{{this_month}}月申請次數</div>
          <div style="font-size: 30px;">{{apply_num}}</div>
        </div>

        <div class="verifying_box">
          <div style="margin: 10px; font-weight: 700; font-size: 20px;">審核中資料</div>
          <el-table :data="verifying_data" height= 200px class="shadow_box">
            <el-table-column type="expand">
              <template slot-scope="props">
                  <el-table :data="props.row.data">
                    <el-table-column prop="operator" label="操作"></el-table-column>
                    <el-table-column prop="customer" label="客戶"></el-table-column>
                    <el-table-column prop="sn" label="KeyID"></el-table-column>
                    <el-table-column prop="product" label="產品"></el-table-column>
                    <el-table-column prop="module" label="模組"></el-table-column>
                    <el-table-column prop="version" label="版本"></el-table-column>
                    <el-table-column prop="type" label="類型"></el-table-column>
                    <el-table-column prop="count" label="數量"></el-table-column>
                    <el-table-column prop="expiration" label="到期日期"></el-table-column>
                    <el-table-column prop="region" label="地區"></el-table-column>
                    <el-table-column prop="comment" label="備註"></el-table-column>
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
      </div>

      <div class="expire_box">
        <div style="height: 40px">
          <span style="font-weight: 700; font-size: 20px; top: 7px; position: relative;">即將過期的資料(聯絡人、負責人)</span>
        </div>
        <el-table :data="expiring_data" height= 219px class="shadow_box">
          <el-table-column prop="customer" label="客戶"></el-table-column>
          <el-table-column prop="sn" label="KeyID"></el-table-column>
          <el-table-column prop="product" label="產品"></el-table-column>
          <el-table-column prop="module" label="模組"></el-table-column>
          <el-table-column prop="version" label="版本"></el-table-column>
          <el-table-column prop="type" label="類型"></el-table-column>
          <el-table-column prop="count" label="數量"></el-table-column>
          <el-table-column prop="expiration" label="到期日期"></el-table-column>
          <el-table-column prop="region" label="地區"></el-table-column>
          <el-table-column prop="comment" label="備註"></el-table-column>
          <el-table-column prop="contact" label="聯絡人" show-overflow-tooltip></el-table-column>
          <el-table-column prop="user" label="負責人" show-overflow-tooltip></el-table-column>
        </el-table>
      </div>
      
      <div class="applied_box">
        <div style="height: 40px">
          <span style="font-weight: 700; font-size: 20px; position: relative; top: 6px;">申請過的資料</span>
        </div>
        <el-table :data="vaild_applied_data" height= 219px class="shadow_box">
            <el-table-column type="expand">
              <template slot-scope="props">
                  <el-table :data="props.row.data">
                    <el-table-column prop="operator" label="操作"></el-table-column>
                    <el-table-column prop="customer" label="客戶"></el-table-column>
                    <el-table-column prop="sn" label="KeyID"></el-table-column>
                    <el-table-column prop="product" label="產品"></el-table-column>
                    <el-table-column prop="module" label="模組"></el-table-column>
                    <el-table-column prop="version" label="版本"></el-table-column>
                    <el-table-column prop="type" label="類型"></el-table-column>
                    <el-table-column prop="count" label="數量"></el-table-column>
                    <el-table-column prop="expiration" label="到期日期"></el-table-column>
                    <el-table-column prop="region" label="地區"></el-table-column>
                    <el-table-column prop="comment" label="備註"></el-table-column>
                    <el-table-column prop="contact" label="聯絡人" show-overflow-tooltip></el-table-column>
                  </el-table>
              </template>
            </el-table-column>
            <el-table-column label="申請ID" prop="id"></el-table-column>
            <el-table-column label="申請日期" prop="date">
              <template slot="header" slot-scope="scope">
                <el-popover ref="popover" title="到期日" placement="bottom" width="350" trigger="click">
                  <el-date-picker @change="expiration_filter" value-format="yyyy-MM-dd" size="mini" v-model="expiration_value" 
                    type="daterange" range-separator="-" start-placeholder="開始日期" end-placeholder="結束日期"> 
                  </el-date-picker>
                  <el-button  icon="el-icon-search" circle slot="reference" size='mini'  @click.stop></el-button>
                </el-popover>
                申請日期
                <el-button  v-if="expiration_mode=='7'" circle  size='mini'  @click.stop="expiration_filter_7" class="expiration_7">7</el-button>
                <el-button  v-else circle  size='mini'  @click.stop="expiration_filter_7" style="width: 30px">7</el-button>
                <el-button  circle  size='mini'  @click.stop="expiration_filter_all">All</el-button>
              </template>
            </el-table-column>

            <el-table-column label="申請人" prop="applicant"></el-table-column>
            <el-table-column label="狀態" prop="status"></el-table-column>
            <el-table-column label="驗證時間" prop="verify_time"></el-table-column>
        </el-table>
      </div>
    </el-main>
    </el-container>
    
  </div>
</template>
<script>
import Aside from '@/admin/aside'
  export default {
    components: {Aside},
    data() {
      return {
        all_Data:[],
        user_data:[],
        user:[],
        this_month:1,
        apply_num:0,
        verifying_data:[],
        expiring_data:[],
        applied_data:[],
        default_applied_data:[],
        vaild_applied_data:[],
        expiration_value:[],
        expiration_mode:7,
      };
    },
    created(){
      this.axios.get("/admin_user",{
          params:{ user:JSON.stringify(JSON.parse(sessionStorage.getItem('user'))) }
        }).then((response)=>{
          //所有數據傳入all_Data
          this.all_Data = JSON.parse(JSON.stringify(response.data));
          let option_dict = JSON.parse(JSON.stringify(this.all_Data['option_dict']))
          let product_dict = JSON.parse(JSON.stringify(this.all_Data['product_dict']))

          /* 一個月內過期資料 */
          this.expiring_data = JSON.parse(JSON.stringify(this.all_Data['expiring_data']))
          this.user = JSON.parse(sessionStorage.getItem('user'))
          var application_data = JSON.parse(JSON.stringify(this.all_Data['application_data']))
          var user_application = application_data.filter( item => item['applicant'] == this.user[0])
          var today = new Date()
          this.this_month = today.getMonth()+1

          for(let app of user_application){
            var apply_year = app['date'].split('-')[0]
            var apply_month = app['date'].split('-')[1]
            // 轉成符合getMonth的形式 ex:05 -> 5
            if(apply_month[0]=='0')
              apply_month = apply_month[1]
            
            /* 當月申請次數 */
            if((apply_year == today.getFullYear()) && (apply_month == today.getMonth()+1))
              this.apply_num += 1


            var app_data = JSON.parse(app['data'])
            for(let i of app_data){
              // 轉換舊版本資料
              if(i['product'] == undefined){
                i['product'] = i['func_uid']
              }
            }
            
            
            if(app['verify_time'].length > 0)
              app['verify_time'] = JSON.parse(app['verify_time'])
            if(app['status'].includes('wait_for_verification'))
              app['verify_time'] = ''

            /* 審核中資料 */
            if(app['status'].includes('wait')){
              this.verifying_data.push({'id':app['id'], 'date':app['date'], 'applicant':app['applicant'], 
              'status':app['status'], 'verify_time':app['verify_time'], 'data':app_data})
            }

            /* 申請過資料 */
            this.applied_data.push({'id':app['id'], 'date':app['date'], 'applicant':app['applicant'], 
              'status':app['status'], 'verify_time':app['verify_time'], 'data':app_data})
          }

          for(let i of this.applied_data){
            var app_date = new Date(i['date'])
            var today = new Date()
            var days = parseInt(Math.abs( app_date - today ) / 1000 / 60 / 60 / 24);
            if(days <= 7)
              this.default_applied_data.push(i)
          }

          this.vaild_applied_data = JSON.parse(JSON.stringify(this.default_applied_data))
        });
    },
    methods: {
      expiration_filter(time_range){
        if(time_range == null){
          this.vaild_applied_data = this.default_applied_data
          this.expiration_mode = '7'
        }
        else{
          var start_time = new Date(time_range[0])
          var end_time = new Date(time_range[1])
          this.vaild_applied_data = []
          for(let i of this.applied_data){
            var applied_date = new Date(i['date'].slice(0,10))
            if((applied_date.toDateString() == start_time.toDateString()) && (applied_date.toDateString() == end_time.toDateString())){
              this.vaild_applied_data.push(i)
            }
            else if((applied_date >= start_time) &&　(applied_date <= end_time)){
              this.vaild_applied_data.push(i)
            }
          }
          this.expiration_mode = ''
        }
      },
      expiration_filter_7(){
        this.vaild_applied_data = this.default_applied_data
        this.expiration_value = []
        this.expiration_mode = '7'
      },
      expiration_filter_all(){
        this.vaild_applied_data = this.applied_data
        this.expiration_value = []
        this.expiration_mode = 'all'
      },

    }
  }
</script>