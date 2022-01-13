import { InjectionKey } from "vue";
import { createStore, Store, useStore as baseUseStore } from "vuex";

export interface GlobalState {
  count: number;
}

export const StateKey: InjectionKey<Store<GlobalState>> = Symbol();

export const store = createStore({
  state() {
    return {
      count: 0,
    };
  },

  mutations: {
    // increment(state: GlobalState) {
    //   state.count++;
    //   localStorage.setItem("count", String(state.count));
    // },
    // initializeStore(state: GlobalState) {
    //   console.log("yes");
    //   if (localStorage.getItem("count")) {
    //     state.count = Number(localStorage.getItem("count"));
    //   } else {
    //     state.count = 0;
    //   }
    // },
    // setCount(state: GlobalState, count: number) {
    //   state.count = count;
    // },
  },
});

// useState を呼び出す度、 StateKey で型を定義するのを避けるために、ここであらかじめ定義する
export function useStore() {
  return baseUseStore(StateKey);
}
