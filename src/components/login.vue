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
.src{
    border: none;
    color: black;
    background-color: white;
    cursor: pointer;
    text-decoration:underline;
    font-size:20px;
}

</style>

<template>
  <div style="margin-top:-50px">
    <img src="../assets/eastek.png"><br>
    <div class="title">Welcome to License Application Service</div><br>
    <el-card style="margin:0 auto; width:500px;">
        <div style="margin:0 auto; width:400px; font-size:20px">
            <br><br>
            <div class="title">Log in to your account</div><br><br>
            <div class="caption">Account</div>
            <el-input class="input" v-model="user[0]" placeholder="請輸入帳號(使用者名稱)"></el-input><br><br>
            <div class="caption">Password</div>
            <el-input class="input" v-model="user[1]" placeholder="請輸入密碼" show-password></el-input><br><br><br>
            <el-button class="button"  plain @click="login">Log in</el-button><br><br>
            <button  class="src" @click="signup"> Sign Up </button><br>
            or<br>
            <button  class="src" @click="resetPassword">Forget Password</button><br>
        </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'login',
  data: function() {
        return { 
            user:['','','',''],//user[0]:user user[1]:password user[2]:email user[3]:region
        }
  },
  created(){
        this.$router.replace({query: ''}).catch(()=>{});
  },
  mounted() {//監聽enter 若按enter則觸發login
    let _this = this;
    document.onkeydown = function(e) {
        if (_this.$route.name == "login") {
            let key = window.event.keyCode;
            if (key == 13) 
                _this.login();
            }
    }
  },
  methods:{
    login(){
        this.axios.get("/login",{
            params:{
                user: JSON.stringify(this.user),
                mode:'login'
            }
        }).then((response)=>{
            let res = response.data;
            if(res.msg == '登入成功!'){
                this.user[2] = res.email;
                this.$message({message: res.msg, type: 'success'});
                sessionStorage.setItem('token', 'ImLogin');//驗證器
                sessionStorage.setItem("user", JSON.stringify(this.user));//驗證器
                sessionStorage.setItem("authority",JSON.stringify(res.authority));//驗證器
                sessionStorage.setItem("first_time_login",'yes');//第一次登入
                this.$router.push({name: 'Show_All'});
            }
            else if (res.msg == '密碼錯誤!')
                this.$message({message: res.msg, type: 'error'});
            else 
                this.$message({message: res.msg, type: 'error'});
        
        });
    },
    signup(){
        this.$router.push({name: 'signup'});
    },
    resetPassword(){
        this.$router.push({name: 'resetPassword'});
    },
  }
}
</script>

