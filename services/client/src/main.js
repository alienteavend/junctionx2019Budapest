import 'bootstrap/dist/css/bootstrap.css';
import 'es6-promise/auto';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import Vuex from 'vuex';

import App from './App';
import router from './router';

Vue.config.productionTip = false;

Vue.use(Vuex);
Vue.use(BootstrapVue);

const store = new Vuex.Store({
  state: {
    cart: [],
  },
  mutations: {
    addItems(state, items) {
      items.forEach((element) => {
        state.cart.push(element);
      });
    },
  },
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>',
});
