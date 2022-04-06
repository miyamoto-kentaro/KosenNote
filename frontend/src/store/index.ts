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
  user: User;
  saved_article: SavedArticle;
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
      saved_article: {
        title: "",
        tags: [],
        content: "",
        category: "",
        publish: false
      },
      isLoading: false
    };
  },
  mutations: {
    initializeStore(state : GlobalState) {},
    reloadStore(state : GlobalState) {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");
      const saved_article = localStorage.getItem("saved_article");
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

      if (!(saved_article === '"') && !(saved_article === null)) {
        state.saved_article = JSON.parse(saved_article);
      } else {
        state.saved_article = {
          title: "",
          tags: [],
          content: "",
          category: "",
          publish: false
        };
      }
      console.log(state);
    },

    setToken(state : GlobalState, token) {
      state.token = token;
      state.isAuthenticated = true;

      console.log(token);

      localStorage.setItem("token", token);
      axios.defaults.headers.common["Authorization"] = "Token " + token;
    },
    removeToken(state : GlobalState) {
      state.token = "";
      state.isAuthenticated = false;
      localStorage.setItem("token", state.token);
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
    },
    setSavedArticle(state : GlobalState, saved_article) {
      state.saved_article = saved_article;

      localStorage.setItem("saved_article", JSON.stringify(state.saved_article));
    },
    removeSavedArticle(state : GlobalState) {
      (state.saved_article = {
        title: "",
        tags: [],
        content: "",
        category: "",
        publish: false
      }),
      localStorage.setItem("saved_article", JSON.stringify(state.saved_article));
    }
  }
});

// useState を呼び出す度、 StateKey で型を定義するのを避けるために、ここであらかじめ定義する
export function useStore() {
  return baseUseStore(StateKey);
}
