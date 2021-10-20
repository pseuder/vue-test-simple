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
            <div class="title">Reset Password</div><br><br>
            <div class="caption">Email address <span style="color:red">*</span></div>
            <el-autocomplete class="suggestion" v-model="email" :fetch-suggestions="querySearch_email"></el-autocomplete><br><br>
            <br><br><br>
            <div>
                <el-button class="button" @click="reset">Reset Password</el-button><br><br>
            </div>
        </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'resetPassword',
  data: function() {
        return { 
            email:'',
        }
  },
  mounted() {//監聽enter 若按enter則觸發login
    let _this = this;
    document.onkeydown = function(e) {
        if (_this.$route.name == "resetPassword") {
            let key = window.event.keyCode;
            if (key == 13) 
                _this.reset();
            }
    }
  },
  methods:{
    reset(){
        this.axios.get("/reset_password",{
            params:{
                email: JSON.stringify(this.email),
            }
        }).then((response)=>{
            let res = response.data;
            if (res.msg == '無此信箱!')
                this.$message({message: res.msg, type: 'error'});
            else if (res.msg == '找到信箱!'){
                this.$alert(`原密碼已改為隨機數字，若要變更請到後台管理更改<br>原帳號: ${res.user}<br>新密碼: ${res.password}`, '密碼變更!', {
                    dangerouslyUseHTMLString:true,
                    confirmButtonText: '確定',
                });
                this.$router.push({name: 'login'});
            }
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

