<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.title{
    text-align:center; 
    font-size:30px;
}
.caption{
    text-align:left; 
    font-size:20px;
}
.input{
    width:400px;
    border-color:black;
}
.button{
    font-size:30px;
    width:400px;
    background-color:#439EFF;
    color:black;
}
.suggestion{
    width:445px;
    border-color:black;
    text-align:left
}
</style>
<template>
  
  <div style="margin-top:-50px">
    <img src="../assets/eastek.png"><br>
    <div class="title">Welcome to License Application Service</div><br>
    <el-card style="margin:0 auto; width:500px; position: relative;">
        <div style="position: absolute; right: 0; top: 0;">
            <el-button  icon="el-icon-close" circle  @click="exit"></el-button>
        </div>
        <div style="margin:0 auto; width:400px;">
            <br><br>
            <div class="title">Sign up</div><br><br>
            <div class="caption">Account <span style="color:red">*</span></div>
            <el-input class="input" v-model="form.user"></el-input><br><br>
            <div class="caption">Email address <span style="color:red">*</span></div>
            <el-autocomplete class="suggestion" v-model="form.email" :fetch-suggestions="querySearch_email"></el-autocomplete><br><br>
            <div class="caption">Password <span style="color:red">*</span></div>
            <el-input class="input" v-model="form.mypassword" show-password></el-input><br><br>
            <div class="caption">Business area <span style="color:red">*</span></div>
            <el-select style="width:445px; border-color:black;" v-model="form.myregion">
                <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
            <br><br><br>
            <div>
                <el-button class="button" @click="signup">Create Account</el-button><br><br>
            </div>
        </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'signup',
  data: function() {
        return { 
            all_Data:[],
            user_data:[],
            group_data:[],
            groups_opt:[],
            region_opt:[],
            form:{
              id:0,//edit才用的到
              user:'',
              password:'',
              mypassword:'',
              email:'',
              groups:'',
              region:'',
              myregion:'',
              record:'',
              description:'',
              admin_mail:'',
            },
            // 防止重複點擊
            submit_status:false,
        }
  },
  created(){
    this.axios.get("/admin_user",{
        }).then((response)=>{
            this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
            this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']));
            this.group_data = JSON.parse(JSON.stringify(this.all_Data['group_data']));
            this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']));
            for (let region of this.region_data){
                this.region_opt.push({'value':region.name,'label':region.name});
            }
            for(let user of this.user_data)
                for(let group of user['groups'])
                    if(group == '1')
                        this.form.admin_mail += `${user['email']};`;
        });
  },
  mounted() {//監聽enter 若按enter則觸發login
    let _this = this;
    document.onkeydown = function(e) {
        if (_this.$route.name == "signup") {
            let key = window.event.keyCode;
            if (key == 13) 
                _this.signup();
            }
    }
  },
  methods:{
    signup(){
        if(this.submit_status == true)
            return
        this.submit_status = true
        if(this.form.user == ''){
            this.$message({message: '請填入使用者名稱', type: 'error'});
            this.submit_status = false
            return;
        }
        if(this.form.mypassword == ''){
            this.$message({message: '請填入使用者密碼', type: 'error'});
            this.submit_status = false
            return;
        }
        if(this.form.email == ''){
            this.$message({message: '請填入使用者信箱', type: 'error'});
            this.submit_status = false
            return;
        }
        if(this.form.myregion == ''){
            this.$message({message: '請選擇使用者地區', type: 'error'});
            this.submit_status = false
            return;
        }
        if(this.form.email.split('@')[1] == undefined){
            this.$message({message:'請填入正確email格式', type:'error'});
            this.submit_status = false
            return;
        }
        for(let user of this.user_data){
            if(this.form.user == user['user']){
                if(user['description'] == 'to be confirmed')
                    this.$message({message: '使用者 '+this.form.user+' 等待審核中!', type: 'error'});
                else
                    this.$message({message: '使用者 '+this.form.user+' 已存在!', type: 'error'});
                this.submit_status = false
                return;
            }
        }
        for(let user of this.user_data){
            if(this.form.email == user['email']){
                if(user['description'] == 'to be confirmed')
                    this.$message({message: 'Email： '+this.form.email+' 等待審核中!', type: 'error'});
                else
                    this.$message({message: 'Email： '+this.form.email+' 已存在!', type: 'error'});
                this.submit_status = false
                return;
            }
        }

        this.form.record = JSON.stringify({"type":"new", "user":this.form.user, "email":this.form.email, "password":this.form.mypassword, "region":this.form.myregion});
        this.form.description = "to be confirmed";

        //密碼改為隨機數，等到admin確認後才改成正確的
        this.form.password = Date.now().toString(16).slice(-5);

        //groups
        for (let group of this.group_data){
            if(group['caption'] == this.form.myregion){
                this.form.groups = group['group_id'];
            }
        }
        this.form.groups = '[' + JSON.stringify(this.form.groups) + ']';

        //region
        for(let region of this.region_data)
            if(this.form.myregion == region['name'])
                this.form.region = region['region_id']
        this.form.region = '[' + JSON.stringify(this.form.region) + ']';
        
        

        this.axios.post("/send_signup_email",{
            origin_data:this.form
        }).then((response)=>{
            if(response.data=='郵件傳送成功!'){
                this.$message({ showClose: true, message: '已傳送帳號申請通知!', type: 'success' });
                this.axios.get("/operator_user",{
                    params:{
                        form: JSON.stringify(this.form),
                        operator:'add'
                    }
                });
                this.$router.push({name: 'login'});
            }
            else
                this.$message({ showClose: true, message: '帳號申請失敗!', type: 'error' });
        }).catch(()=>{
            this.$message({ showClose: true, message: 'smtp失效!', type: 'error' });
        });


        
    },
    exit(){
        this.$router.push({name: 'login'});
    },
    querySearch_email(queryString, cb){
        //如果輸入eastek以外的信箱就停止顯示建議
        if (queryString.indexOf("@") == -1){
            var results = [
                {value:`${queryString}@eastek.com.tw`,label:`${queryString}@eastek.com.tw`},
                {value:`${queryString}@eastek.com.cn`,label:`${queryString}@eastek.com.cn`}
            ]
        }
        else{
            var results = []
            let email_name = queryString.split('@')[0];
            let email_address = queryString.split('@')[1];
            if ("@eastek.com.tw".indexOf(email_address) != -1)
                results.push({value:`${email_name}@eastek.com.tw`,label:`${email_name}@eastek.com.tw`},)
            if ("@eastek.com.cn".indexOf(email_address) != -1)
                results.push({value:`${email_name}@eastek.com.cn`,label:`${email_name}@eastek.com.cn`},)
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
  }
}
</script>

