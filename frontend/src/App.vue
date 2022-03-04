<template>
  <div class="">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>

    <section class="section">
      <router-view />
    </section>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted } from "vue";
import { useRoute, useRouter } from 'vue-router';
import {useStore} from "vuex"
import { toast } from "bulma-toast";
import axios from "axios";

export default defineComponent({
  setup() {
    const router = useRouter()
    const route = useRoute()
    const store = useStore()

    let is_loading:boolean = false

    const reload = () => {
      store.commit("reloadStore");
      const token = store.state.token;
      if (token) {
        axios.defaults.headers.common["Authorization"] = "token " + token;
      } else {
        axios.defaults.headers.common["Authorization"] = "";
      }
      console.log(store.state)
    }    
    onMounted(() => {
      reload()
      is_loading = store.state.is_loading;
    })
    return {
      is_loading,
    };
  },
  computed: {},
})
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
  &.is-loading {
    height: 80px;
  }
}
</style>