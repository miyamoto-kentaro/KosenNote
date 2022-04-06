<template>
  <div class="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"
          ><strong>Kosen Note</strong></router-link
        >

        <a
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="switch_show_mobile"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div
        class="navbar-menu"
        id="navbar-menu"
        v-bind:class="{ 'is-active': showMobileMenuComputed }"
      >
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input
                    type="text"
                    class="input"
                    placeholder="キーワードを入力"
                    name="query"
                  />
                </div>

                <div class="control">
                  <button class="button is-success">
                    <span class="icon">
                      <i class="icon kosen-note-icon-search"></i>
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="isAuthenticated">
                <router-link :to="my_profile" class="button is-light"
                  >アカウント</router-link
                >
                <router-link to="/create-article" class="button is-success">
                  <span class="icon kosen-note-icon-quill"></span>
                  <span>投稿</span>
                </router-link>
              </template>

              <template v-else>
                <router-link to="/log-in" class="button is-light"
                  >Log in</router-link
                >
                <router-link
                  to="/sign-in/email/send-mail"
                  class="button is-success"
                  >Sign in</router-link
                >
              </template>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div
      class="is-loading-bar has-text-centered"
      v-bind:class="{ 'is-loading': isLoading }"
    >
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>
    <footer class="fotter">
      <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
  <!-- <router-view/> -->
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

export default defineComponent({
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    console.log("store", store.state.user);

    // const isLoading = ref(false);

    // const isLoadingComputed = computed({
    //   get: () => isLoading.value,
    //   set: value => (isLoading.value = value)
    // });

    let showMobileMenu = ref(false);
    let showMobileMenuComputed = computed({
      get: () => showMobileMenu.value,
      set: value => (showMobileMenu.value = value)
    });

    const reload = () => {
      store.commit("setIsLoading", true);

      store.commit("reloadStore");
      const token = store.state.token;
      if (token) {
        axios.defaults.headers.common["Authorization"] = "token " + token;
      } else {
        axios.defaults.headers.common["Authorization"] = "";
      }
      // console.log(store.state);
      store.commit("setIsLoading", false);
    };
    const switch_show_mobile = () => {
      // console.log("yes");

      showMobileMenuComputed.value = !showMobileMenuComputed.value;
      // console.log(showMobileMenuComputed.value);
    };
    onMounted(() => {
      reload();
      // is_loading = store.state.is_loading;
    });
    return {
      isLoading: computed(() => store.state.isLoading),
      isAuthenticated: computed(() => store.state.isAuthenticated),
      user: computed(() => store.state.user),
      showMobileMenuComputed,
      switch_show_mobile,
      my_profile: computed(() => "/profile/" + store.state.user.username + "/")
    };
  },
  computed: {}
});
</script>

<style lang="scss">
@import "../node_modules/bulma";

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid rgb(5, 5, 5);
  border-color: rgb(0, 0, 0) transparent #fff transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0px;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  // height: 80px;
  &.is-loading {
    height: 80px;
  }
}
</style>
