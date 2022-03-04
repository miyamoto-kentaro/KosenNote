import {InjectionKey} from "vue";
import axios from "axios";
import {createStore, Store, useStore as baseUseStore} from "vuex";

interface User {
  username: string;
  email: string;
}

export interface GlobalState {
  isAuthenticated: boolean;
  token: string | null;
  user: User;
  isLoading: boolean;
}

export const StateKey: InjectionKey<Store<GlobalState>> = Symbol();

export const store = createStore({
  state() {
    return {
      isAuthenticated: false,
      token: "",
      user: {
        username: "",
        email: ""
      },
      isLoading: false
    };
  },
  mutations: {
    initializeStore(state : GlobalState) {},
    reloadStore(state : GlobalState) {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");
      console.log("is token");
      if (!(user === '""') && !(user === null)) {
        state.user = JSON.parse(user);
      } else {
        state.user = {
          username: "",
          email: ""
        };
      }

      if (!(token === '""') && !(token === null)) {
        state.token = token;
        console.log("is_token has", "Token :", token);
        state.isAuthenticated = true;
      } else {
        state.token = "";
        state.isAuthenticated = false;
      }
      console.log(state);
    },
    setToken(state : GlobalState, token) {
      state.token = token;
      state.isAuthenticated = true;

      localStorage.setItem("token", JSON.stringify(state.token));
      axios.defaults.headers.common["Authorization"] = "Token " + token;
    },
    removeToken(state : GlobalState) {
      state.token = "";
      state.isAuthenticated = false;
      localStorage.setItem("token", JSON.stringify(state.token));
      axios.defaults.headers.common["Authorization"] = "";
    },
    setIsLoading(state : GlobalState, status) {
      state.isLoading = status;
    },
    setUser(state : GlobalState, user) {
      state.user = user;

      localStorage.setItem("user", JSON.stringify(state.user));
    },
    removeUser(state : GlobalState) {
      state.user = {
        username: "",
        email: ""
      };
      localStorage.setItem("user", JSON.stringify(state.user));
    }
  }
});

// useState を呼び出す度、 StateKey で型を定義するのを避けるために、ここであらかじめ定義する
export function useStore() {
  return baseUseStore(StateKey);
}
