import {InjectionKey} from "vue";
import axios from "axios";
import {createStore, Store, useStore as baseUseStore} from "vuex";

interface User {
  username: string;
  email: string;
}

interface SavedArticle {
  title: string;
  tags: string[];
  content: string;
  category: string;
  publish: boolean;
}

export interface GlobalState {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  saved_article: SavedArticle | null;
  isLoading: boolean;
}

export const StateKey: InjectionKey<Store<GlobalState>> = Symbol();

export const store = createStore({
  state() {
    return {isAuthenticated: false, token: null, user: null, saved_article: null, isLoading: false};
  },
  mutations: {
    setToken(state : GlobalState, token) {
      state.token = token;
      state.isAuthenticated = true;
      console.log("token:", token);

      localStorage.setItem("token", JSON.stringify(state.token));
      console.log("1");
      console.log(axios.defaults.headers.common["Authorization"]);

      axios.defaults.headers.common["Authorization"] = `Token ${token}`;
      console.log(axios.defaults.headers.common["Authorization"]);
    },
    removeToken(state : GlobalState) {
      state.token = null;
      state.isAuthenticated = false;
      localStorage.removeItem("token");
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
      state.user = null;
      localStorage.removeItem("user");
    },

    setSavedArticle(state : GlobalState, saved_article) {
      state.saved_article = saved_article;
      localStorage.setItem("saved_article", JSON.stringify(state.saved_article));
    },
    removeSavedArticle(state : GlobalState) {
      state.saved_article = null;
      localStorage.removeItem("saved_article");
    }
  },
  actions: {
    reloadStore({commit}) {
      var token = localStorage.getItem("token");
      var user = localStorage.getItem("user");
      var saved_article = localStorage.getItem("saved_article");
      console.log("token:", token, "user:", user, "art:", saved_article);

      if (user != null) {
        commit("setUser", JSON.parse(user));
      } else {
        commit("removeUser");
        commit("removeToken");
        (token = null),
        (user = null);
        saved_article = null;
      }

      if (token != null) {
        commit("setToken", JSON.parse(token));
      } else {
        commit("removeUser");
        commit("removeToken");
        (token = null),
        (user = null);
        saved_article = null;
      }

      if (saved_article != null) {
        commit("setSavedArticle", JSON.parse(saved_article));
      } else {
        commit("removeSavedArticle");
      }
    },

    async InitializationStore({commit, dispatch}) {
      commit("removeUser");
      commit("removeToken");
      commit("removeSavedArticle");
      await dispatch("reloadStore");
    }
  }
});

// useState を呼び出す度、 StateKey で型を定義するのを避けるために、ここであらかじめ定義する
export function useStore() {
  return baseUseStore(StateKey);
}
