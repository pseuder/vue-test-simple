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
</style>

<template>
  <div>
  <el-link type="success" style="position:relative;left:280px;bottom:50px;" icon="el-icon-s-custom">{{user}}</el-link>
  <el-table style="width:60%; margin:0 auto;" :data="tableData">
    <el-table-column prop="user" label="使用者" min-width></el-table-column>
    <el-table-column prop="password" label="密碼" min-width></el-table-column>
    <el-table-column prop="email" label="信箱" min-width></el-table-column>
    <el-table-column prop="region" label="地區" min-width></el-table-column>
    <el-table-column prop="record" label="確認申請資訊" min-width>
      <template slot-scope = "{row,$index}" >
        <el-button type="primary" icon="el-icon-s-claim" size="small" circle @click="confirm(row)"></el-button>
        <el-dialog title="申請資訊" :visible.sync="edit_lock">
          <el-form :model="form" label-width="80px">
            <el-form-item prop="user" label="使用者" required><el-input v-model="form.user" style="width:30%;"placeholder="請輸入使用者名稱"></el-input></el-form-item>
            <el-form-item prop="password" label="密碼" required><el-input v-model="form.password" style="width:30%;"placeholder="請輸入密碼"></el-input></el-form-item>
            <el-form-item prop="email" label="信箱" required><el-input v-model="form.email" style="width:30%;"placeholder="請輸入信箱"></el-input></el-form-item>
            <el-form-item prop="groups" label="群組" >
              <el-select v-model="form.groups" style="width:34%" multiple placeholder="請輸入群組">
                <el-option v-for="item in groups_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </el-form-item>
            <el-form-item prop="region" label="區域" >
              <el-select v-model="form.myregion" style="width:34%" placeholder="請輸入區域">
                  <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </el-form-item>
            <el-form-item prop="description" label="描述" ><el-input v-model="form.description" style="width:50%;"placeholder="請輸入描述"></el-input></el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
              <el-button type="warning" @click="deny" plain>否決</el-button>
              <el-button type="danger" @click="edit_lock=false" plain>取消</el-button>
              <el-button type="primary" @click="submit" plain>確定</el-button>
          </div>
        </el-dialog>
      </template>
    </el-table-column>
  </el-table>
      
  </div>
</template>
<script>
import Aside from '@/admin/aside'
  export default {
    components: {Aside},
    data() {
      return {
        user:[],
        tableData:[],
        all_Data:[],
        user_data:[],
        region_data:[],
        region_opt:[],
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
        edit_lock:false,
      };
    },
    created(){
        this.user = this.$route.params.verifyname;
        this.axios.get("/admin_user",{
        }).then((response)=>{
            this.all_Data = JSON.parse(JSON.stringify(response.data));
            this.group_data = JSON.parse(JSON.stringify(this.all_Data['group_data']));
            this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']));
            this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']));
            for(let userdata of this.user_data){
              let ifJSON = (userdata['record'].indexOf('{"type":"new"'));
              if (ifJSON != -1){
                let record = JSON.parse(userdata['record']);
                if(record['type'] == 'new')
                  this.tableData.push({id:userdata['user_id'], user:record['user'], password:record['password'], email:record['email'], region:record['region']});
              }
            }

            for(let user of this.user_data)
                for(let group of user['groups'])
                    if(group == '1')
                        this.form.admin_mail += `${user['email']},`;
            for (let group of this.group_data)
              this.groups_opt.push({'value':group.caption,'label':group.caption});
            for (let region of this.region_data)
              this.region_opt.push({'value':region.name,'label':region.name})
          });
          
    },
    methods: {
        confirm(row_data){
          this.edit_lock = true;
          this.form.id = row_data['id'];
          this.form.user = row_data['user'];
          this.form.password = row_data['password'];
          this.form.email = row_data['email'];
          this.form.region = row_data['region'];
          this.form.myregion = row_data['region'];
        },
        submit(){
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
                          this.add_lock = false;
                          this.form.id = 0;
                          this.form.user = '';
                          this.form.password = '';
                          this.form.email = '';
                          this.form.groups = [];
                          this.form.region = '';
                          this.form.record = '';
                          this.form.description = '';
                          this.form.admin_mail = '';
                          this.form.inspector = '';
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