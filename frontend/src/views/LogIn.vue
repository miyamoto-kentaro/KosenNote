<template>
  <div class="page-log-in">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Username</label>
            <div class="control">
              <input type="text" class="input" v-model="username" />
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" class="input" v-model="password" />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark">Log in</button>
            </div>
          </div>

          <hr />

          Or <router-link to="/sign-up">click here</router-link> to sign up!
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  name: "LogIn",
  data() {
    return {
      username: "",
      password: "",
      errors: [],
    };
  },
  mounted() {
    document.title = "Log In | KosenNote";
  },
  methods: {
    // async submitForm() {
    //   this.$store.commit("setIsLoading", true);
    //   axios.defaults.headers.common["Authorization"] = "";
    //   localStorage.removeItem("token");
    //   const formData = {
    //     username: this.username,
    //     password: this.password,
    //   };
    //   await axios
    //     .post("/api/v1/token/login/", formData)
    //     .then((response) => {
    //       console.log("response :", response);
    //       const token = response.data.auth_token;
    //       this.$store.commit("setToken", token);
    //       axios.defaults.headers.common["Authorization"] = "token " + token;
    //       localStorage.setItem("token", token);
    //     })
    //     .catch((error) => {
    //       toast({
    //         message: "ユーザー名かパスワードが間違っています。",
    //         type: "is-danger",
    //         dismissible: true,
    //         pauseOnHover: true,
    //         duration: 2000,
    //         position: "bottom-right",
    //       });
    //     });
    //   await axios
    //     .get("/api/v1/users/me/")
    //     .then((response) => {
    //       this.$store.commit("setUser", response.data);
    //       this.$router.push("/my-account");
    //     })
    //     .catch((error) => {
    //       // console.log(JSON.stringify(error));
    //     });
    //   this.$store.commit("setIsLoading", false);
    // },
  },
};
</script>
